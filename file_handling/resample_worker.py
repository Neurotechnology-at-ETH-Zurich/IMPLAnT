# This Python file uses the following encoding: utf-8
"""Runs gui_utils/buttons_gui_structural.py's resample100um/resample25um
compute steps (ResampleData.resampling100um/resampling25um) in their own
process. Invoked by that file's resample100um/resample25um via
gui_utils/subprocess_worker.py's run_json_subprocess -- mirrors samri/
samri_worker.py's --op/--input/--output JSON-payload convention. Also works
when main_window.py's --resample-worker sentinel re-invokes a frozen
build."""
import argparse
import json
import os
import sys

# Python auto-prepends this script's own directory (repo_root/file_handling)
# to sys.path, not repo_root itself -- needed for `from file_handling... import
# ...` below when this file is invoked directly (dev/source runs; a frozen
# build already has _MEIPASS, i.e. repo_root, on sys.path via
# main_window.py's --resample-worker sentinel).
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from file_handling.resample_data import ResampleData


class _ShimVolume:
    def __init__(self, file_path, raw_DICOMOrient):
        self.file_path = file_path
        self.raw_DICOMOrient = raw_DICOMOrient


class _ShimLoadMRI:
    """Minimal stand-in for a LoadMRI instance -- just enough for
    ResampleData.resampling100um/resampling25um to run outside the GUI (same
    technique as samri/samri_main.py's _ShimLoadMRI). Both methods only ever
    read volumes[the index passed in]/.file_path and volumes[0]/.
    raw_DICOMOrient, so normalizing everything to index 0 here (see
    _do_resample below, which always calls with index=0) covers both."""
    def __init__(self, file_path, session_path, raw_DICOMOrient):
        self.volumes = {0: _ShimVolume(file_path, raw_DICOMOrient)}
        self.session_path = session_path


def _do_resample(payload):
    """Pure logic behind resample100um/resample25um's old work() closures --
    runs inside this subprocess, not the GUI process. Returns
    {'default_name': ...} (the actual saved path, despite the name --
    matches ResampleData.resampling100um/25um's own return value)."""
    op = payload['op']
    shim = _ShimLoadMRI(payload['file_path'], payload['session_path'], payload['raw_DICOMOrient'])
    resampler = ResampleData(shim)
    if op == 'resample100':
        default_name = resampler.resampling100um(0)
    else:
        default_name = resampler.resampling25um(0)
    return {'default_name': default_name}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run a resample step out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_resample(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
