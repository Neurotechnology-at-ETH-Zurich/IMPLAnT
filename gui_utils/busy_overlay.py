# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QProgressDialog, QApplication
from PySide6.QtCore import Qt, QTimer


class BusyOverlay(QProgressDialog):
    def __init__(self, parent, message="Processing, please wait…"):
        super().__init__(message, None, 0, 0, parent)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Please wait")
        self.setMinimumDuration(0)
        self.setMinimumWidth(350)
        self.setAutoClose(False)
        self.setAutoReset(False)

    def run(self, fn, *args, **kwargs):
        self.show()
        self.setValue(0)
        self.repaint()
        QApplication.processEvents()
        QTimer.singleShot(50, lambda: self._execute(fn, args, kwargs))

    def _execute(self, fn, args, kwargs):
        fn(*args, **kwargs)
        self.close()
