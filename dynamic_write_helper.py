from brain import ask_ai
from voice import listen
from tts_system import speak

# =========================
# CONVERSATION CONTEXT
# =========================
_CONTEXT = []

def add_to_context(text: str):
    _CONTEXT.append(text)
    if len(_CONTEXT) > 10:
        _CONTEXT.pop(0)

def get_context() -> str:
    return " ".join(_CONTEXT)

def clear_context():
    _CONTEXT.clear()


# =========================
# PERMISSION SYSTEM
# =========================
def ask_permission(action: str) -> bool:
    speak(f"I am ready to {action}. Should I proceed?")
    response = listen()
    if response and any(x in response.lower() for x in ["yes", "ok", "go ahead", "haan", "do it"]):
        return True

    speak("Understood. I will not proceed.")
    return False


# =========================
# DYNAMIC CONTENT GENERATION
# =========================
def generate_from_context(context: str) -> str:
    prompt = f"""
Based on the following conversation, write a clear, well-structured response.
Do not mention the conversation itself.

Conversation:
{context}
"""
    return ask_ai(prompt)
