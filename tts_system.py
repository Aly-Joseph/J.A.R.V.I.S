# tts_system.py — JARVIS TTS (WITH HINDI/HINGLISH SUPPORT)

import os
import threading
import queue
import requests
import io
import pyttsx3
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
import re

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# ELEVENLABS CONFIG
# =========================
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
ELEVENLABS_HINGLISH_VOICE_ID = os.getenv("ELEVENLABS_HINGLISH_VOICE_ID", ELEVENLABS_VOICE_ID)
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "pyttsx3").lower()

# Alternative Hindi voice IDs if primary doesn't work well
HINDI_VOICE_IDS = [
    ELEVENLABS_HINGLISH_VOICE_ID,  # Primary (user configured)
    "HV1aLCqKy8wzXBo8lWu7",        # Alternative 1 (warm, accent)
    "yoZ06aMxZJJ28mfd3foE",        # Alternative 2 (clear, Hindi)
    "LJ8kO8OADi33N2u0C6bH",        # Alternative 3 (natural, accent)
]

# =========================
# STATE
# =========================
_speech_queue = queue.Queue()
_stop_flag = threading.Event()
_thread = None
_pyttsx3_engine = None

# =========================
# PYTTSX3 INIT
# =========================
def _init_engine(language="english"):
    global _pyttsx3_engine
    if _pyttsx3_engine is None:
        _pyttsx3_engine = pyttsx3.init()
    
    # Set language for pyttsx3
    if language in ("hindi", "hinglish"):
        try:
            # Try to use Hindi language
            _pyttsx3_engine.setProperty("language", "hi_IN")
        except:
            # Fallback to English if Hindi not available
            _pyttsx3_engine.setProperty("language", "en_US")
    else:
        _pyttsx3_engine.setProperty("language", "en_US")
    
    return _pyttsx3_engine

# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text: str) -> str:
    """
    Detects language from text.
    Returns: "hinglish" or "english" (no pure Hindi support)
    """
    text_lower = text.lower()
    
    # Hinglish detection - Hindi words in English
    # Extended patterns for better detection
    hinglish_patterns = [
        r'\bhai\b', r'\bkya\b', r'\bnahi\b', r'\bhaan\b', r'\bthik\b',
        r'\bphir\b', r'\bjao\b', r'\bkaro\b', r'\blao\b', r'\bde\b',
        r'\bsuno\b', r'\bbolo\b', r'\bacha\b', r'\bdadiya\b',
        r'\bchar\b', r'\bthoda\b', r'\badi\b', r'\bpehle\b', r'\bfir\b',
        r'\bkuch\b', r'\bwahi\b', r'\bvo\b', r'\bji\b', r'\bjaao\b',
        r'\bsab\b', r'\bchal\b', r'\bmain\b', r'\btum\b', r'\bmujhe\b', r'\bmere\b'
    ]
    
    for pattern in hinglish_patterns:
        if re.search(pattern, text_lower):
            return "hinglish"
    
    return "english"

# =========================
# EMOTION SPEED MAP (LANGUAGE-AWARE)
# =========================
EMOTION_RATE = {
    "calm": 130,
    "serious": 150,
    "warning": 170
}

# Slower rates for Hindi/Hinglish for better clarity
EMOTION_RATE_HINDI = {
    "calm": 120,
    "serious": 140,
    "warning": 160
}

# ElevenLabs voice settings for optimal accent
ELEVEN_SETTINGS = {
    "calm":    {"stability": 0.50, "similarity": 0.80},
    "serious": {"stability": 0.65, "similarity": 0.85},
    "warning": {"stability": 0.75, "similarity": 0.90},
}

# Special settings for Hinglish/Hindi voice (warmer, natural accent with multilingual model)
ELEVEN_SETTINGS_HINGLISH = {
    "calm":    {"stability": 0.65, "similarity": 0.92},  # Higher for clearer Hindi
    "serious": {"stability": 0.75, "similarity": 0.95},
    "warning": {"stability": 0.85, "similarity": 0.98},
}

# =========================
# PYTTSX3 PLAY WITH LANGUAGE SUPPORT
# =========================
def _play_pyttsx3(text, emotion, language="english"):
    engine = _init_engine(language)
    
    # Select appropriate rate map
    if language in ("hindi", "hinglish"):
        rate = EMOTION_RATE_HINDI.get(emotion, EMOTION_RATE_HINDI["calm"])
        volume = 0.95
    else:
        rate = EMOTION_RATE.get(emotion, EMOTION_RATE["calm"])
        volume = 1.0
    
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    engine.say(text)
    engine.runAndWait()

# =========================
# SPEECH LOOP WITH LANGUAGE SUPPORT
# =========================
def _speech_loop():
    while True:
        item = _speech_queue.get()
        if item is None:
            break

        text, emotion, language = item

        if _stop_flag.is_set():
            _speech_queue.task_done()
            continue

        try:
            if TTS_PROVIDER == "elevenlabs":
                if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
                    raise RuntimeError("ElevenLabs credentials missing")

                # Select appropriate voice ID and settings for language
                if language == "hinglish" and ELEVENLABS_HINGLISH_VOICE_ID:
                    voice_id = ELEVENLABS_HINGLISH_VOICE_ID
                    settings = ELEVEN_SETTINGS_HINGLISH.get(emotion, ELEVEN_SETTINGS_HINGLISH["calm"])
                    model_id = "eleven_multilingual_v2"  # Better for Hindi/Hinglish
                    language_hint = "hi"  # Hindi language hint for better accent
                    
                    # Add preprocessing for better Hindi accent
                    # Mark text as Hindi with phonetic hints
                    processed_text = f"[spoken as Hindi: {text}]" if "[" not in text else text
                else:
                    voice_id = ELEVENLABS_VOICE_ID
                    settings = ELEVEN_SETTINGS.get(emotion, ELEVEN_SETTINGS["calm"])
                    model_id = "eleven_turbo_v2"
                    language_hint = "en"
                    processed_text = text

                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                headers = {
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                }
                payload = {
                    "text": processed_text,
                    "model_id": model_id,
                    "language_code": language_hint,
                    "voice_settings": {
                        "stability": settings["stability"],
                        "similarity_boost": settings["similarity"],
                    },
                }

                r = requests.post(url, headers=headers, json=payload, timeout=30)
                r.raise_for_status()

                audio = AudioSegment.from_mp3(io.BytesIO(r.content))
                samples = np.array(audio.get_array_of_samples())

                if audio.channels == 2:
                    samples = samples.reshape((-1, 2))

                sd.play(samples, samplerate=audio.frame_rate)
                sd.wait()

            else:
                _play_pyttsx3(text, emotion, language)

        except Exception:
            # silent by design (no debug spam)
            pass

        _speech_queue.task_done()

# =========================
# THREAD ENSURE
# =========================
def _ensure_thread():
    global _thread
    if _thread is None or not _thread.is_alive():
        _thread = threading.Thread(target=_speech_loop, daemon=True)
        _thread.start()

# =========================
# PUBLIC API WITH LANGUAGE SUPPORT
# =========================
def speak(text, emotion="calm", language=None):
    """
    Speak text as JARVIS with automatic language detection.
    Auto-detects language (Hinglish or English) and switches voice accordingly.
    Default: English. If Hinglish detected, automatically switches to Hinglish voice.
    """
    if not text:
        return

    # Auto-detect language if not provided
    if language is None:
        language = detect_language(text)

    # Show detection in console
    if language == "hinglish":
        print(f"[HINGLISH MODE] 🎭 JARVIS: {text}")
    else:
        print(f"JARVIS: {text}")

    _stop_flag.clear()
    _ensure_thread()
    _speech_queue.put((text, emotion, language))

def stop_speaking():
    _stop_flag.set()
    with _speech_queue.mutex:
        _speech_queue.queue.clear()

def wait_until_done():
    _speech_queue.join()
