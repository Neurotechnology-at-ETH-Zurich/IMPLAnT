# This Python file uses the following encoding: utf-8
"""Theta-state detection on ephys LFP data.

Port of Peter's MATLAB pipeline (MATLAB_Peter/thetaDetectionWrapper.m and
friends). The detection *algorithm* mirrors the MATLAB exactly (see the
MATLAB_Peter/*.py reference port); the one deliberate difference is the input:
the MATLAB wrapper reads the raw wideband amplifier.dat, whereas this GUI runs
detection on the pre-computed LFP file (the downsampled `<stem>.lfp` produced by
the LFP-creation step) at the LFP sample rate. Theta and delta (2-10 Hz) live
well inside the LFP band, so this is numerically equivalent to the MATLAB for
the bands that matter, while being far cheaper than filtering and
Hilbert-transforming the wideband trace.

The three stages are rate-agnostic and identical to the reference:
  1. get_theta_states       - spectrogram at 100 log-spaced freqs -> theta/delta
                              magnitude ratio -> candidate windows
  2. get_theta_phase        - order-40 Butterworth bandpass (filtfilt) + Hilbert
                              -> instantaneous phase over the whole trace
  3. postprocess_theta_segments - reject/split on peak phase, amplitude, cycle
                              period and duration

Detection runs at the LFP rate: `work_fs` is that LFP rate and `decimation` is
the acquisition/LFP ratio, so `segments_samples` is reported in raw acquisition
samples (start * decimation) while `segments_s` stays in seconds. The raw
acquisition .dat is never read here.
"""

import numpy as np
from scipy.signal import butter, sosfiltfilt, hilbert, find_peaks

BIT_TO_UV = 0.195            # same int16 -> uV scaling the rest of the ephys view uses
_BANDPASS_PROTO_ORDER = 20   # scipy prototype order; bandpass doubles it -> order-40
                             # filter, matching MATLAB designfilt('FilterOrder',40)
_N_SPEC_FREQS = 100          # MATLAB logspace(...,100) spectrogram frequencies


# ----------------------------------------------------------------------
# Raw file access
# ----------------------------------------------------------------------

def open_raw(dat_path, n_channels):
    """Memory-map an interleaved int16 .dat as (n_samples, n_channels).

    Row-major on purpose: the file is [ch0_t0, ch1_t0, ..., chN_t0, ch0_t1, ...],
    so a sample-major view keeps single-channel reads on a strided slice instead
    of pulling the whole file through.
    """
    raw = np.memmap(dat_path, dtype='int16', mode='r')
    n_samples = len(raw) // n_channels
    return raw[:n_samples * n_channels].reshape(n_samples, n_channels)


def load_channels(dat_path, n_channels, channels, bit_scaling=BIT_TO_UV):
    """Load `channels` (0-indexed ids, as used everywhere else in the GUI) from
    an interleaved int16 .dat/.lfp file, scaled to uV.

    Returns
    -------
    data : ndarray (n_samples, n_selected) float32, in uV
    n_samples : int
    """
    raw_2d = open_raw(dat_path, n_channels)
    n_samples = raw_2d.shape[0]
    cols = [raw_2d[:, ch].astype(np.float32) * bit_scaling for ch in channels]
    return np.column_stack(cols), n_samples


# ----------------------------------------------------------------------
# Spectrogram at arbitrary frequencies (MATLAB spectrogram semantics)
# ----------------------------------------------------------------------

def _stft_magnitude_at_freqs(x, nperseg, noverlap, fs, freqs, block=256):
    """Short-time Fourier magnitude evaluated at arbitrary `freqs`.

    Faithful to MATLAB ``spectrogram(x, nperseg, noverlap, freqs, fs)``:
      - each segment is weighted by a symmetric Hamming window (what MATLAB uses
        when the window argument is a scalar length),
      - the transform is evaluated at exactly the requested frequencies via the
        DFT sum (NOT the linear FFT grid scipy.signal.spectrogram would use),
      - no per-segment mean removal (MATLAB does not detrend),
      - MATLAB takes ``abs(...)`` of the STFT, i.e. the magnitude, not power/PSD.

    Returns
    -------
    t   : ndarray (n_seg,)          - segment centre times (s)
    mag : ndarray (n_freqs, n_seg)  - |STFT| at `freqs`
    """
    x = np.ascontiguousarray(x, dtype=np.float64)
    freqs = np.asarray(freqs, dtype=np.float64)
    step = nperseg - noverlap
    if len(x) < nperseg:
        return np.empty(0), np.empty((len(freqs), 0))

    n_seg = 1 + (len(x) - nperseg) // step
    win = np.hamming(nperseg)                       # symmetric, == MATLAB hamming(nperseg)
    n = np.arange(nperseg)
    basis = np.exp(-2j * np.pi * np.outer(n, freqs) / fs)   # (nperseg, n_freqs)
    windows = np.lib.stride_tricks.sliding_window_view(x, nperseg)[::step]  # (n_seg, nperseg)

    mag = np.empty((len(freqs), n_seg))
    for b0 in range(0, n_seg, block):
        b1 = min(b0 + block, n_seg)
        seg = windows[b0:b1] * win                  # (blk, nperseg)
        mag[:, b0:b1] = np.abs(seg @ basis).T       # (n_freqs, blk)

    t = (np.arange(n_seg) * step + nperseg / 2) / fs
    return t, mag


# ----------------------------------------------------------------------
# Stage 1: theta/delta ratio
# ----------------------------------------------------------------------

def get_theta_states(lfp, fs, freqlist=(2, 20), window=2.0, noverlap=1.0,
                     f_theta=(6, 10), f_delta=(2, 3), th2d_ratio_threshold=1.5,
                     min_consecutive=3, consensus=False):
    """Windows where theta power dominates delta power.

    Parameters
    ----------
    lfp : ndarray (n_samples,) or (n_samples, n_channels) - uV
    fs : float - sampling rate of `lfp`
    freqlist : tuple - (fmin, fmax); the spectrogram is evaluated at 100
        log-spaced frequencies between fmin and fmax, matching MATLAB
        ``logspace(log10(fmin), log10(fmax), 100)``
    window, noverlap : float - spectrogram window / overlap in seconds
    f_theta, f_delta : tuple - band edges in Hz
    th2d_ratio_threshold : float
    min_consecutive : int - runs shorter than this many spectrogram bins are dropped
    consensus : bool - with more than one channel, keep only the bins where
        *every* channel is above threshold. When False, the first column decides
        on its own, which is what the MATLAB does.

    Returns
    -------
    theta_windows : ndarray (N, 2) - [start_time, end_time] in seconds
    """
    if lfp.ndim == 1:
        lfp = lfp[:, np.newaxis]

    nperseg = int(round(window * fs))
    noverlap_samples = int(round(noverlap * fs))
    freqs = np.logspace(np.log10(freqlist[0]), np.log10(freqlist[1]), _N_SPEC_FREQS)
    theta_mask = (freqs >= f_theta[0]) & (freqs <= f_theta[1])
    delta_mask = (freqs >= f_delta[0]) & (freqs <= f_delta[1])

    theta_moments = None
    t = None
    for ch in range(lfp.shape[1]):
        t, mag = _stft_magnitude_at_freqs(lfp[:, ch], nperseg, noverlap_samples, fs, freqs)

        theta_power = mag[theta_mask].sum(axis=0)
        delta_power = mag[delta_mask].sum(axis=0)
        with np.errstate(divide='ignore', invalid='ignore'):
            th2d_ratio = np.where(delta_power > 0, theta_power / delta_power, 0.0)
        above = th2d_ratio > th2d_ratio_threshold

        theta_moments = above if theta_moments is None else (theta_moments & above)
        if not consensus:
            break

    if theta_moments is None or len(theta_moments) == 0:
        return np.zeros((0, 2))

    # runs of at least `min_consecutive` consecutive above-threshold bins
    windows = []
    run_start = None
    for i, is_theta in enumerate(theta_moments):
        if is_theta:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None and i - run_start >= min_consecutive:
                windows.append([t[run_start], t[i - 1]])
            run_start = None
    if run_start is not None and len(theta_moments) - run_start >= min_consecutive:
        windows.append([t[run_start], t[-1]])

    return np.array(windows, dtype=float) if windows else np.zeros((0, 2))


# ----------------------------------------------------------------------
# Stage 2: theta-band signal and instantaneous phase
# ----------------------------------------------------------------------

def get_theta_phase(data, fs, f_theta=(6, 10), proto_order=_BANDPASS_PROTO_ORDER):
    """Zero-phase order-40 Butterworth bandpass + Hilbert, over the whole trace.

    Parameters
    ----------
    data : ndarray (n_samples,) or (n_samples, n_channels), uV
    fs : float - sampling rate of `data`
    f_theta : tuple - band edges in Hz
    proto_order : int - scipy prototype order; the bandpass has twice this order
        (so the default 20 gives an order-40 filter, matching MATLAB
        designfilt('bandpassiir','FilterOrder',40,'DesignMethod','butter')), and
        filtfilt then applies it forwards and backwards.

    Returns
    -------
    theta_phase : ndarray (n_samples, n_channels) - instantaneous phase, degrees
    theta_lfp   : ndarray (n_samples, n_channels) - band-filtered signal, uV
    """
    if data.ndim == 1:
        data = data[:, np.newaxis]

    sos = butter(proto_order, [f_theta[0], f_theta[1]], btype='bandpass',
                 fs=fs, output='sos')
    theta_lfp = sosfiltfilt(sos, data, axis=0).astype(np.float32)

    theta_phase = np.degrees(np.angle(hilbert(theta_lfp, axis=0))).astype(np.float32)
    return theta_phase, theta_lfp


def theta_cycle_starts(theta_phase, fs, sel_channel_idx=0, segments_s=None):
    """Times (s) of the trough that opens each theta cycle.

    `get_theta_phase` returns angle(hilbert(...)) in degrees, so 0 deg is a peak
    of the band-filtered signal and the wrap from +180 back to -180 is the trough
    between two cycles: a cycle boundary is a large negative step in the phase.
    Consecutive returned times therefore delimit one full cycle.

    Parameters
    ----------
    theta_phase : ndarray (n_samples,) or (n_samples, n_channels) - degrees
    fs : float - sampling rate of `theta_phase` (the detection rate, work_fs)
    sel_channel_idx : int - column to read when `theta_phase` is 2-D
    segments_s : ndarray (n_segments, 2) or None - when given, only boundaries
        falling inside a detected theta segment are returned

    Returns
    -------
    ndarray (n_boundaries,) - ascending times in seconds
    """
    phase = np.asarray(theta_phase)
    if phase.ndim > 1:
        phase = phase[:, sel_channel_idx]

    boundaries = np.where(np.diff(phase) < -180.0)[0] + 1
    times = boundaries / float(fs)

    if segments_s is not None:
        seg = np.asarray(segments_s, dtype=float).reshape(-1, 2)
        if len(seg) == 0:
            return times[:0]
        seg = seg[np.argsort(seg[:, 0])]
        # the segment that could contain each time is the last one starting at
        # or before it; inside means it also ends at or after it
        idx = np.searchsorted(seg[:, 0], times, side='right') - 1
        inside = (idx >= 0) & (times <= seg[np.clip(idx, 0, None), 1])
        times = times[inside]

    return times


# ----------------------------------------------------------------------
# Stage 3: refine the candidate windows (MATLAB postprocessThetaSegments.m)
# ----------------------------------------------------------------------

def _samples_between(t_lo, t_hi, n, fs):
    """Indices k in [0, n-1] with t_lo < time_vec[k] < t_hi, where
    time_vec = linspace(0, n/fs, n) (the MATLAB Time_vector_LFP), computed
    without materialising the full vector."""
    if n < 2:
        return np.arange(0)
    scale = (n / fs) / (n - 1)                 # seconds per index
    k0 = max(int(np.floor(t_lo / scale)) + 1, 0)      # smallest index strictly > t_lo
    k1 = min(int(np.ceil(t_hi / scale)) - 1, n - 1)   # largest index strictly < t_hi
    if k1 < k0:
        return np.arange(0)
    return np.arange(k0, k1 + 1)


def postprocess_theta_segments(theta_windows, theta_lfp, theta_phase, fs,
                               sel_channel_idx=0, phase_threshold=15.0,
                               amplitude_threshold=60.0, duration_threshold=0.5,
                               cycle_threshold_buffer=0.01, f_theta=(6, 10)):
    """Split and filter candidate windows on peak phase/amplitude, cycle period
    and duration - a faithful port of postprocessThetaSegments.m.

    Parameters
    ----------
    theta_windows : ndarray (N, 2) - [start, end] in seconds, from get_theta_states
    theta_lfp, theta_phase : ndarray (n_samples, n_channels) at rate `fs`
    fs : float
    sel_channel_idx : int - column of theta_lfp/theta_phase to judge on
    phase_threshold : float - max deviation of a peak's phase from the window mean (deg)
    amplitude_threshold : float - min peak amplitude (uV)
    duration_threshold : float - min surviving segment duration (s)
    cycle_threshold_buffer : float - tolerance on the theta cycle period (s)
    f_theta : tuple - band edges, used for the expected cycle period

    Returns
    -------
    segments : ndarray (M, 2) int - [start_sample, end_sample] at rate `fs`
    """
    n_samples = theta_lfp.shape[0]
    lfp_sel = theta_lfp[:, sel_channel_idx]
    phase_sel = theta_phase[:, sel_channel_idx]

    # --- pass 1: peak phase and amplitude thresholds ---
    stage1 = []
    for w_start, w_end in theta_windows:
        window_idx = _samples_between(w_start, w_end, n_samples, fs)
        if len(window_idx) == 0:
            continue

        peaks_rel, _ = find_peaks(lfp_sel[window_idx])
        if len(peaks_rel) == 0:
            continue
        peaks = window_idx[peaks_rel]

        mean_peak_phase = float(np.mean(phase_sel[peaks]))
        start_idx = peaks[0]
        break_detected = False
        count = 0
        for i in range(1, len(peaks) - 1):
            bad = (abs(phase_sel[peaks[i]] - mean_peak_phase) > phase_threshold or
                   lfp_sel[peaks[i]] < amplitude_threshold)
            if bad:
                break_detected = True
                if count > 2:
                    end_idx = peaks[i - 1]
                    if start_idx < end_idx:
                        stage1.append([int(start_idx), int(end_idx)])
                        start_idx = peaks[i + 1]
                        count = 0
                else:  # count <= 2
                    start_idx = peaks[i + 1]
            count += 1
        if not break_detected:
            stage1.append([int(window_idx[0]), int(window_idx[-1])])

    # --- pass 2: cycle period check via phase crossings ---
    period_max = 1.0 / f_theta[0] + cycle_threshold_buffer
    period_min = 1.0 / f_theta[1] - cycle_threshold_buffer

    stage2 = []
    for w_start_samp, w_end_samp in stage1:
        window_idx = _samples_between(w_start_samp / fs, w_end_samp / fs, n_samples, fs)
        if len(window_idx) == 0:
            continue

        # crossings where the phase steps by more than phase_threshold, shifted
        # back one index as MATLAB does (find(abs(diff(phase))>thr) - 1)
        cross = np.where(np.abs(np.diff(phase_sel[window_idx])) > phase_threshold)[0] - 1
        # MATLAB `if idx_peak_phase` skips the window when it is empty or has a
        # zero entry (cross == -1 here); replicate that.
        if cross.size == 0 or np.any(cross < 0):
            continue

        start_idx = window_idx[cross[0]]
        break_detected = False
        count = 0
        for i in range(1, len(cross) - 1):
            dt = (cross[i] - cross[i - 1]) / fs
            if dt > period_max or dt < period_min:
                break_detected = True
                if count > 2:
                    end_idx = window_idx[cross[i - 1]]
                    if start_idx < end_idx:
                        stage2.append([int(start_idx), int(end_idx)])
                        start_idx = window_idx[cross[i + 1]]
                        count = 0
                else:  # count <= 2
                    start_idx = window_idx[cross[i + 1]]
            count += 1
        if not break_detected:
            stage2.append([int(window_idx[0]), int(window_idx[-1])])

    if not stage2:
        return np.zeros((0, 2), dtype=np.int64)

    # --- pass 3: duration filter ---
    segments = np.array(stage2, dtype=np.int64)
    durations = (segments[:, 1] - segments[:, 0]) / fs
    return segments[durations >= duration_threshold]


# ----------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------

def detect_theta(lfp_path, n_channels, lfp_fs, channels, sel_channel_idx=0,
                 raw_sample_rate=None, bit_scaling=BIT_TO_UV, freqlist=(2, 20),
                 t_window=2.0, noverlap=1.0, f_theta=(6, 10), f_delta=(2, 3),
                 th2d_ratio_threshold=1.5, phase_threshold=15.0,
                 amplitude_threshold=60.0, duration_threshold=0.5,
                 cycle_threshold_buffer=0.01, consensus=True, progress=None):
    """Run the full pipeline on the pre-computed LFP file, at the LFP rate.

    With two channels loaded, the theta/delta ratio test can be required to pass
    on both (`consensus`, an option the MATLAB does not have); the peak amplitude
    and phase tests always stay on the primary channel. With `consensus=False`
    the result matches the single-channel MATLAB algorithm exactly.

    Parameters
    ----------
    lfp_path : str - interleaved int16 LFP file (`<stem>.lfp`)
    n_channels : int - channels in that file (from the XML)
    lfp_fs : float - LFP sample rate (Hz); detection runs at this rate
    channels : sequence of int - 0-indexed channel ids to load
    sel_channel_idx : int - which entry of `channels` drives the detection
    raw_sample_rate : int or None - acquisition rate (Hz). Used only to report
        `segments_samples` in raw acquisition samples; if None, samples are in
        LFP samples (decimation == 1).
    consensus : bool - require the ratio test to pass on every loaded channel
    progress : callable(str) or None - progress messages for the caller's overlay

    Returns
    -------
    dict with
        segments_s       : ndarray (M, 2) - [start, end] in seconds
        segments_samples : ndarray (M, 2) - [start, end] in raw acquisition samples
        theta_lfp        : ndarray (n_lfp, n_channels) - band-filtered, uV, at lfp_fs
        theta_phase      : ndarray (n_lfp, n_channels) - degrees, at lfp_fs
        work_fs, decimation, channels, sel_channel_idx, n_raw_samples
        params           : dict of the detection parameters
    """
    def say(msg):
        if progress is not None:
            progress(msg)

    # acquisition/LFP ratio, so segment boundaries can be reported in raw samples
    decimation = max(1, int(round(raw_sample_rate / lfp_fs))) if raw_sample_rate else 1

    say("Loading LFP data…")
    data, n_lfp_samples = load_channels(lfp_path, n_channels, channels,
                                        bit_scaling=bit_scaling)

    say("Detecting theta states…")
    # with consensus on, every loaded channel must agree; the primary channel is
    # put first so it still decides on its own when consensus is off
    order = [sel_channel_idx] + [c for c in range(data.shape[1]) if c != sel_channel_idx]
    theta_windows = get_theta_states(
        data[:, order], lfp_fs, freqlist=freqlist, window=t_window,
        noverlap=noverlap, f_theta=f_theta, f_delta=f_delta,
        th2d_ratio_threshold=th2d_ratio_threshold, consensus=consensus)

    say("Computing theta phase…")
    theta_phase, theta_lfp = get_theta_phase(data, lfp_fs, f_theta=f_theta)

    say("Refining segments…")
    segments = postprocess_theta_segments(
        theta_windows, theta_lfp, theta_phase, lfp_fs,
        sel_channel_idx=sel_channel_idx, phase_threshold=phase_threshold,
        amplitude_threshold=amplitude_threshold, duration_threshold=duration_threshold,
        cycle_threshold_buffer=cycle_threshold_buffer, f_theta=f_theta)

    segments_s = segments / lfp_fs
    segments_samples = np.round(segments * decimation).astype(np.int64)

    return {
        'segments_s': segments_s,
        'segments_samples': segments_samples,
        'theta_lfp': theta_lfp,
        'theta_phase': theta_phase,
        'work_fs': float(lfp_fs),        # detection runs at the LFP rate
        'decimation': decimation,        # raw acquisition samples per LFP sample
        'channels': list(channels),
        'sel_channel_idx': sel_channel_idx,
        'n_raw_samples': int(n_lfp_samples * decimation),
        'params': {
            'sample_rate': raw_sample_rate if raw_sample_rate else lfp_fs,
            'lfp_sample_rate': lfp_fs,
            'freqlist': list(freqlist),
            'f_theta': list(f_theta),
            'f_delta': list(f_delta),
            'th2d_ratio_threshold': th2d_ratio_threshold,
            't_window': t_window,
            'noverlap': noverlap,
            'phase_threshold': phase_threshold,
            'amplitude_threshold': amplitude_threshold,
            'duration_threshold': duration_threshold,
            'cycle_threshold_buffer': cycle_threshold_buffer,
            'consensus': bool(consensus),
        },
    }


# ----------------------------------------------------------------------
# Debug plotting (kept out of the pipeline path; matplotlib imported lazily)
# ----------------------------------------------------------------------

def plot_theta_windows(result, max_windows=10):
    """Plot the band-filtered signal and phase for each detected segment.

    Diagnostic only — used when validating against the MATLAB, not by the GUI.
    """
    import matplotlib.pyplot as plt

    fs = result['work_fs']
    theta_lfp = result['theta_lfp']
    theta_phase = result['theta_phase']
    sel = result['sel_channel_idx']
    segments = result['segments_samples']

    for start, end in segments[:max_windows]:
        idx = np.arange(start, end + 1)
        t = idx / fs

        fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
        axes[0].plot(t, theta_lfp[idx, sel], 'k', linewidth=1.2)
        axes[0].set_ylabel('Amplitude (μV)')
        axes[0].set_title(f'Theta-filtered LFP, channel {result["channels"][sel]}')
        axes[1].plot(t, theta_phase[idx, sel])
        axes[1].set_ylabel('Theta phase (deg)')
        axes[1].set_xlabel('Time (s)')
        plt.tight_layout()
        plt.show()
