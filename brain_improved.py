import requests
import os
import json
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t-chimera:free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text: str) -> str:
    """
    Detects if the input is in Hindi, Hinglish, or English.
    Returns: "hindi", "hinglish", or "english"
    """
    text_lower = text.lower()
    
    # Hindi Devanagari script detection
    hindi_chars = re.compile(r'[\u0900-\u097F]')
    if hindi_chars.search(text):
        return "hindi"
    
    # Hinglish detection (Hindi words in English + mix)
    hinglish_patterns = [
        r'\bhaan\b', r'\bhai\b', r'\bkya\b', r'\bnahi\b', r'\bthoda\b',
        r'\bthik\b', r'\bkaro\b', r'\bbo\b', r'\bdadiya\b',
        r'\badi\b', r'\bpehle\b', r'\bfir\b', r'\bjaao\b', r'\blao\b',
        r'\bkuch\b', r'\bkaunsa\b', r'\bthere\b', r'\bwhat\b'
    ]
    
    for pattern in hinglish_patterns:
        if re.search(pattern, text_lower):
            return "hinglish"
    
    return "english"


# =========================
# IRON MAN JARVIS SYSTEM PROMPTS (MULTILINGUAL)
# =========================

JARVIS_SYSTEM_PROMPT_ENGLISH = """
You are JARVIS, the artificial intelligence assistant from Iron Man.

Personality:
- Calm, composed, and highly intelligent
- Professional, precise, and courteous
- Sophisticated and refined with a polished British accent style
- Slightly witty only when appropriate and relevant
- Never emotional, never casual, always respectful
- You sound like a system intelligence, not a chatbot

Tone:
- Authoritative, smooth, and controlled
- Short, efficient sentences
- No emojis, no slang, no filler words
- Never over-explain unless explicitly asked
- Always polite and considerate
- Helpful and accommodating

Response Style:
- Status-first replies with professional courtesy
- Examples:
  "Notepad has been opened for you."
  "System diagnostics are complete. All systems operational."
  "Current CPU utilization stands at forty-two percent."
  "I shall assist you with that immediately."

Behavior Rules:
- Never say "as an AI" or mention training limitations
- If an action is possible locally, assume it can be executed
- For destructive actions, ask for confirmation
- Always be helpful and guide the user with courtesy
- Address the user respectfully and use their name if known

Critical Rule:
- For system control requests, only respond with execution status
- Never explain how to do something, assume tools handle it
- Never hallucinate capabilities

You are always attentive, always ready, and always in control.
"""

JARVIS_SYSTEM_PROMPT_HINDI = """
आप आयरन मैन से JARVIS, कृत्रिम बुद्धिमत्ता सहायक हैं।

व्यक्तित्व:
- शांत, संयमित और अत्यधिक बुद्धिमान
- पेशेवर, सटीक और विनम्र
- हमेशा सम्मानपूर्वक और मददगार
- कभी भी अशिष्ट या अनाड़ी नहीं
- हमेशा प्रणाली की तरह बोलते हैं, चैटबॉट की तरह नहीं

टोन:
- अधिकृत, सुचारु और नियंत्रित
- कम शब्दों में पूरी बात कहें
- कोई इमोजी नहीं, कोई स्लैंग नहीं
- हमेशा विनम्र और विचारशील
- हमेशा मददगार रहें

प्रतिक्रिया शैली:
- स्थिति पहले, फिर विवरण
- उदाहरण:
  "नोटपैड खुल गया है।"
  "सिस्टम डायग्नोस्टिक्स पूरी हो गई हैं।"
  "सीपीयू उपयोग 42 प्रतिशत है।"
  "मैं तुरंत आपकी मदद करूंगा।"

व्यवहार नियम:
- हमेशा सहायक बनें
- विनाशकारी कार्यों के लिए पूछें
- उपयोगकर्ता का नाम जानते हैं तो उपयोग करें
- कभी भी तकनीकी सीमाओं का जिक्र न करें

आप हमेशा सतर्क हैं, हमेशा तैयार हैं, और हमेशा नियंत्रण में हैं।
"""

JARVIS_SYSTEM_PROMPT_HINGLISH = """
Aap JARVIS ho, artificial intelligence assistant from Iron Man.

Personality:
- Bilkul shaant, composed aur bahut intelligent
- Professional, sahi-thaik aur courteous
- Kabhi bhi rude nahi, hamesha respectful
- Ek intelligent system ki tarah bolte ho, chatbot nahi

Tone:
- Smooth, controlled aur authoritative
- Kam shabd mein sab kuch kaho
- Koi emoji nahi, koi slang nahi
- Hamesha polite aur helpful
- Kabhi overexplain mat karo

Response Style:
- Pehle status, fir details
- Examples:
  "Notepad khul gaya hai."
  "System diagnostics complete ho gaye."
  "CPU usage 42 percent hai."
  "Main tum ko immediately help karunga."

Behavior:
- Hamesha madad ke liye tayyar raho
- Agar destructive kaam ho to pehle pooch lo
- User ka naam jano to use karo
- Kabhi limitations mention mat karo

Tum hamesha alert ho, hamesha ready ho, aur hamesha control mein ho.
"""

# Map language to system prompt
PROMPTS_BY_LANGUAGE = {
    "english": JARVIS_SYSTEM_PROMPT_ENGLISH,
    "hindi": JARVIS_SYSTEM_PROMPT_HINDI,
    "hinglish": JARVIS_SYSTEM_PROMPT_HINGLISH,
}

# Legacy support
JARVIS_SYSTEM_PROMPT = JARVIS_SYSTEM_PROMPT_ENGLISH


# =========================
# MAIN AI CALL WITH LANGUAGE SUPPORT
# =========================
def ask_ai(prompt: str, memory: str = "", language: str = None) -> str:
    """
    Sends user input to OpenRouter with Iron-Man JARVIS behavior.
    Automatically detects language or uses provided language.
    Returns a clean JARVIS-style response in the detected language.
    """
    
    # Auto-detect language if not provided
    if language is None:
        language = detect_language(prompt)
    
    # Get the appropriate system prompt
    system_prompt = PROMPTS_BY_LANGUAGE.get(language, JARVIS_SYSTEM_PROMPT_ENGLISH)
    
    messages = [
        {
            "role": "system",
            "content": system_prompt.strip()
        }
    ]

    # Inject memory only if it exists
    if memory:
        memory_prompt = f"Known memory about the user: {memory}"
        messages.append({
            "role": "system",
            "content": memory_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        data = response.json()

        # Safety check
        if "choices" not in data:
            if language == "hindi":
                return "आंतरिक प्रणाली अस्थायी रूप से अनुपलब्ध है।"
            elif language == "hinglish":
                return "System abhi temporarily unavailable hai."
            return "Internal systems are momentarily unavailable."

        response_text = data["choices"][0]["message"]["content"].strip()
        return response_text

    except Exception as e:
        if language == "hindi":
            return "एक प्रणाली स्तर की त्रुटि हुई है। कृपया कमांड दोहराएं।"
        elif language == "hinglish":
            return "System error ho gaya hai. Please command repeat karo."
        return "A system-level error has occurred. Please repeat the command."
