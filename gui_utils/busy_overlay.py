# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QDockWidget
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QPainter, QColor


class BusyOverlay(QWidget):
    def __init__(self, parent, message="Processing, please wait…", cover_floating_docks=True):
        super().__init__(parent)
        self.setGeometry(parent.rect())
        self._message = message
        self._companions = []

        self.label = QLabel(message, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # follow the parent's size (e.g. a dock going fullscreen while we are shown)
        parent.installEventFilter(self)

        # a docked QDockWidget is already covered by the main window's overlay, a floating
        # one is its own top level window and needs an overlay of its own
        if cover_floating_docks:
            for dock in parent.window().findChildren(QDockWidget):
                if dock.isFloating() and not dock.isHidden():
                    self.also_cover(dock)

        self.hide()

    def set_message(self, text):
        """Update the overlay's text in place, e.g. to show live progress
        ("ripple 12 / 450") while it's up -- proof of life for a run long
        enough that a static message reads as hung."""
        self._message = text
        self.label.setText(text)
        for companion in self._companions:
            companion.set_message(text)

    def also_cover(self, *widgets):
        """
        Shade additional widgets with the same overlay, e.g. the ephys dock while it is
        floating. The companions follow show/hide/close of this overlay.
        """
        for widget in widgets:
            if widget is None or widget is self.parentWidget():
                continue
            self._companions.append(BusyOverlay(widget, self._message, cover_floating_docks=False))
        return self

    def eventFilter(self, obj, event):
        if obj is self.parentWidget() and event.type() == QEvent.Resize:
            self.setGeometry(obj.rect())
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 160))

    def showEvent(self, event):
        super().showEvent(event)
        for companion in self._companions:
            companion.setGeometry(companion.parentWidget().rect())
            companion.raise_()
            companion.show()
            # the floating dock is a separate top level window: force it to paint now,
            # otherwise it stays unshaded once the heavy work blocks the event loop
            companion.repaint()

    def hideEvent(self, event):
        super().hideEvent(event)
        for companion in self._companions:
            companion.hide()

    def closeEvent(self, event):
        for companion in self._companions:
            companion.close()
            companion.deleteLater()
        self._companions.clear()
        super().closeEvent(event)

    def run(self, fn, *args, **kwargs):
        self.setGeometry(self.parentWidget().rect())
        self.raise_()
        self.show()
        QApplication.processEvents()
        QTimer.singleShot(50, lambda: self._execute(fn, args, kwargs))

    def _execute(self, fn, args, kwargs):
        try:
            fn(*args, **kwargs)
        finally:
            self.close()
