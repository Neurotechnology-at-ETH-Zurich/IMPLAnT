# This Python file uses the following encoding: utf-8
"""Runs trajectory_planning_3d/window.py's _rebuild_background_mesh compute
step in its own process. Invoked by that file's work() closure via
gui_utils/subprocess_worker.py's run_json_subprocess -- mirrors samri/
samri_worker.py's --input/--output JSON-payload convention. Also works when
main_window.py's --background-mesh-worker sentinel re-invokes a frozen
build.

pyvista.PolyData objects can't cross a process boundary -- the mesh this
builds crosses back as plain points/faces/intensity arrays (a temp .npz,
same convention as ephys_utils/theta_worker.py's large-array outputs), and
the caller reconstructs a pv.PolyData(points, faces) from them."""
import argparse
import json
import os
import sys
import tempfile

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import numpy as np
import pyvista as pv

pv.global_theme.background = 'black'


def _do_build_background_mesh(payload):
    """Pure logic behind _rebuild_background_mesh's old work() closure --
    runs inside this subprocess, not the GUI process."""
    mri_label_vol = np.load(payload['mri_label_vol_path'])
    mri_arr = np.load(payload['mri_arr_path'])
    mri_spacing = np.array(payload['mri_spacing'])
    downsample = payload['downsample']

    data_zyx = mri_label_vol[::downsample, ::downsample, ::downsample]
    data_xyz = np.transpose(data_zyx, (2, 1, 0))
    vol = pv.ImageData()
    vol.dimensions = np.array(data_xyz.shape) + 1
    vol.spacing = tuple(s * downsample for s in mri_spacing)
    vol.origin = (0.0, 0.0, 0.0)
    vol.cell_data['NIFTI'] = data_xyz.flatten(order='F')

    background = vol.threshold(value=0.5)
    background = background.extract_surface(algorithm='dataset_surface')
    background = background.clean().triangulate()
    background = background.fill_holes(hole_size=1e10)
    background = background.clean().triangulate()
    background = background.decimate(0.75)
    smoothed = background.smooth_taubin(n_iter=50, pass_band=0.1)

    mri_shape = mri_arr.shape
    idx = smoothed.points / mri_spacing  # (N,3) float xyz
    rounded = np.round(idx).astype(int)
    in_bounds = (
        (rounded[:, 0] >= 0) & (rounded[:, 0] < mri_shape[2]) &
        (rounded[:, 1] >= 0) & (rounded[:, 1] < mri_shape[1]) &
        (rounded[:, 2] >= 0) & (rounded[:, 2] < mri_shape[0])
    )
    clipped = np.clip(rounded, 0, np.array(mri_shape[::-1]) - 1)
    intensity = np.where(
        in_bounds, mri_arr[clipped[:, 2], clipped[:, 1], clipped[:, 0]], 0
    ).astype(float)

    nonzero = intensity[intensity > 0]
    clim = [float(np.percentile(nonzero, 1)), float(np.percentile(nonzero, 99))] if nonzero.size else None

    out_dir = tempfile.mkdtemp()
    mesh_arrays_path = os.path.join(out_dir, 'mesh_arrays.npz')
    np.savez(mesh_arrays_path, points=smoothed.points, faces=smoothed.faces, intensity=intensity)

    return {'mesh_arrays_path': mesh_arrays_path, 'clim': clim}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run background-mesh building out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_build_background_mesh(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
