# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QThread, Signal
import traceback

# Every BusyWorker ever started, pruned to just the still-running ones each
# time a new one starts. run_callable has no cancellation point, so there is
# nothing to wait on gracefully -- this registry only exists so the app can
# tell, at close time, whether one is still in flight (see any_running()).
_all_workers = []


class BusyWorker(QThread):
    """Runs an arbitrary no-arg callable off the GUI thread, pairing with
    BusyOverlay: show the overlay, start this, close the overlay from a
    done/failed slot."""
    done = Signal()
    failed = Signal(str)

    def __init__(self, run_callable, parent=None):
        super().__init__(parent)
        self._run_callable = run_callable

    def start(self, *args, **kwargs):
        _all_workers[:] = [w for w in _all_workers if w.isRunning()]
        _all_workers.append(self)
        super().start(*args, **kwargs)

    def run(self):
        try:
            self._run_callable()
            self.done.emit()
        except Exception:
            self.failed.emit(traceback.format_exc())


def any_running():
    """True if some BusyWorker's run_callable is still executing -- used to
    warn before a close/quit that would otherwise leave the process running
    in the background until that callable happens to return on its own."""
    return any(w.isRunning() for w in _all_workers)


class _OffThreadRunner(QThread):
    """Backs run_off_thread below -- carries the actual return value/
    exception object (not just a formatted traceback string, unlike
    BusyWorker) since run_off_thread re-raises with the original type."""
    finished_ok = Signal(object)
    finished_err = Signal(object)

    def __init__(self, run_callable, parent=None):
        super().__init__(parent)
        self._run_callable = run_callable

    def run(self):
        try:
            value = self._run_callable()
        except Exception as e:
            self.finished_err.emit(e)
        else:
            self.finished_ok.emit(value)


def run_off_thread(run_callable):
    """Runs run_callable() on a background thread while pumping the calling
    (GUI) thread's Qt event loop -- so a BusyOverlay already up keeps
    repainting/animating instead of looking frozen -- until it finishes,
    then returns its result, or re-raises whatever it raised, here, in the
    calling thread with its original type intact.

    For code that must return a fully-computed result synchronously (e.g. a
    constructor whose very next line depends on it, so a work()/on_done()
    BusyWorker split would mean restructuring every caller) but whose
    computation is heavy enough to want off the GIL-holding call stack.
    Purely pure computation must be behind this call -- exactly like
    BusyWorker, run_callable must not touch any Qt/VTK object, since it
    still executes on the worker thread.

    Only call this from the GUI thread, with a BusyOverlay (or other
    input-blocking widget) already up over the relevant area: pumping the
    event loop here can let the user re-enter code that isn't ready for
    it, the same reentrancy risk BusyOverlay.run()/QDialog.exec()'s own
    nested loops already carry elsewhere in this codebase."""
    from PySide6.QtCore import QEventLoop
    outcome = {}

    runner = _OffThreadRunner(run_callable)
    loop = QEventLoop()
    runner.finished_ok.connect(lambda v: outcome.update(value=v))
    runner.finished_err.connect(lambda e: outcome.update(exc=e))
    runner.finished_ok.connect(loop.quit)
    runner.finished_err.connect(loop.quit)
    runner.start()
    loop.exec()
    runner.wait()
    if 'exc' in outcome:
        raise outcome['exc']
    return outcome.get('value')


def show_worker_error(parent, title, tb):
    """Show a BusyWorker's `failed` traceback string, connected to that
    signal. `parent` is the widget to center the dialog on (usually self.MW)."""
    from PySide6.QtWidgets import QMessageBox, QLayout
    from PySide6.QtCore import Qt
    import logging
    logging.error(tb)
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(f"{title}.")
    msg.setDetailedText(tb)
    msg.addButton("OK", QMessageBox.ActionRole)
    msg.setWindowFlags(msg.windowFlags() & ~Qt.MSWindowsFixedSizeDialogHint)
    msg.setSizeGripEnabled(True)
    msg.layout().setSizeConstraint(QLayout.SetNoConstraint)
    msg.exec()
