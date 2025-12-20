import json
import os

FILE = "memory.json"

def _load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(mem: dict):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)

def remember(key: str, value):
    mem = _load()
    mem[key] = value
    _save(mem)

def recall(key: str = None):
    mem = _load()
    if key:
        return mem.get(key)
    return mem
