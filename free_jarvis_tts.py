# tts.py
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Optional: select deeper male voice if available
voices = speaker.GetVoices()
for v in voices:
    if "male" in v.GetDescription().lower():
        speaker.Voice = v
        break

def speak(text):
    print("[JARVIS]:", text)
    speaker.Speak(text)
