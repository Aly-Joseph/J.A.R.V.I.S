# language_support.py — Complete language support for JARVIS

import re

def detect_language(text: str) -> str:
    """
    Language detection for English and Hinglish only (no pure Hindi).
    Returns: "hinglish" or "english"
    """
    if not text or not isinstance(text, str):
        return "english"
    
    text_lower = text.lower()
    
    # Hinglish patterns - common Hindi words in English
    hinglish_patterns = [
        r'\bhai\b', r'\bkya\b', r'\bnahi\b', r'\bhaan\b', r'\bthik\b',
        r'\bphir\b', r'\bjao\b', r'\bkaro\b', r'\blao\b', r'\bde\b',
        r'\bsuno\b', r'\bbolo\b', r'\bacha\b', r'\bdadiya\b', r'\bchar\b',
        r'\bchal\b', r'\bmain\b', r'\btum\b', r'\bmujhe\b', r'\bmere\b',
        r'\bka\b', r'\bki\b', r'\bko\b'
    ]
    
    for pattern in hinglish_patterns:
        if re.search(pattern, text_lower):
            return "hinglish"
    
    return "english"


def translate_to_hindi(text: str) -> str:
    """
    Simple mapping of common English phrases to Hindi.
    For full translation, use a real translation API.
    """
    translations = {
        "hello": "नमस्ते",
        "hi": "नमस्ते",
        "goodbye": "अलविदा",
        "thank you": "धन्यवाद",
        "thanks": "धन्यवाद",
        "yes": "हाँ",
        "no": "नहीं",
        "ok": "ठीक है",
        "okay": "ठीक है",
        "system ready": "सिस्टम तैयार है",
        "what do you need": "आपको क्या चाहिए",
        "how can i help": "मैं कैसे मदद कर सकता हूँ",
    }
    
    text_lower = text.lower()
    for english, hindi in translations.items():
        text_lower = text_lower.replace(english, hindi)
    
    return text_lower


def translate_to_hinglish(text: str) -> str:
    """
    Simple conversion to Hinglish style.
    """
    conversions = {
        "is": "hai",
        "are": "ho",
        "what": "kya",
        "ok": "thik hai",
        "understood": "samjh gaya",
        "good": "acha",
    }
    
    result = text.lower()
    for english, hinglish in conversions.items():
        result = re.sub(r'\b' + english + r'\b', hinglish, result, flags=re.IGNORECASE)
    
    return result


def get_language_config(language: str) -> dict:
    """
    Returns configuration for a specific language.
    """
    configs = {
        "english": {
            "language_name": "English",
            "tts_speed": 130,
            "default_greeting": "System ready. How may I assist you?",
            "system_prompt_key": "JARVIS_SYSTEM_PROMPT_ENGLISH",
        },
        "hindi": {
            "language_name": "Hindi",
            "tts_speed": 120,  # Slightly slower for clarity
            "default_greeting": "प्रणाली तैयार है। मैं आपकी कैसे मदद कर सकता हूँ?",
            "system_prompt_key": "JARVIS_SYSTEM_PROMPT_HINDI",
        },
        "hinglish": {
            "language_name": "Hinglish",
            "tts_speed": 125,
            "default_greeting": "System ready. Main kya kar sakta hoon?",
            "system_prompt_key": "JARVIS_SYSTEM_PROMPT_HINGLISH",
        },
    }
    
    return configs.get(language, configs["english"])


def format_response_for_language(response: str, language: str) -> str:
    """
    Formats AI response appropriately for the language.
    Removes any language-specific markers if present.
    """
    # Remove any language markers or prefixes
    markers = [
        r'^\[EN\]\s*', r'^\[ENGLISH\]\s*',
        r'^\[HI\]\s*', r'^\[HINDI\]\s*',
        r'^\[HH\]\s*', r'^\[HINGLISH\]\s*',
    ]
    
    for marker in markers:
        response = re.sub(marker, '', response, flags=re.IGNORECASE)
    
    return response.strip()
