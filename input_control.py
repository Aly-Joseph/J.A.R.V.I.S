import pyautogui
import time
import pygetwindow as gw
import subprocess
import pyperclip

pyautogui.FAILSAFE = False

# ==================================================
# 🔍 WINDOW FOCUS (SAFE)
# ==================================================
def focus_window(title_keywords, timeout=5):
    end_time = time.time() + timeout

    while time.time() < end_time:
        for w in gw.getAllWindows():
            try:
                title = (w.title or "").lower()
                if any(k.lower() in title for k in title_keywords):
                    w.activate()
                    time.sleep(0.4)
                    return True
            except:
                pass
        time.sleep(0.2)

    return False


# ==================================================
# 🧱 APPLICATION OPENERS (STABLE)
# ==================================================

def open_notepad():
    pyautogui.press("win")
    time.sleep(0.4)
    pyautogui.write("notepad")
    pyautogui.press("enter")
    time.sleep(1)

    # Windows 11 Notepad title unreliable
    # optimistic success (IMPORTANT)
    return True


def open_calculator():
    pyautogui.press("win")
    time.sleep(0.4)
    pyautogui.write("calculator")
    pyautogui.press("enter")
    time.sleep(1)

    return True


def open_browser():
    pyautogui.press("win")
    time.sleep(0.4)
    pyautogui.write("chrome")
    pyautogui.press("enter")
    time.sleep(2)

    return True


def open_task_manager():
    pyautogui.hotkey("ctrl", "shift", "esc")
    time.sleep(1)

    return True


def open_settings():
    pyautogui.hotkey("win", "i")
    time.sleep(1)

    return True


def open_vscode():
    pyautogui.press("win")
    time.sleep(0.4)
    pyautogui.write("visual studio code")
    pyautogui.press("enter")
    time.sleep(2)

    return True


def open_any_application(app_name: str):
    try:
        subprocess.Popen(app_name)
        time.sleep(2)
    except:
        pyautogui.press("win")
        time.sleep(0.4)
        pyautogui.write(app_name)
        pyautogui.press("enter")
        time.sleep(2)

    return True


# ==================================================
# ⌨️ CLIPBOARD SAFE PASTE
# ==================================================
def paste_text(text: str):
    if not text:
        return False

    pyperclip.copy(text)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)

    return True


# ==================================================
# 💾 SAVE FILE (NOTEPAD + VS CODE)
# ==================================================
def save_current_file(filename: str):
    if not filename:
        return False

    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)

    if "." not in filename:
        filename += ".html"

    pyautogui.write(filename)
    time.sleep(0.3)
    pyautogui.press("enter")

    return True

def type_text_slow(text: str, interval=0.015):
    """
    Human-like live typing (no clipboard)
    """
    if not text:
        return False

    for line in text.split("\n"):
        pyautogui.write(line, interval=interval)
        pyautogui.press("enter")
        time.sleep(0.05)

    return True
