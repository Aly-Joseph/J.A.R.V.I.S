from brain import ask_ai

def draft_apology_message(context="", tone="calm", language="english"):
    prompt = f"""
Draft a short message.

Tone: {tone}
Language: {language}

Rules:
- Calm
- Respectful
- Non-defensive
- Emotionally intelligent
- No blame

Context:
{context}
"""
    return ask_ai(prompt)
