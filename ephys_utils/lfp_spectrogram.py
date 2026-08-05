# This Python file uses the following encoding: utf-8
import numpy as np
import pyqtgraph as pg
import pywt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QRectF

from ephys_utils.spiking_ruster import TimeAxisItem


class HzAxisItem(pg.AxisItem):
    """Frequency axis that labels log ticks as plain numbers.

    In log mode pyqtgraph writes each tick as a power of ten (1×10¹, 1×10²),
    which is hard to read for a 1-250 Hz range. Label the actual frequency
    instead: 1, 10, 100. Linear mode is untouched, because AxisItem.tickStrings
    only routes here when the axis is logarithmic.
    """

    def logTickStrings(self, values, scale, spacing):
        return [f"{v:g}" for v in
                10 ** np.asarray(values, dtype=float) * float(scale)]


_FOOOF_CACHE = None


def _load_fooof():
    """Import FOOOF once, then undo the global ``warnings.simplefilter('always')``
    that its ``__init__`` runs. That call wipes existing warning filters and makes
    every warning (e.g. pandas' find_common_type) print on repeat; here we restore
    the default show-once behaviour and re-silence that one cosmetic message.
    Returns (FOOOF, gen_aperiodic)."""
    global _FOOOF_CACHE
    if _FOOOF_CACHE is None:
        import warnings
        from fooof import FOOOF
        from fooof.sim.gen import gen_aperiodic
        warnings.simplefilter('default')
        warnings.filterwarnings(
            'ignore', message='np.find_common_type is deprecated',
            category=DeprecationWarning)
        _FOOOF_CACHE = (FOOOF, gen_aperiodic)
    return _FOOOF_CACHE


class LFPSpectrogram(QWidget):
    """Time-frequency map of one LFP channel over the same time window
    (start s -> end s) that widget_pgEphys and the spike raster show.

    Uses a continuous wavelet transform (complex Morlet) rather than an STFT:
    each frequency is analysed with a wavelet whose width scales with the
    frequency (constant-Q). Ripples are localised sharply in time, slow
    rhythms sharply in frequency, without picking one fixed window for both.

    One map covers the whole LFP range (F_MIN..F_MAX) instead of a theta and a
    ripple panel. That is what the constant-Q wavelet is for: the same setting
    resolves 8 Hz in frequency and a 100 ms ripple in time. The frequency axis is
    logarithmic, so theta gets as much height as the ripple band instead of two
    pixels out of the linear 1-250 Hz span."""

    # The complex Morlet is cmor<bandwidth>-<center>: a larger bandwidth widens
    # the wavelet's Gaussian envelope, sharpening frequency at the cost of time.
    # 2.0 sits between the old per-band settings (ripple 1.5 / theta 3.0), which
    # is what a single map spanning both bands needs.
    BANDWIDTH = 2.0
    CENTER = 1.0
    # Rows, log-spaced over F_MIN..F_MAX. One wavelet spans ~23 % of its centre
    # frequency while adjacent rows are ~2.4 % apart, so the grid oversamples the
    # transform ~10x — the extra rows buy a smooth image, not extra detail, which
    # is why they are safe: nothing here is interpolated or invented.
    N_FREQS = 240
    F_MIN = 1.0
    F_MAX = 250.0
    CLIM_DB = 20.0       # colour scale never wider than +-this

    MAX_COLUMNS = 8000   # column budget; the CWT yields one column per sample,
                         # so long windows get decimated down to this
    EDGE_SIGMAS = 3.0    # read this many wavelet sigmas past both edges, so the
                         # cone of influence stays outside the viewed window
    BIT_TO_UV = 0.195    # same int16 -> uV scaling the ephys view uses
    DB_CLIM_MIN = 3.0    # colour scale never tighter than +-3 dB

    # FOOOF aperiodic (1/f) fit used to flatten the spectrum across frequency.
    # 'knee' rather than 'fixed': over 1-250 Hz the LFP background is not a
    # straight line in log-log, and a fixed slope would leave a tilt in the map
    # that reads as broadband power. A few peaks are allowed so oscillations
    # aren't absorbed into the background.
    FOOOF_APERIODIC = 'knee'
    FOOOF_MAX_PEAKS = 6
    N_FIT_FREQS = 512    # points of the even linear grid the fit is done on

    LOG_FREQ = True      # start on the log frequency axis; toggled at runtime

    # cycled by pushButton_colorMap. RdBu_r rather than RdBu so that red stays
    # "above the 1/f background" in both maps — plain RdBu puts red at the
    # negative end and would invert the reading of the same image.
    COLORMAPS = ('jet', 'RdBu_r')

    def __init__(self, parent=None, label=None):
        super().__init__(parent)
        self._channel = None     # LFP row (== xml channel id) currently shown
        self._timeline = None
        self._last_args = None   # last (memmap, fs, t_start, t_end), for re-rendering
        self._pending = None     # update_view args deferred while this tab is hidden
        # {log_freq: render payload}, for the current _cache_base_key (memmap,
        # t_start, t_end, channel -- everything update_view is called with
        # EXCEPT log_freq). Toggling the frequency axis without anything else
        # changing then reuses whichever of the two was already computed,
        # instead of rerunning the CWT -- see set_log_frequency.
        self._cache_base_key = None
        self._cache = {}
        self.log_freq = self.LOG_FREQ
        self._cmap_name = self.COLORMAPS[0]

        self.wavelet = f"cmor{self.BANDWIDTH}-{self.CENTER}"
        # central frequency of the mother wavelet, needed to turn scales back
        # into the wavelet's temporal width for edge padding and the title
        self._central = pywt.central_frequency(self.wavelet)

        # optional QLineEdit title (both per-band ones were removed from the .ui,
        # so this is normally None and the band shows in the plot title instead)
        self.label_mode = label
        if self.label_mode is not None:
            self.label_mode.setReadOnly(True)
            self.label_mode.setText(f"LFP {self.F_MIN:.0f}-{self.F_MAX:.0f} Hz")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget(
            background='k', axisItems={'bottom': TimeAxisItem(orientation='bottom'),
                                       'left': HzAxisItem(orientation='left')})
        self.plot = self.plot_widget.getPlotItem()
        self.plot.setLabel('left', 'Frequency', units='Hz')
        # the axis labels Hz directly, so no SI prefix rescaling of the ticks
        self.plot.getAxis('left').enableAutoSIPrefix(False)
        # log frequency axis: view coordinates are log10(Hz) — the image rect is
        # placed in those units below — while the axis still labels real Hz
        self.plot.setLogMode(x=False, y=self.log_freq)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.hideButtons()
        self.plot.getViewBox().setMenuEnabled(False)
        layout.addWidget(self.plot_widget)

        self.img = pg.ImageItem()
        self.img.setOpts(axisOrder='row-major')   # image[freq, time]
        # there are far more columns than screen pixels; average the ones sharing
        # a pixel instead of letting the renderer pick one of them, which aliases
        # short events and makes them flicker as the window scrolls
        self.img.setAutoDownsample(True)
        self.plot.addItem(self.img)

        self.colorbar = pg.ColorBarItem(
            values=(-1, 1), colorMap=self._colormap(self._cmap_name),
            label='Power over 1/f  (dB)', interactive=False, pen='w',
        )
        self.colorbar.setImageItem(self.img, insert_in=self.plot)

    # ------------------------------------------------------------------
    # Colour map (cycled by pushButton_colorMap)
    # ------------------------------------------------------------------

    def set_colormap(self, name):
        """Use the named colour map. The ColorBarItem applies its LUT to the
        linked ImageItem, so no re-render of the CWT is needed."""
        cmap = self._colormap(name)
        if cmap is None:
            return
        self._cmap_name = name
        self.colorbar.setColorMap(cmap)

    def toggle_colormap(self):
        """Step to the next map in COLORMAPS; returns the new name."""
        try:
            nxt = (self.COLORMAPS.index(self._cmap_name) + 1) % len(self.COLORMAPS)
        except ValueError:
            nxt = 0
        self.set_colormap(self.COLORMAPS[nxt])
        return self._cmap_name

    @property
    def colormap_name(self):
        return self._cmap_name

    # ------------------------------------------------------------------
    # Frequency axis (log <-> linear, driven by pushButton_axisLog)
    # ------------------------------------------------------------------

    def set_log_frequency(self, enabled):
        """Switch the frequency axis between log and linear Hz.

        This moves the analysed frequencies too, not just the axis: the rows have
        to be evenly spaced in whatever the axis shows, because the image is
        placed with a single rect. Log -> rows even in log10(f); linear -> rows
        even in Hz, which spends most of them above 30 Hz and leaves theta a
        couple of pixels. Re-renders the current window."""
        enabled = bool(enabled)
        if enabled == self.log_freq:
            return
        self.log_freq = enabled
        self.plot.setLogMode(x=False, y=enabled)
        if self._last_args is not None:
            self.update_view(*self._last_args)

    def toggle_log_frequency(self):
        """Flip the frequency axis; returns the new state (True = log)."""
        self.set_log_frequency(not self.log_freq)
        return self.log_freq

    # ------------------------------------------------------------------
    # Time cursor (mirrors the ephys-plot timeline, like the spike raster)
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
    # Channel selection (driven by the ephys-view channel highlight)
    # ------------------------------------------------------------------

    def set_channel(self, channel):
        """Show `channel` (xml channel id). Redraw is done by the next
        update_view call, so pass the current window afterwards if needed."""
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    # ------------------------------------------------------------------
    # Call this every time the time window (or channel) changes
    # ------------------------------------------------------------------

    def showEvent(self, event):
        """Render the window that was requested while this tab was hidden."""
        super().showEvent(event)
        if self._pending is not None:
            args, kwargs = self._pending
            self._pending = None
            self.update_view(*args, **kwargs)

    def update_view(self, lfp_memmap, lfp_sample_rate, t_start, t_end, channel=None,
                    force=False):
        """lfp_memmap: (n_channels, n_samples) int16 memmap; rows are channel ids.
        force=True bypasses the hidden-tab defer below -- used once right after
        a file/tag loads, to prewarm this tab before it's first clicked."""
        if channel is not None:
            self._channel = channel
        self._last_args = (lfp_memmap, lfp_sample_rate, t_start, t_end)

        # The CWT runs on every scroll step; skip it while another tab of
        # tabWidget_LFP is in front and remember the request instead (like
        # AllChannelsSpectrogram), rendered when this tab is shown (showEvent above).
        if not force and not self.isVisible():
            self._pending = ((lfp_memmap, lfp_sample_rate, t_start, t_end),
                              {'channel': channel})
            return
        self._pending = None

        if lfp_memmap is None or self._channel is None or t_end <= t_start:
            self._clear()
            return

        fs = float(lfp_sample_rate)
        n_samples = lfp_memmap.shape[1]
        s0 = max(0, int(t_start * fs))
        s1 = min(n_samples, int(t_end * fs))
        if s1 - s0 < 32:
            self._clear()
            return

        fmax = min(self.F_MAX, fs / 2.0 * 0.99)
        if fmax <= self.F_MIN:
            self._clear()
            return

        # cache keyed on log_freq, for everything else about this call -- an
        # axis toggle alone (t_start/t_end/channel unchanged) hits this and
        # skips the CWT entirely; any real change (scroll, channel switch, ...)
        # invalidates both entries and both get recomputed on next use
        base_key = (id(lfp_memmap), t_start, t_end, self._channel)
        if base_key != self._cache_base_key:
            self._cache_base_key = base_key
            self._cache = {}

        cached = self._cache.get(self.log_freq)
        if cached is not None:
            self._render(cached, t_start, t_end)
            return

        # The lowest frequency has the widest wavelet, so it sets how far past
        # each edge we read (in samples). At F_MIN = 1 Hz that is seconds, not
        # milliseconds — the price of covering the slow end in the same map. The
        # padding is cropped from the view afterwards, so the cone of influence
        # never reaches the shown window.
        sigma_t_max = self._sigma_t(self.F_MIN)
        pad = int(np.ceil(self.EDGE_SIGMAS * sigma_t_max * fs))
        p0 = max(0, s0 - pad)
        p1 = min(n_samples, s1 + pad)

        trace = lfp_memmap[self._channel, p0:p1].astype(np.float32) * self.BIT_TO_UV
        trace = trace - trace.mean()

        freqs, power = self._morlet_cwt(trace, fs, fmax)   # power [n_freqs, n_trace]
        if power.shape[1] == 0:
            self._clear()
            return

        # absolute time of every column, then decimate to the column budget
        t_abs = (p0 + np.arange(power.shape[1])) / fs
        hop = int(np.clip(np.ceil(power.shape[1] / self.MAX_COLUMNS), 1, None))
        if hop > 1:
            power = power[:, ::hop]
            t_abs = t_abs[::hop]

        # only the columns actually inside the requested window feed the
        # baseline/clim, so padded edges can't skew them
        inwin = (t_abs >= t_start) & (t_abs <= t_end)
        ref = power[:, inwin] if inwin.any() else power

        # absolute power, flattened across frequency by dividing out the
        # aperiodic (1/f) background that FOOOF fits to this window's spectrum,
        # then shown in dB. 0 dB = the 1/f background for that frequency, so slow
        # and fast rhythms sit on one colour scale and an oscillation reads as its
        # true power above the background rather than as a percentage.
        baseline = self._aperiodic_baseline(freqs, ref)
        flat_db = 10.0 * np.log10(np.maximum(power, 1e-20) / baseline)

        # image spans the actual times/frequencies of the columns +- half a step.
        # The rows are evenly spaced in whatever the axis shows — log10(f) in log
        # mode, Hz in linear mode — so the vertical extent is computed in those
        # same units and maps linearly onto the axis.
        f_ax = np.log10(freqs) if self.log_freq else freqs
        dt = t_abs[1] - t_abs[0] if t_abs.size > 1 else (trace.size / fs)
        df = f_ax[1] - f_ax[0] if f_ax.size > 1 else 1.0
        x0 = t_abs[0] - dt / 2.0
        y0 = f_ax[0] - df / 2.0

        # Symmetric around 0 dB, so the diverging colours mean what they look
        # like. Clamped: a burst in a band that is otherwise near-empty reaches
        # tens of dB and would flatten everything else, while a very quiet window
        # would otherwise be stretched into pure noise. Outliers saturate
        # instead, and the colours stay comparable as you scroll.
        #
        # The percentile is deliberately far out in the tail: at the 95th, exactly
        # 5 % of the pixels saturate in every window by construction, so deep red
        # appeared even in a window holding nothing but background. At 99.9 the
        # scale normally pins to CLIM_DB and only genuine outliers reach the ends
        # of the colour bar.
        ref_db = flat_db[:, inwin] if inwin.any() else flat_db
        v = float(np.percentile(np.abs(ref_db), 99.9))
        v = float(np.clip(v, self.DB_CLIM_MIN, self.CLIM_DB))

        payload = dict(flat_db=flat_db, t_abs=t_abs, f_ax=f_ax, dt=dt, df=df,
                       x0=x0, y0=y0, v=v, fmax=fmax)
        self._cache[self.log_freq] = payload
        self._render(payload, t_start, t_end)

    def _render(self, payload, t_start, t_end):
        """Draw an already-computed CWT result -- freshly computed, or a hit
        in _cache from toggling back to an axis mode already seen for this
        window/channel."""
        flat_db = payload['flat_db']
        t_abs = payload['t_abs']
        f_ax = payload['f_ax']
        dt = payload['dt']
        df = payload['df']
        x0 = payload['x0']
        y0 = payload['y0']
        v = payload['v']
        fmax = payload['fmax']

        self.img.setImage(flat_db, autoLevels=False)
        self.img.setRect(QRectF(x0, y0, t_abs[-1] - t_abs[0] + dt,
                                f_ax[-1] - f_ax[0] + df))
        self.colorbar.setLevels((-v, v))

        # spell out the resolution actually achieved: the wavelet's temporal
        # width (FWHM) shrinks with frequency, so report it at both band edges
        fwhm = 2.0 * np.sqrt(2.0 * np.log(2.0))
        self.plot.setTitle(
            f'ch {self._channel} — {self.F_MIN:.0f}–{fmax:.0f} Hz — {self.wavelet} — '
            f'{1000 * fwhm * self._sigma_t(fmax):.0f}–'
            f'{1000 * fwhm * self._sigma_t(self.F_MIN):.0f} ms',
            color='w', size='8pt')
        # exactly the ephys/raster window, so the three views stay aligned
        vb = self.plot.getViewBox()
        vb.disableAutoRange()
        vb.setLimits(xMin=t_start, xMax=t_end)   # nothing may pad past the window
        self.plot.setXRange(t_start, t_end, padding=0)
        # fixed frequency axis so it doesn't jump between zoom levels, in the same
        # units as the rect above (log10 in log mode — the axis still shows Hz)
        if self.log_freq:
            self.plot.setYRange(np.log10(self.F_MIN), np.log10(fmax), padding=0)
        else:
            self.plot.setYRange(self.F_MIN, fmax, padding=0)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sigma_t(self, f):
        """Temporal std (seconds) of the Morlet envelope at frequency f. In the
        wavelet's own units the Gaussian std is sqrt(bandwidth/2); stretched to
        centre on f it scales by central_freq / f."""
        return np.sqrt(self.BANDWIDTH / 2.0) * self._central / f

    def _aperiodic_baseline(self, freqs, ref):
        """Per-frequency background power to divide out before display, as linear
        power of shape (n_freqs, 1). FOOOF fits the aperiodic (1/f) component to
        this window's time-median spectrum; the periodic peaks are left in the
        image rather than removed. Falls back to the plain per-frequency median
        if FOOOF is missing or the fit fails (e.g. a flat/near-silent channel)."""
        # median over time is a burst-robust estimate of the background spectrum
        psd = np.maximum(np.median(ref, axis=1), 1e-20)
        try:
            FOOOF, gen_aperiodic = _load_fooof()
            # FOOOF rejects frequency vectors that are not equidistant in LINEAR
            # space ("The input frequency values are not evenly spaced"), which is
            # exactly what the log-spaced rows are. So resample the spectrum onto
            # an even linear grid for the fit only — interpolated in log-log, where
            # the 1/f model lives — and keep it dense enough that the low end is
            # still represented (a 120-point linear grid would put only ~14 points
            # below 30 Hz). The fitted parameters are then evaluated analytically
            # back on our own rows, so nothing about the image changes.
            n_fit = max(len(freqs), self.N_FIT_FREQS)
            lin_f = np.linspace(float(freqs[0]), float(freqs[-1]), n_fit)
            lin_psd = np.power(10.0, np.interp(np.log10(lin_f), np.log10(freqs),
                                               np.log10(psd)))
            fm = FOOOF(aperiodic_mode=self.FOOOF_APERIODIC,
                       max_n_peaks=self.FOOOF_MAX_PEAKS, verbose=False)
            fm.fit(lin_f, lin_psd, freq_range=(float(lin_f[0]), float(lin_f[-1])))
            # rebuild the aperiodic fit (log10 power) on our own frequency grid,
            # so it lines up with `power` regardless of FOOOF's internal cropping
            ap_log10 = gen_aperiodic(freqs.astype(float), fm.aperiodic_params_)
            baseline = np.power(10.0, ap_log10)
        except Exception:
            baseline = psd
        return np.maximum(baseline, 1e-20).reshape(-1, 1)

    def _morlet_cwt(self, trace, fs, fmax):
        """Complex Morlet CWT via PyWavelets. Returns (freqs, power) with power
        shape [N_FREQS, len(trace)], freqs ascending and evenly spaced in whatever
        the axis currently shows (log10 or Hz) so the image rect stays valid.

        Log is the default: one map spans 1-250 Hz, where a linear grid spends
        almost every row above 30 Hz, and even-in-log10 matches the constant-Q
        wavelet, whose relative bandwidth is the same at every frequency.

        Absolute wavelet normalisation is irrelevant here — the aperiodic baseline
        in update_view divides any constant scaling straight back out."""
        if self.log_freq:
            freqs = np.logspace(np.log10(self.F_MIN), np.log10(fmax), self.N_FREQS)
        else:
            freqs = np.linspace(self.F_MIN, fmax, self.N_FREQS)
        freqs = freqs.astype(np.float64)
        scales = pywt.frequency2scale(self.wavelet, freqs / fs)
        coef, _ = pywt.cwt(trace, scales, self.wavelet,
                           sampling_period=1.0 / fs, method='fft')
        power = (coef.real ** 2 + coef.imag ** 2).astype(np.float32)
        return freqs, power

    def _clear(self):
        self.img.clear()
        self.plot.setTitle(None)


    @staticmethod
    def _colormap(name='jet'):
        # `name` first (matplotlib, then pyqtgraph's own registry), otherwise the
        # jet-like fallbacks: sinks deep blue, sources deep red, and enough
        # contrast in between that a blob is visible before it saturates
        for cand, source in ((name, 'matplotlib'), (name, None),
                             ('jet', 'matplotlib'), ('turbo', 'matplotlib'),
                             ('CET-R4', None)):
            try:
                cm = pg.colormap.get(cand, source=source)
            except Exception:
                cm = None
            if cm is not None:
                return cm
        return pg.colormap.ColorMap(
            [0.0, 0.25, 0.5, 0.75, 1.0],
            [(0, 0, 143, 255), (0, 200, 255, 255), (120, 255, 120, 255),
             (255, 180, 0, 255), (143, 0, 0, 255)])
