class JarvisHUDState:
    """
    Bridge between real JARVIS logic and HUD.
    Later main.py will control this.
    """

    def __init__(self):
        self.listening = False
        self.thinking = False
        self.speaking = False

    def set_listening(self, v: bool):
        self.listening = v

    def set_thinking(self, v: bool):
        self.thinking = v

    def set_speaking(self, v: bool):
        self.speaking = v
