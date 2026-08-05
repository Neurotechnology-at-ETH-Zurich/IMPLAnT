# This Python file uses the following encoding: utf-8
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QRectF

# kcsd's __init__ pulls in ValidateKCSD, which still does
# `from scipy.integrate import simps` — dropped in scipy 1.14. Put the name back
# before importing, so the released kcsd works unpatched.
import scipy.integrate
if not hasattr(scipy.integrate, 'simps'):
    scipy.integrate.simps = scipy.integrate.simpson
from kcsd import KCSD1D

from ephys_utils.spiking_ruster import TimeAxisItem


class CSDWidget(QWidget):
    """kCSD sink/source map over the same time window as widget_pgEphys, with the
    LFP traces of every channel drawn on top of it.

    X axis = time (s), Y axis = depth along the probe, ticked with the channel
    that sits at each depth. The colour is the kCSD1D estimate on a fine depth
    grid, so sinks and sources show up as continuous blobs spanning several
    channels rather than one row per electrode: blue = sink, red = source.

    The channel highlighted in the ephys plot is drawn white and thicker here,
    so the same channel is easy to follow across both plots.
    """

    BIT_TO_UV = 0.195
    DEFAULT_SPACING_MM = 0.05    # 50 µm fallback when atlas coords are absent
    GDENSITY = 200               # lower bound on the number of depth estimation points
    MAX_COLUMNS = 4000           # time-column budget, keeps long windows responsive
    TRACE_SPAN = 1.8             # LFP trace height, in multiples of electrode spacing

    # --- colour limits -------------------------------------------------
    # percentile of |CSD| mapped to full colour, then widened by CLIM_GAIN.
    # Raise either one if the map still saturates into flat red/blue patches;
    # lower them to bring out weak sinks and sources.
    CLIM_PCT = 99.5
    CLIM_GAIN = 1.5

    # --- kCSD spatial smoothness ---------------------------------------
    # How densely basis sources are placed, and the depth padding (ext_x) that
    # lets them reach past the end electrodes so the map isn't squeezed to zero
    # at top and bottom. R_SPACINGS sets that padding, in electrode spacings.
    R_SPACINGS = 3.0
    N_SRC_PER_CHANNEL = 8

    # --- regularisation: cross-validated, then cached ------------------
    # The basis width R and ridge λ are chosen by kCSD's leave-one-electrode-out
    # cross validation rather than fixed constants — that is what stops the map
    # breaking into one-channel-wide (slim) sinks and sources. CV runs once per
    # electrode geometry and the result is reused while scrolling, since
    # re-solving the whole grid on every window would stall the GUI.
    #   CV_R_SPACINGS      = basis widths searched, in electrode spacings
    #   CV_LAMBDA_LOGSPACE = np.logspace(*this) * mean(diag(k_pot)); the diagonal
    #                        scaling puts the grid at the kernel's own magnitude
    CV_R_SPACINGS = (1.5, 2.0, 3.0, 4.0, 6.0)
    CV_LAMBDA_LOGSPACE = (-3.0, 1.0, 16)

    TRACE_PEN = ('k', 1)         # (colour, width) of a normal LFP trace
    HIGHLIGHT_PEN = ('k', 3)     # ... and of the selected one

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timeline = None
        self._trace_items = []   # overlaid LFP curves, rebuilt on every update
        self._trace_channels = []  # channel ID of each entry in _trace_items
        self._highlight_channel = None
        self._pending = None     # update_view args deferred while this tab is hidden

        # cross-validated (R, λ) cached per electrode geometry; see update_view
        self._cv_key = None
        self._cv_R = None
        self._cv_lambd = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget(
            background='k',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')},
        )
        self.plot = self.plot_widget.getPlotItem()
        self.plot.setLabel('left', 'Channel')
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.hideButtons()
        vb = self.plot.getViewBox()
        vb.setMenuEnabled(False)
        vb.invertY(True)   # shallowest channel on top, like the ephys plot
        layout.addWidget(self.plot_widget)

        self.img = pg.ImageItem()
        self.img.setOpts(axisOrder='row-major')   # image[depth, time]
        self.plot.addItem(self.img)

        self.colorbar = pg.ColorBarItem(
            values=(-1, 1),
            colorMap=self._colormap(),
            label='sink  <—  CSD (norm.)  —>  source',
            interactive=False,
            pen='w',
        )
        self.colorbar.setImageItem(self.img, insert_in=self.plot)

    # ------------------------------------------------------------------
    # Channel highlight (mirrors the ephys plot, same as SpikeRuster)
    # ------------------------------------------------------------------

    def set_highlight(self, channel):
        """Draw the trace of `channel` white and thicker, the rest plain.
        Pass None to clear the highlight."""
        self._highlight_channel = channel

        for curve, ch in zip(self._trace_items, self._trace_channels):
            selected = channel is not None and int(ch) == int(channel)
            colour, width = self.HIGHLIGHT_PEN if selected else self.TRACE_PEN
            curve.setPen(pg.mkPen(colour, width=width))
            # keep the selected trace above its neighbours, so it stays readable
            # where the traces overlap
            curve.setZValue(11 if selected else 10)

    # ------------------------------------------------------------------
    # Time cursor (same pattern as LFPSpectrogram / SpikeRuster)
    # ------------------------------------------------------------------

    def set_timeline(self, x):
        if self._timeline is None:
            self._timeline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
            self.plot.addItem(self._timeline)
        self._timeline.setPos(x)
        self._timeline.setVisible(True)

    def clear_timeline(self):
        if self._timeline is not None:
            self._timeline.setVisible(False)

    # ------------------------------------------------------------------
    # Main update  (called from VisualisationEphys.update_csd)
    # ------------------------------------------------------------------

    def showEvent(self, event):
        """Render the window that was requested while this tab was hidden."""
        super().showEvent(event)
        if self._pending is not None:
            args, kwargs = self._pending
            self._pending = None
            self.update_view(*args, **kwargs)

    def update_view(self, lfp_memmap, lfp_sample_rate, t_start, t_end,
                    active_channels, ele_pos_1d=None, force=False):
        """Recompute the kCSD from the LFP and redraw it as channel over time.

        Parameters
        ----------
        lfp_memmap : (n_channels, n_samples) int16 memmap
        lfp_sample_rate : int
        t_start, t_end : float  seconds
        active_channels : list[int]  channel IDs to include
        ele_pos_1d : (n_active, 1) float array in mm, or None for uniform spacing
        force : bypasses the hidden-tab defer below -- used once right after a
            file/tag loads, to prewarm this tab before it's first clicked.
        """
        # The kCSD solve runs on every scroll step; skip it while another tab of
        # tabWidget_LFP is in front and remember the request instead (like
        # AllChannelsSpectrogram), rendered when this tab is shown (showEvent above).
        if not force and not self.isVisible():
            self._pending = ((lfp_memmap, lfp_sample_rate, t_start, t_end, active_channels),
                              {'ele_pos_1d': ele_pos_1d})
            return
        self._pending = None

        if lfp_memmap is None or len(active_channels) < 2 or t_end <= t_start:
            self._clear()
            return

        fs = float(lfp_sample_rate)
        n_samples = lfp_memmap.shape[1]
        s0 = max(0, int(t_start * fs))
        s1 = min(n_samples, int(t_end * fs))
        if s1 - s0 < 4:
            self._clear()
            return

        # keep the number of time columns bounded — kCSD solves every column,
        # and a long window would otherwise stall the GUI
        step = max(1, int(np.ceil((s1 - s0) / self.MAX_COLUMNS)))

        # LFP slice → µV, shape (n_active, n_time)
        pots = lfp_memmap[active_channels, s0:s1:step].astype(np.float32) * self.BIT_TO_UV
        pots = pots - pots.mean(axis=1, keepdims=True)

        channel_ids = np.asarray(active_channels)

        # 1D electrode positions in mm
        if ele_pos_1d is None or np.asarray(ele_pos_1d).shape[0] != len(active_channels):
            ele_pos_1d = (np.arange(len(active_channels)) * self.DEFAULT_SPACING_MM
                          ).reshape(-1, 1)
        else:
            ele_pos_1d = np.asarray(ele_pos_1d, dtype=float).reshape(-1, 1)

        # ensure strictly increasing depth (sort, then drop exact duplicates).
        # channel_ids follows along so every image row keeps its channel label
        order = np.argsort(ele_pos_1d[:, 0])
        ele_pos_1d = ele_pos_1d[order]
        pots = pots[order]
        channel_ids = channel_ids[order]

        _, unique_idx = np.unique(ele_pos_1d[:, 0], return_index=True)
        if len(unique_idx) < len(ele_pos_1d):
            ele_pos_1d = ele_pos_1d[unique_idx]
            pots = pots[unique_idx]
            channel_ids = channel_ids[unique_idx]

        if len(ele_pos_1d) < 2:
            self._clear()
            return

        try:
            span = float(ele_pos_1d[-1, 0] - ele_pos_1d[0, 0])
            spacing = span / max(len(ele_pos_1d) - 1, 1)
            # fine enough that no two electrodes fall on the same grid point
            gdx = max(span / max(self.GDENSITY, 4 * len(ele_pos_1d)), 1e-4)

            # depth padding for the basis sources (mm), so they reach past the
            # end electrodes instead of the map being squeezed to zero there;
            # also the starting basis width before CV refines it
            ext = max(self.R_SPACINGS * spacing, gdx)
            # many more basis sources than electrodes: the CSD becomes a smooth
            # field sampled by the electrodes, not one bump per electrode
            n_src = max(self.N_SRC_PER_CHANNEL * len(ele_pos_1d), 100)

            # CV depends only on the probe geometry here, so run it once per
            # channel layout and reuse the (R, λ) it found on every later scroll
            cv_key = (tuple(int(c) for c in channel_ids),
                      tuple(np.round(ele_pos_1d[:, 0], 6).tolist()))

            if cv_key == self._cv_key and self._cv_R is not None:
                k = KCSD1D(ele_pos_1d, pots, gdx=gdx, R_init=self._cv_R,
                           n_src_init=n_src, ext_x=ext)
                k.lambd = self._cv_lambd   # absolute λ, reused as-is
            else:
                k = KCSD1D(ele_pos_1d, pots, gdx=gdx, R_init=ext,
                           n_src_init=n_src, ext_x=ext)
                # λ grid at the kernel's own magnitude; CV scores each (R, λ) by
                # leave-one-electrode-out prediction error and applies the best
                scale = float(np.mean(np.diag(k.k_pot)))
                Rs = spacing * np.asarray(self.CV_R_SPACINGS, dtype=float)
                lambdas = scale * np.logspace(*self.CV_LAMBDA_LOGSPACE)
                cv_R, cv_lambd = k.cross_validate(lambdas=lambdas, Rs=Rs)
                # cross_validate already set the solver to (cv_R, cv_lambd)
                self._cv_key = cv_key
                self._cv_R = float(cv_R)
                self._cv_lambd = float(cv_lambd)

            csd = k.values()   # (n_depth_pts, n_time)
            depth_axis = np.asarray(k.estm_x).ravel()
        except Exception:
            import traceback
            traceback.print_exc()
            self._clear()
            return

        times = np.linspace(t_start, t_end, csd.shape[1])
        n_ch = len(ele_pos_1d)

        # symmetric colour limits, so the diverging colours mean what they look
        # like. A high percentile (not the max) keeps a single noisy sample from
        # washing the whole map out to green.
        v = self.CLIM_GAIN * float(np.percentile(np.abs(csd), self.CLIM_PCT))
        if v < 1e-12:
            self._clear()
            return

        csd_norm = np.clip(csd / v, -1.0, 1.0)

        dt = times[1] - times[0] if len(times) > 1 else (t_end - t_start)
        dd = depth_axis[1] - depth_axis[0] if len(depth_axis) > 1 else gdx
        x0 = times[0] - dt / 2.0
        y0 = depth_axis[0] - dd / 2.0

        self.img.setImage(csd_norm, autoLevels=False, levels=(-1.0, 1.0))
        self.img.setRect(QRectF(
            x0, y0,
            times[-1] - times[0] + dt,
            depth_axis[-1] - depth_axis[0] + dd,
        ))
        self.colorbar.setLevels((-1, 1))

        # LFP traces on top, each at its own depth. One shared scale factor, so
        # the relative amplitudes between channels stay readable.
        peak = float(np.abs(pots).max())
        scale = (self.TRACE_SPAN * spacing / peak) if peak > 1e-12 else 0.0
        # minus, because the depth axis is inverted: a positive potential should
        # still deflect upwards on screen
        trace_y = ele_pos_1d[:, [0]] - pots * scale      # (n_ch, n_time)
        self._clear_traces()
        colour, width = self.TRACE_PEN
        for i in range(n_ch):
            curve = pg.PlotDataItem(times, trace_y[i],
                                    pen=pg.mkPen(colour, width=width))
            curve.setZValue(10)
            self.plot.addItem(curve)
            self._trace_items.append(curve)
            self._trace_channels.append(int(channel_ids[i]))

        # the traces are new objects, so the highlight has to be painted again
        self.set_highlight(self._highlight_channel)

        # channel ids at the depth each electrode sits at
        self.plot.getAxis('left').setTicks(
            [[(float(ele_pos_1d[i, 0]), str(ch)) for i, ch in enumerate(channel_ids)]])

        vb = self.plot.getViewBox()
        vb.disableAutoRange()
        vb.setLimits(xMin=t_start, xMax=t_end)
        self.plot.setXRange(t_start, t_end, padding=0)
        # the CSD image fills the electrode span; let the edge channels' traces
        # spill just past it so their full waveform shows instead of being
        # clipped at the panel edge. Windows where nothing overshoots the span
        # keep the tight range, since min()/max() then land on the electrodes.
        y_top = min(float(depth_axis[0]), float(trace_y.min()))
        y_bot = max(float(depth_axis[-1]), float(trace_y.max()))
        self.plot.setYRange(y_top, y_bot, padding=0)
        self.plot.setTitle(
            f'kCSD — {n_ch} channels, {1000 * spacing:.0f} µm apart',
            color='w', size='8pt')

    # ------------------------------------------------------------------
    # Whole-recording export (same pipeline as update_view, no time cap)
    # ------------------------------------------------------------------

    def export_csd(self, lfp_memmap, lfp_sample_rate, active_channels, ele_pos_1d,
                   out_path, t_start=0.0, chunk_seconds=1.0, progress=None):
        """Solve the kCSD over the WHOLE recording at the LFP sample rate — same
        depth grid, electrode geometry and cross-validated (R, λ) as the on-screen
        map, just without the MAX_COLUMNS decimation — and stream it to a raw
        float32 binary (`.bin`) with a JSON sidecar (`.json`) describing the axes.

        The recording is processed in independent windows of `chunk_seconds`
        (~1 s), each with its OWN per-channel mean removed before solving —
        exactly what the on-screen map does for the window it shows. That local
        detrending is what keeps the dynamic sinks/sources filling the colour
        scale; a single global mean would leave a large static per-depth offset
        in every window that shrinks them. CV also runs on one such window, so the
        smoothing (R, λ) matches the display instead of the flatter fit a long
        slice gives. Raw kCSD values are written (what the colours encode before
        the display clips them to ±percentile). Returns the sidecar dict.

        On disk the array is time-major (n_time, n_depth) — that is the order in
        which the streamed time-chunks land — so:
            csd = np.fromfile(path, '<f4').reshape(meta['shape'])   # (time, depth)
            csd = csd.T                                             # (depth, time), as shown
        """
        import os
        import json

        fs = float(lfp_sample_rate)
        n_samples = int(lfp_memmap.shape[1])

        # --- geometry: identical to update_view (sort by depth, drop dupes) ---
        channel_ids = np.asarray(active_channels)
        if ele_pos_1d is None or np.asarray(ele_pos_1d).shape[0] != len(active_channels):
            ele_pos_1d = (np.arange(len(active_channels)) * self.DEFAULT_SPACING_MM
                          ).reshape(-1, 1)
        else:
            ele_pos_1d = np.asarray(ele_pos_1d, dtype=float).reshape(-1, 1)

        order = np.argsort(ele_pos_1d[:, 0])
        ele_pos_1d = ele_pos_1d[order]
        channel_ids = channel_ids[order]
        _, unique_idx = np.unique(ele_pos_1d[:, 0], return_index=True)
        ele_pos_1d = ele_pos_1d[unique_idx]
        channel_ids = channel_ids[unique_idx]
        if len(ele_pos_1d) < 2:
            raise ValueError('CSD export needs at least 2 live channels')

        rows = [int(c) for c in channel_ids]   # memmap rows, in depth order
        span = float(ele_pos_1d[-1, 0] - ele_pos_1d[0, 0])
        spacing = span / max(len(ele_pos_1d) - 1, 1)
        gdx = max(span / max(self.GDENSITY, 4 * len(ele_pos_1d)), 1e-4)
        ext = max(self.R_SPACINGS * spacing, gdx)
        n_src = max(self.N_SRC_PER_CHANNEL * len(ele_pos_1d), 100)

        # each window gets its OWN per-channel mean removed, exactly like
        # update_view does for the window it shows — so no static per-depth offset
        # is left to hog the colour scale and shrink the dynamic sinks/sources
        def read_uv(a, b):
            p = lfp_memmap[rows, a:b].astype(np.float32) * self.BIT_TO_UV
            return p - p.mean(axis=1, keepdims=True)

        # --- (R, λ): reuse the displayed cache if the geometry matches, else CV
        # once on a representative slice (mirrors update_view's CV block) ---
        cv_key = (tuple(rows), tuple(np.round(ele_pos_1d[:, 0], 6).tolist()))
        chunk = max(1, int(round(chunk_seconds * fs)))
        if cv_key == self._cv_key and self._cv_R is not None:
            R_use, lambd_use = float(self._cv_R), float(self._cv_lambd)
        else:
            k0 = KCSD1D(ele_pos_1d, read_uv(0, min(n_samples, chunk)),
                        gdx=gdx, R_init=ext, n_src_init=n_src, ext_x=ext)
            scale = float(np.mean(np.diag(k0.k_pot)))
            Rs = spacing * np.asarray(self.CV_R_SPACINGS, dtype=float)
            lambdas = scale * np.logspace(*self.CV_LAMBDA_LOGSPACE)
            cv_R, cv_lambd = k0.cross_validate(lambdas=lambdas, Rs=Rs)
            R_use, lambd_use = float(cv_R), float(cv_lambd)
            self._cv_key, self._cv_R, self._cv_lambd = cv_key, R_use, lambd_use

        # --- build the solver once, then stream chunks through it ---
        k = KCSD1D(ele_pos_1d, read_uv(0, min(n_samples, chunk)),
                   gdx=gdx, R_init=R_use, n_src_init=n_src, ext_x=ext)
        k.lambd = lambd_use
        depth_axis = np.asarray(k.estm_x).ravel()
        n_depth = int(depth_axis.size)

        bin_path = os.path.splitext(out_path)[0] + '.bin'
        json_path = os.path.splitext(out_path)[0] + '.json'
        with open(bin_path, 'wb') as f:
            for a in range(0, n_samples, chunk):
                b = min(n_samples, a + chunk)
                pots = read_uv(a, b)
                k.pots = pots
                k.n_time = pots.shape[1]
                csd = k.values().astype(np.float32)      # (n_depth, b-a)
                # time-major on disk: streamed time-chunks concatenate into a
                # valid (n_time, n_depth) C-order array
                f.write(np.ascontiguousarray(csd.T).tobytes())
                if progress is not None:
                    progress(b / n_samples)

        meta = {
            'shape': [n_samples, n_depth],
            'dtype': 'float32', 'order': 'C',
            'axes': ['time', 'depth'],
            'lfp_sample_rate_hz': fs,
            't_start_s': float(t_start),
            'depth_mm': [float(x) for x in depth_axis],
            'channel_ids': [int(c) for c in channel_ids],
            'channel_depth_mm': [float(x) for x in ele_pos_1d[:, 0]],
            'spacing_mm': float(spacing), 'gdx_mm': float(gdx), 'ext_mm': float(ext),
            'n_src': int(n_src), 'R_mm': R_use, 'lambda': lambd_use,
            'bit_to_uv': self.BIT_TO_UV,
            'detrend_window_s': float(chunk_seconds),
            'units': ('kCSD1D estimate (arb.); potentials in µV, per-channel mean '
                      'removed independently within each detrend_window_s window'),
            'note': ('raw kCSD values; solved in independent windows of '
                     'detrend_window_s (each mean-removed), like the on-screen map. '
                     'The map is this clipped to ±(CLIM_GAIN·percentile). '
                     'time[i] = t_start_s + i / lfp_sample_rate_hz'),
            'bin_file': os.path.basename(bin_path),
        }
        with open(json_path, 'w') as f:
            json.dump(meta, f, indent=2)
        return meta

    # ------------------------------------------------------------------

    def _clear(self):
        self.img.clear()
        self._clear_traces()
        self.plot.getAxis('left').setTicks(None)   # back to automatic ticks
        self.plot.setTitle(None)

    def _clear_traces(self):
        for curve in self._trace_items:
            self.plot.removeItem(curve)
        self._trace_items = []
        self._trace_channels = []   # _highlight_channel is kept, see update_view

    @staticmethod
    def _colormap():
        # jet-like: sinks deep blue, sources deep red, and enough contrast in
        # between that a blob is visible before it saturates
        for name, source in (('jet', 'matplotlib'), ('turbo', 'matplotlib'), ('CET-R4', None)):
            try:
                cm = pg.colormap.get(name, source=source)
            except Exception:
                cm = None
            if cm is not None:
                return cm
        return pg.colormap.ColorMap(
            [0.0, 0.25, 0.5, 0.75, 1.0],
            [(0, 0, 143, 255), (0, 200, 255, 255), (120, 255, 120, 255),
             (255, 180, 0, 255), (143, 0, 0, 255)])
