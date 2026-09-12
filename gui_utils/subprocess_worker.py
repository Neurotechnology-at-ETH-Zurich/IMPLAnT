# This Python file uses the following encoding: utf-8
"""Generic out-of-process JSON-payload worker runner, shared by the
subprocess conversions added after samri/samri_main.py's
_run_worker_subprocess (which stays as its own copy -- it also has to
handle SAMRI's op dispatch and cancellation, which don't generalize here).
Every caller still needs its own worker .py file (with a `main(argv=None)`
that reads --input, writes --output) and its own --*-worker sentinel branch
near the top of main_window.py, exactly like --samri-worker/
--trajectory-worker; this just factors out the boilerplate of building the
subprocess command, passing the JSON payload, and reading the JSON result."""
import json
import os
import subprocess
import sys
import tempfile

from paths_config import _base_dir


def run_json_subprocess(rel_script_path, sentinel, payload, on_progress=None):
    """rel_script_path: the worker script's path relative to the repo root
    (e.g. 'core/registration_worker.py') -- used in dev/source runs.
    sentinel: the --*-worker flag a frozen build re-invokes itself with (see
    main_window.py's sentinel branches) -- used instead of rel_script_path
    when frozen, since a frozen build has no separate python3/script file to
    point at.
    on_progress, if given, is called with each stripped stdout line as it
    streams in (see samri_main.py's _run_worker_subprocess for the same
    convention) -- use this for a worker that can run long enough to need
    live overlay text; omit it for a quick one to just capture output.

    Raises RuntimeError with the last ~4000 characters of combined stdout/
    stderr on a non-zero exit, same tail-slicing convention as
    samri_main.py's _run_worker_subprocess."""
    frozen = getattr(sys, 'frozen', False)
    worker_dir = getattr(sys, '_MEIPASS', _base_dir)
    script = os.path.join(worker_dir, rel_script_path)
    cmd = [sys.executable, sentinel] if frozen else [sys.executable, script]

    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, 'input.json')
        output_path = os.path.join(tmp, 'output.json')
        with open(input_path, 'w') as f:
            json.dump(payload, f)

        cmd = cmd + ['--input', input_path, '--output', output_path]

        if on_progress is None:
            proc = subprocess.run(cmd, capture_output=True, text=True)
            stdout, stderr = proc.stdout, proc.stderr
            returncode = proc.returncode
        else:
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      text=True, bufsize=1)
            tail_lines = []
            for line in popen.stdout:
                print(line, end='', flush=True)
                tail_lines.append(line)
                if line.strip():
                    on_progress(line.strip())
            popen.wait()
            stdout, stderr = ''.join(tail_lines), ''
            returncode = popen.returncode

        if returncode != 0:
            outcome = 'was killed' if returncode < 0 else f'failed (exit code {returncode})'
            tail = (stdout + stderr)[-4000:]
            raise RuntimeError(f"Subprocess worker {outcome}.\n{tail}")

        with open(output_path) as f:
            return json.load(f)
