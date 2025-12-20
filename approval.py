from voice import listen
from tts_system import speak

def ask_confirmation(message: str) -> bool:
    speak("I have prepared a message.")
    speak("Here is the draft.")
    speak(message)
    speak("Do you want me to send this message? Please say yes or no.")

    response = listen()
    if response and any(x in response for x in ["yes", "haan", "send", "ok"]):
        return True

    speak("Understood. I will not send it.")
    return False
