from message_drafter import draft_apology_message
from tts_system import speak

def auto_suggest_response(context):
    speak("I can suggest a message if you want.")
    draft = draft_apology_message(context)
    speak("Here is a suggested message.")
    speak(draft)
    speak("I will not send this automatically.")
    return draft
