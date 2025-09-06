import os
import random

class LLM:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "MOCK").upper()

    def chat(self, prompt: str) -> str:
        if self.provider == "MOCK":
            replies = [
                "Makes sense. Want me to keep it short and friendly?",
                "Noted. I won't guess things I don't know; here's what I can do instead.",
                "Alright! Quick idea you can try right now: break it into two tiny steps.",
                "Thanks for sharing. I remember your preference — let me adapt to that.",
                "Got it! Based on what you told me before, here's a simple next step.",
            ]
            return random.choice(replies)
        elif self.provider == "OPENAI":
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            resp = client.chat.completions.create(
                model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content.strip()
        else:
            return "Error: Unknown LLM provider"
