import speech_recognition as sr
import threading
import time

# Global recognizer to reuse across calls
_recognizer = sr.Recognizer()
_recognizer.dynamic_energy_threshold = True

def listen(on_start=None, on_end=None, timeout=6, phrase_time_limit=8) -> str:
    """
    Listen for voice input with better error handling and timeout management.
    """
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise (quick)
            _recognizer.adjust_for_ambient_noise(source, duration=0.3)

            if on_start:
                try:
                    on_start()   # 🔵 ring listening ON
                except Exception as e:
                    print(f"[VOICE] on_start callback error: {e}")

            try:
                # Listen with timeout
                audio = _recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            except sr.RequestError as e:
                print(f"[VOICE] Microphone error: {e}")
                if on_end:
                    try: on_end()
                    except: pass
                return ""
            except sr.UnknownValueError:
                print(f"[VOICE] Could not understand audio")
                if on_end:
                    try: on_end()
                    except: pass
                return ""

        # Signal listening complete
        if on_end:
            try:
                on_end()  # ⚪ ring listening OFF
            except Exception as e:
                print(f"[VOICE] on_end callback error: {e}")

        # Recognize speech
        try:
            text = _recognizer.recognize_google(audio).lower()
            print(f"[VOICE] Recognized: {text}")
            return text
        except sr.RequestError as e:
            print(f"[VOICE] Google API error: {e}")
            return ""
        except sr.UnknownValueError:
            print(f"[VOICE] Could not understand audio")
            return ""

    except Exception as e:
        print(f"[VOICE] Unexpected error: {e}")
        if on_end:
            try: on_end()
            except: pass
        return ""
