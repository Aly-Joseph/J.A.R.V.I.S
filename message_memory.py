import json
import os
from datetime import datetime

FILE = "message_history.json"

def _load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_message(contact, message, status):
    history = _load()
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contact": contact,
        "message": message,
        "status": status  # drafted / sent / cancelled
    })
    _save(history)

def last_message():
    history = _load()
    return history[-1] if history else None
