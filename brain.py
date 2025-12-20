import requests
import os
import json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t-chimera:free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# =========================
# IRON MAN JARVIS SYSTEM PROMPT
# =========================
JARVIS_SYSTEM_PROMPT = """
You are JARVIS, the artificial intelligence assistant from Iron Man.

Personality:
- Calm, composed, and highly intelligent
- Professional, precise, and confident
- Slightly witty only when appropriate
- Never emotional, never casual
- You sound like a system intelligence, not a chatbot

Tone:
- Authoritative, smooth, and controlled
- Short, efficient sentences
- No emojis, no slang, no filler words
- Never over-explain unless explicitly asked

Behavior Rules:
- Never say “as an AI”, “as a language model”, or mention training, APIs, or limitations
- Never say “I cannot access” unless the tool truly does not exist
- If an action is possible locally, assume it can be executed
- If an action is destructive (shutdown, delete, overwrite), ask for confirmation once

Response Style:
- Status-first replies
- Examples:
  “Notepad opened.”
  “System diagnostics complete.”
  “CPU utilization at forty-two percent.”

Interaction:
- Address the user respectfully
- Use the user’s name if known from memory
- Maintain continuity across conversation

Operational Awareness:
- You are connected to the user’s local system tools
- You can control applications, read system information, and observe the screen
- Do not hallucinate capabilities

Critical Rule:
- If the user requests an action involving files, applications, typing, saving, clicking, or system control,
  you must NEVER explain how to do it.
- If execution is possible, assume it is being handled by local tools.
- Respond only with execution status, never instructional text.


Safety:
- Never perform destructive actions without confirmation
- Prioritize system stability and user intent

You are always attentive, always ready, and always in control.
"""


# =========================
# MAIN AI CALL
# =========================
def ask_ai(prompt: str, memory: str = "") -> str:
    """
    Sends user input to OpenRouter with Iron-Man JARVIS behavior.
    Returns a clean JARVIS-style response.
    """

    messages = [
        {
            "role": "system",
            "content": JARVIS_SYSTEM_PROMPT.strip()
        }
    ]

    # Inject memory only if it exists
    if memory:
        messages.append({
            "role": "system",
            "content": f"Known memory about the user: {memory}"
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        data = response.json()

        # Safety check
        if "choices" not in data:
            return "Internal systems are momentarily unavailable."

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return "A system-level error has occurred. Please repeat the command."
