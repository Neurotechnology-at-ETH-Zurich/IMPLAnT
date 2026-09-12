# This Python file uses the following encoding: utf-8
"""Runs gui_utils/buttons_gui_time_series.py's activate_get_gaussian_analysis
compute step (core/electrode_localization.py's ElectrodeLoc.
get_gaussian_centers) in its own process. Invoked by that file's work()
closure via gui_utils/subprocess_worker.py's run_json_subprocess -- mirrors
samri/samri_worker.py's --input/--output JSON-payload convention. Also
works when main_window.py's --gaussian-centers-worker sentinel re-invokes a
frozen build."""
import argparse
import json
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import nibabel as nib
import numpy as np
import SimpleITK as sitk

from mrid_utils import gauss_aux, handlers, warper


def _get_roinames(filename):
    """Duplicate of ElectrodeLoc.get_roinames (core/electrode_localization.py)
    -- that method never touches `self`, so this is a verbatim copy rather
    than an import, keeping this worker self-contained."""
    labels = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 8:
                label = parts[-1].strip('"')
                labels.append(label)
    labels.pop(0)

    roi_names = []
    pure_labels = [l.rstrip("0123456789") for l in labels]

    for i, label in enumerate(labels):
        if label.endswith("1"):
            roi_names.append((pure_labels[i]))

    return roi_names


def _do_gaussian_centers(payload):
    """Pure logic behind ElectrodeLoc.get_gaussian_centers -- runs inside
    this subprocess, not the GUI process. Returns {'skipped': [[data_view,
    message], ...]}. Lets a FileNotFoundError from a missing labels.txt
    propagate uncaught (same as the original, which never wrapped that
    specific read in the per-ROI try/except) -- main() below catches it at
    the top level and reports it distinctly."""
    session_path = payload['session_path']
    labels_path = os.path.join(session_path, "anat", "labels.txt")
    transformation_files = payload['transformation_files']
    data_views = payload['data_views']
    volume_file_paths = payload['volume_file_paths']

    labelsdf = handlers.read_labels(labels_path)

    skipped = []
    for idx, data_view in enumerate(data_views):
        filename = os.path.basename(volume_file_paths[idx][:-7])
        roi_names = _get_roinames(labels_path)
        orientation = data_view

        transform_filename = transformation_files[idx]

        if isinstance(transform_filename, str):
            transform_path = transform_filename
            tx = sitk.ReadTransform(transform_path)
            fixed_ind = transform_filename.split("-")[-1].rsplit(".", 1)[0]
        elif isinstance(transform_filename, list):
            tx = warper.create_composite_transform(transform_filename, os.path.join(session_path, "anat"))
            fixed_ind = transform_filename[-1].split("-")[-1].rsplit(".", 1)[0]
        else:
            print("No valid transformation!")

        try:
            for roi_name in roi_names:
                heatmap_filename = ".".join((filename + "-" + roi_name + "-heatmap", "nii", "gz"))
                heatmap_path = os.path.join(session_path, "analysed", roi_name, data_view, heatmap_filename)
                if os.path.exists(heatmap_path):
                    savepath = os.path.join(session_path, 'analysed', roi_name, data_view)
                    fixed_path = warper.heatmap_warp(filename, roi_name, savepath, session_path, fixed_ind, tx)
                    volume3d_resampled = np.asanyarray(nib.load(fixed_path).dataobj)
                    gauss_aux.run_gaussian_analysis(filename, savepath, roi_name, data_view, volume3d_resampled, labelsdf)
        except FileNotFoundError as e:
            skipped.append([data_view, str(e)])
            continue

    return {'skipped': skipped}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run Gaussian-center extraction out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    try:
        result = _do_gaussian_centers(payload)
    except FileNotFoundError as e:
        result = {'missing_error': str(e)}

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
