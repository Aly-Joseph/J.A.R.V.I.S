# Vision Automation Skill

## Overview
The Vision Automation skill provides screen reading, object detection, and automated clicking capabilities using computer vision and OCR.

## Slug
`vision-automation`

## Features
- Screen text recognition (OCR)
- UI element detection
- Automated clicking on detected elements
- Visual search and locate
- Screenshot capture and analysis

## Implementation
- **Modules**: `vision_engine.py`, `vision_ocr.py`, `vision_click.py`
- **Primary Libraries**: `OpenCV`, `Tesseract-OCR`, `PyAutoGUI`
- **Detection Methods**: Template matching, feature detection

## Configuration
```python
from vision_engine import read_screen_text, click_on_text

# Read text from screen
text_lines = read_screen_text()

# Click on detected text
success = click_on_text("Submit Button")
```

## Voice Commands
- "Jarvis, what is on screen?"
- "Jarvis, click on [element]"
- "Jarvis, read the text"
- "Jarvis, find the button"

## Performance
- Detection Speed: 100-500ms
- Accuracy: 90%+ for UI elements
- Maximum Screen Resolution: 4K

## Dependencies
- OpenCV
- Tesseract-OCR
- PyAutoGUI
- Pillow
- numpy

## Author
Aly-Joseph

## Version
1.0.0

## Last Updated
2026-01-31
