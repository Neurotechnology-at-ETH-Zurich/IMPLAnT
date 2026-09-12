# This Python file uses the following encoding: utf-8
"""Runs ephys/visualisation3D.py's create_atlas_region_file compute step
in its own process. Invoked by that file's _create_atlas_region_file_impl
via gui_utils/subprocess_worker.py's run_json_subprocess -- mirrors samri/
samri_worker.py's --input/--output JSON-payload convention. Also works when
main_window.py's --atlas-region-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import numpy as np
import pandas as pd
import pyvista as pv
import SimpleITK as sitk

from paths_config import _paths


def _load_channel_excel(path):
    """Duplicate of Visualisation3D._load_channel_excel (ephys/
    visualisation3D.py) -- that staticmethod never touches `self`, so this
    is a verbatim copy rather than an import, keeping this worker
    self-contained (no PySide6/VTK/pyvistaqt needed)."""
    df = pd.read_excel(path, header=0)
    if 'Channel ID' in df.columns:
        df = df[df['Channel ID'] != -1].reset_index(drop=True)
    return df


def _do_create_atlas_region_file(payload):
    """Pure logic behind _create_atlas_region_file_impl -- runs inside this
    subprocess, not the GUI process. Returns {'skipped': bool} -- True if
    the existing atlas-regions.nii.gz already matches (nothing written)."""
    session_path = payload['session_path']
    mrid = payload['mrid']
    force = payload['force']

    filepath_atlas = os.path.join(session_path, "analysed", 'atlas-regions.nii.gz')
    points_electrodes_path = os.path.join(session_path, "analysed", mrid, 'channel_atlas_coordinates.xlsx')

    channel_labels = np.unique(_load_channel_excel(points_electrodes_path).iloc[:, 1].values)
    if not force and os.path.exists(filepath_atlas):
        mesh = pv.read(filepath_atlas)
        old_labels = np.unique(mesh.point_data['NIFTI'])
        if np.array_equal(old_labels[old_labels != 0], channel_labels[channel_labels != 0]):
            return {'skipped': True}

    atlas_image = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
    volume = sitk.GetArrayFromImage(atlas_image)
    volume[~np.isin(volume, channel_labels)] = 0
    label_image = sitk.GetImageFromArray(volume)
    label_image.CopyInformation(atlas_image)
    sitk.WriteImage(label_image, filepath_atlas)

    return {'skipped': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run atlas-region-file creation out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_create_atlas_region_file(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
