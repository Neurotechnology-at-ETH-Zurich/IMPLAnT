import logging
import sys
from PySide6.QtCore import QObject, Signal, Qt,QThread
from PySide6.QtGui import QTextCursor
import re
# core/gui/samri_worker.py
import traceback

class SamriWorker(QThread):
    done = Signal()
    failed = Signal(str)

    def __init__(self, run_callable, parent=None):
        super().__init__(parent)
        self._run_callable = run_callable           # function that does the actual work

    def run(self):
        try:
            self._run_callable()
            self.done.emit()
        except Exception:
            self.failed.emit(traceback.format_exc())


class _Signals(QObject):
    message = Signal(str)


class LogAdapter:
    """Redirects stdout/stderr and logging output into an existing QPlainTextEdit.
    Thread-safe via a QueuedConnection — worker threads can emit safely."""
    def __init__(self, plain_text_edit):
        self._widget = plain_text_edit
        self._widget.setReadOnly(True)
        #self._widget.setMaximumBlockCount(max_lines)

        self._signals = _Signals()
        self._signals.message.connect(self._append, Qt.QueuedConnection)

        self._handler = None

    def install(self, capture_stdout=True, capture_stderr=True, level=logging.INFO):
        if capture_stdout:
            sys.stdout = _StreamRedirector(self._signals.message, sys.__stdout__)
        if capture_stderr:
            sys.stderr = _StreamRedirector(self._signals.message, sys.__stderr__)

        self._handler = _QtLogHandler(self._signals.message)
        self._handler.setLevel(level)
        self._handler.setFormatter(logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s: %(message)s", datefmt="%H:%M:%S"))
        root = logging.getLogger()
        root.addHandler(self._handler)
        root.setLevel(level)

    def uninstall(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if self._handler is not None:
            logging.getLogger().removeHandler(self._handler)
            self._handler = None

    def _append(self, text):
        cursor = self._widget.textCursor()
        cursor.movePosition(QTextCursor.End)

        # normalize Windows line endings
        text = text.replace('\r\n', '\n')
        # split keeping separators
        parts = re.split(r'([\r\n])', text)

        for part in parts:
            if part == '\n':
                cursor.insertBlock()                             # commit current line, start new one
            elif part == '\r':
                # move to start of current line and wipe its contents
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
            elif part:
                cursor.insertText(part)

        self._widget.setTextCursor(cursor)
        self._widget.ensureCursorVisible()


class _StreamRedirector:
    def __init__(self, signal, original):
        self._signal = signal
        self._original = original

    def write(self, text):
        if text:
            self._signal.emit(text)
            try:
                self._original.write(text)
            except Exception:
                pass

    def flush(self):
        try:
            self._original.flush()
        except Exception:
            pass

    def isatty(self):
        return False


class _QtLogHandler(logging.Handler):
    def __init__(self, signal):
        super().__init__()
        self._signal = signal

    def emit(self, record):
        try:
            self._signal.emit(self.format(record))
        except Exception:
            self.handleError(record)