def detect_emotion(text: str) -> str:
    t = text.lower()

    if any(x in t for x in [
        "fight", "argument", "ladayi", "ladai",
        "angry", "upset", "sad", "hurt",
        "wife", "girlfriend", "partner"
    ]):
        return "relationship_conflict"

    if any(x in t for x in [
        "tired", "stress", "pressure", "depressed"
    ]):
        return "stress"

    return "neutral"
