from brain import ask_ai

def normalize_language(text: str, target_language: str = "english") -> str:
    """
    Converts mixed-language content into clean English or Hindi.
    """

    prompt = f"""
Convert the following content into clean, simple {target_language}.
Rules:
- No foreign language words
- No emojis
- Clear spoken sentences
- Short and natural for voice output

Content:
{text}
"""

    return ask_ai(prompt)
