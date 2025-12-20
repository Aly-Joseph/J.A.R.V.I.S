from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPen
import math

class JarvisRing(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.glow = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle = (self.angle + 2) % 360
        self.update()

    def set_listening(self, active: bool):
        self.glow = active

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        r = min(w, h) // 3

        pen = QPen(Qt.cyan if self.glow else Qt.darkCyan, 4)
        p.setPen(pen)

        p.translate(w // 2, h // 2)
        p.rotate(self.angle)

        p.drawEllipse(-r, -r, r * 2, r * 2)
