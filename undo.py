from message_memory import last_message, log_message
from tts_system import speak

def undo_last_action():
    last = last_message()
    if not last:
        speak("There is nothing to undo.")
        return

    log_message(
        last["contact"],
        last["message"],
        "cancelled"
    )
    speak("Last action has been cancelled.")
