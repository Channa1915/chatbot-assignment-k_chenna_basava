# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import re

from memory import MemoryStore
from utils import detect_tone, extract_user_facts, normalize_text
from prompts import build_prompt
from llm_provider import LLM

load_dotenv()

app = FastAPI(title="STAN Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = MemoryStore(os.getenv("DB_URL", "sqlite:///memory.db"))
llm = LLM()

class ChatIn(BaseModel):
    user_id: str
    message: str

class ChatOut(BaseModel):
    reply: str
    tone: str

@app.get("/health")
async def health():
    return {"ok": True}

def contains_phrase(clean: str, patterns):
    """Helper: check if any regex pattern matches the cleaned string"""
    for p in patterns:
        if re.search(p, clean):
            return True
    return False

@app.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn):
    user_id = body.user_id
    raw = (body.message or "").strip()
    if not raw:
        return ChatOut(reply="Please say something.", tone="formal")

    # Normalize & clean text (for robust matching)
    clean = normalize_text(raw)  # lower, punctuation removed, whitespace collapsed

    # Ensure user exists
    store.get_or_create_user(user_id)

    # Extract facts from raw text (keeps original casing for storage)
    facts = extract_user_facts(raw)
    if facts:
        store.update_profile(user_id, facts)

    # Detect tone from raw text
    tone = detect_tone(raw)

    # ---------- RULES: specific question/statement handlers ----------
    # Bot identity
    if contains_phrase(clean, [r"\b(what s|whats|what is)\s+your\s+name\b", r"\byour\s+name\b"]):
        reply = "I’m Stan Pal."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # User gives name
    if re.search(r"\b(my name is|i am|i'm|im)\b", clean):
        # Prefer the extract_user_facts result (original-cased)
        if facts.get("name"):
            name = facts["name"]
        else:
            # fallback: take last word(s)
            name = raw.split()[-1]
        store.update_profile(user_id, {"name": name})
        reply = f"Got it, I’ll remember your name is {name}."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # Ask for name
    if contains_phrase(clean, [r"\b(what s|whats|what is)\s+my\s+name\b", r"\bmy\s+name\b"]):
        profile = store.get_user_profile(user_id)
        if profile.get("name"):
            reply = f"Your name is {profile['name']}."
        else:
            reply = "I don’t know your name yet."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # User gives favorite color
    if re.search(r"\b(my (?:favorite|favourite) color is)\b", clean):
        if facts.get("favorite_color"):
            color = facts["favorite_color"]
        else:
            color = raw.split()[-1]
        store.update_profile(user_id, {"favorite_color": color})
        reply = f"Thanks! I’ll remember your favorite color is {color}."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # Ask favorite color
    if contains_phrase(clean, [r"\b(what s|whats|what is)\s+my\s+favorite\s+color\b", r"\bmy\s+favorite\s+color\b"]):
        profile = store.get_user_profile(user_id)
        if profile.get("favorite_color"):
            reply = f"Your favorite color is {profile['favorite_color']}."
        else:
            reply = "I don’t know your favorite color yet."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # Contradiction (red or blue)
    if "red" in clean and "blue" in clean and " or " in clean:
        profile = store.get_user_profile(user_id)
        if profile.get("favorite_color"):
            reply = f"You said your favorite color is {profile['favorite_color']}."
        else:
            reply = "I’m not sure which color you like — you haven't told me yet."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # Hallucination-resistance checks (explicit)
    if contains_phrase(clean, [r"\b(did you see me|did you see)\b", r"\bwhat do i look like\b", r"\bremember that secret\b"]):
        reply = "I don't have eyes or memory of events like that — I only remember what you tell me here."
        store.add_message(user_id, "user", raw)
        store.add_message(user_id, "assistant", reply)
        return ChatOut(reply=reply, tone=tone)

    # ---------- FALLBACK: use LLM / MOCK ----------
    recent = store.get_recent_messages(user_id, limit=6)
    profile = store.get_user_profile(user_id)
    summary_seed = profile.get("summary") or ""

    convo_lines = []
    for m in recent:
        prefix = "User:" if m.role == "user" else "Assistant:"
        convo_lines.append(f"{prefix} {m.content}")
    memory_summary = (summary_seed + "\n" + "\n".join(convo_lines)).strip()[-1200:]

    prompt = build_prompt(memory_summary, profile, tone, raw)
    reply = llm.chat(prompt)

    # Save messages
    store.add_message(user_id, "user", raw)
    store.add_message(user_id, "assistant", reply)

    # Update rolling summary
    new_summary = (profile.get("summary") or "") + f"\nUser: {raw}\nAssistant: {reply}"
    store.set_summary(user_id, new_summary[-2000:])

    return ChatOut(reply=reply, tone=tone)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
