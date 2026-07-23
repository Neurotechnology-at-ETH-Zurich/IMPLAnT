# This Python file uses the following encoding: utf-8

import numpy as np
import scipy.signal
import xml.etree.ElementTree as ET
import os

def parse_recording_xml(filename):
    """
    Parse a Neuroscope XML file.

    Returns
    -------
    lfp_sampling_rate, sampling_rate, n_channels, channel_order, skip
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    lfp_sampling_rate = int(root.find('.//lfpSamplingRate').text)
    sampling_rate = int(root.find('.//samplingRate').text)
    n_channels = int(root.find('.//nChannels').text)

    channel_order = []
    skip = [False] * n_channels

    channel_groups_node = root.find('.//anatomicalDescription/channelGroups')
    if channel_groups_node is not None:
        for group in channel_groups_node.findall('group'):
            for channel in group.findall('channel'):
                ch_num = int(channel.text)
                skip_attr = channel.get('skip', '0')
                if ch_num < n_channels:
                    skip[ch_num] = (skip_attr == '1')
                channel_order.append(ch_num)

    return lfp_sampling_rate, sampling_rate, n_channels, channel_order, skip


def downsample_filter_LFP(raw_data_dir, filename,
                           num_channels=64, sample_rate=30000,
                           cutoff=250, stopband=450, filter_order=270):
    """
    Lowpass filter and downsample a raw multichannel ephys .dat file to LFP.

    Same approach as the MATLAB script: Parks-McClellan (equiripple) FIR,
    filtfilt (zero-phase), then integer downsampling (no separate anti-alias
    filter — the lowpass already serves that role). Output is interleaved
    int16, compatible with Neuroscope, with the channel order identical to
    the input .dat.

    Parameters
    ----------
    raw_data_dir : str - directory containing the .dat and .xml files
    filename : str - name of the .dat file (e.g. 'amplifier.dat')
    num_channels : int - number of channels in the raw file
    sample_rate : int - raw acquisition sample rate (Hz)
    cutoff : float - lowpass passband edge in Hz (default 250, matches MATLAB)
    stopband : float - stopband edge in Hz (default 450, matches MATLAB); the
                       250 -> 450 Hz transition band is what the filter rolls off across
    filter_order : int - FIR filter order (numtaps = filter_order + 1).
                         Default 270: ~60 dB attenuation for a 200 Hz transition at
                         20 kHz (fred-harris rule N ≈ fs/Δf × A/22). Higher = sharper
                         but slower; the MATLAB used 600 (overkill at 20 kHz).

    Returns
    -------
    ds_data_file : str - path to the saved LFP file
    """
    ds_factor = 10 #ds factor is always 10!
    nyquist = sample_rate / 2.0
    stopband = min(stopband, nyquist - 1)  # keep stopband edge below Nyquist
    stem = os.path.splitext(filename)[0]
    ds_data_file = os.path.join(raw_data_dir, stem + '.lfp')

    xml_filename = os.path.splitext(filename)[0] + '.xml'
    xml_path = os.path.join(raw_data_dir, xml_filename)
    if os.path.exists(xml_path):
        parse_recording_xml(xml_path)
    else:
        print(f"Warning: XML not found at {xml_path}, proceeding with supplied parameters")

    # Memory-mapped load — raw data is interleaved: [ch0_t0, ch1_t0, ..., chN_t0, ch0_t1, ...]
    raw_data_file = os.path.join(raw_data_dir, filename)
    raw = np.memmap(raw_data_file, dtype='int16', mode='r')
    n_samples = len(raw) // num_channels
    raw_data = raw[:n_samples * num_channels].reshape(n_samples, num_channels).T.astype(np.float64)
    # raw_data shape: (num_channels, n_samples)

    print(f"Shape of data array: {raw_data.shape}")

    # Parks-McClellan (equiripple) lowpass FIR — same design as MATLAB designfilt lowpassfir
    # numtaps = filter_order + 1, passband=cutoff Hz, stopband=cutoff+transition Hz
    b = scipy.signal.remez(filter_order + 1, [0, cutoff, stopband, nyquist], [1, 0], fs=sample_rate)

    n_ds_samples = len(raw_data[0, ::ds_factor])
    data_ds = np.zeros((num_channels, n_ds_samples), dtype=np.float64)

    for ch in range(num_channels):
        print(f"Processing channel {ch + 1}/{num_channels}")
        temp_lp = scipy.signal.filtfilt(b, [1.0], raw_data[ch])
        data_ds[ch] = temp_lp[::ds_factor]

    # Write interleaved int16 (Neuroscope-compatible, matches MATLAB fwrite(fid, data_ds', 'int16'))
    data_ds.T.astype(np.int16).ravel(order='C').tofile(ds_data_file)
    print("Done!")

    return ds_data_file
