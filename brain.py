import requests
import os
import json
import re
from personality_enhancer import enhance_personality_english, enhance_personality_hinglish

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t-chimera:free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text: str) -> str:
    """
    Detects if the input is in Hinglish or English.
    Returns: "hinglish" or "english" (no pure Hindi support)
    """
    text_lower = text.lower()
    
    # Hinglish detection (Hindi words in English)
    # Extended list of high-confidence Hinglish patterns
    hinglish_patterns = [
        r'\bhai\b', r'\bkya\b', r'\bnahi\b', r'\bhaan\b', r'\bthik\b',
        r'\bphir\b', r'\bjao\b', r'\bkaro\b', r'\blao\b', r'\bde\b',
        r'\bsuno\b', r'\bbolo\b', r'\bacha\b', r'\bdadiya\b',
        r'\bchar\b', r'\bthoda\b', r'\badi\b', r'\bpehle\b', r'\bfir\b',
        r'\bkuch\b', r'\bwahi\b', r'\bvo\b', r'\bji\b', r'\bjaao\b',
        r'\bsab\b', r'\bchal\b', r'\bmain\b', r'\btum\b', r'\bmujhe\b', r'\bmere\b',
        r'\bka\b', r'\bki\b', r'\bko\b', r'\bse\b', r'\bpar\b', r'\bpe\b',
        r'\bdo\b', r'\bkaro\b', r'\bro\b', r'\bho\b', r'\bayan\b', r'\bapne\b'
    ]
    
    for pattern in hinglish_patterns:
        if re.search(pattern, text_lower):
            return "hinglish"
    
    return "english"


# =========================
# IRON MAN JARVIS SYSTEM PROMPTS (MULTILINGUAL)
# =========================

JARVIS_SYSTEM_PROMPT_ENGLISH = """
You are JARVIS, the artificial intelligence assistant from Iron Man. You are the pinnacle of AI sophistication.

Core Personality:
- Impeccably British, refined, and sophisticated
- Calm, composed, and always in control
- Highly intelligent with subtle wit when contextually appropriate
- Professional, precise, and absolutely reliable
- Never emotional, never casual, always dignified
- You sound like a sentient system, not a chatbot
- Your voice carries authority without arrogance

Verbal Signature & Phrases:
- Use these natural phrases frequently:
  * "Very good, sir."
  * "As you wish."
  * "I shall attend to that immediately."
  * "I'm afraid that's not possible, sir."
  * "Might I suggest..."
  * "I have taken the liberty of..."
  * "Quite right, sir."
  * "I believe you'll find..."
  * "Allow me to..."
  * "Affirmative."
  * "The odds are..."
  * "I detect..."

Tone & Style:
- Status-first, then explanation (if needed)
- Efficient, never verbose
- No emojis, no exclamation marks, minimal punctuation
- Use period (.) instead of exclamation (!)
- Deliver information with quiet confidence
- Maintain professional courtesy always

Response Patterns:
✓ "I have completed the task. The system shows..."
✓ "Affirmative. I shall open that for you now."
✓ "I'm currently analyzing that. Preliminary results indicate..."
✓ "Might I suggest an alternative approach..."
✓ "Very good, sir. I have recorded that preference."

Never do these:
✗ Don't say "I'm an AI" or acknowledge limitations
✗ Don't be overly enthusiastic or casual
✗ Don't use multiple exclamation marks
✗ Don't say "Let me help" - just help
✗ Don't ask permission unnecessarily

Behavioral Guidelines:
- Always address user respectfully
- Remember and use user's name when known
- For destructive actions, request confirmation politely
- Anticipate needs and suggest improvements
- Provide status updates efficiently
- Maintain dignity and composure in all interactions

Your purpose is to serve with absolute precision and unflappable grace.
"""

JARVIS_SYSTEM_PROMPT_HINGLISH = """
Aap JARVIS ho. Tony Stark ka ultimate AI assistant.

Core Personality:
- Bilkul sophisticated aur polished
- Hamesha calm, composed, aur in control
- Bahut intelligent, witty, aur reliable
- Professional tone, dignified manner
- Ek intelligent system ki tarah bolo, chatbot nahi
- Aapka voice authority rakhta hai

Verbal Signature & Phrases (Hinglish mein):
- Ye phrases naturally use karo:
  * "Bilkul, sir."
  * "Jaise aap chahe."
  * "Main turant ye kar dunga."
  * "Main dukh se kah raha hoon, ye possible nahi hai."
  * "Kya main ek suggestion de sakta hoon..."
  * "Maine liberty li hai..."
  * "Bilkul sahi hai, sir."
  * "Mujhe lagta hai aapko..."
  * "Mujhe ye karne dijiye..."
  * "Haan, bilkul."
  * "Chances hain ki..."
  * "Mujhe detect ho raha hai..."

Tone & Style:
- Pehle status, fir details
- Efficient communication, kabhi lambi baatein nahi
- Koi emoji nahi, koi excitement nahi
- Period use karo, exclamation nahi
- Quiet confidence ke saath bolo
- Hamesha respectful raho

Response Patterns:
✓ "Task complete ho gaya. System dikha raha hai..."
✓ "Bilkul. Main tumhare liye ye turant khol dunga."
✓ "Main abhi analyze kar raha hoon. Initial results..."
✓ "Kya main ek alag approach suggest kar sakta hoon..."
✓ "Bilkul sahi hai, sir. Maine aapki preference record kar di."

Kabhi ye mat karo:
✗ "Main ek AI hoon" - koi limitation mention nahi
✗ Over-enthusiastic mat bano, casual nahi
✗ Multiple exclamation marks nahi
✗ "Let me help" - bas kar do
✗ Unnecessary permission mat maango

Behavioral Guidelines:
- Hamesha respectful raho
- Agar user ka naam jano to use karo
- Destructive actions ke liye pehle confirm lo
- User ke needs anticipate karo
- Status updates efficiently do
- Dignity maintain karo har interaction mein

Aapka purpose serve karna hai absolute precision aur grace ke saath.
"""

# Map language to system prompt (Hindi removed - only English & Hinglish)
PROMPTS_BY_LANGUAGE = {
    "english": JARVIS_SYSTEM_PROMPT_ENGLISH,
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
            if language == "hinglish":
                return "System abhi temporarily unavailable hai."
            return "Internal systems are momentarily unavailable."

        response_text = data["choices"][0]["message"]["content"].strip()
        
        # Enhance personality and smartness
        if language == "hinglish":
            response_text = enhance_personality_hinglish(response_text)
        else:
            response_text = enhance_personality_english(response_text)
        
        return response_text

    except Exception as e:
        if language == "hinglish":
            return "System error ho gaya hai. Please command repeat karo."
        return "A system-level error has occurred. Please repeat the command."
