def route_task(task: str) -> str:
    t = task.lower()

    # ==================================================
    # 💾 SAVE CURRENT FILE (HIGHEST PRIORITY)
    # ==================================================
    if any(x in t for x in [
        "save this",
        "save it",
        "save page",
        "is page ko save",
        "file save kar do",
        "save the file"
    ]):
        return "save_file"

    # ==================================================
    # 🧠 GENERATE IN VS CODE (EXPLICIT)
    # ==================================================
    if any(x in t for x in ["vs code", "vscode", "visual studio"]):
        if any(x in t for x in [
            "generate", "create", "build",
            "write", "make", "code", "script"
        ]):
            return "generate_in_vscode"

    # ==================================================
    # 🔥 UNIVERSAL GENERATION (TOP PRIORITY)
    # ==================================================
    if any(x in t for x in [
        # intent verbs
        "generate", "create", "build", "make",
        "write", "draft", "design",

        # content types
        "code", "script", "program",
        "html", "css", "javascript",
        "python", "sql", "react", "node",
        "backend", "frontend",

        # page intents
        "login page", "signup page",
        "web page", "webpage",
        "website", "page", "form"
    ]):
        return "universal_generate"

    # ==================================================
    # 👁️ SCREEN VISION
    # ==================================================
    if "click on" in t:
        return "vision_click"

    # ==================================================
    # 📁 FILE NAVIGATION
    # ==================================================
    if "open folder" in t:
        return "file_navigation"

    # ==================================================
    # 🔁 AUTO-FIX APP OPEN
    # ==================================================
    if "retry" in t and any(x in t for x in ["open", "launch", "start"]):
        return "auto_fix"

    # ==================================================
    # 🎬 MACROS
    # ==================================================
    if "record macro" in t:
        return "record_macro"
    if "run macro" in t:
        return "run_macro"

    # ==================================================
    # ⌨️ GENERIC KEYBOARD (LAST RESORT)
    # ==================================================
    if any(x in t for x in ["type", "enter text"]):
        return "keyboard"

    # ==================================================
    # APPLICATION OPEN
    # ==================================================
    if any(x in t for x in ["open", "launch", "start"]):
        if "calculator" in t:
            return "open_calculator"
        if "notepad" in t:
            return "open_notepad"
        if "browser" in t or "chrome" in t:
            return "open_browser"
        if "task manager" in t:
            return "open_task_manager"
        if "settings" in t:
            return "open_settings"
        return "open_any_app"

    # ==================================================
    # 🌐 INTERNET
    # ==================================================
    if any(x in t for x in [
        "latest", "news", "today",
        "search", "google", "bing",
        "weather", "crypto", "bitcoin"
    ]):
        return "internet"

    # ==================================================
    # 🖥 SYSTEM INFO
    # ==================================================
    if any(x in t for x in [
        "system info", "cpu", "ram",
        "battery", "time", "date"
    ]):
        return "system_info"

    # ==================================================
    # 🧠 MEMORY
    # ==================================================
    if any(x in t for x in [
        "remember", "my name is",
        "what do you remember"
    ]):
        return "memory"

    # ==================================================
    # 👁️ SCREEN VISION CLICK
    # ==================================================
    if "click on" in t:
        return "vision_click"

    # ==================================================
    # 👁️ SCREEN VISION READ
    # ==================================================
    if "what is on screen" in t or "read my screen" in t:
        return "vision_read"

    # ==================================================
    # 🤖 FALLBACK AI
    # ==================================================
    return "ai"
