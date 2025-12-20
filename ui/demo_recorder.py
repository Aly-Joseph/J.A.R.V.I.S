import time

class DemoMode:
    """
    Safe demo mode:
    - No mic
    - No API
    - Loop animations
    """

    def __init__(self):
        self.active = True
        self.start_time = time.time()

    def status_text(self):
        t = int(time.time() - self.start_time)
        return f"DEMO MODE · {t}s"
