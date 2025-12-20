from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ring_widget import JarvisRing

class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("J.A.R.V.I.S")
        self.setGeometry(200, 100, 1200, 700)
        self.setStyleSheet("background-color: #050b14;")

        container = QWidget()
        layout = QVBoxLayout(container)

        # 🔵 RING INSTANCE
        self.ring = JarvisRing()
        self.ring.setMinimumSize(400, 400)

        layout.addStretch()
        layout.addWidget(self.ring)
        layout.addStretch()

        self.setCentralWidget(container)
