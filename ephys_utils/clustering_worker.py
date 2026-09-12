# This Python file uses the following encoding: utf-8
"""Runs ephys/init_ephys.py's run_hierarchical_clustering compute step
(build_activity_matrix/compute_correlation_matrix/hierarchical_clustering,
ephys_utils/hierarchical_clustering.py) in its own process. Invoked by that
file's run_hierarchical_clustering via gui_utils/subprocess_worker.py's
run_json_subprocess -- mirrors samri/samri_worker.py's --input/--output
JSON-payload convention. Also works when main_window.py's
--clustering-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import numpy as np

from ephys_utils.hierarchical_clustering import (
    build_activity_matrix, compute_correlation_matrix,
    hierarchical_clustering, load_custom_colormap,
)


def _do_clustering(payload):
    """Pure logic behind run_hierarchical_clustering's old work() closure --
    runs inside this subprocess, not the GUI process. spike_times_samples/
    spike_units cross the process boundary as a temp .npz file (payload
    just carries its path) since a full session's spike train can be large;
    everything else here is small enough for plain JSON.

    Returns 'lut' as a raw (256,4) uint8 list -- not a matplotlib colormap
    object, which can't cross a process boundary -- for
    _embed_clustering_heatmap to turn into a pg.ColorMap directly."""
    spike_data = np.load(payload['spike_data_path'])
    spike_times_samples = spike_data['spike_times_samples']
    spike_units = spike_data['spike_units']
    unit_ids = np.array(payload['unit_ids'])
    sample_rate = payload['sample_rate']
    unit_labels = payload['unit_labels']
    unit_channel = {int(k): v for k, v in payload['unit_channel'].items()}

    activity, _ = build_activity_matrix(
        spike_times_samples, spike_units, unit_ids, sample_rate
    )
    corr_matrix = compute_correlation_matrix(activity)

    # try to load Peter's custom colormap; fall back to magma (the fallback
    # itself -- pg.colormap.get('berlin', ...) -- stays in
    # _embed_clustering_heatmap, since it's a pyqtgraph/GUI-side concern)
    colormap = load_custom_colormap(payload['cmap_path'], key='CustomColormap3')
    lut = None
    if colormap is not None:
        lut = (colormap(np.linspace(0, 1, 256)) * 255).astype(np.uint8).tolist()

    cluster_labels, reordered = hierarchical_clustering(corr_matrix, unit_labels)
    unit_labels_reordered = [lbl for lbl, _ in cluster_labels]
    channels_reordered = [unit_channel[int(unit_ids[i])] for i in range(len(unit_ids))]

    return {
        'lut': lut,
        'reordered': reordered.tolist(),
        'unit_labels_reordered': unit_labels_reordered,
        'channels_reordered': channels_reordered,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run hierarchical clustering out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_clustering(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
