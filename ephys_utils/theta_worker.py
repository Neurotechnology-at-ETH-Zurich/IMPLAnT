# This Python file uses the following encoding: utf-8
"""Runs ephys/init_ephys.py's _run_theta_detection compute step
(ephys_utils/theta_detection.detect_theta) in its own process. Invoked by
that file's work() closure via gui_utils/subprocess_worker.py's
run_json_subprocess -- mirrors samri/samri_worker.py's --input/--output
JSON-payload convention, with progress streamed as plain stdout lines (same
convention as ephys_utils/ripple_spec_worker.py). Also works when
main_window.py's --theta-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys
import tempfile

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import numpy as np

from ephys_utils import theta_detection


def _do_theta_detection(payload):
    """Pure logic behind _run_theta_detection's old work() closure -- runs
    inside this subprocess, not the GUI process. theta_lfp/theta_phase are
    (n_lfp_samples, n_channels) arrays over the whole recording -- cross
    back via a temp .npz file path, not inline JSON, same as
    ephys_utils/clustering_worker.py's spike_data.npz convention.

    That .npz is written to its own dedicated tempfile.mkdtemp() directory
    (NOT run_json_subprocess's --input/--output directory, which is a `with
    TemporaryDirectory()` on the caller's side and gets deleted the instant
    run_json_subprocess returns -- before the caller would ever get a
    chance to read this path back out of the result). The caller is
    responsible for reading arrays_path back and then removing its parent
    directory itself."""
    def progress(msg):
        print(msg, flush=True)

    result = theta_detection.detect_theta(
        payload['lfp_path'],
        payload['n_channels'],
        payload['lfp_sample_rate'],
        channels=payload['channels'],
        sel_channel_idx=payload['sel_channel_idx'],
        raw_sample_rate=payload['raw_sample_rate'],
        f_theta=tuple(payload['f_theta']),
        f_delta=tuple(payload['f_delta']),
        th2d_ratio_threshold=payload['th2d_ratio_threshold'],
        amplitude_threshold=payload['amplitude_threshold'],
        phase_threshold=payload['phase_threshold'],
        duration_threshold=payload['duration_threshold'],
        consensus=payload['consensus'],
        progress=progress,
    )

    out_dir = tempfile.mkdtemp()
    arrays_path = os.path.join(out_dir, 'theta_arrays.npz')
    np.savez(
        arrays_path,
        segments_s=result['segments_s'],
        segments_samples=result['segments_samples'],
        theta_lfp=result['theta_lfp'],
        theta_phase=result['theta_phase'],
    )

    return {
        'arrays_path': arrays_path,
        'work_fs': result['work_fs'],
        'decimation': result['decimation'],
        'channels': result['channels'],
        'sel_channel_idx': result['sel_channel_idx'],
        'n_raw_samples': result['n_raw_samples'],
        'params': result['params'],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run theta detection out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_theta_detection(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
