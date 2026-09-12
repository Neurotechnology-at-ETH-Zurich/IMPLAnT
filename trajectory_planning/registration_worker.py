# This Python file uses the following encoding: utf-8
"""Runs trajectory_planning/registration.py's register_to_main_img compute
step (rigid registration via core.registration.Registration + an ants
apply_transforms/image_write full-volume warp) in its own process. Invoked
by that file's _run_trajectory_registration_subprocess -- mirrors samri/
samri_worker.py's --input/--output JSON-payload convention. Also works when
main_window.py's --trajectory-registration-worker sentinel re-invokes a
frozen build."""
import argparse
import json
import os
import re
import sys

# Python auto-prepends this script's own directory (repo_root/
# trajectory_planning) to sys.path, not repo_root itself -- needed for
# `from core... import ...` below when this file is invoked directly
# (dev/source runs; a frozen build already has _MEIPASS, i.e. repo_root, on
# sys.path via main_window.py's sentinel).
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import ants

from core.registration import Registration


class _ShimVolume:
    def __init__(self, file_path):
        self.file_path = file_path


class _ShimLoadMRI:
    """Minimal stand-in for a LoadMRI instance -- just enough for
    core.registration.Registration to run outside the GUI (same technique as
    samri/samri_main.py's _ShimLoadMRI)."""
    def __init__(self, session_path, fixed_path, moving_path, coarsest_index,
                 finest_index, metric_index):
        self.session_path = session_path
        self.volumes = {0: _ShimVolume(fixed_path)}
        self.movingimg_filename = [moving_path]
        self.coarsest_index = coarsest_index
        self.finest_index = finest_index
        self.metric_index = metric_index


def _do_register_to_main_img(payload):
    """Pure logic behind register_to_main_img's old
    _register_to_main_img_compute -- runs inside this subprocess, not the
    GUI process. Returns {'new_name': ...}; a no-op (the file already
    exists) after the first call for a given fixed/moving pair."""
    fixed_path = payload['fixed_path']
    moving_path = payload['moving_path']
    session_path = payload['session_path']
    coarsest_index = payload['coarsest_index']
    finest_index = payload['finest_index']
    metric_index = payload.get('metric_index', 0)

    m = re.search(r"ind_(\d+)", fixed_path)
    fixed_ind = int(m.group(1))
    moving_ind = int(moving_path.split("ind_")[1].split(".")[0])
    transform_filename = f"transformation-ind_{moving_ind}-to-ind_{fixed_ind}.txt"
    transform_file_path = os.path.join(session_path, "anat", transform_filename)
    new_name = moving_path[:-7] + f"-aligned_to_ind_{fixed_ind}.nii.gz"

    if not os.path.exists(new_name):
        if not os.path.exists(transform_file_path):
            shim = _ShimLoadMRI(session_path, fixed_path, moving_path,
                                 coarsest_index, finest_index, metric_index)
            Registration(shim, None, 0)

        fixed = ants.image_read(fixed_path)
        moving = ants.image_read(moving_path)
        img_aligned = ants.apply_transforms(
            fixed=fixed,
            moving=moving,
            transformlist=transform_file_path,
            interpolator="lanczosWindowedSinc",
        )
        ants.image_write(img_aligned, new_name)

    return {'new_name': new_name}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run register_to_main_img\'s compute step out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_register_to_main_img(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
