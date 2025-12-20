import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QTimer

from hud_core import JarvisHUDCore
from audio_input import MicListener

class JarvisHUDWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS HUD – MIC REACTIVE MODE")
        self.setGeometry(80, 60, 1500, 950)

        # glass / hologram
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QMainWindow {
                background: rgba(0, 10, 20, 150);
            }
        """)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(30, 30, 30, 30)

        self.hud = JarvisHUDCore()
        self.mic = MicListener()

        self.label = QLabel("MIC ACTIVE · SPEAK TO SEE WAVES")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "color: rgba(180,220,255,160); font-size:13px;"
        )

        layout.addWidget(self.hud, 1)
        layout.addWidget(self.label)

        self.setCentralWidget(root)

        # 🔁 mic → hud sync loop
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_audio)
        self.sync_timer.start(30)

    def sync_audio(self):
        self.hud.set_audio_level(self.mic.get_level())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = JarvisHUDWindow()
    win.show()
    sys.exit(app.exec())
