# vision_engine.py — JARVIS VISION CORE

import pytesseract
import cv2
import numpy as np
import pyautogui

# If Tesseract is not in PATH (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================
# SCREENSHOT
# =========================
def capture_screen():
    img = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return frame


# =========================
# OCR (POLISHED)
# =========================
def read_screen_text():
    frame = capture_screen()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(gray, config=config)

    clean = [line.strip() for line in text.splitlines() if len(line.strip()) > 2]
    return clean

# =========================
# FIND TEXT LOCATION
# =========================
def find_text_position(target: str):
    frame = capture_screen()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT
    )

    target = target.lower()

    for i, txt in enumerate(data["text"]):
        if target in txt.lower():
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            cx = x + w // 2
            cy = y + h // 2

            return (cx, cy)

    return None

# =========================
# CLICK ELEMENT
# =========================
def click_on_text(target: str):
    pos = find_text_position(target)

    if pos is None:
        return False

    pyautogui.moveTo(pos[0], pos[1], duration=0.2)
    pyautogui.click()
    return True
