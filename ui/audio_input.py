import sounddevice as sd
import numpy as np

class MicListener:
    def __init__(self):
        self.raw = 0.0
        self.smooth = 0.0

        self.stream = sd.InputStream(
            channels=1,
            callback=self.callback,
            blocksize=1024,
            samplerate=44100
        )
        self.stream.start()

    def callback(self, indata, frames, time, status):
        volume = np.linalg.norm(indata) * 10
        self.raw = min(volume, 1.0)

    def get_level(self):
        # 🔥 exponential smoothing (NO BLINK)
        alpha = 0.15
        self.smooth = (1 - alpha) * self.smooth + alpha * self.raw
        return self.smooth
