def detect_language(text):
    t = text.lower()

    if any(x in t for x in ["hindi", "हिंदी"]):
        return "hindi"

    if any(x in t for x in ["hinglish"]):
        return "hinglish"

    return "english"
