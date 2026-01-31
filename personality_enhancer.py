#!/usr/bin/env python3
"""
🧠 JARVIS PERSONALITY ENHANCER
Post-processing layer to add extra JARVIS smartness and vocabulary
"""

import re

# JARVIS vocabulary and phrases
JARVIS_VOCAB_ENGLISH = [
    ("i have", "I have taken the liberty of"),
    ("i can", "I shall"),
    ("yes", "Affirmative"),
    ("no", "I'm afraid that's not possible"),
    ("ok", "Very well"),
    ("good", "Excellent"),
    ("hello", "Good day, sir"),
    ("done", "Task complete"),
    ("working", "Currently operational"),
]

JARVIS_VOCAB_HINGLISH = [
    ("haan", "Bilkul, sir"),
    ("nahi", "Mujhe dukh se kah raha hoon, ye possible nahi hai"),
    ("theek hai", "Bilkul sahi hai"),
    ("acha", "Bahut acha"),
    ("namaste", "Aapko swagat hai, sir"),
    ("ho gaya", "Complete ho gaya"),
    ("chal raha", "Operational hai"),
]

def enhance_personality_english(response: str) -> str:
    """
    Post-process English response to add JARVIS personality
    """
    # If response is very short, add more sophistication
    if len(response) < 20 and response.lower() not in ["affirmative", "understood"]:
        if not any(phrase in response for phrase in ["sir", "Very", "Affirmative", "I"]):
            response = f"Very good, sir. {response}"
    
    # Add "sir" if missing in longer responses
    if len(response) > 50 and "sir" not in response.lower():
        # Add "sir" at a natural point
        if response.endswith("."):
            response = response[:-1] + ", sir."
    
    # Replace casual phrases with JARVIS vocabulary
    for casual, jarvis_style in JARVIS_VOCAB_ENGLISH:
        pattern = rf'\b{re.escape(casual)}\b'
        response = re.sub(pattern, jarvis_style, response, flags=re.IGNORECASE)
    
    # Ensure periods instead of exclamation marks
    response = response.replace("!", ".")
    
    return response

def enhance_personality_hinglish(response: str) -> str:
    """
    Post-process Hinglish response to add JARVIS personality
    """
    # If response is very short, add more sophistication
    if len(response) < 20 and response.lower() not in ["bilkul", "haan"]:
        if not any(phrase in response for phrase in ["sir", "bilkul", "main"]):
            response = f"Bilkul, sir. {response}"
    
    # Replace casual phrases with JARVIS vocabulary
    for casual, jarvis_style in JARVIS_VOCAB_HINGLISH:
        pattern = rf'\b{re.escape(casual)}\b'
        response = re.sub(pattern, jarvis_style, response, flags=re.IGNORECASE)
    
    # Ensure periods instead of exclamation marks
    response = response.replace("!", ".")
    
    return response

# Test
if __name__ == "__main__":
    test_en = "yes, i can help you with that"
    test_hi = "haan, main tumhare liye madad kar sakta hoon"
    
    print("English Enhancement:")
    print(f"  Before: {test_en}")
    print(f"  After:  {enhance_personality_english(test_en)}\n")
    
    print("Hinglish Enhancement:")
    print(f"  Before: {test_hi}")
    print(f"  After:  {enhance_personality_hinglish(test_hi)}")
