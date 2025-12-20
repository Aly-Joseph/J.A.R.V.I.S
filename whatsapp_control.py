import pyautogui
import time

def send_whatsapp_message(contact_name: str, message: str):
    # Open WhatsApp
    pyautogui.press("win")
    time.sleep(0.5)
    pyautogui.write("whatsapp")
    pyautogui.press("enter")
    time.sleep(3)

    # Search contact
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.5)
    pyautogui.write(contact_name)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)

    # Type message
    pyautogui.write(message, interval=0.04)
    time.sleep(0.5)
    pyautogui.press("enter")
