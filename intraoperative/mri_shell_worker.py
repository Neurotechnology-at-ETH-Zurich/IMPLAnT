# This Python file uses the following encoding: utf-8
"""Runs intraoperative/mri_preview.py's _compute_shell (and the
_build_atlas_warped_shell/_build_otsu_shell helpers it calls) in its own
process. Invoked by that file's _render via gui_utils/subprocess_worker.py's
run_json_subprocess -- mirrors samri/samri_worker.py's --input/--output
JSON-payload convention. Also works when main_window.py's
--mri-shell-worker sentinel re-invokes a frozen build.

None of _compute_shell/_build_atlas_warped_shell/_build_otsu_shell/
_locate_registration_transform touch self.plotter or any other Qt/VTK scene
object in intraoperative/mri_preview.py -- duplicated here verbatim (rather
than imported) since SurgeryMRIPreview.__init__ constructs a real
QtInteractor, which needs a live Qt widget/QApplication this worker never
has. pyvista.PolyData can't cross a process boundary either way -- the
built shell crosses back as plain points/faces/intensity/point_opacity
arrays (a temp .npz, same convention as the other mesh-building workers
this session), and the caller reconstructs a pv.PolyData(points, faces)
from them."""
import argparse
import json
import os
import sys
import tempfile

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import numpy as np
from scipy import ndimage
from skimage.filters import threshold_otsu
import SimpleITK as sitk
import pyvista as pv

from paths_config import _paths

pv.global_theme.background = 'black'


def _locate_registration_transform(mri_path):
    """Duplicate of SurgeryMRIPreview._locate_registration_transform."""
    registration_dir = os.path.join(os.path.dirname(os.path.dirname(mri_path)), 'registration')
    transform_path = os.path.join(registration_dir, 'output_Composite.h5')
    return transform_path if os.path.exists(transform_path) else None


def _build_atlas_warped_shell(mri_img_ras, transform_path, downsample):
    """Duplicate of SurgeryMRIPreview._build_atlas_warped_shell -- see that
    method's docstring for the full rationale."""
    try:
        fixed_img = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        atlas_vol = sitk.GetArrayFromImage(fixed_img)
        transform = sitk.ReadTransform(transform_path)
    except Exception:
        return None

    data_zyx = atlas_vol[::downsample, ::downsample, ::downsample]
    data_xyz = np.transpose(data_zyx, (2, 1, 0))
    vol = pv.ImageData()
    vol.dimensions = np.array(data_xyz.shape) + 1
    vol.spacing = tuple(s * downsample for s in fixed_img.GetSpacing())
    vol.origin = (0.0, 0.0, 0.0)
    vol.cell_data['NIFTI'] = data_xyz.flatten(order='F')

    background = vol.threshold(value=0.5)
    background = background.extract_surface(algorithm='dataset_surface')
    background = background.clean().triangulate()
    background = background.fill_holes(hole_size=1e10)
    background = background.clean().triangulate()
    background = background.decimate(0.75)
    smoothed = background.smooth_taubin(n_iter=50, pass_band=0.1)

    atlas_spacing = np.array(fixed_img.GetSpacing())
    mri_idx = np.empty_like(smoothed.points)
    for i, pt in enumerate(smoothed.points):
        fixed_pt = fixed_img.TransformContinuousIndexToPhysicalPoint((pt / atlas_spacing).tolist())
        moving_pt = transform.TransformPoint(fixed_pt)
        mri_idx[i] = mri_img_ras.TransformPhysicalPointToContinuousIndex(moving_pt)

    mri_spacing = np.array(mri_img_ras.GetSpacing())
    mri_arr = sitk.GetArrayFromImage(mri_img_ras).astype(np.float32)  # zyx, full resolution
    coords_zyx = mri_idx[:, ::-1].T
    intensity = ndimage.map_coordinates(mri_arr, coords_zyx, order=1, mode='constant', cval=0.0)

    smoothed.points = mri_idx * mri_spacing
    smoothed.point_data['MRI'] = intensity
    return smoothed


def _build_otsu_shell(arr_zyx_full, spacing, downsample):
    """Duplicate of SurgeryMRIPreview._build_otsu_shell."""
    arr_zyx = arr_zyx_full[::downsample, ::downsample, ::downsample]
    arr_xyz = np.transpose(arr_zyx, (2, 1, 0))

    missing_mask = np.isnan(arr_xyz)
    if missing_mask.any():
        valid_mask = ~missing_mask
        neighbor_sum = ndimage.uniform_filter(np.where(valid_mask, arr_xyz, 0.0), size=3) * 27
        neighbor_count = ndimage.uniform_filter(valid_mask.astype(np.float32), size=3) * 27
        with np.errstate(invalid='ignore', divide='ignore'):
            local_mean = np.where(neighbor_count > 0, neighbor_sum / neighbor_count, 0.0)
        arr_xyz = np.where(missing_mask, local_mean, arr_xyz)

    otsu = threshold_otsu(arr_xyz[arr_xyz > 0])
    mask = arr_xyz > otsu
    mask = ndimage.binary_fill_holes(mask)
    labeled, num_components = ndimage.label(mask)
    if num_components > 0:
        sizes = ndimage.sum(mask, labeled, range(1, num_components + 1))
        mask = labeled == (1 + np.argmax(sizes))
    arr_xyz = np.where(mask, arr_xyz, 0.0)

    vol = pv.ImageData()
    vol.dimensions = np.array(arr_xyz.shape) + 1
    vol.spacing = spacing
    vol.origin = (0.0, 0.0, 0.0)
    vol.cell_data['MRI'] = arr_xyz.flatten(order='F')

    mesh = vol.threshold(value=1e-6, scalars='MRI')
    mesh = mesh.extract_surface(algorithm='dataset_surface')
    mesh = mesh.clean().triangulate()
    mesh = mesh.fill_holes(hole_size=1e10)
    mesh = mesh.clean().triangulate()
    mesh = mesh.decimate(0.75)
    smoothed = mesh.smooth_taubin(n_iter=50, pass_band=0.1)

    voxel_coords = smoothed.points / spacing  # continuous (x, y, z) indices
    intensity = ndimage.map_coordinates(arr_xyz, voxel_coords.T, order=1, mode='nearest')
    smoothed.point_data['MRI'] = intensity
    return smoothed


def _do_compute_shell(payload):
    """Pure logic behind _compute_shell -- runs inside this subprocess, not
    the GUI process. Returns spacing/clim as small JSON values, and the
    mesh (points/faces/intensity/point_opacity) via a temp .npz (its own
    tempfile.mkdtemp(), NOT run_json_subprocess's --input/--output
    directory -- see ephys_utils/theta_worker.py's identical note)."""
    mri_path = payload['mri_path']
    downsample = payload['downsample']

    img = sitk.ReadImage(mri_path)
    img = sitk.DICOMOrient(img, "RAS")
    orig_spacing = np.array(img.GetSpacing())

    transform_path = _locate_registration_transform(mri_path)
    smoothed = None
    if transform_path is not None:
        smoothed = _build_atlas_warped_shell(img, transform_path, downsample)
    if smoothed is None:
        arr_zyx_full = sitk.GetArrayFromImage(img).astype(np.float32)
        smoothed = _build_otsu_shell(arr_zyx_full, orig_spacing * downsample, downsample)

    intensity = smoothed.point_data['MRI']
    nonzero = intensity[intensity > 0]
    clim = [float(p) for p in np.percentile(nonzero, [1, 99])] if nonzero.size else None
    print(f"[mri_shell_worker] sampled shell intensity: min={intensity.min():.3g} "
          f"max={intensity.max():.3g} mean={intensity.mean():.3g} "
          f"nonzero_frac={nonzero.size / max(intensity.size, 1):.3f} clim={clim}", flush=True)
    point_opacity = np.where(intensity > 0, 0.5, 0.0)

    out_dir = tempfile.mkdtemp()
    arrays_path = os.path.join(out_dir, 'shell_arrays.npz')
    np.savez(arrays_path, points=smoothed.points, faces=smoothed.faces,
             intensity=intensity, point_opacity=point_opacity)

    return {'arrays_path': arrays_path, 'orig_spacing': orig_spacing.tolist(), 'clim': clim}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the intraoperative MRI shell build out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_compute_shell(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
