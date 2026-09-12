# This Python file uses the following encoding: utf-8
"""Runs ephys_utils/all_channels_spectrogram.py's ripple-triggered average
(_compute_ripple_triggered_spec, formerly on _RippleSpecWorker's QThread) in
its own process. Invoked by that file's _update_ripple_triggered via
gui_utils/subprocess_worker.py's run_json_subprocess -- mirrors samri/
samri_worker.py's --input/--output JSON-payload convention, with progress
streamed as plain stdout lines (run_json_subprocess's on_progress) since a
session with many ripples can take minutes. Also works when
main_window.py's --ripple-spec-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import numpy as np
import pywt
from scipy.signal import butter, filtfilt, hilbert

from ephys.ephysrecording import EphysRecording

# Duplicated from ephys_utils/all_channels_spectrogram.py's
# AllChannelsSpectrogram class constants -- must stay in sync with that
# class if those ever change (same relationship as trajectory_worker.py's
# _ShimLoadMRI being a duplicate of samri_main.py's).
BANDWIDTH = 2.0
CENTER = 1.0
EDGE_SIGMAS = 3.0
BIT_TO_UV = 0.195
RIPPLE_HALF_WINDOW_S = 0.025
RIPPLE_BAND = (120.0, 200.0)

WAVELET = f"cmor{BANDWIDTH}-{CENTER}"
_CENTRAL = pywt.central_frequency(WAVELET)


def _sigma_t(f):
    """Temporal std (seconds) of the Morlet envelope at frequency f, same as
    LFPSpectrogram/AllChannelsSpectrogram: sqrt(bandwidth/2) * central_freq / f."""
    return np.sqrt(BANDWIDTH / 2.0) * _CENTRAL / f


def _mean_power(traces, fs, freqs, i0, i1):
    """Mean raw wavelet power over samples [i0:i1] of `traces`. Returns
    (n_channels, n_freqs), or None if the transform produced nothing."""
    scales = pywt.frequency2scale(WAVELET, freqs / fs)
    out = np.empty((traces.shape[0], len(freqs)), dtype=np.float64)
    chunk = max(1, int(64e6 / max(traces.size * 16, 1)))
    for a in range(0, len(freqs), chunk):
        b = min(len(freqs), a + chunk)
        coef, _ = pywt.cwt(traces, scales[a:b], WAVELET,
                           sampling_period=1.0 / fs, method='fft', axis=-1)
        if coef.shape[-1] == 0:
            return None
        power = coef.real ** 2 + coef.imag ** 2
        out[:, a:b] = power[:, :, i0:i1].mean(axis=2).T
    return out


def _ripple_peak_times(lfp_memmap, fs, ripple_events, ripple_channels):
    """Peak time of every ripple event: the sample of maximum ripple-band
    envelope within its (start, end), averaged over the detection channels."""
    centers = ripple_events.mean(axis=1)
    if not ripple_channels:
        return centers

    n_samples = lfp_memmap.shape[1]
    nyq = fs / 2.0
    low = max(RIPPLE_BAND[0] / nyq, 1e-6)
    high = min(RIPPLE_BAND[1] / nyq, 0.999)
    b, a = butter(4, [low, high], btype='band')

    peaks = centers.copy()
    for i, (t0, t1) in enumerate(ripple_events):
        s0 = max(0, int(t0 * fs))
        s1 = min(n_samples, int(t1 * fs))
        if s1 - s0 < 8:
            continue
        try:
            trace = lfp_memmap[ripple_channels, s0:s1].astype(np.float64) * BIT_TO_UV
            trace = trace - trace.mean(axis=1, keepdims=True)
            filtered = filtfilt(b, a, trace, axis=1)
            envelope = np.abs(hilbert(filtered, axis=1)).mean(axis=0)
            peaks[i] = (s0 + int(np.argmax(envelope))) / fs
        except Exception:
            continue
    return peaks


def _compute_ripple_triggered_spec(lfp_memmap, fs, freqs, channel_ids,
                                    ripple_events, ripple_channels=None,
                                    progress_cb=None):
    """Mean raw power over ±RIPPLE_HALF_WINDOW_S around every detected
    ripple's true peak, across the whole recording. Returns (spec, n_used);
    spec is None if there are no usable ripples."""
    n_samples = lfp_memmap.shape[1]
    pad = int(np.ceil(EDGE_SIGMAS * _sigma_t(freqs[0]) * fs))
    half_samples = int(round(RIPPLE_HALF_WINDOW_S * fs))

    centers = _ripple_peak_times(lfp_memmap, fs, ripple_events, ripple_channels)
    total_n = len(centers)
    total = np.zeros((len(channel_ids), len(freqs)), dtype=np.float64)
    n_used = 0
    for i, tc in enumerate(centers):
        c = int(round(tc * fs))
        s0, s1 = c - half_samples, c + half_samples + 1
        p0, p1 = s0 - pad, s1 + pad
        if not (p0 < 0 or p1 > n_samples):
            traces = lfp_memmap[channel_ids, p0:p1].astype(np.float32) * BIT_TO_UV
            traces = traces - traces.mean(axis=1, keepdims=True)
            power = _mean_power(traces, fs, freqs, s0 - p0, s1 - p0)
            if power is not None:
                total += power
                n_used += 1
        if progress_cb is not None:
            progress_cb(i + 1, total_n)

    if n_used == 0:
        return None, 0
    return total / n_used, n_used


def _do_compute(payload):
    lfp_path = payload['lfp_path']
    n_channels = payload['n_channels']
    fs = payload['fs']
    freqs = np.array(payload['freqs'], dtype=np.float64)
    channel_ids = payload['channel_ids']
    ripple_events = np.array(payload['ripple_events'], dtype=np.float64)
    ripple_channels = payload.get('ripple_channels')

    lfp_memmap = EphysRecording._load_lfp_memmap(lfp_path, n_channels)

    def progress_cb(done, total):
        # plain stdout line -- run_json_subprocess's on_progress relays this
        # straight to BusyOverlay.set_message, same convention as
        # samri_main.py's _run_worker_subprocess.
        print(f"Averaging ripple {done} / {total}, please wait…", flush=True)

    spec, n_used = _compute_ripple_triggered_spec(
        lfp_memmap, fs, freqs, channel_ids, ripple_events, ripple_channels,
        progress_cb=progress_cb,
    )
    return {'spec': spec.tolist() if spec is not None else None, 'n_used': n_used}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the ripple-triggered spectrogram average out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_compute(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
