# This Python file uses the following encoding: utf-8
"""Runs the trajectory-planning resample step (main_window.py's old
_resample_for_trajectory_planning) in its own process. Invoked by
main_window.py's _run_trajectory_worker_subprocess -- mirrors samri/
samri_worker.py's --op/--input/--output JSON-payload convention (see that
file's docstring for the general rationale: a stuck/heavy resample no longer
has to share the GUI process's memory footprint or block a `kill` from
taking effect immediately). Also works when main_window.py's
--trajectory-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys

# Python auto-prepends this script's own directory (repo_root/
# trajectory_planning) to sys.path, not repo_root itself -- needed for
# `from file_handling... import ...` below when this file is invoked
# directly (dev/source runs; a frozen build already has _MEIPASS, i.e.
# repo_root, on sys.path via main_window.py's --trajectory-worker sentinel).
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import nibabel as nib

from file_handling.mri_volume import MRIVolume
from file_handling.resample_data import ResampleData


class _ShimLoadMRI:
    """Minimal stand-in for a LoadMRI instance -- just enough for
    ResampleData.resampling25um to run outside the GUI (same shim as samri/
    samri_main.py's _ShimLoadMRI; duplicated here so this worker stays
    self-contained and doesn't need to import the SAMRI package)."""
    def __init__(self, volumes, session_path):
        self.volumes = volumes
        self.session_path = session_path


def _do_resample(payload):
    """Pure logic behind _resample_for_trajectory_planning -- runs inside
    this subprocess, not the GUI process. Returns {'resampled_path': ...};
    a no-op (the file already exists) after the first call for a given
    path/spacing."""
    file_path = payload['file_path']
    spacing = payload['spacing']

    if abs(spacing - 0.025) < 1e-9:
        # reuse the exact file/function samri_main.py's start_registration
        # uses to build the atlas<->MRI correspondence (ResampleData.
        # resampling25um, fixed "_resampled.nii.gz" name) instead of
        # resampling50um_trajectoryPlanning's own separate implementation --
        # two different resample functions at the same nominal spacing
        # aren't guaranteed pixel/geometry-identical, and mri_label_overlay.
        # py's reconciliation needs them to be exactly the same file.
        resampled_path = f"{file_path[:-7]}_resampled.nii.gz"
        if not os.path.exists(resampled_path):
            raw_DICOMOrient = "".join(nib.aff2axcodes(nib.load(file_path).affine))
            _volume = MRIVolume(file_path=file_path, slices={}, DICOMOrient=raw_DICOMOrient,
                                 raw_DICOMOrient=raw_DICOMOrient, view_names=[])
            _shim_loadmri = _ShimLoadMRI(volumes={0: _volume}, session_path=os.path.dirname(file_path))
            ResampleData(_shim_loadmri).resampling25um(0)
    else:
        resampled_path = f"{file_path[:-7]}_resampled{spacing*1000:.10g}um.nii.gz"
        if not os.path.exists(resampled_path):
            ResampleData.resampling50um_trajectoryPlanning(file_path, new_spacing_mm=spacing)

    return {'resampled_path': resampled_path}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the trajectory-planning resample step out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    # argv=None -> argparse reads sys.argv[1:] itself, same as the plain CLI
    # always has; explicit argv lets main_window.py's --trajectory-worker
    # sentinel pass its own remaining args through when re-invoking the
    # frozen app as this worker (see main_window.py's
    # _run_trajectory_worker_subprocess).
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_resample(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
