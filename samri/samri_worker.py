# This Python file uses the following encoding: utf-8
"""Runs one SAMRI pipeline stage (bruker2bids fetch, registration, or bias
correction) in its own process. Invoked by samri_main.py's
_run_worker_subprocess -- see that function's docstring for why. Mirrors
rippl-AI/run_rippl.py's main(argv=None) convention, so this same script also
works when main_window.py's --samri-worker sentinel re-invokes a frozen
build (sys.executable there is the frozen app itself, not a bare python you
could point at this file directly)."""
import argparse
import importlib
import importlib.util
import json
import os
import sys

# Python auto-prepends this script's own directory (repo_root/samri) to
# sys.path before any of this file's code runs. Left in place, that breaks
# `from samri.samri_main import ...` below: repo_root/samri also contains
# samri/samri/__init__.py (the vendored SAMRI library, a real package), and
# PEP 420 namespace-package resolution stops at the first regular-package
# hit anywhere in the scan -- so with repo_root/samri on sys.path in its own
# right, `import samri` resolves to repo_root/samri/samri (the inner
# library) instead of treating repo_root as the search root for this outer
# wrapper package, and samri_main.py (a sibling of this file) is never
# found. Remove that auto-added entry and rely solely on repo_root (parent
# of this file's own directory) so `samri` resolves the same way it already
# does for every other caller in this codebase (none of which run a script
# from inside samri/ itself). Harmless in the frozen case, where
# main_window.py's --samri-worker sentinel already put _MEIPASS on
# sys.path before importing this module as `samri.samri_worker` (so its
# own directory was never auto-prepended in the first place).
_here = os.path.dirname(os.path.abspath(__file__))
while _here in sys.path:
    sys.path.remove(_here)
sys.path.insert(0, os.path.dirname(_here))


class _AliasLoader:
    """Loader for _InnerSamriAliasFinder below -- create_module() hands back
    an already-imported module object as-is, so exec_module() has nothing
    left to do."""
    def __init__(self, real_module):
        self._real_module = real_module

    def create_module(self, spec):
        return self._real_module

    def exec_module(self, module):
        pass


class _InnerSamriAliasFinder:
    """The vendored SAMRI library (samri/samri/) self-references its own
    submodules as bare 'samri.X' everywhere internally -- e.g.
    samri/samri/pipelines/extra_functions.py's get_bids_scan does
    `from samri.pipelines.utils import bids_naming` -- because it was
    written to be pip-installed as a standalone top-level 'samri' package.
    This app instead nests it one level deeper at samri/samri/, and this
    app's own code (samri_main.py, main_window.py) imports it as
    'samri.samri.X' -- because samri_main.py itself needs to be importable
    as 'samri.samri_main', which requires repo_root (not repo_root/samri) on
    sys.path (see the comment above this class).

    Both conventions can't be satisfied by sys.path alone: 'samri' can only
    mean one directory at a time via normal path-based resolution (confirmed
    by hand -- pip show samri / import samri; samri.__path__ -- while
    debugging a `ModuleNotFoundError: No module named 'samri.pipelines'`
    crash from inside a nipype MultiProc-forked worker running
    get_bids_scan). This finder bridges the two conventions instead of
    forcing a much larger rewrite of every existing samri.samri.* import in
    this app: any import of 'samri.<something>' that isn't itself
    'samri.samri' or a deeper 'samri.samri.*' name is transparently
    redirected to 'samri.samri.<something>', so the vendored library's own
    bare self-references (used pervasively -- pipelines, report, fetch,
    plotting, analysis, optimization, utilities, manipulations,
    typesetting, ...) resolve correctly wherever they run.

    Installed once, at import time, into sys.meta_path -- which, like
    sys.path and sys.modules, is part of the interpreter state a forked
    child process inherits, so nipype MultiProc's worker processes (forked
    from this one) see it too. Linux-only relevance: MultiProc's default
    'fork' start method is what makes this inheritance work; a 'spawn'-based
    setup (Windows' multiprocessing default) would need this reinstalled in
    each child instead, which isn't verified here."""

    def find_spec(self, fullname, path, target=None):
        if fullname == 'samri' or fullname.startswith('samri.samri'):
            return None
        if not fullname.startswith('samri.'):
            return None
        real_name = 'samri.samri.' + fullname[len('samri.'):]
        try:
            real_module = importlib.import_module(real_name)
        except ImportError:
            return None
        return importlib.util.spec_from_loader(fullname, _AliasLoader(real_module))


sys.meta_path.insert(0, _InnerSamriAliasFinder())


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run one SAMRI pipeline stage out-of-process')
    parser.add_argument('--op', required=True, choices=['init', 'register', 'biascorrect'])
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    # argv=None -> argparse reads sys.argv[1:] itself, same as the plain CLI
    # always has; explicit argv lets main_window.py's --samri-worker sentinel
    # pass its own remaining args through when re-invoking the frozen app as
    # this worker (see samri_main.py's _run_worker_subprocess).
    args = parser.parse_args(argv)

    from samri.samri_main import (
        _do_bruker2bids, _do_registration, _do_biascorrection, _setup_ants_env,
    )

    _setup_ants_env()

    with open(args.input) as f:
        payload = json.load(f)

    if args.op == 'init':
        result = _do_bruker2bids(payload)
    elif args.op == 'register':
        filepath = _do_registration(payload['_bids_base'], payload['_animal_id'], payload)
        result = {'filepath': filepath}
    else:
        filepath = _do_biascorrection(payload['_bids_base'], payload['_animal_id'], payload)
        result = {'filepath': filepath}

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
