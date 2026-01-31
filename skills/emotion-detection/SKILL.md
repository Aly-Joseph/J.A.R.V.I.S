# Emotion Detection Skill

## Overview
The Emotion Detection skill analyzes user input to detect emotional state and adapts JARVIS responses accordingly.

## Slug
`emotion-detection`

## Features
- Emotional state detection
- Sentiment analysis
- Tone adaptation
- Sarcasm level control
- Response personalization
- Mood-based behavior adjustment

## Implementation
- **Modules**: `emotion_ai.py`, `emotion.py`
- **Analysis Methods**: Keyword matching, NLP analysis
- **Adaptation System**: Dynamic response tuning

## Configuration
```python
from emotion_ai import detect_emotion

# Detect user emotion
emotion = detect_emotion("I'm so frustrated with this!")
print(f"Detected emotion: {emotion}")
```

## Detected Emotions
- Angry / Frustrated
- Happy / Excited
- Sad / Disappointed
- Calm / Neutral
- Serious / Warning
- Confused / Uncertain

## Voice Commands
- "Jarvis, I'm happy"
- "Jarvis, I need help"
- "Jarvis, I'm stressed"
- "How do I sound?"

## Response Adaptation
- **Angry**: Calm, reassuring tone
- **Happy**: Enthusiastic, positive tone
- **Sad**: Empathetic, supportive tone
- **Serious**: Professional, focused tone

## Performance
- Detection Time: < 100ms
- Accuracy: 80-85%
- Real-time processing

## Dependencies
- re (regex)
- textblob or similar NLP library

## Author
Aly-Joseph

## Version
1.0.0

## Last Updated
2026-01-31
