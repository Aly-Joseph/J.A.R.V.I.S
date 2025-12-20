from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor, QPen, QRadialGradient, QFont
import math
import random


# =========================
# PARTICLE
# =========================
class Particle:
    def __init__(self, cx, cy, angle, speed):
        self.x = cx
        self.y = cy
        self.vx = math.cos(angle) * speed + random.uniform(-0.4, 0.4)
        self.vy = math.sin(angle) * speed + random.uniform(-0.4, 0.4)
        self.life = random.randint(120, 260)
        self.size = random.uniform(2.0, 4.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def alive(self, w, h):
        return (
            self.life > 0
            and -50 < self.x < w + 50
            and -50 < self.y < h + 50
        )


# =========================
# JARVIS HUD CORE
# =========================
class JarvisHUDCore(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0.0
        self.audio = 0.0
        self.energy = 0.0

        # fake audio bands
        self.low = 0.0
        self.mid = 0.0
        self.high = 0.0

        self.wave_noise = [random.uniform(0.6, 1.4) for _ in range(180)]
        self.boxes = [
            {
                "offset": random.uniform(0, 360),
                "speed": random.uniform(0.15, 1.1)
            }
            for _ in range(18)
        ]

        self.particles = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    # 🎤 mic input
    def set_audio_level(self, level: float):
        self.audio = max(0.0, min(1.0, level))

    def animate(self):
        # smooth energy
        self.energy += (self.audio - self.energy) * 0.06

        # fake band split (stable & cinematic)
        self.low = self.energy * 0.9
        self.mid = min(1.0, self.energy * 1.4)
        self.high = min(1.0, self.energy * 2.2)

        self.angle += 0.5

        cx = self.width() // 2
        cy = self.height() // 2
        base = min(cx, cy) - 100

        # =========================
        # PARTICLE SPAWN (DENSE)
        # =========================
        spawn_count = int(2 + self.mid * 8)
        for _ in range(spawn_count):
            ang = random.uniform(0, math.tau)
            speed = 1.8 + self.high * 4.0
            px = cx + math.cos(ang) * base
            py = cy + math.sin(ang) * base
            self.particles.append(Particle(px, py, ang, speed))

        # update particles
        w, h = self.width(), self.height()
        self.particles = [p for p in self.particles if p.alive(w, h)]
        for p in self.particles:
            p.update()

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2
        base = min(cx, cy) - 100

        # =========================
        # UNEVEN OUTER WAVES
        # =========================
        pen = QPen(QColor(0, 220, 255, 220), 4)
        p.setPen(pen)

        for i in range(180):
            a1 = math.radians(i * 2 + self.angle)
            a2 = math.radians((i + 1) * 2 + self.angle)

            noise = self.wave_noise[i] * self.energy * 22
            r = base + noise

            x1 = cx + math.cos(a1) * r
            y1 = cy + math.sin(a1) * r
            x2 = cx + math.cos(a2) * r
            y2 = cy + math.sin(a2) * r

            p.drawLine(int(x1), int(y1), int(x2), int(y2))

        # =========================
        # BOXES (MULTI SEQUENCE)
        # =========================
        pen = QPen(QColor(0, 180, 255, 170), 3)
        p.setPen(pen)

        for b in self.boxes:
            ang = math.radians(self.angle * b["speed"] + b["offset"])
            rx = cx + math.cos(ang) * (base - 30)
            ry = cy + math.sin(ang) * (base - 30)
            p.drawRect(int(rx - 6), int(ry - 6), 12, 12)

        # =========================
        # INNER STABLE RING
        # =========================
        pen = QPen(QColor(160, 255, 255, 180), 3)
        p.setPen(pen)
        p.drawEllipse(
            cx - (base - 80),
            cy - (base - 80),
            (base - 80) * 2,
            (base - 80) * 2
        )

        # =========================
        # SMOKE (SLOW & CINEMATIC)
        # =========================
        smoke_radius = base + 40 + self.low * 60
        smoke = QRadialGradient(cx, cy, smoke_radius)
        smoke.setColorAt(0.0, QColor(120, 220, 255, int(120 * self.low)))
        smoke.setColorAt(0.6, QColor(40, 140, 200, int(60 * self.low)))
        smoke.setColorAt(1.0, QColor(0, 0, 0, 0))

        p.setBrush(smoke)
        p.setPen(Qt.NoPen)
        p.drawEllipse(
            int(cx - smoke_radius),
            int(cy - smoke_radius),
            int(smoke_radius * 2),
            int(smoke_radius * 2)
        )

        # =========================
        # PARTICLES (FULL SCREEN)
        # =========================
        for pt in self.particles:
            alpha = int(200 * (pt.life / 260))
            p.setBrush(QColor(120, 220, 255, alpha))
            p.setPen(Qt.NoPen)
            p.drawEllipse(int(pt.x), int(pt.y),
                          int(pt.size), int(pt.size))

        # =========================
        # CENTER TEXT
        # =========================
        font = QFont("Arial Black")
        font.setPointSize(36)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 6)
        p.setFont(font)

        text = "J A R V I S"
        fm = p.fontMetrics()
        w = fm.horizontalAdvance(text)

        p.setPen(QColor(220, 255, 255))
        p.drawText(cx - w // 2, cy + fm.height() // 3, text)

        p.end()
