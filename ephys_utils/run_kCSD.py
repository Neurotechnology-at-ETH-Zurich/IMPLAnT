# This Python file uses the following encoding: utf-8
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from kcsd import KCSD1D


class RunkCSD:
    """Thin wrapper around KCSD1D for use in the GUI.

    Usage
    -----
    runner = RunkCSD()
    csd, depth, times = runner.compute(lfp_memmap, lfp_sample_rate,
                                        t_start, t_end, active_channels,
                                        ele_pos_1d=None)
    """

    BIT_TO_UV = 0.195
    DEFAULT_SPACING_MM = 0.025
    N_DEPTH_POINTS = 50

    def compute(self, lfp_memmap, lfp_sample_rate, t_start, t_end,
                active_channels, ele_pos_1d=None):
        """Run kCSD1D and return arrays ready for display.

        Parameters
        ----------
        lfp_memmap : (n_channels, n_samples) int16 memmap
        lfp_sample_rate : int/float  Hz
        t_start, t_end : float  seconds
        active_channels : list[int]  row indices into lfp_memmap
        ele_pos_1d : (n_active, 1) float array in mm, or None

        Returns
        -------
        csd : (n_depth, n_time) float32
        depth_axis : (n_depth,) float  mm
        times : (n_time,) float  s
        None if computation cannot proceed.
        """
        if lfp_memmap is None or len(active_channels) < 2:
            return None

        fs = float(lfp_sample_rate)
        s0 = max(0, int(t_start * fs))
        s1 = min(lfp_memmap.shape[1], int(t_end * fs))
        if s1 - s0 < 4:
            return None

        pots = lfp_memmap[active_channels, s0:s1].astype(np.float32) * self.BIT_TO_UV
        pots = pots - pots.mean(axis=1, keepdims=True)

        n = len(active_channels)
        if ele_pos_1d is None or np.asarray(ele_pos_1d).shape[0] != n:
            ele_pos_1d = (np.arange(n) * self.DEFAULT_SPACING_MM).reshape(-1, 1)
        else:
            ele_pos_1d = np.asarray(ele_pos_1d, dtype=float).reshape(-1, 1)

        order = np.argsort(ele_pos_1d[:, 0])
        ele_pos_1d = ele_pos_1d[order]
        pots = pots[order]

        span = float(ele_pos_1d[-1, 0] - ele_pos_1d[0, 0])
        gdx = max(span / self.N_DEPTH_POINTS, 1e-4)

        k = KCSD1D(ele_pos_1d, pots, gdx=gdx, n_src_init=n * 2)
        csd = k.values().astype(np.float32)
        depth_axis = np.asarray(k.estm_x).ravel()
        times = np.linspace(t_start, t_end, csd.shape[1])

        return csd, depth_axis, times
