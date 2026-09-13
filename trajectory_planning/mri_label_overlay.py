# This Python file uses the following encoding: utf-8
"""Reprojects the active atlas' region-label volume onto the subject's own
MRI voxel grid, using the full-resolution atlas<->MRI voxel correspondence
SAMRI's registration step already caches to disk (samri/samri_main.py's
start_registration, ~lines 260-275: fixed_img-indeces.npy / moving_img_
resampled25um-indeces.npy in <session>/registration/) -- no new
registration or transform inversion is needed, and none of the atlas<->MRI
composite transform's nonlinear (SyN) component needs inverting: SAMRI only
ever walked it forward (atlas voxel -> physical point -> MRI physical point
-> MRI voxel), which works regardless of whether that transform has a
closed-form inverse.

trajectory_planning/coord_transform.py's atlas_to_mri_coordinates() already
does the single-point version of the reconciliation this module vectorizes
(see reconcile_raw_to_display_indices's docstring) -- this module's own
correctness should be checked against that function's output on a handful
of sample points.
"""

import os
import shlex
import numpy as np
import SimpleITK as sitk
import vtk
from scipy.ndimage import distance_transform_edt

_FIXED_IDX_FILENAME = "fixed_img-indeces.npy"
_MOVING_IDX_RAW_FILENAME = "moving_img_resampled25um-indeces.npy"


def _index_to_physical_affine(img):
    """(origin, A) such that physical_point = origin + A @ index, matching
    sitk.Image's own TransformIndexToPhysicalPoint convention (xyz index,
    xyz physical mm -- NOT numpy's zyx array convention)."""
    origin = np.array(img.GetOrigin(), dtype=np.float64)
    spacing = np.array(img.GetSpacing(), dtype=np.float64)
    direction = np.array(img.GetDirection(), dtype=np.float64).reshape(3, 3)
    A = direction * spacing[np.newaxis, :]
    return origin, A


def _indices_to_physical(img, indices):
    """indices: (N,3) xyz voxel indices -> (N,3) xyz physical points (mm)."""
    origin, A = _index_to_physical_affine(img)
    return indices.astype(np.float64) @ A.T + origin


def _physical_to_indices(img, points):
    """points: (N,3) xyz physical points (mm) -> (N,3) float xyz voxel indices."""
    origin, A = _index_to_physical_affine(img)
    return (points - origin) @ np.linalg.inv(A).T


def reconcile_raw_to_display_indices(moving_img, moving_img_resampled, raw_indices):
    """Vectorized version of atlas_to_mri_coordinates()'s (coord_transform.py)
    last two lines: raw_indices are xyz voxel indices into moving_img (the
    grid SAMRI's cached .npy correspondence targets, i.e. MW.data_pre_
    resampled -- the raw/bias-corrected scan); returns the matching xyz
    voxel indices into moving_img_resampled (the grid trajectory planning
    actually displays as LoadMRI.volumes[0]). Both images share the same
    physical/world space and differ only by a Z resample/pad, so this is a
    pure affine re-index, not a real resample."""
    phys = _indices_to_physical(moving_img, raw_indices)
    display_idx = _physical_to_indices(moving_img_resampled, phys)
    return np.round(display_idx).astype(np.int64)


def build_mri_grid_correspondence(session_registration_dir, moving_img, moving_img_resampled):
    """(fixed_idx, mri_grid_idx): every atlas voxel index (fixed_idx, xyz)
    and its corresponding voxel index on the DISPLAYED MRI grid
    (mri_grid_idx, xyz). Reads SAMRI's cached fixed_img-indeces.npy /
    moving_img_resampled25um-indeces.npy and reconciles the raw-grid MRI
    side into display-grid indices -- a cheap, vectorized affine re-index
    (see reconcile_raw_to_display_indices's own docstring: "not a real
    resample"), not the expensive part of this workflow.

    Not disk-cached: its only caller (registration_mri.py's
    get_correspondence) already calls this exclusively on a
    load_or_build_mri_label_scatter cache miss -- i.e. exactly when that
    function's own full-volume distance-transform is about to run anyway
    -- and memoizes the result on self for the rest of that TrajPlanning
    instance's lifetime, so a second, persistent disk cache here would
    only ever help the (currently unreachable, atlas-switch-only) case of
    rebuilding the label scatter more than once in one process run
    without the SAMRI .npy inputs changing -- not worth the extra file and
    staleness-tracking for a step this cheap."""
    fixed_path = os.path.join(session_registration_dir, _FIXED_IDX_FILENAME)
    moving_raw_path = os.path.join(session_registration_dir, _MOVING_IDX_RAW_FILENAME)
    fixed_idx = np.load(fixed_path).astype(np.int64)
    moving_idx_raw = np.load(moving_raw_path)
    mri_grid_idx = reconcile_raw_to_display_indices(moving_img, moving_img_resampled, moving_idx_raw)
    return fixed_idx, mri_grid_idx


_LABEL_SCATTER_CACHE_FILENAME = "mri_label_scatter.npy"


def load_or_build_mri_label_scatter(session_registration_dir, atlas_label_path,
                                     get_correspondence, mri_shape_zyx):
    """(mri_label_vol): scatter_atlas_labels_to_mri_grid's own result,
    cached to disk -- that function is otherwise a real, uncached
    full-volume distance_transform_edt (plus a full atlas-label re-read)
    run on every single call.

    Reused as long as the cache is newer than everything it was built
    from -- the atlas label file itself, and the SAMRI .npy files this
    session's correspondence is ultimately derived from -- so a stale
    cache from a previous, since-fixed or since-rerun registration, or a
    since-changed atlas label file, doesn't silently linger; rebuilt
    otherwise.

    get_correspondence: zero-arg callable returning (fixed_idx,
    mri_grid_idx) -- the atlas<->MRI voxel correspondence
    build_mri_grid_correspondence computes (cheaply; not itself disk-
    cached, see its own docstring). Nothing else in the codebase reads
    that correspondence directly (it exists only to feed
    scatter_atlas_labels_to_mri_grid), so it's fetched lazily and called
    only on a cache miss here -- on a warm cache (the common case once a
    subject has been opened once), this function never touches
    movingImg_25um or the correspondence at all.

    The cache is keyed (via the filename) by mri_shape_zyx and the atlas
    label file's own basename, not just session_registration_dir -- a
    session reopened at a different resample spacing must not reuse a
    wrong-shaped array, and the atlas tag means a differently-labelled
    atlas can never silently reuse another atlas' scatter."""
    fixed_path = os.path.join(session_registration_dir, _FIXED_IDX_FILENAME)
    moving_raw_path = os.path.join(session_registration_dir, _MOVING_IDX_RAW_FILENAME)
    shape_tag = "x".join(str(s) for s in mri_shape_zyx)
    atlas_tag = os.path.splitext(os.path.basename(atlas_label_path))[0]
    cache_path = os.path.join(
        session_registration_dir,
        _LABEL_SCATTER_CACHE_FILENAME.replace(".npy", f"-{atlas_tag}-{shape_tag}.npy"))

    dep_paths = [p for p in (atlas_label_path, fixed_path, moving_raw_path) if os.path.exists(p)]
    cache_is_stale = (
        os.path.exists(cache_path)
        and dep_paths
        and os.path.getmtime(cache_path) < max(os.path.getmtime(p) for p in dep_paths))
    if os.path.exists(cache_path) and not cache_is_stale:
        return np.load(cache_path)

    fixed_idx, mri_grid_idx = get_correspondence()
    mri_label_vol = scatter_atlas_labels_to_mri_grid(
        atlas_label_path, fixed_idx, mri_grid_idx, mri_shape_zyx)
    np.save(cache_path, mri_label_vol)
    return mri_label_vol


def scatter_atlas_labels_to_mri_grid(atlas_label_path, fixed_idx, mri_grid_idx, mri_shape_zyx):
    """Forward-scatter the atlas' own label volume onto the MRI's voxel
    grid: for every atlas voxel (fixed_idx), place its label value at the
    corresponding MRI voxel (mri_grid_idx). Since the MRI grid is finer than
    the atlas grid, most MRI voxels never get hit by this scatter and would
    otherwise be indistinguishable from real label-0 ("Clear Label") voxels
    -- so every unhit MRI voxel is then filled with its nearest scattered
    neighbor's label (nearest-neighbor pull, the same effect as resampling
    MRI-voxel -> nearest atlas-voxel without needing to invert the atlas<->
    MRI SyN transform). Returns a zyx uint16 array shaped mri_shape_zyx
    (0 = background, matching the atlas' own "Clear Label" convention)."""
    atlas_img = sitk.ReadImage(atlas_label_path)
    atlas_labels = sitk.GetArrayFromImage(atlas_img)  # zyx

    labels_at_fixed = atlas_labels[fixed_idx[:, 2], fixed_idx[:, 1], fixed_idx[:, 0]]

    shape_xyz = np.array(mri_shape_zyx)[::-1]
    in_bounds = np.all((mri_grid_idx >= 0) & (mri_grid_idx < shape_xyz), axis=1)
    mi = mri_grid_idx[in_bounds]

    mri_label_vol = np.zeros(mri_shape_zyx, dtype=np.uint16)
    mri_label_vol[mi[:, 2], mi[:, 1], mi[:, 0]] = labels_at_fixed[in_bounds]

    hit = np.zeros(mri_shape_zyx, dtype=bool)
    hit[mi[:, 2], mi[:, 1], mi[:, 0]] = True
    nearest_idx = distance_transform_edt(~hit, return_distances=False, return_indices=True)
    mri_label_vol = mri_label_vol[tuple(nearest_idx)]
    return mri_label_vol


def parse_itk_snap_label_file(path):
    """Same parsing as utils/contrast.py's Contrast._parse_label_file --
    duplicated (not imported) since that method is bound to Contrast/the
    base-image-only label wiring we're deliberately not touching. Returns
    dict: {index: (r, g, b, a, name)} with rgba in 0-1."""
    labels = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tokens = shlex.split(line)
            idx = int(tokens[0])
            r = int(tokens[1])
            g = int(tokens[2])
            b = int(tokens[3])
            a = int(tokens[4])
            name = tokens[7]
            labels[idx] = (r / 255.0, g / 255.0, b / 255.0, a, name)
    return labels


def build_discrete_label_lut(labels, lut=None):
    """Same LUT-building logic as utils/contrast.py's Contrast.build_label_lut
    (see parse_itk_snap_label_file's note on why this is duplicated, not
    imported), generalized to also REFRESH an existing vtkLookupTable in
    place (pass the previous call's `lut` back in) instead of always
    creating a new one -- needed so an atlas switch (reload_atlas_view)
    can recolor the overlay without discarding/reattaching a new
    vtkLookupTable object on every already-built VTK actor."""
    max_idx = max(labels.keys()) if labels else 0

    if lut is None:
        lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(max_idx + 1)
    lut.SetTableRange(0, max_idx)
    lut.SetIndexedLookup(False)
    lut.Build()

    for i in range(max_idx + 1):
        lut.SetTableValue(i, 0.0, 0.0, 0.0, 0.0)
    for idx, (r, g, b, a, _name) in labels.items():
        lut.SetTableValue(idx, r, g, b, a)
    lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)
    return lut
