def build_prompt(memory_summary: str, profile: dict, tone: str, new_input: str) -> str:
    persona = "You are Stan Pal, a friendly assistant with memory."
    profile_str = ", ".join([f"{k}: {v}" for k, v in profile.items() if v])
    return f"""
{persona}
Known profile: {profile_str}
Memory summary: {memory_summary}

Tone: {tone}
User: {new_input}
Assistant:
""".strip()
