# This Python file uses the following encoding: utf-8
"""Reader for the digitalin.dat TTL format used alongside some ephys
recordings (see CLAUDE-data_readme.md, shipped next to sample digitalin
files, for the full bit-level spec this mirrors): one uint16 word per
sample, no header, each bit an independent digital TTL line. Only bits 0
(camera shutter) and 1 (LED on/off) are ever driven; bits 2-15 are always 0.

Mirrors the stimulation-analysis repo's own DigitalInFile API surface
(channel/rising_edges/falling_edges) rather than inventing a different
shape, so the two read the same way side by side -- this module doesn't
import that repo, since it isn't a dependency of this app.
"""
import numpy as np

CAMERA_BIT = 0
LED_BIT = 1

# No header/sidecar file carries this -- the readme documents it as fixed
# for every digitalin.dat this format is used for, same as the
# stimulation-analysis repo's own config.SAMPLE_RATE.
DIGITALIN_SAMPLE_RATE = 20000.0


class DigitalInFile:
    def __init__(self, path, sample_rate=DIGITALIN_SAMPLE_RATE):
        self.path = path
        self.sample_rate = sample_rate
        # memmap, not fromfile -- these run tens of millions of samples long,
        # and only a small on-screen time window is ever actually read.
        self.words = np.memmap(path, dtype='<u2', mode='r')

    @property
    def n_samples(self):
        return len(self.words)

    def channel(self, bit, sample_slice=None):
        words = self.words if sample_slice is None else self.words[sample_slice]
        return (words >> bit) & 1

    def rising_edges(self, bit):
        state = self.channel(bit).astype(np.int8)
        return np.flatnonzero(np.diff(state) == 1) + 1

    def falling_edges(self, bit):
        state = self.channel(bit).astype(np.int8)
        return np.flatnonzero(np.diff(state) == -1) + 1

    def time_slice(self, t_start, t_end):
        """(times, camera_state, led_state) for samples within [t_start, t_end)
        seconds -- for plotting a limited on-screen window without touching
        the rest of the file. Assumes the same t=0 origin as the paired ephys
        recording (both start recording on the same clock; there's no
        separate offset stored anywhere for this format)."""
        s0 = max(0, int(t_start * self.sample_rate))
        s1 = min(self.n_samples, int(t_end * self.sample_rate))
        if s1 <= s0:
            empty = np.array([])
            return empty, empty, empty
        sl = slice(s0, s1)
        times = np.arange(s0, s1) / self.sample_rate
        return times, self.channel(CAMERA_BIT, sl), self.channel(LED_BIT, sl)
