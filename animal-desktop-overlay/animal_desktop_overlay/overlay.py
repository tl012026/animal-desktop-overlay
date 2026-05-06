from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QGuiApplication, QKeyEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QWidget


@dataclass(frozen=True)
class OverlayOptions:
    scale: float = 1.0
    seed: int | None = None


class AnimalOverlay(QWidget):
    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self._label = QLabel(self)
        self._label.setPixmap(pixmap)
        self._label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowType.Tool, True)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._label.adjustSize()
        self.resize(self._label.size())

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event is not None and event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)


def _scaled(p: QPixmap, scale: float) -> QPixmap:
    if scale <= 0:
        raise ValueError("--scale must be > 0")
    if abs(scale - 1.0) < 1e-6:
        return p
    new_w = max(1, int(p.width() * scale))
    new_h = max(1, int(p.height() * scale))
    return p.scaled(QSize(new_w, new_h), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)


def _random_position(screen_rect: QRect, win_size: QSize, rng: random.Random) -> tuple[int, int]:
    max_x = max(0, screen_rect.width() - win_size.width())
    max_y = max(0, screen_rect.height() - win_size.height())
    x = screen_rect.x() + (rng.randint(0, max_x) if max_x > 0 else 0)
    y = screen_rect.y() + (rng.randint(0, max_y) if max_y > 0 else 0)
    return x, y


def show_overlay(image_path: str | Path, *, options: OverlayOptions) -> int:
    if options.seed is not None:
        rng = random.Random(options.seed)
    else:
        rng = random.Random()

    app = QApplication([])

    pix = QPixmap(str(Path(image_path)))
    if pix.isNull():
        raise RuntimeError(f"Failed to load image: {image_path}")
    pix = _scaled(pix, options.scale)

    w = AnimalOverlay(pix)
    w.show()

    screen = QGuiApplication.primaryScreen()
    if screen is not None:
        rect = screen.availableGeometry()
        x, y = _random_position(rect, w.size(), rng)
        w.move(x, y)

    return app.exec()

