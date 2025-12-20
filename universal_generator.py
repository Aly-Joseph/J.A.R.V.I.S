from brain import ask_ai

def generate_anything(user_command: str, context: str = "") -> str:
    prompt = f"""
You are an expert software engineer and technical writer.

User request:
{user_command}

Context (if any):
{context}

Rules:
- Generate COMPLETE output
- Do not explain
- Do not add markdown fences
- Output must be directly usable
"""
    return ask_ai(prompt)
