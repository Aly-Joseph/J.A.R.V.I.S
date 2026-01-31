# JARVIS Skills Directory

This directory contains organized skill modules for the JARVIS AI Assistant.

## Available Skills

### 1. Voice Recognition
**Slug**: `voice-recognition`
- Real-time voice input capture
- Speech-to-text conversion
- Multi-language support
- [View Details](./voice-recognition/SKILL.md)

### 2. Vision Automation
**Slug**: `vision-automation`
- Screen reading and OCR
- UI element detection
- Automated clicking
- [View Details](./vision-automation/SKILL.md)

### 3. Robotic Control (OpenClaw)
**Slug**: `robotic-control`
- Robotic arm manipulation
- Gripper control
- Force/torque sensing
- Collision detection
- [View Details](./robotic-control/SKILL.md)

### 4. AI Generation
**Slug**: `ai-generation`
- Code generation
- Content writing
- Context-aware generation
- [View Details](./ai-generation/SKILL.md)

### 5. Memory System
**Slug**: `memory-system`
- User information storage
- Context persistence
- Conversation history
- [View Details](./memory-system/SKILL.md)

### 6. Emotion Detection
**Slug**: `emotion-detection`
- Emotional state analysis
- Sentiment detection
- Response adaptation
- [View Details](./emotion-detection/SKILL.md)

### 7. Task Routing
**Slug**: `task-routing`
- Intent detection
- Command routing
- Task prioritization
- [View Details](./task-routing/SKILL.md)

## Skill Structure

Each skill folder contains:
- `SKILL.md` - Complete skill documentation
- Implementation files (Python modules)
- Configuration files (if needed)
- Test files (if applicable)

## Adding New Skills

To add a new skill:

1. Create a new folder with lowercase slug format (e.g., `new-skill`)
2. Create a `SKILL.md` file following the template
3. Include implementation files
4. Update this index file

### SKILL.md Template

```markdown
# Skill Name

## Overview
Brief description of what the skill does.

## Slug
`skill-slug-name`

## Features
- Feature 1
- Feature 2
- Feature 3

## Implementation
- **Module**: module_name.py
- **Primary Library**: Library name
- **Methods**: Main methods/functions

## Voice Commands
- "Example command 1"
- "Example command 2"

## Performance
- Metric 1: Value
- Metric 2: Value

## Dependencies
- Dependency 1
- Dependency 2

## Author
Aly-Joseph

## Version
1.0.0

## Last Updated
YYYY-MM-DD
```

## Integration Guide

### Using Skills in Code

```python
# Example: Voice Recognition Skill
from voice import listen

command = listen()
```

```python
# Example: Vision Automation Skill
from vision_engine import read_screen_text, click_on_text

text = read_screen_text()
click_on_text("button_name")
```

```python
# Example: Robotic Control Skill
from openclaw_control import init_claw

claw = init_claw()
claw.grab(force=50.0)
```

### Accessing Skill Documentation

Each skill is self-documenting through its `SKILL.md` file. View the documentation to understand:
- Capabilities and features
- Usage examples
- Performance metrics
- Dependencies
- Configuration options

## Skill Versioning

Skills follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to the skill interface
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes and improvements

## Contributing Skills

When contributing a new skill:

1. Follow the folder naming convention (lowercase with dashes)
2. Create comprehensive `SKILL.md` documentation
3. Include working code examples
4. Test thoroughly
5. Update this index file
6. Submit a pull request

## License

All skills are part of the JARVIS AI project and licensed under MIT License.

## Support

For skill-related questions or issues:
- Check the skill's `SKILL.md` documentation
- Review code examples in the skill folder
- Open an issue on GitHub: [github.com/Aly-Joseph/J.A.R.V.I.S/issues](https://github.com/Aly-Joseph/J.A.R.V.I.S/issues)

---

**Last Updated**: 2026-01-31  
**Total Skills**: 7  
**Status**: Active Development
