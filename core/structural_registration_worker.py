# This Python file uses the following encoding: utf-8
"""Runs gui_utils/buttons_gui_structural.py's _start_registration compute
step (rigid registration via core.registration.Registration + a linear ants
apply_transforms/image_write warp) in its own process. Invoked by that
file's _start_registration via gui_utils/subprocess_worker.py's
run_json_subprocess -- mirrors samri/samri_worker.py's --input/--output
JSON-payload convention. Also works when main_window.py's
--structural-registration-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys
import tempfile

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import ants
import SimpleITK as sitk

from core.registration import Registration


class _ShimVolume:
    def __init__(self, file_path):
        self.file_path = file_path


class _ShimLoadMRI:
    """Minimal stand-in for a LoadMRI instance -- just enough for
    core.registration.Registration to run outside the GUI (same technique
    as samri/samri_main.py's _ShimLoadMRI)."""
    def __init__(self, session_path, fixed_path, moving_path_entry, coarsest_index,
                 finest_index, metric_index):
        self.session_path = session_path
        self.volumes = {0: _ShimVolume(fixed_path)}
        self.movingimg_filename = [moving_path_entry]
        self.coarsest_index = coarsest_index
        self.finest_index = finest_index
        self.metric_index = metric_index


def _do_structural_registration(payload):
    """Pure logic behind _start_registration's old work() closure -- runs
    inside this subprocess, not the GUI process. Unlike
    trajectory_planning/registration_worker.py's register_to_main_img, this
    always reruns the rigid registration (Registration.__init__ always
    rewrites the transform file -- this mirrors the original code, which had
    no exists-check guard around it, since the "Register" button is meant to
    redo the fit whenever the coarsest/finest/metric settings change) and
    always rewrites the aligned output. Returns {'aligned_path': ...} (None
    if the transform file the registration should have just written isn't
    there -- mirrors the original's silent-return-without-result path)."""
    session_path = payload['session_path']
    fixed_path = payload['fixed_path']
    moving_path_entry = payload['moving_path_entry']

    shim = _ShimLoadMRI(session_path, fixed_path, moving_path_entry,
                         payload['coarsest_index'], payload['finest_index'],
                         payload.get('metric_index', 0))
    reg = Registration(shim, None, 0)

    transform_filename = f"transformation-ind_{reg.moving_ind}-to-ind_{reg.fixed_ind}.txt"
    transform_path = os.path.join(session_path, "anat", transform_filename)
    if not os.path.exists(transform_path):
        return {'aligned_path': None}

    fixed_ants = ants.image_read(fixed_path)

    # reg.moving_image is already DICOMOrient'd to RAS and extracted to 3D
    moving_for_apply = reg.moving_image
    if moving_for_apply.GetNumberOfComponentsPerPixel() > 1:
        moving_for_apply = sitk.VectorIndexSelectionCast(moving_for_apply, 0)
    with tempfile.TemporaryDirectory() as _tmpdir:
        moving_tmp = os.path.join(_tmpdir, 'moving.nii.gz')
        sitk.WriteImage(sitk.Cast(moving_for_apply, sitk.sitkFloat32), moving_tmp)
        moving_ants = ants.image_read(moving_tmp)
        # linear, not lanczosWindowedSinc: sinc kernels have negative
        # side-lobes and ring at sharp edges (skull/background etc.),
        # producing large negative overshoot that doesn't exist in the
        # source data; linear is a convex combination of neighbours so
        # it can't overshoot the input's value range
        img_aligned = ants.apply_transforms(
            fixed=fixed_ants,
            moving=moving_ants,
            transformlist=transform_path,
            interpolator="linear",
        )

    base = reg.moving_filepath
    suffix = f"-aligned_to_ind_{reg.fixed_ind}.nii.gz"
    aligned_path = (base[:-7] if base.endswith('.nii.gz') else base[:-4]) + suffix
    ants.image_write(img_aligned, aligned_path)

    return {'aligned_path': aligned_path}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run _start_registration\'s compute step out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_structural_registration(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
