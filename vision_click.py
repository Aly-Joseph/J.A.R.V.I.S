import pyautogui
import pytesseract
import cv2

def click_text_on_screen(target_text, image_path):
    image = cv2.imread(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data["text"]):
        if target_text.lower() in word.lower():
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            cx = x + w // 2
            cy = y + h // 2

            pyautogui.click(cx, cy)
            return True

    return False
