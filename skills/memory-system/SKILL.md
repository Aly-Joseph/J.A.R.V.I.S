# Memory System Skill

## Overview
The Memory System skill provides persistent JSON-based storage for user information, context, and conversation history.

## Slug
`memory-system`

## Features
- User information storage
- Context persistence
- Conversation history
- Preference learning
- Task continuation tracking
- Named position saving
- Contextual recall

## Implementation
- **Modules**: `memory.py`, `message_memory.py`, `continuation_handler.py`
- **Storage Format**: JSON files
- **Persistence**: Local file-based

## Configuration
```python
from memory import remember, recall

# Store information
remember("user_name", "John")
remember("favorite_color", "blue")

# Retrieve information
name = recall("user_name")
color = recall("favorite_color")
```

## Voice Commands
- "Jarvis, remember my name is [name]"
- "Jarvis, what do you remember about me?"
- "Jarvis, forget that"
- "Jarvis, remember this task"

## Memory Types
- User Profile (name, role, preferences)
- Conversation Context
- Task History
- Named Positions (for robotic operations)
- User Emotions
- Task Continuations

## Performance
- Recall Time: < 10ms
- Storage Limit: Unlimited (file-based)
- Persistence: Permanent across sessions

## Dependencies
- json
- os
- datetime

## Author
Aly-Joseph

## Version
1.0.0

## Last Updated
2026-01-31
