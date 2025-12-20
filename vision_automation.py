import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import json
import os
import subprocess

# ⚠️ SET TESSERACT PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

MACRO_FILE = "macros.json"


# ==================================================
# 🔍 SCREEN READING (OCR)
# ==================================================
def read_screen():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    elements = []

    for i, text in enumerate(data["text"]):
        if text.strip():
            elements.append({
                "text": text.lower(),
                "x": data["left"][i],
                "y": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i]
            })
    return elements


# ==================================================
# 🖱️ CLICK BASED ON SPOKEN TEXT
# ==================================================
def click_on_text(target: str) -> bool:
    elements = read_screen()
    target = target.lower()

    for el in elements:
        if target in el["text"]:
            x = el["x"] + el["w"] // 2
            y = el["y"] + el["h"] // 2
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            return True
    return False


# ==================================================
# 📁 FILE EXPLORER NAVIGATION
# ==================================================
def open_file_explorer():
    pyautogui.hotkey("win", "e")
    time.sleep(1)


def navigate_to(path: str):
    open_file_explorer()
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.4)
    pyautogui.write(path)
    pyautogui.press("enter")


# ==================================================
# 🔁 AUTO-FIX APP OPEN
# ==================================================
def app_visible(name: str) -> bool:
    elements = read_screen()
    return any(name.lower() in el["text"] for el in elements)


def open_any_app(app_name: str):
    try:
        subprocess.Popen(app_name)
        return True
    except:
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write(app_name)
        pyautogui.press("enter")
        return True


def open_with_retry(app_name: str, retries=3):
    for _ in range(retries):
        open_any_app(app_name)
        time.sleep(2)
        if app_visible(app_name):
            return True
    return False


# ==================================================
# 🎬 MACRO ENGINE (RECORD & PLAY)
# ==================================================
def record_macro(name: str, duration=5):
    actions = []
    start = time.time()

    while time.time() - start < duration:
        x, y = pyautogui.position()
        actions.append({"x": x, "y": y})
        time.sleep(0.2)

    save_macro(name, actions)


def save_macro(name, actions):
    if os.path.exists(MACRO_FILE):
        with open(MACRO_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[name] = actions

    with open(MACRO_FILE, "w") as f:
        json.dump(data, f, indent=2)


def play_macro(name: str):
    if not os.path.exists(MACRO_FILE):
        return

    with open(MACRO_FILE, "r") as f:
        data = json.load(f)

    for action in data.get(name, []):
        pyautogui.moveTo(action["x"], action["y"], duration=0.2)
        pyautogui.click()
