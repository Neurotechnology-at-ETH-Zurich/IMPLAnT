# This Python file uses the following encoding: utf-8
import numpy as np
import pyqtgraph as pg
import pywt
from scipy.signal import butter, filtfilt, hilbert
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QRectF, Qt, QThread, QObject, Signal, Slot

from gui_utils.busy_overlay import BusyOverlay


class AllChannelsSpectrogram(QWidget):
    """Wavelet spectrum of EVERY channel at one point in time: frequency on the
    x axis, probe depth (one row per channel) on the y axis, colour = wavelet
    power.

    Where LFPSpectrogram shows one channel over time, this shows one time over
    all channels — the depth profile of each rhythm, so the pyramidal layer
    (ripple band) and the sharp-wave sink separate visibly along the probe.

    The time point is the middle of the window currently shown in the ephys plot,
    and the whole visible window is the interval averaged over (capped at
    MAX_INTERVAL_S so a very long window can't stall the GUI). This is the plot
    from Peter's Wavlet_All_Channels_Plot.mlx: mean wavelet power over the
    interval, plus the sharp-wave and ripple depth profiles on top.

    pushButton_Timeframe_spectogram flips this to the MATLAB script's other
    mode (CWT_TOTAL): instead of the current window, average over every
    detected ripple in the whole recording, each contributing its own
    ±RIPPLE_HALF_WINDOW_S around its true peak — the sample of maximum
    ripple-band envelope within the event, the same as the MATLAB's
    ripples.peaks — rather than just the (start+end)/2 midpoint. A
    session-wide ripple-triggered map instead of a single-window one. Averaging
    over every ripple can take minutes on a session with many events, so it
    runs on a background QThread (_RippleSpecWorker below) with a BusyOverlay
    over this tab while it computes -- the rest of the GUI stays responsive.
    Cached by (ripple_events identity, channels, log_freq), so this only runs
    again when one of those actually changes, not on every scroll.

    Each channel's raw mean wavelet power is flattened against its own FOOOF
    aperiodic (1/f) fit, exactly like LFPSpectrogram: 0 dB = that channel's
    fitted background, so a channel with more overall power doesn't read as
    having more oscillatory power than a quieter one. The colour scale is
    adaptive (percentile-clipped, symmetric around 0 dB), not a fixed range.
    """

    # Emitted True while the ripple-triggered average runs on its background
    # thread, False once it's done (or failed) -- init_ephys uses this to block
    # the buttons that would start an overlapping run.
    busyChanged = Signal(bool)

    # Same complex Morlet as LFPSpectrogram, so the two panels report the same
    # power for the same data (cmor<bandwidth>-<center>).
    BANDWIDTH = 2.0
    CENTER = 1.0

    # The image is placed with a single rect, so the analysed frequencies have
    # to be evenly spaced in whatever the x axis shows: evenly in Hz for the
    # linear axis (the MATLAB figure's 0-250 Hz span), evenly in log10(f) for
    # the log axis. pushButton_allChannels_axis toggles between the two.
    F_MIN = 1.0
    F_MAX = 250.0
    N_FREQS = 125            # ~2 Hz rows when linear; upsampled for display only

    EDGE_SIGMAS = 3.0        # read this many wavelet sigmas past both edges, so
                             # the cone of influence stays out of the interval
    BIT_TO_UV = 0.195        # same int16 -> uV scaling the ephys view uses

    # The CWT runs on every channel, so the cost scales with the interval. Long
    # windows are cropped to this many seconds around the centre time point.
    MAX_INTERVAL_S = 10.0

    # Ripple-triggered mode (pushButton_Timeframe_spectogram): half-span around
    # each ripple's centre, in seconds. 25 ms is the MATLAB script's window
    # (CWT_TOTAL averages samples 1000-50:1000+50 of a 2000 Hz recording).
    RIPPLE_HALF_WINDOW_S = 0.025

    # FOOOF aperiodic (1/f) fit used to flatten each channel's spectrum, same
    # settings as LFPSpectrogram (see its class docstring for why 'knee').
    FOOOF_APERIODIC = 'knee'
    FOOOF_MAX_PEAKS = 6
    N_FIT_FREQS = 512    # points of the even linear grid the fit is done on

    # Adaptive colour scale (dB, symmetric around 0 = each channel's own 1/f
    # background), same clipping as LFPSpectrogram: never tighter than
    # DB_CLIM_MIN so a quiet map doesn't get stretched into pure noise, never
    # wider than CLIM_DB so one outlier can't wash out the rest of the map.
    CLIM_DB = 20.0
    DB_CLIM_MIN = 3.0

    # Depth profiles drawn on top, with their own amplitude axis (top): the
    # sharp-wave band at a fixed frequency, and the ripple band at whichever
    # frequency inside RIPPLE_BAND carries the most power in this map — the same
    # choice the MATLAB makes when it looks for the pyramidal layer.
    SW_FREQ = 20.0
    RIPPLE_BAND = (120.0, 200.0)
    SW_PEN = ((190, 190, 190), 2)      # (colour, width) — grey, like the figure
    RIPPLE_PEN = ((0, 0, 0), 2)        # ... and black for the ripple profile
    # Amplitude range of the profile axis (top). Both profiles are min-max
    # normalised to 0-1, so this is just a little padding on each side to keep
    # the flat parts of a profile off the panel edge, as in the MATLAB figure.
    PROFILE_XRANGE = (-0.1, 1.1)

    # Display-only interpolation of the map (the MATLAB draws it with surf
    # 'FaceColor','interp'). ImageItem paints one rectangle per data point, so
    # without this the 32-64 channel rows read as coarse bands.
    DISPLAY_ROWS = 240
    DISPLAY_COLS = 400

    def __init__(self, parent=None):
        super().__init__(parent)
        self._highlight_channel = None
        self._rows = []          # channel id of each map row, top to bottom
        self._highlight_line = None
        self._pending = None     # update_view args deferred while hidden
        self._last_args = None   # last update_view args, replayed by the toggle
        self.log_freq = False     # frequency x-axis: True = log Hz (as Peter's
        #                          figure), False = linear Hz. Toggled by button.
        self.ripple_mode = False # False = entire visible window (default),
        #                          True = session-wide ripple-triggered average.
        #                          Toggled by pushButton_Timeframe_spectogram.
        # {log_freq: (spec, n_used)}, for the current _ripple_cache_base_key
        # (id(ripple_events), channels, ripple-detection channels -- everything
        # about a ripple-triggered run EXCEPT log_freq). Toggling the frequency
        # axis then reuses whichever of the two was already computed, instead
        # of rerunning the whole ripple average -- see _update_ripple_triggered.
        self._ripple_cache_base_key = None
        self._ripple_cache = {}
        self._title = ''                 # set by _window_spec / _ripple_triggered_spec

        # ripple-triggered mode averages over every detected ripple, which can
        # take minutes on a session with many events -- run on a QThread (see
        # _update_ripple_triggered / _RippleSpecWorker) so the rest of the GUI
        # stays responsive, with a BusyOverlay over this tab while it computes.
        self._ripple_thread = None
        self._ripple_worker = None
        self._busy_overlay = None
        # context for the in-flight worker's result, read back in
        # _on_ripple_worker_finished (see the comment in _update_ripple_triggered
        # on why this isn't just closed over in a lambda)
        self._ripple_pending_base_key = None
        self._ripple_pending_log_freq = None
        self._ripple_pending_freqs = None
        self._ripple_pending_channel_ids = None

        # window mode: {log_freq: (spec, freqs, channel_ids, title)}, for the
        # current _window_cache_base_key (everything update_view is called with
        # EXCEPT log_freq). Toggling the frequency axis without anything else
        # changing then reuses whichever of the two was already computed,
        # instead of rerunning the CWT -- see set_log_frequency.
        self._window_cache_base_key = None
        self._window_cache = {}

        self.wavelet = f"cmor{self.BANDWIDTH}-{self.CENTER}"
        # central frequency of the mother wavelet, needed to turn frequencies
        # into the wavelet's temporal width for the edge padding
        self._central = pywt.central_frequency(self.wavelet)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget(background='k')
        self.plot = self.plot_widget.getPlotItem()
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.plot.getAxis('bottom').enableAutoSIPrefix(False)
        self.plot.setLabel('left', 'Channel')
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.hideButtons()
        vb = self.plot.getViewBox()
        vb.setMenuEnabled(False)
        vb.invertY(True)   # shallowest channel on top, like the ephys plot
        layout.addWidget(self.plot_widget)

        self.img = pg.ImageItem()
        self.img.setOpts(axisOrder='row-major')   # image[channel, frequency]
        self.plot.addItem(self.img)

        self.colorbar = pg.ColorBarItem(
            values=(-1, 1), colorMap=self._colormap(),
            label='Power over 1/f  (dB)', interactive=False, pen='w',
        )
        self.colorbar.setImageItem(self.img, insert_in=self.plot)

        # The two depth profiles are amplitudes, not frequencies, so they get
        # their own x axis on top: a second ViewBox sharing this one's y axis
        # (same channel rows) with an independent x range.
        self.profile_vb = pg.ViewBox()
        self.profile_vb.setMouseEnabled(x=False, y=False)
        self.profile_vb.setMenuEnabled(False)
        # a ViewBox sits at z = -100, so as a sibling of the PlotItem it would be
        # painted under the map. Lift it: it draws nothing but the two curves,
        # and it is clipped to the plot area, so nothing else is covered.
        self.profile_vb.setZValue(10)
        self.plot.scene().addItem(self.profile_vb)
        self.plot.showAxis('top')
        top_axis = self.plot.getAxis('top')
        top_axis.linkToView(self.profile_vb)
        top_axis.setLabel('Amplitude (a.u.)')
        # the y range is shared, but the inversion is per ViewBox: without this
        # the profiles would run bottom-up while the map runs top-down
        self.profile_vb.invertY(True)
        self.profile_vb.setYLink(vb)
        self.profile_vb.setXRange(*self.PROFILE_XRANGE, padding=0)
        vb.sigResized.connect(self._sync_profile_vb)
        self._sync_profile_vb()

        colour, width = self.SW_PEN
        self.sw_curve = pg.PlotDataItem(pen=pg.mkPen(colour, width=width))
        colour, width = self.RIPPLE_PEN
        self.ripple_curve = pg.PlotDataItem(pen=pg.mkPen(colour, width=width))
        for curve in (self.sw_curve, self.ripple_curve):
            curve.setZValue(10)
            self.profile_vb.addItem(curve)

        self.legend = pg.LegendItem(offset=(-10, 10), labelTextColor='k',
                                    brush=pg.mkBrush(255, 255, 255, 200),
                                    pen=pg.mkPen('k'))
        # in the profile ViewBox, so the curves' legend is not painted over by it
        self.legend.setParentItem(self.profile_vb)
        self.legend.addItem(self.sw_curve, 'SW')
        self.legend.addItem(self.ripple_curve, 'R')

    # ------------------------------------------------------------------
    # Channel highlight (mirrors the ephys plot, same as CSDWidget)
    # ------------------------------------------------------------------

    def set_highlight(self, channel):
        """Mark the row of `channel` with a dashed line. None clears it."""
        self._highlight_channel = channel
        if self._highlight_line is None:
            self._highlight_line = pg.InfiniteLine(
                angle=0, movable=False,
                pen=pg.mkPen('w', width=2, style=Qt.DashLine))
            self._highlight_line.setZValue(20)
            self.plot.addItem(self._highlight_line)

        row = self._rows.index(int(channel)) if (
            channel is not None and int(channel) in self._rows) else None
        if row is None:
            self._highlight_line.setVisible(False)
        else:
            self._highlight_line.setPos(row)
            self._highlight_line.setVisible(True)

    # ------------------------------------------------------------------
    # Frequency axis: linear <-> log (pushButton_allChannels_axis)
    # ------------------------------------------------------------------

    def set_log_frequency(self, enabled):
        """Switch the frequency (x) axis between log and linear Hz.

        Like LFPSpectrogram, this moves the analysed frequencies too, not just
        the axis: the image is placed with a single rect, so the rows have to be
        evenly spaced in whatever the axis shows. Log spaces them evenly in
        log10(f), which (like Peter's figure) gives theta and the ripple band
        comparable room; linear spends most rows above 30 Hz. Re-renders the
        current window."""
        enabled = bool(enabled)
        if enabled == self.log_freq:
            return
        self.log_freq = enabled
        if self._last_args is not None:
            self.update_view(*self._last_args)

    def toggle_log_frequency(self):
        """Flip the frequency axis; returns the new state (True = log)."""
        self.set_log_frequency(not self.log_freq)
        return self.log_freq

    # ------------------------------------------------------------------
    # Timeframe: entire window <-> ripple-triggered
    # (pushButton_Timeframe_spectogram)
    # ------------------------------------------------------------------

    def set_ripple_mode(self, enabled):
        """Switch between the entire-visible-window map and the session-wide
        ripple-triggered average (MATLAB's CWT_TOTAL). Re-renders from the
        last known update_view args, same as set_log_frequency."""
        enabled = bool(enabled)
        if enabled == self.ripple_mode:
            return
        self.ripple_mode = enabled
        if self._last_args is not None:
            self.update_view(*self._last_args)

    def toggle_ripple_mode(self):
        """Flip the timeframe mode; returns the new state (True = ripple-triggered)."""
        self.set_ripple_mode(not self.ripple_mode)
        return self.ripple_mode

    # ------------------------------------------------------------------
    # Main update  (called from VisualisationEphys.update_channel_spectrogram)
    # ------------------------------------------------------------------

    def showEvent(self, event):
        """Render the window that was requested while this tab was hidden."""
        super().showEvent(event)
        if self._pending is not None:
            args, kwargs = self._pending
            self._pending = None
            self.update_view(*args, **kwargs)

    def update_view(self, lfp_memmap, lfp_sample_rate, t_start, t_end,
                    active_channels, ele_pos_1d=None, ripple_events=None,
                    ripple_channels=None, force=False):
        """Recompute the frequency x channel map.

        Parameters
        ----------
        lfp_memmap : (n_channels, n_samples) int16 memmap
        lfp_sample_rate : int
        t_start, t_end : float  seconds — the window shown in the ephys plot.
            Ignored in ripple mode (the average spans the whole recording).
        active_channels : list[int]  channel IDs to include
        ele_pos_1d : (n_active, 1) float array in mm, or None. Only used to sort
            the rows by depth; the rows themselves are drawn evenly spaced and
            labelled with their channel id.
        ripple_events : (n_events, 2) float array of ripple (start, end) times
            in seconds, or None. Only used in ripple mode (self.ripple_mode).
        ripple_channels : list[int] or None. The channels rippl-AI detection was
            run on; used to find each ripple's true peak (max ripple-band
            envelope) instead of just its (start+end)/2 midpoint. Only used in
            ripple mode; falls back to the midpoint if None.
        force : bypasses the hidden-tab defer below -- used once right after a
            file/tag loads, to prewarm this tab before it's first clicked.
        """
        # The CWT runs on every channel, which is most of a second on a 64-channel
        # probe — too much to spend on every scroll step while another tab of
        # tabWidget_LFP is in front. Remember the request instead and render it
        # when this tab is shown (showEvent above).
        # remember the request so the axis/timeframe toggles can re-render this
        self._last_args = (lfp_memmap, lfp_sample_rate, t_start, t_end,
                           active_channels, ele_pos_1d, ripple_events,
                           ripple_channels)

        if not force and not self.isVisible():
            self._pending = ((lfp_memmap, lfp_sample_rate, t_start, t_end,
                              active_channels), {'ele_pos_1d': ele_pos_1d,
                                                  'ripple_events': ripple_events,
                                                  'ripple_channels': ripple_channels})
            return
        self._pending = None

        if lfp_memmap is None or len(active_channels) < 2 or t_end <= t_start:
            self._clear()
            return

        fs = float(lfp_sample_rate)
        fmax = min(self.F_MAX, fs / 2.0 * 0.99)
        if fmax <= self.F_MIN:
            self._clear()
            return

        # rows in depth order, so row 0 is the shallowest contact
        channel_ids = np.asarray(active_channels, dtype=int)
        if ele_pos_1d is not None and np.asarray(ele_pos_1d).shape[0] == len(channel_ids):
            depths = np.asarray(ele_pos_1d, dtype=float).ravel()
            channel_ids = channel_ids[np.argsort(depths)]

        if self.log_freq:
            freqs = np.logspace(np.log10(self.F_MIN), np.log10(fmax),
                                self.N_FREQS)
        else:
            freqs = np.linspace(self.F_MIN, fmax, self.N_FREQS)

        if self.ripple_mode:
            self._update_ripple_triggered(lfp_memmap, fs, freqs, channel_ids,
                                           ripple_events, ripple_channels)
            return

        # cache keyed on log_freq, for everything else about this call -- an
        # axis toggle alone (t_start/t_end/channels unchanged) hits this and
        # skips the CWT entirely; any real change (scroll, channel skip, ...)
        # invalidates both entries and both get recomputed on next use
        base_key = (id(lfp_memmap), t_start, t_end, tuple(int(c) for c in channel_ids))
        if base_key != self._window_cache_base_key:
            self._window_cache_base_key = base_key
            self._window_cache = {}

        cached = self._window_cache.get(self.log_freq)
        if cached is not None:
            cached_spec, cached_freqs, cached_channel_ids, cached_title = cached
            self._title = cached_title
            self._finish_update_view(cached_spec, cached_freqs, cached_channel_ids)
            return

        spec = self._window_spec(lfp_memmap, fs, freqs, channel_ids,
                                  t_start, t_end)
        if spec is None:
            self._clear()
            return
        self._window_cache[self.log_freq] = (spec, freqs, channel_ids, self._title)
        self._finish_update_view(spec, freqs, channel_ids)

    def _finish_update_view(self, spec, freqs, channel_ids):
        """Render `spec` (n_channels, n_freqs raw power): FOOOF-flatten it,
        pick the colour scale, draw the image, depth profiles and axes.

        Shared tail of update_view for the window path (synchronous) and the
        ripple-triggered path (synchronous on a cache hit, or from the
        _RippleSpecWorker "finished" callback otherwise)."""
        # flatten each channel's raw power against its own FOOOF 1/f fit, then
        # scale the colour bar adaptively to whatever dB range this map holds
        flat_db = self._fooof_flatten(freqs, spec)
        finite = flat_db[np.isfinite(flat_db)]
        if finite.size == 0:
            self._clear()
            return
        v = float(np.percentile(np.abs(finite), 99.9))
        v = float(np.clip(v, self.DB_CLIM_MIN, self.CLIM_DB))
        # ripple-triggered mode floors the colour scale at 0 dB (each channel's
        # own 1/f background) -- below-background dips aren't the point of that
        # map. The entire-window mode keeps the symmetric +-v range.
        lo = 0.0 if self.ripple_mode else -v

        self._rows = [int(c) for c in channel_ids]
        n_ch = len(self._rows)

        # column coordinate of the image: Hz on the linear axis, log10(Hz) on the
        # log one. freqs is evenly spaced in that coordinate either way (lin- /
        # logspace above), so the single rect maps the columns correctly.
        x = np.log10(freqs) if self.log_freq else freqs

        # display-only interpolation between channels and frequencies; the grid
        # keeps the same endpoints, so the rect below still spans the data
        disp = self._resample(flat_db, min(self.DISPLAY_ROWS, 8 * n_ch), axis=0)
        disp = self._resample(disp, self.DISPLAY_COLS, axis=1)
        dy = (n_ch - 1) / max(disp.shape[0] - 1, 1)
        dx = (x[-1] - x[0]) / max(disp.shape[1] - 1, 1)

        self.img.setImage(disp, autoLevels=False, levels=(lo, v))
        self.img.setRect(QRectF(x[0] - dx / 2.0, -dy / 2.0,
                                x[-1] - x[0] + dx, (n_ch - 1) + dy))
        self.colorbar.setLevels((lo, v))

        # plain-Hz tick labels on the log axis (10, 20, 30 …, not 10^1); the
        # linear axis keeps pyqtgraph's automatic Hz ticks
        self.plot.getAxis('bottom').setTicks(
            self._log_ticks(freqs[0], freqs[-1]) if self.log_freq else None)

        self._draw_profiles(flat_db, freqs)

        # channel id of every row, and the highlight back onto its new row
        self.plot.getAxis('left').setTicks(
            [[(float(i), str(ch)) for i, ch in enumerate(self._rows)]])
        self.set_highlight(self._highlight_channel)

        vb = self.plot.getViewBox()
        vb.disableAutoRange()
        self.plot.setXRange(x[0], x[-1], padding=0)
        self.plot.setYRange(-0.5, n_ch - 0.5, padding=0)
        self._sync_profile_vb()

        self.plot.setTitle(
            f'{self._title} — {n_ch} channels — {self.wavelet}',
            color='w', size='8pt')

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sigma_t(self, f):
        """Temporal std (seconds) of the Morlet envelope at frequency f, same as
        LFPSpectrogram: sqrt(bandwidth/2) * central_freq / f."""
        return np.sqrt(self.BANDWIDTH / 2.0) * self._central / f

    def _mean_power(self, traces, fs, freqs, i0, i1):
        """Mean raw wavelet power over samples [i0:i1] of `traces`.

        Returns (n_channels, n_freqs), or None if the transform produced nothing.
        Raw, not whitened: the 1/f background is removed per channel afterwards
        by _fooof_flatten instead of the crude ``* freq`` the MATLAB uses.

        The CWT runs on all channels at once but in chunks of frequencies: the
        full coefficient array would be n_freqs x n_channels x n_samples complex,
        which is gigabytes for a 64-channel probe, while a chunk of it is tens of
        megabytes and just as fast.
        """
        scales = pywt.frequency2scale(self.wavelet, freqs / fs)
        out = np.empty((traces.shape[0], len(freqs)), dtype=np.float64)
        # ~64 MB per chunk of complex128 coefficients
        chunk = max(1, int(64e6 / max(traces.size * 16, 1)))
        for a in range(0, len(freqs), chunk):
            b = min(len(freqs), a + chunk)
            coef, _ = pywt.cwt(traces, scales[a:b], self.wavelet,
                               sampling_period=1.0 / fs, method='fft', axis=-1)
            if coef.shape[-1] == 0:
                return None
            power = coef.real ** 2 + coef.imag ** 2      # (n_chunk, n_ch, n_t)
            # crop the padding, average over the interval
            out[:, a:b] = power[:, :, i0:i1].mean(axis=2).T
        return out

    def _fooof_flatten(self, freqs, spec):
        """Per-channel dB power over its own FOOOF aperiodic (1/f) fit.

        Exactly LFPSpectrogram._aperiodic_baseline, run once per row here
        because each row is a different channel's spectrum rather than the
        same channel at different times. 0 dB = that channel's fitted
        background. Falls back to flat 0 dB for a channel whose fit fails
        (e.g. a silent/dead channel), same as LFPSpectrogram's fallback.
        """
        from ephys_utils.lfp_spectrogram import _load_fooof
        try:
            FOOOF, gen_aperiodic = _load_fooof()
        except Exception:
            FOOOF = None

        n_fit = max(len(freqs), self.N_FIT_FREQS)
        lin_f = np.linspace(float(freqs[0]), float(freqs[-1]), n_fit)
        log_freqs = np.log10(freqs)
        log_lin_f = np.log10(lin_f)

        flat_db = np.zeros_like(spec)
        for ch in range(spec.shape[0]):
            psd = np.maximum(spec[ch], 1e-20)
            baseline = None
            if FOOOF is not None:
                try:
                    lin_psd = np.power(10.0, np.interp(
                        log_lin_f, log_freqs, np.log10(psd)))
                    fm = FOOOF(aperiodic_mode=self.FOOOF_APERIODIC,
                               max_n_peaks=self.FOOOF_MAX_PEAKS, verbose=False)
                    fm.fit(lin_f, lin_psd,
                           freq_range=(float(lin_f[0]), float(lin_f[-1])))
                    ap_log10 = gen_aperiodic(freqs.astype(float),
                                              fm.aperiodic_params_)
                    baseline = np.power(10.0, ap_log10)
                except Exception:
                    baseline = None
            if baseline is None:
                baseline = psd
            flat_db[ch] = 10.0 * np.log10(psd / np.maximum(baseline, 1e-20))
        return flat_db

    def _window_spec(self, lfp_memmap, fs, freqs, channel_ids, t_start, t_end):
        """Mean raw power over the visible ephys window (default mode).

        The time point is the middle of the window, with the whole window as
        the averaging interval (cropped around that point if it is very long).
        Returns (n_channels, n_freqs), or None if the window is unusable. Sets
        self._title.
        """
        t_mid = 0.5 * (t_start + t_end)
        half = min(0.5 * (t_end - t_start), 0.5 * self.MAX_INTERVAL_S)
        a0, a1 = t_mid - half, t_mid + half

        n_samples = lfp_memmap.shape[1]
        s0 = max(0, int(a0 * fs))
        s1 = min(n_samples, int(a1 * fs))
        if s1 - s0 < 32:
            return None

        # The lowest frequency has the widest wavelet, so it sets how far past
        # each edge we read. Cropped off again below, so the cone of influence
        # never reaches the averaged interval.
        pad = int(np.ceil(self.EDGE_SIGMAS * self._sigma_t(self.F_MIN) * fs))
        p0 = max(0, s0 - pad)
        p1 = min(n_samples, s1 + pad)

        traces = lfp_memmap[channel_ids, p0:p1].astype(np.float32) * self.BIT_TO_UV
        traces = traces - traces.mean(axis=1, keepdims=True)

        spec = self._mean_power(traces, fs, freqs, s0 - p0, s1 - p0)
        if spec is None:
            return None

        cropped = '' if half >= 0.5 * (t_end - t_start) else ' (window cropped)'
        self._title = f't = {t_mid:.3f} s ± {1000 * half:.0f} ms{cropped}'
        return spec

    def _ripple_peak_times(self, lfp_memmap, fs, ripple_events, ripple_channels):
        """Peak time of every ripple event: the sample of maximum ripple-band
        envelope within its (start, end), averaged over the detection channels
        — the MATLAB script's ripples.peaks (bandpass -> abs(hilbert) ->
        per-event argmax), rather than the (start+end)/2 midpoint.

        Falls back to the midpoint (per event) when there are no detection
        channels, or when that event is too short to filter.
        """
        centers = ripple_events.mean(axis=1)
        if not ripple_channels:
            return centers

        n_samples = lfp_memmap.shape[1]
        nyq = fs / 2.0
        low = max(self.RIPPLE_BAND[0] / nyq, 1e-6)
        high = min(self.RIPPLE_BAND[1] / nyq, 0.999)
        b, a = butter(4, [low, high], btype='band')

        peaks = centers.copy()
        for i, (t0, t1) in enumerate(ripple_events):
            s0 = max(0, int(t0 * fs))
            s1 = min(n_samples, int(t1 * fs))
            if s1 - s0 < 8:
                continue
            try:
                trace = lfp_memmap[ripple_channels, s0:s1].astype(np.float64) * self.BIT_TO_UV
                trace = trace - trace.mean(axis=1, keepdims=True)
                filtered = filtfilt(b, a, trace, axis=1)
                envelope = np.abs(hilbert(filtered, axis=1)).mean(axis=0)
                peaks[i] = (s0 + int(np.argmax(envelope))) / fs
            except Exception:
                continue
        return peaks

    def _update_ripple_triggered(self, lfp_memmap, fs, freqs, channel_ids,
                                  ripple_events, ripple_channels):
        """ripple_mode branch of update_view. Renders immediately on a cache
        hit; otherwise kicks off the session-wide ripple-triggered average
        (Peter's CWT_TOTAL) on a background QThread, since it can take minutes
        on a session with many events, and shows a BusyOverlay over this tab
        meanwhile so the rest of the GUI stays usable.

        Cached by (ripple_events identity, channels, ripple-detection
        channels), with a separate slot per log_freq -- so toggling the
        frequency axis reuses whichever of the two was already computed
        instead of rerunning the average, and only a real change (new
        ripples, different channels) invalidates both.
        """
        if ripple_events is None or len(ripple_events) == 0:
            self._clear()
            return

        # id() of the caller's own array (self.events['ripple']), before any
        # conversion below creates a new object -- otherwise a non-float64
        # input would allocate a fresh array every call and the cache would
        # never hit.
        base_key = (id(ripple_events), tuple(int(c) for c in channel_ids),
                    tuple(int(c) for c in ripple_channels) if ripple_channels else None)
        if base_key != self._ripple_cache_base_key:
            self._ripple_cache_base_key = base_key
            self._ripple_cache = {}

        cached = self._ripple_cache.get(self.log_freq)
        if cached is not None:
            spec, n_used = cached
            self._title = (f'{n_used} ripples '
                            f'± {1000 * self.RIPPLE_HALF_WINDOW_S:.0f} ms')
            if spec is None:
                self._clear()
                return
            self._finish_update_view(spec, freqs, channel_ids)
            return

        if self._ripple_thread is not None:
            # a computation is already running -- it will render with whatever
            # args it started with; this request is dropped rather than queued
            return

        self._title = 'averaging every detected ripple…'
        self.plot.setTitle(self._title, color='w', size='8pt')

        if self._busy_overlay is None:
            self._busy_overlay = BusyOverlay(
                self, "Averaging every detected ripple, please wait…")
        self._busy_overlay.setGeometry(self.rect())
        self._busy_overlay.raise_()
        self._busy_overlay.show()
        self.busyChanged.emit(True)

        # stashed on self rather than closed over in a lambda: PySide can only
        # tell a signal/slot connection needs to be queued to the GUI thread
        # when the slot is a real bound method of a QObject it recognises --
        # connecting to a lambda instead silently falls back to a DIRECT
        # connection, so _on_ripple_worker_finished (and every pyqtgraph/Qt
        # call inside it) would run ON THE WORKER THREAD and crash.
        self._ripple_pending_base_key = base_key
        self._ripple_pending_log_freq = self.log_freq
        self._ripple_pending_freqs = freqs
        self._ripple_pending_channel_ids = channel_ids

        ripple_events = np.asarray(ripple_events, dtype=float)
        self._ripple_thread = QThread()
        self._ripple_worker = _RippleSpecWorker(
            self, lfp_memmap, fs, freqs, channel_ids, ripple_events, ripple_channels)
        self._ripple_worker.moveToThread(self._ripple_thread)
        self._ripple_thread.started.connect(self._ripple_worker.run)
        self._ripple_worker.progress.connect(
            self._on_ripple_progress, Qt.QueuedConnection)
        self._ripple_worker.finished.connect(
            self._on_ripple_worker_finished, Qt.QueuedConnection)
        self._ripple_worker.error.connect(
            self._on_ripple_worker_error, Qt.QueuedConnection)
        self._ripple_worker.finished.connect(self._ripple_thread.quit)
        self._ripple_worker.error.connect(self._ripple_thread.quit)
        self._ripple_thread.finished.connect(self._after_ripple_thread_stopped)
        self._ripple_thread.start()

    def _compute_ripple_triggered_spec(self, lfp_memmap, fs, freqs, channel_ids,
                                        ripple_events, ripple_channels=None,
                                        progress_cb=None):
        """Mean raw power over ±RIPPLE_HALF_WINDOW_S around every detected
        ripple's true peak, across the whole recording — the session-wide
        ripple-triggered average from Peter's Wavlet_All_Channels_Plot.mlx
        (CWT_TOTAL, averaged over all ripples).

        Pure computation -- touches no cache/Qt state, so it's safe to run
        from _RippleSpecWorker's thread. Returns (spec, n_used); spec is None
        if there are no usable ripples.

        progress_cb(done, total), if given, is called after every ripple is
        attempted (used or skipped) -- proof of life for the caller to show,
        since a single ripple's CWT can take a couple of seconds (see the
        class docstring), so hundreds of them can look identical to a hang.
        """
        n_samples = lfp_memmap.shape[1]
        pad = int(np.ceil(self.EDGE_SIGMAS * self._sigma_t(freqs[0]) * fs))
        half_samples = int(round(self.RIPPLE_HALF_WINDOW_S * fs))

        centers = self._ripple_peak_times(lfp_memmap, fs, ripple_events, ripple_channels)
        total_n = len(centers)
        total = np.zeros((len(channel_ids), len(freqs)), dtype=np.float64)
        n_used = 0
        for i, tc in enumerate(centers):
            c = int(round(tc * fs))
            s0, s1 = c - half_samples, c + half_samples + 1
            p0, p1 = s0 - pad, s1 + pad
            if not (p0 < 0 or p1 > n_samples):
                traces = lfp_memmap[channel_ids, p0:p1].astype(np.float32) * self.BIT_TO_UV
                traces = traces - traces.mean(axis=1, keepdims=True)
                power = self._mean_power(traces, fs, freqs, s0 - p0, s1 - p0)
                if power is not None:
                    total += power
                    n_used += 1
            if progress_cb is not None:
                progress_cb(i + 1, total_n)

        if n_used == 0:
            return None, 0
        return total / n_used, n_used

    def _on_ripple_progress(self, done, total):
        """_RippleSpecWorker.progress, on the GUI thread: keep the overlay's
        text moving so a long run doesn't read as a hang."""
        if self._busy_overlay is not None:
            self._busy_overlay.set_message(
                f"Averaging ripple {done} / {total}, please wait…")

    def _on_ripple_worker_finished(self, spec, n_used):
        """_RippleSpecWorker.finished, on the GUI thread: store the result in
        the cache, hide the overlay, and render (or clear, if no ripple was
        usable).

        If the ripple set/channels changed while this run was in flight (a new
        detection, a channel skipped, ...), _ripple_cache_base_key has already
        moved on -- this result belongs to neither the old nor the current
        state, so it's dropped rather than cached or rendered over whatever
        a later call may already have drawn.
        """
        freqs = self._ripple_pending_freqs
        channel_ids = self._ripple_pending_channel_ids
        stale = self._ripple_pending_base_key != self._ripple_cache_base_key
        if self._busy_overlay is not None:
            self._busy_overlay.hide()
        self.busyChanged.emit(False)
        if stale:
            return
        self._ripple_cache[self._ripple_pending_log_freq] = (spec, n_used)
        if spec is None:
            self._clear()
            return
        self._title = f'{n_used} ripples ± {1000 * self.RIPPLE_HALF_WINDOW_S:.0f} ms'
        self._finish_update_view(spec, freqs, channel_ids)

    def _on_ripple_worker_error(self, message):
        if self._busy_overlay is not None:
            self._busy_overlay.hide()
        self.busyChanged.emit(False)
        self._clear()
        print(f"AllChannelsSpectrogram: ripple-triggered computation failed: {message}",
              flush=True)

    @Slot()
    def _after_ripple_thread_stopped(self):
        """Mirrors SegmentationEvolution's cleanup (segmentation/evolution.py):
        wait for the thread to actually exit before dropping references."""
        if self._ripple_worker is not None:
            self._ripple_worker.deleteLater()
        if self._ripple_thread is not None:
            self._ripple_thread.deleteLater()
        self._ripple_worker = None
        self._ripple_thread = None

    def _draw_profiles(self, norm, freqs):
        """Depth profiles of the sharp-wave and ripple bands, each min-max
        normalised to 0-1 so their shapes can be read off one amplitude axis."""
        rows = np.arange(norm.shape[0], dtype=float)

        sw_idx = int(np.argmin(np.abs(freqs - self.SW_FREQ)))

        # ripple profile at the frequency carrying the most power in the band —
        # the MATLAB's way of picking the ripple frequency of this recording
        band = (freqs >= self.RIPPLE_BAND[0]) & (freqs <= self.RIPPLE_BAND[1])
        if band.any():
            band_idx = np.flatnonzero(band)
            r_idx = int(band_idx[np.argmax(norm[:, band_idx].max(axis=0))])
        else:
            r_idx = int(np.argmax(norm.max(axis=0)))

        for curve, idx, name in ((self.sw_curve, sw_idx, 'SW'),
                                 (self.ripple_curve, r_idx, 'R')):
            profile = norm[:, idx]
            lo, hi = float(profile.min()), float(profile.max())
            profile = (profile - lo) / (hi - lo) if hi - lo > 1e-30 \
                else np.zeros_like(profile)
            curve.setData(profile, rows)
            self.legend.getLabel(curve).setText(f'{name} ({freqs[idx]:.0f} Hz)')

    def _sync_profile_vb(self):
        """Keep the amplitude ViewBox exactly on top of the map's ViewBox.

        Only the y axis is copied — x is the amplitude scale of the profiles and
        has nothing to do with the frequency axis underneath."""
        vb = self.plot.getViewBox()
        self.profile_vb.setGeometry(vb.sceneBoundingRect())
        self.profile_vb.linkedViewChanged(vb, self.profile_vb.YAxis)

    @staticmethod
    def _resample(a, n_out, axis):
        """Linearly interpolate `a` to n_out points along `axis`, endpoints kept.
        Used for display only — a no-op when the data is already finer."""
        n_in = a.shape[axis]
        if n_in < 2 or n_out <= n_in:
            return a
        dst = np.linspace(0, n_in - 1, n_out)
        i0 = np.clip(np.floor(dst).astype(int), 0, n_in - 2)
        w = (dst - i0).reshape([-1] + [1] * (a.ndim - 1))
        m = np.moveaxis(a, axis, 0)
        return np.moveaxis(m[i0] * (1.0 - w) + m[i0 + 1] * w, 0, axis)

    @staticmethod
    def _log_ticks(f0, f1):
        """Major/minor tick spec for a log10(Hz) x-axis, labelled with plain Hz
        (10, 20, 30 …) instead of powers of ten. Ticks sit at n·10^k; leading
        digits 1/2/5 form the major level so those labels are kept first when the
        panel is narrow, and the rest fill in when there is room."""
        major, minor = [], []
        k0 = int(np.floor(np.log10(f0)))
        k1 = int(np.floor(np.log10(f1)))
        for k in range(k0, k1 + 1):
            for n in range(1, 10):
                v = n * 10.0 ** k
                if v < f0 or v > f1:
                    continue
                entry = (float(np.log10(v)), f"{v:g}")
                (major if n in (1, 2, 5) else minor).append(entry)
        return [major, minor]

    def _clear(self):
        self.img.clear()
        self.sw_curve.clear()
        self.ripple_curve.clear()
        self._rows = []
        if self._highlight_line is not None:
            self._highlight_line.setVisible(False)
        self.plot.getAxis('left').setTicks(None)   # back to automatic ticks
        self.plot.setTitle(None)

    @staticmethod
    def _colormap():
        # jet, like the MATLAB figure; the fallbacks keep the same reading
        # (blue = little power, red = much) if it isn't available
        for name, source in (('jet', 'matplotlib'), ('turbo', 'matplotlib'),
                             ('CET-R4', None)):
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


class _RippleSpecWorker(QObject):
    """Runs AllChannelsSpectrogram._compute_ripple_triggered_spec off the GUI
    thread -- looping a wavelet CWT over every detected ripple can take
    minutes on a session with many events. Same worker/thread lifecycle as
    segmentation/evolution.py's EvolutionWorker."""

    finished = Signal(object, int)   # spec (n_channels, n_freqs) or None, n_used
    error = Signal(str)
    progress = Signal(int, int)      # (ripples done, ripples total)

    def __init__(self, owner, lfp_memmap, fs, freqs, channel_ids, ripple_events,
                 ripple_channels):
        super().__init__()
        self._owner = owner
        self._lfp_memmap = lfp_memmap
        self._fs = fs
        self._freqs = freqs
        self._channel_ids = channel_ids
        self._ripple_events = ripple_events
        self._ripple_channels = ripple_channels

    @Slot()
    def run(self):
        try:
            spec, n_used = self._owner._compute_ripple_triggered_spec(
                self._lfp_memmap, self._fs, self._freqs, self._channel_ids,
                self._ripple_events, self._ripple_channels,
                progress_cb=self.progress.emit)
            self.finished.emit(spec, n_used)
        except Exception as e:
            self.error.emit(str(e))
