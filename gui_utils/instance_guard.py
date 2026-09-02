# This Python file uses the following encoding: utf-8
"""Cross-session cleanup for leaked main_window.py process trees.

Every launch used to be able to leave its whole process tree (the GUI
process plus every nipype/ProcessPoolExecutor worker it had spawned)
running forever if the app crashed hard (a Qt qFatal()/abort(), a segfault)
or simply hung -- neither of those runs any Python-level cleanup (atexit,
finally, context managers), so nothing ever reaped them. Over a few days
those piled up into the dozens, each holding an X11 connection and a
VTK/OpenGL context, which is what eventually made brand new launches hang
inside their own first render() call with nothing left to acquire.

Design: each running instance periodically (every HEARTBEAT_MS) writes its
own PID, start time, and current child-PID list to a small JSON file. A
frozen main thread stops updating that file just as surely as a dead
process does -- so staleness catches BOTH cases, not just "is the PID
still running" (which would have missed the render()-hung instances we
found: they were alive the whole time). Every launch reaps any other
instance's file that is missing, dead, or stale before doing anything
else, killing that whole last-known process tree.

This never touches a live, responsive instance (heartbeat keeps ticking
regardless of how long the actual work underneath takes -- SAMRI's
registration runs on a background thread, not the Qt main thread, so a
run that's legitimately still going after 20 hours is never at risk), and
it never touches the current process itself.
"""
import json
import os
import tempfile
import time

import psutil
from PySide6.QtCore import QTimer

HEARTBEAT_MS = 15_000
STALE_SECONDS = 90
_MARKER = 'main_window.py'


def _instances_dir():
    d = os.path.join(tempfile.gettempdir(), 'mrid_gui_instances')
    os.makedirs(d, exist_ok=True)
    return d


def _atomic_write_json(path, record):
    tmp_path = f"{path}.tmp{os.getpid()}"
    with open(tmp_path, 'w') as f:
        json.dump(record, f)
    os.replace(tmp_path, path)


def _is_same_process(pid, expected_create_time):
    try:
        return abs(psutil.Process(pid).create_time() - expected_create_time) < 1.0
    except psutil.Error:
        return False


def _is_mrid_gui_process(pid):
    try:
        return any(_MARKER in part for part in psutil.Process(pid).cmdline())
    except psutil.Error:
        return False


def _kill(pid):
    if pid == os.getpid() or not _is_mrid_gui_process(pid):
        return
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except psutil.TimeoutExpired:
            proc.kill()
    except psutil.Error:
        pass


def reap_stale_instances():
    """Kill any other instance's process tree that is dead or hasn't
    heartbeated in STALE_SECONDS, using its last-recorded child-PID list
    (the root may already be gone -- that snapshot is the only remaining
    record of what it left running). Call once, before registering the
    current instance, so the current PID never gets reaped by mistake."""
    directory = _instances_dir()
    for name in os.listdir(directory):
        if not name.endswith('.json'):
            continue
        path = os.path.join(directory, name)
        try:
            with open(path) as f:
                record = json.load(f)
        except (OSError, ValueError):
            try:
                os.remove(path)
            except OSError:
                pass
            continue

        pid = record.get('pid')
        if pid == os.getpid():
            continue

        root_alive = pid is not None and _is_same_process(pid, record.get('create_time'))
        stale = time.time() - record.get('heartbeat', 0) > STALE_SECONDS
        if root_alive and not stale:
            continue

        for child_pid in record.get('children', []):
            _kill(child_pid)
        if root_alive:
            _kill(pid)

        try:
            os.remove(path)
        except OSError:
            pass


def register_instance():
    """Create this instance's own heartbeat file and return its path."""
    path = os.path.join(_instances_dir(), f"{os.getpid()}.json")
    proc = psutil.Process(os.getpid())
    _atomic_write_json(path, {
        'pid': os.getpid(),
        'create_time': proc.create_time(),
        'heartbeat': time.time(),
        'children': [],
    })
    return path


def start_heartbeat(app, path, interval_ms=HEARTBEAT_MS):
    """Keep `path` updated with a fresh timestamp and current child-PID
    list for as long as the Qt event loop keeps running turns -- a frozen
    main thread (e.g. stuck inside a hung render()) stops this exactly
    like a dead process would, which is the whole point."""
    def _beat():
        try:
            proc = psutil.Process(os.getpid())
            _atomic_write_json(path, {
                'pid': os.getpid(),
                'create_time': proc.create_time(),
                'heartbeat': time.time(),
                'children': [c.pid for c in proc.children(recursive=True)],
            })
        except (psutil.Error, OSError):
            pass

    timer = QTimer(app)
    timer.timeout.connect(_beat)
    timer.start(interval_ms)
    _beat()
    return timer


def unregister_instance(path):
    try:
        os.remove(path)
    except OSError:
        pass
