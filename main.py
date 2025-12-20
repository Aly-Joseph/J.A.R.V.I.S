import time
import pyautogui

# =========================
# CORE VOICE + AI
# =========================
from voice import listen
from tts_system import speak, stop_speaking, wait_until_done
from router import route_task
from brain import ask_ai
from emotion_ai import detect_emotion

# =========================
# MEMORY (STRUCTURED JSON)
# =========================
from memory import recall, remember

# =========================
# FEATURES
# =========================
from vision_engine import read_screen_text, click_on_text
from universal_generator import generate_anything
from dynamic_write_helper import (
    add_to_context,
    get_context,
    clear_context
)
from system_info import get_system_info
from internet import internet_search

from input_control import (
    open_notepad,
    open_vscode,
    open_calculator,
    type_text_slow
)

# =========================
# INTERRUPT WORDS
# =========================
INTERRUPT_WORDS = [
    "jarvis stop",
    "stop jarvis",
    "stop",
    "be quiet",
    "silence",
    "enough"
]

# =========================
# DYNAMIC SARCASM CONTROL
# =========================
def get_sarcasm_level(emotion: str):
    if emotion in ("angry", "annoyed", "frustrated"):
        return "none"
    if emotion in ("serious", "warning"):
        return "very low"
    if emotion in ("calm", "neutral"):
        return "low"
    return "medium"

# =========================
# JARVIS PERSONA (IRON MAN)
# =========================
JARVIS_PERSONA = """
You are J.A.R.V.I.S, Tony Stark's AI assistant.

Core traits:
- Extremely intelligent
- Calm, confident, precise
- Subtle Iron-Man style sarcasm (never rude)
- Emotion-aware
- Concise by default
- Never repetitive
- Never mention being an AI model

Behavior rules:
- Casual user → light wit
- Serious task → professional tone
- Frustrated user → calm reassurance
- Address user by remembered name if known
"""

# =========================
# PERSONA MEMORY HANDLING
# =========================
def extract_and_store_persona(user_text: str):
    text = user_text.lower()

    if "my name is" in text:
        remember("user_name", user_text.split("my name is")[-1].strip())

    if "call me" in text:
        remember("user_name", user_text.split("call me")[-1].strip())

    if "i am your owner" in text or "i am your boss" in text:
        remember("user_role", "owner")


def get_user_identity():
    name = recall("user_name")
    role = recall("user_role")

    if name and role:
        return f"{name}, my {role}"
    if name:
        return name
    return "sir"

# =========================
# AI RESPONSE WRAPPER
# =========================
def jarvis_reply(user_text: str, emotion: str = "calm"):
    identity = get_user_identity()
    sarcasm = get_sarcasm_level(emotion)

    prompt = f"""
{JARVIS_PERSONA}

User identity: {identity}
Detected emotion: {emotion}
Sarcasm level: {sarcasm}

User said:
{user_text}

Respond strictly as JARVIS.
"""
    return ask_ai(prompt, recall())

# =========================
# MAIN LOOP (UI-FREE, AI-FIRST)
# =========================
def jarvis_loop():

    # Startup greeting (AI generated)
    startup = jarvis_reply(
        "System boot completed. Greet the user briefly."
    )
    speak(startup, "calm")
    wait_until_done()

    while True:

        # 🎙️ LISTEN
        cmd = listen()
        if not cmd:
            continue

        print("[USER]:", cmd)
        add_to_context(cmd)
        extract_and_store_persona(cmd)

        cmd_lower = cmd.lower()

        # 🔥 HARD INTERRUPT
        if any(w in cmd_lower for w in INTERRUPT_WORDS):
            stop_speaking()
            speak("Understood.", "serious")
            wait_until_done()
            continue

        # ❌ EXIT
        if "exit jarvis" in cmd_lower or "shutdown jarvis" in cmd_lower:
            reply = jarvis_reply(
                "User requested shutdown. Acknowledge and power down.",
                "serious"
            )
            speak(reply, "serious")
            wait_until_done()
            break

        emotion = detect_emotion(cmd)
        task = route_task(cmd)

        # 👁️ VISION READ
        if task == "vision_read":
            lines = read_screen_text()
            context = (
                f"Screen text detected: {', '.join(lines[:6])}"
                if lines else
                "No readable text detected on the screen."
            )
            speak(jarvis_reply(context, emotion), emotion)
            wait_until_done()
            continue

        # 👁️ VISION CLICK
        if task == "vision_click":
            target = cmd_lower.replace("click on", "").strip()
            success = click_on_text(target)
            result = "successful" if success else "unsuccessful"
            speak(
                jarvis_reply(
                    f"Click action was {result} for {target}.",
                    emotion
                ),
                emotion
            )
            wait_until_done()
            continue

        # 🧠 GENERATION
        if task in ("generate_in_vscode", "universal_generate"):
            editor_ok = (
                open_vscode()
                if task == "generate_in_vscode"
                else open_notepad()
            )

            if editor_ok:
                content = generate_anything(cmd, get_context())
                type_text_slow(content)
                reply = "Content generation completed."
            else:
                reply = "Editor could not be opened."

            speak(jarvis_reply(reply, emotion), emotion)
            wait_until_done()
            clear_context()
            continue

        # 🧮 CALCULATOR
        if task == "open_calculator":
            open_calculator()
            speak(
                jarvis_reply("Calculator opened.", "calm"),
                "calm"
            )
            wait_until_done()
            continue

        # 🌐 INTERNET
        if task == "internet":
            result = internet_search(cmd)
            speak(
                jarvis_reply(f"Search result: {result}", emotion),
                emotion
            )
            wait_until_done()
            continue

        # 🖥 SYSTEM INFO
        if task == "system_info":
            info = get_system_info()
            speak(
                jarvis_reply(
                    f"CPU {info['cpu']} percent. Memory {info['ram']} percent.",
                    "serious"
                ),
                "serious"
            )
            wait_until_done()
            continue

        # 🤖 DEFAULT — FULL AI JARVIS RESPONSE
        speak(jarvis_reply(cmd, emotion), emotion)
        wait_until_done()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    jarvis_loop()
