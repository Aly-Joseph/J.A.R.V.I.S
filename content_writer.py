from brain import ask_ai

def generate_content(topic: str) -> str:
    prompt = f"""
Write a clear, well-structured response for the following request.
Keep the tone neutral and informative.
Request: {topic}
"""
    return ask_ai(prompt)
