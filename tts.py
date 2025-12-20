# tts.py — JARVIS TTS (XTTS-v2 • OFFLINE • EN + HI • STABLE)

# =========================
# WARNING SUPPRESSION
# =========================
import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)

# =========================
# IMPORTS
# =========================
import threading
import time
import tempfile
import os
import numpy as np

import sounddevice as sd
import soundfile as sf
from TTS.api import TTS

# =========================
# CONFIG
# =========================
REFERENCE_VOICE = r"D:\jarvis-ai\xtts\jarvis_ref.wav"
SAMPLE_RATE = 24000  # XTTS native

# =========================
# INTERNAL STATE
# =========================
_tts = None
_interrupt = False
_lock = threading.Lock()

# =========================
# EMOTION PROFILES (JARVIS)
# =========================
EMOTION_PROFILES = {
    "calm": {
        "speed": 1.0,
        "pause": 0.05
    },
    "serious": {
        "speed": 0.9,
        "pause": 0.1
    },
    "warning": {
        "speed": 0.85,
        "pause": 0.15
    }
}

# =========================
# SELECT REAL SPEAKER
# =========================
def select_real_speaker():
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()

    for i, d in enumerate(devices):
        if d["max_output_channels"] > 0:
            name = d["name"].lower()
            hostapi = hostapis[d["hostapi"]]["name"]

            if any(v in name for v in ["vb-audio", "virtual", "cable", "droidcam"]):
                continue

            if ("speaker" in name or "realtek" in name) and (
                "WASAPI" in hostapi or "DirectSound" in hostapi
            ):
                return i
    return None


DEVICE_INDEX = select_real_speaker()
if DEVICE_INDEX is not None:
    sd.default.device = DEVICE_INDEX
    sd.default.samplerate = SAMPLE_RATE
    print(f"[JARVIS AUDIO]: Using {sd.query_devices(DEVICE_INDEX)['name']}")
else:
    print("[JARVIS AUDIO]: Using system default output")

# =========================
# LOAD XTTS MODEL (ONCE)
# =========================
def _load_model():
    global _tts
    if _tts is None:
        print("[JARVIS TTS]: Loading XTTS-v2...")
        _tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            gpu=False
        )
        print("[JARVIS TTS]: XTTS ready")

# =========================
# LANGUAGE DETECT
# =========================
def detect_language(text: str) -> str:
    for ch in text:
        if "\u0900" <= ch <= "\u097F":
            return "hi"
    return "en"

# =========================
# JARVIS STYLE (EMOTION AWARE)
# =========================
def jarvis_style(text: str, emotion: str) -> str:
    profile = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["calm"])

    text = text.strip()
    text = text.replace("!", ".")
    text = text.replace("?", "...?")

    pause = "." * int(profile["pause"] * 10)
    text = text.replace(".", f"...{pause} ")

    return " ".join(text.split())

# =========================
# SPEED CONTROL
# =========================
def apply_speed(audio, speed):
    if speed == 1.0:
        return audio
    idx = np.round(np.arange(0, len(audio), speed))
    idx = idx[idx < len(audio)].astype(int)
    return audio[idx]

# =========================
# SPEAK WORKER
# =========================
def _speak_worker(text: str, emotion: str):
    global _interrupt

    _load_model()
    lang = detect_language(text)
    profile = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["calm"])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    try:
        _interrupt = False

        _tts.tts_to_file(
            text=text,
            speaker_wav=REFERENCE_VOICE,
            language=lang,
            file_path=wav_path
        )

        audio, sr = sf.read(wav_path)
        audio = apply_speed(audio, profile["speed"])

        sd.play(audio, sr)

        while sd.get_stream().active:
            if _interrupt:
                sd.stop()
                break
            time.sleep(0.05)

        sd.wait()

    except Exception as e:
        print("[JARVIS TTS ERROR]:", e)

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

# =========================
# PUBLIC API
# =========================
def speak(text: str, emotion: str = "calm"):
    if not text:
        return

    stop_speaking()
    styled = jarvis_style(text, emotion)

    print(f"[JARVIS • {emotion.upper()}]: {styled}")

    threading.Thread(
        target=_speak_worker,
        args=(styled, emotion),
        daemon=True
    ).start()


def stop_speaking():
    global _interrupt
    _interrupt = True
