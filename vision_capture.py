import pyautogui
import cv2
import numpy as np
import time

def capture_screen(save_path="screen.png"):
    screenshot = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path, image)
    return save_path
