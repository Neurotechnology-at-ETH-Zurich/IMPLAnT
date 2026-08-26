# This Python file uses the following encoding: utf-8
"""Fetch + one-time conversion of a BrainGlobe atlas (currently just
whs_sd_swc_female_rat_39um, see mrid_utils/atlas_registry.py) into the same
5-file layout mrid_utils/atlas_fetch.py's WHS bundle already uses --
annotation/reference/mask as NIfTI volumes plus an ITK-SNAP .label file --
so every existing consumer (registration.py, rendering.py, electrode.py,
core/electrode_localization.py, ephys/*) keeps reading _paths['atlas_volume'
/'atlas_labels'/'atlas_template'/'atlas_mask'] unchanged, regardless of
which atlas produced them.

bg_atlasapi owns the actual download+cache (under ~/.brainglobe/) -- this
module only does the geometric conversion into IMPLAnT's own voxel-index
convention, once, the first time a given BrainGlobe atlas is selected.
"""
import os

import nibabel as nib
import numpy as np
from PySide6.QtWidgets import QApplication, QMessageBox, QProgressDialog
from PySide6.QtCore import Qt

from paths_config import _paths, save_paths
from mrid_utils.atlas_registry import ATLASES

# The exact affine of IMPLAnT's existing WHS_SD_rat_atlas_v4.nii.gz (39.0625um
# isotropic, RAS). Every BrainGlobe atlas this module converts has already
# been confirmed (see mrid_utils/atlas_registry.py's comments on
# whs_sd_swc_female_rat_39um) to share that exact voxel grid once mapped to
# its own 'brainglobe_target_orientation' -- reusing this fixed affine
# (rather than re-deriving one from BrainGlobeAtlas metadata) is what keeps
# every converted atlas's voxel indices identical to WHS's, including the
# existing hardcoded bregma/lambda coordinates.
_WHS_AFFINE = np.array([
    [0.0390625, 0.0,        0.0,       -9.53125],
    [0.0,        0.0390625, 0.0,      -24.3359375],
    [0.0,        0.0,        0.0390625, -9.6875],
    [0.0,        0.0,        0.0,        1.0],
])


def _target_dir(atlas_id):
    entry = ATLASES[atlas_id]
    return os.path.join(_paths['atlas_folder'], entry['subfolder'])


def _converted_files_present(atlas_id):
    entry = ATLASES[atlas_id]
    target_dir = _target_dir(atlas_id)
    return all(os.path.exists(os.path.join(target_dir, filename))
               for filename in entry['files'].values())


def _write_itk_snap_labels(structures, path):
    """ATLASES[...]['label_format'] == 'itk_snap' files are parsed by
    mrid_utils.handlers.read_itk_snap_labels -- same whitespace/quoted-label
    format as IMPLAnT's existing WHS_SD_rat_atlas_v4.label."""
    lines = [
        "################################################",
        "# ITK-SnAP Label Description File",
        "# IDX   -R-  -G-  -B-  -A--  VIS MSH  LABEL",
        "################################################",
        '    0     0    0    0        0  0  0    "Clear Label"',
    ]
    for structure in structures.values():
        idx = structure['id']
        r, g, b = structure['rgb_triplet']
        name = structure['name'].replace('"', "'")
        lines.append(f'{idx:>5} {r:>4} {g:>4} {b:>4}        1  1  0    "{name}"')
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def _convert(atlas_id, progress_dialog):
    from brainglobe_atlasapi import BrainGlobeAtlas
    from brainglobe_space import AnatomicalSpace

    entry = ATLASES[atlas_id]
    progress_dialog.setLabelText(f"Downloading {entry['display_name']}…")
    QApplication.processEvents()
    atlas = BrainGlobeAtlas(entry['brainglobe_name'])

    progress_dialog.setLabelText(f"Converting {entry['display_name']}…")
    QApplication.processEvents()
    target_orientation = entry.get('brainglobe_target_orientation', 'lpi')
    src = AnatomicalSpace(atlas.orientation, shape=atlas.annotation.shape)
    annotation = src.map_stack_to(target_orientation, atlas.annotation)
    reference = src.map_stack_to(target_orientation, atlas.template)
    mask = (annotation > 0).astype(np.uint8)

    target_dir = _target_dir(atlas_id)
    os.makedirs(target_dir, exist_ok=True)
    nib.save(nib.Nifti1Image(annotation.astype(np.int32), _WHS_AFFINE),
              os.path.join(target_dir, entry['files']['atlas_volume']))
    nib.save(nib.Nifti1Image(reference, _WHS_AFFINE),
              os.path.join(target_dir, entry['files']['atlas_template']))
    nib.save(nib.Nifti1Image(mask, _WHS_AFFINE),
              os.path.join(target_dir, entry['files']['atlas_mask']))
    _write_itk_snap_labels(atlas.structures, os.path.join(target_dir, entry['files']['atlas_labels']))


def ensure_brainglobe_atlas_available(parent_widget, atlas_id):
    """Returns True once every file ATLASES[atlas_id]['files'] names is
    present under atlas_folder/<subfolder>/ -- either because they already
    were, or because this just fetched+converted them. Returns False on
    failure (network, missing brainglobe-atlasapi dependency, etc.) --
    callers should leave whichever atlas was active before this call."""
    if _converted_files_present(atlas_id):
        return True

    entry = ATLASES[atlas_id]
    dlg = QProgressDialog(f"Preparing {entry['display_name']}…", None, 0, 0, parent_widget)
    dlg.setWindowTitle("Preparing Atlas")
    dlg.setWindowModality(Qt.WindowModal)
    dlg.setMinimumDuration(0)
    dlg.setCancelButton(None)
    dlg.show()
    QApplication.processEvents()

    try:
        _convert(atlas_id, dlg)
    except Exception as exc:
        QMessageBox.critical(
            parent_widget, "Atlas preparation failed",
            f"Could not fetch/convert {entry['display_name']}:\n{exc}")
        return False
    finally:
        dlg.close()

    if not _converted_files_present(atlas_id):
        QMessageBox.critical(
            parent_widget, "Atlas preparation failed",
            f"{entry['display_name']} was fetched, but the expected converted "
            f"files still aren't all present under {_target_dir(atlas_id)}.")
        return False

    return True
