def detect_errors(screen_text):
    errors = [
        "error",
        "failed",
        "invalid",
        "exception",
        "not found",
        "unauthorized"
    ]

    found = []
    for e in errors:
        if e in screen_text.lower():
            found.append(e)

    return found
