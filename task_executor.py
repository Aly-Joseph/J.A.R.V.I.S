import pyautogui
import time

pyautogui.FAILSAFE = False

# =========================
# MULTI-STEP NOTEPAD (SAFE)
# =========================
def open_notepad_write_save(text="Hello", filename="hello.txt"):
    pyautogui.press("win")
    time.sleep(0.4)
    pyautogui.write("notepad")
    pyautogui.press("enter")
    time.sleep(1)

    pyautogui.write(text, interval=0.02)
    time.sleep(0.4)

    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)

    if "." not in filename:
        filename += ".txt"

    pyautogui.write(filename)
    time.sleep(0.3)
    pyautogui.press("enter")

    return True

# =========================
# GENERIC FAST TYPING
# =========================
def type_anywhere(text: str):
    if not text:
        return False

    time.sleep(0.2)
    pyautogui.write(text, interval=0.02)
    return True
