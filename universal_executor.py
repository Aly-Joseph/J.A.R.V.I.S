import os
import time
import pyautogui

def type_anywhere(content: str):
    time.sleep(0.5)
    pyautogui.write(content, interval=0.01)


def save_to_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    os.startfile(filename)
