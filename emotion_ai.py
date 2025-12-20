# emotion_ai.py — AI-based emotion selector (Jarvis)

def detect_emotion(user_text: str, ai_reply: str = "") -> str:
    text = (user_text + " " + ai_reply).lower()

    # 🔴 WARNING / ALERT
    if any(k in text for k in [
        "error", "failed", "denied", "blocked", "danger",
        "warning", "alert", "security", "attack", "critical"
    ]):
        return "warning"

    # 🔵 SERIOUS / SYSTEM
    if any(k in text for k in [
        "system", "cpu", "memory", "ram", "disk",
        "network", "server", "admin", "permission",
        "process", "configuration", "status"
    ]):
        return "serious"

    # 🟢 DEFAULT
    return "calm"
