# This Python file uses the following encoding: utf-8
"""
Shared pytest fixtures for the test suite -- see CONTRIBUTING.md's "Testing"
section for what this suite covers (and, just as importantly, what it
deliberately doesn't).
"""
import os
import sys

# Must be set before any PySide6/VTK import -- this suite runs headlessly
# (no display in CI or most dev shells), and Qt needs to know that up front.
# main_window.py's own __main__ block does the same thing for the same
# reason (see its "xcb is Linux-only" comment) -- offscreen is the one
# platform plugin that works with no display at all, on any OS.
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope='session')
def qapp():
    """One QApplication for the whole test session -- Qt only allows a
    single instance per process, and importing main_window pulls in Qt
    widgets regardless of which test runs first."""
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def mw(qapp):
    """
    A fresh MainWindow for each test.

    Never call .show() on it, and never make it load a real file: this
    project's own development hit a confirmed crash (X Error: BadWindow)
    the one time .show() was tried under the offscreen platform, and real
    VTK render-window/interactor creation needs an actual display -- it
    segfaults offscreen too. That's why this suite is construction/
    control-flow level only (does the right attribute exist, does the right
    method get called, does the tab layout match) rather than anything that
    actually renders. See CONTRIBUTING.md's "Testing" section for what still
    needs a manual check against the real app.
    """
    import main_window as main_window_module
    return main_window_module.MainWindow()
