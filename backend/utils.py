# backend/utils.py
import re
import unicodedata
from typing import Dict

def normalize_text(s: str) -> str:
    # Normalize unicode, convert to lower-case, replace fancy quotes, remove punctuation
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("`", "'").replace("“", '"').replace("”", '"')
    s = s.lower()
    # Replace any character that is not letter/number/space/apostrophe with space
    s = re.sub(r"[^\w\s']", " ", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s

def detect_tone(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["sad", "down", "depressed", "upset", "anxious", "stress"]):
        return "supportive"
    if any(w in t for w in ["joke", "roast", "funny", "meme", "lol"]):
        return "playful"
    return "formal"

def extract_user_facts(text: str) -> Dict[str, str]:
    """
    Extracts simple facts from the user's raw text.
    Returns dictionary with keys like: name, location, favorite_color, favorite_sport, favorite_food, favorite_anime
    """
    t = text.strip()
    facts = {}

    # Name patterns: "my name is X", "i am X", "i'm X", "im X"
    m = re.search(r"\b(?:my name is|i am|i'm|im)\s+([A-Za-z][A-Za-z\s\.'-]{0,60})\b", t, re.IGNORECASE)
    if m:
        facts["name"] = m.group(1).strip()

    # Location: "i live in X", "i'm from X", "i am from X"
    m = re.search(r"\b(?:i live in|i'm from|i am from|i am from)\s+([A-Za-z][A-Za-z\s\.'-]{1,80})\b", t, re.IGNORECASE)
    if m:
        facts["location"] = m.group(1).strip()

    # Favorite color
    m = re.search(r"\bmy (?:favorite|favourite) color is\s+([A-Za-z0-9\-\s]{1,30})\b", t, re.IGNORECASE)
    if m:
        facts["favorite_color"] = m.group(1).strip()

    # Favorite sport
    m = re.search(r"\bmy (?:favorite|favourite) sport is\s+([A-Za-z0-9\-\s]{1,40})\b", t, re.IGNORECASE)
    if m:
        facts["favorite_sport"] = m.group(1).strip()

    # Favorite anime
    m = re.search(r"\bmy (?:favorite|favourite) anime is\s+([A-Za-z0-9\:\'\-\s]{1,60})\b", t, re.IGNORECASE)
    if m:
        facts["favorite_anime"] = m.group(1).strip()

    # Favorite food
    m = re.search(r"\bmy (?:favorite|favourite) food is\s+([A-Za-z0-9\-\s]{1,60})\b", t, re.IGNORECASE)
    if m:
        facts["favorite_food"] = m.group(1).strip()

    return facts
