# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor


class BusyOverlay(QWidget):
    def __init__(self, parent, message="Processing, please wait…"):
        super().__init__(parent)
        self.setGeometry(parent.rect())

        label = QLabel(message, self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")

        layout = QVBoxLayout(self)
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 160))

    def run(self, fn, *args, **kwargs):
        self.setGeometry(self.parent().rect())
        self.raise_()
        self.show()
        QApplication.processEvents()
        QTimer.singleShot(50, lambda: self._execute(fn, args, kwargs))

    def _execute(self, fn, args, kwargs):
        try:
            fn(*args, **kwargs)
        finally:
            self.close()
