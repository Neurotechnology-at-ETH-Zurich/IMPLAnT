# This Python file uses the following encoding: utf-8
"""Runs trajectory_planning/rendering_mri.py's reload_atlas_view DWI-load
step (_load_dwi) in its own process. Invoked via gui_utils/
subprocess_worker.py's run_json_subprocess -- mirrors samri/samri_worker.py's
--input/--output JSON-payload convention. Also works when main_window.py's
--dwi-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys
import tempfile

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import nibabel as nib
import numpy as np


def _do_load_dwi(payload):
    """Pure logic behind the old _load_dwi closure -- runs inside this
    subprocess, not the GUI process. The extracted 3D volume can be a
    genuinely large array, so it crosses back via a temp .npy file (its own
    tempfile.mkdtemp(), NOT run_json_subprocess's --input/--output
    directory, which is deleted the instant that call returns -- see
    ephys_utils/theta_worker.py's identical note), not inline JSON."""
    nii_dwi = nib.load(payload['dwi_path'])
    dwi = np.asanyarray(nii_dwi.dataobj)[:, :, :, 0]

    out_dir = tempfile.mkdtemp()
    dwi_array_path = os.path.join(out_dir, 'dwi.npy')
    np.save(dwi_array_path, dwi)

    return {'dwi_array_path': dwi_array_path}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the DWI volume load out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_load_dwi(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
