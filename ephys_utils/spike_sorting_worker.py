# This Python file uses the following encoding: utf-8
"""Runs ephys/init_ephys.py's _load_spike_sorting_file compute step
(ephys_utils/spiking_ruster.py's SpikeRuster.read_and_filter_matlab_files and
the static helpers it calls) in its own process. Invoked by that file's
work() closure via gui_utils/subprocess_worker.py's run_json_subprocess --
mirrors samri/samri_worker.py's --input/--output JSON-payload convention.
Also works when main_window.py's --spike-sorting-worker sentinel
re-invokes a frozen build.

The three staticmethods this needs (_read_mat/_read_prm_sitemap/
_valid_unit_ids) never touch `self` as a QWidget in
ephys_utils/spiking_ruster.py either -- duplicated here verbatim rather
than imported, so this worker doesn't need PySide6/pyqtgraph at all."""
import argparse
import json
import os
import re
import sys
import tempfile

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import h5py
import numpy as np
import scipy.io as sio


def _is_hdf5(path):
    with open(path, 'rb') as f:
        header = f.read(128)
    return b'MATLAB 7.3' in header


def _read_mat(path):
    """Return (spike_times_samples, spike_clusters, cluster_sites, cluster_notes)."""
    if not _is_hdf5(path):
        res = sio.loadmat(path, squeeze_me=True)
        spike_times    = res['spikeTimes'].flatten()
        spike_clusters = res['spikeClusters'].flatten().astype(int)
        cluster_sites  = res.get('clusterSites', np.array([])).flatten().astype(int)
        notes          = res.get('clusterNotes', np.array([]))
        cluster_notes  = np.array([str(n).strip() for n in np.atleast_1d(notes).flatten()])
        return spike_times, spike_clusters, cluster_sites, cluster_notes

    with h5py.File(path, 'r') as f:
        spike_times    = f['spikeTimes'][:].flatten()
        spike_clusters = f['spikeClusters'][:].flatten().astype(int)
        cluster_sites  = f['clusterSites'][:].flatten().astype(int) if 'clusterSites' in f else np.array([])
        if 'clusterNotes' in f:
            refs = f['clusterNotes'][:]
            cluster_notes = np.array([
                ''.join(chr(c) for c in f[r][:].flatten())
                for r in refs.flatten()
            ])
        else:
            cluster_notes = np.array([])
    return spike_times, spike_clusters, cluster_sites, cluster_notes


def _read_prm_sitemap(prm_path):
    """Parse the `siteMap` vector from a JRCLUST .prm file."""
    try:
        with open(prm_path, 'r') as f:
            text = f.read()
    except OSError:
        return None

    text = re.sub(r'%[^\n]*', '', text)
    m = re.search(r'\bsiteMap\b\s*=\s*(.+?);', text, re.DOTALL)
    if not m:
        return None
    rhs = m.group(1).strip().strip('[]').strip()

    if ':' in rhs:
        try:
            parts = [int(float(p)) for p in rhs.split(':')]
        except ValueError:
            return None
        if len(parts) == 2:
            return list(range(parts[0], parts[1] + 1))
        if len(parts) == 3:
            return list(range(parts[0], parts[2] + 1, parts[1]))
        return None

    nums = re.findall(r'-?\d+', rhs)
    return [int(n) for n in nums] if nums else None


def _valid_unit_ids(spike_clusters, cluster_notes, good_only):
    all_ids = np.unique(spike_clusters[spike_clusters > 0])
    if not good_only or len(cluster_notes) == 0:
        return set(all_ids.tolist())
    valid = set()
    for uid in all_ids:
        idx = uid - 1  # JRCLUST is 1-indexed
        if idx < len(cluster_notes) and cluster_notes[idx].lower() in ('good', ''):
            valid.add(uid)
    return valid if valid else set(all_ids.tolist())


def _read_and_filter_matlab_files(path, sample_rate, good_only=True, prm_path=None):
    """Verbatim port of SpikeRuster.read_and_filter_matlab_files."""
    spike_times_raw, spike_clusters, cluster_sites, cluster_notes = _read_mat(path)

    valid_ids = list(_valid_unit_ids(spike_clusters, cluster_notes, good_only))
    site_map = [s - 1 for s in _read_prm_sitemap(prm_path)]  # 1-based -> 0-based

    unit_channel_all = {
        uid: int(site_map[int(cluster_sites[uid - 1]) - 1]) for uid in valid_ids
    }
    keep = np.isin(spike_clusters, valid_ids)
    all_spike_times = spike_times_raw[keep].astype(np.float64) / sample_rate
    all_spike_units = spike_clusters[keep]
    return unit_channel_all, all_spike_times, all_spike_units


def _do_spike_sorting(payload):
    """Pure logic behind _load_spike_sorting_file's old work() closure --
    runs inside this subprocess, not the GUI process. all_spike_times/
    all_spike_units are full-session spike arrays -- cross back via a temp
    .npz file (its own tempfile.mkdtemp(), NOT run_json_subprocess's
    --input/--output directory, which is deleted the instant that call
    returns -- see ephys_utils/theta_worker.py's identical note), not
    inline JSON."""
    unit_channel_all, all_spike_times, all_spike_units = _read_and_filter_matlab_files(
        payload['path'], payload['sample_rate'],
        good_only=payload.get('good_only', True), prm_path=payload['prm_path'],
    )

    out_dir = tempfile.mkdtemp()
    arrays_path = os.path.join(out_dir, 'spike_arrays.npz')
    np.savez(arrays_path, all_spike_times=all_spike_times, all_spike_units=all_spike_units)

    return {
        'arrays_path': arrays_path,
        # dict keys must be strings to survive JSON -- caller converts back
        'unit_channel_all': {str(k): v for k, v in unit_channel_all.items()},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run spike-sorting-file parsing out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_spike_sorting(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
