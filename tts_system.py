# tts_system.py — JARVIS TTS (CLEAN, NO DEBUG NO EMOTION LABELS)

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

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# ELEVENLABS CONFIG
# =========================
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "pyttsx3").lower()

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
def _init_engine():
    global _pyttsx3_engine
    if _pyttsx3_engine is None:
        _pyttsx3_engine = pyttsx3.init()
    return _pyttsx3_engine

# =========================
# EMOTION SPEED MAP
# =========================
EMOTION_RATE = {
    "calm": 130,
    "serious": 150,
    "warning": 170
}

ELEVEN_SETTINGS = {
    "calm":    {"stability": 0.55, "similarity": 0.75},
    "serious": {"stability": 0.45, "similarity": 0.85},
    "warning": {"stability": 0.35, "similarity": 0.9},
}

# =========================
# PYTTSX3 PLAY
# =========================
def _play_pyttsx3(text, emotion):
    engine = _init_engine()
    rate = EMOTION_RATE.get(emotion, EMOTION_RATE["calm"])
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

# =========================
# SPEECH LOOP
# =========================
def _speech_loop():
    while True:
        item = _speech_queue.get()
        if item is None:
            break

        text, emotion = item

        if _stop_flag.is_set():
            _speech_queue.task_done()
            continue

        try:
            if TTS_PROVIDER == "elevenlabs":
                if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
                    raise RuntimeError("ElevenLabs credentials missing")

                settings = ELEVEN_SETTINGS.get(emotion, ELEVEN_SETTINGS["calm"])

                url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
                headers = {
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                }
                payload = {
                    "text": text,
                    "model_id": "eleven_turbo_v2",
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
                _play_pyttsx3(text, emotion)

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
# PUBLIC API
# =========================
def speak(text, emotion="calm"):
    """
    Speak text as JARVIS.
    Console shows JARVIS reply text only (no emotion, no debug).
    """
    if not text:
        return

    # 👇 THIS IS INTENTIONALLY KEPT
    print(f"JARVIS: {text}")

    _stop_flag.clear()
    _ensure_thread()
    _speech_queue.put((text, emotion))

def stop_speaking():
    _stop_flag.set()
    with _speech_queue.mutex:
        _speech_queue.queue.clear()

def wait_until_done():
    _speech_queue.join()
