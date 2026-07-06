# This Python file uses the following encoding: utf-8
import numpy as np
from scipy.signal import butter, firwin, sosfiltfilt, sosfreqz, filtfilt, freqz, welch
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QVBoxLayout, QDialog
from PySide6.QtCore import Qt

_FIR_TAPS = 101   # default numtaps for FIR
_IIR_ORDER = 4    # default order for IIR Butterworth


class FilterData:
    def __init__(self, MW):
        self.MW = MW
        self.ui = MW.ui
        self.canvas = None

        self.popup = QDialog(MW)
        self.popup.setWindowTitle("Filter Channels")
        self.popup.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        popup_layout = QVBoxLayout(self.popup)
        popup_layout.addWidget(self.ui.frame_filterchannels)
        self.ui.frame_filterchannels.setVisible(True)

        self.ui.pushButton_filterpopup.clicked.connect(self.toggle_frame)

        self.ui.radioButton_lowPass.toggled.connect(self.on_shape_changed)
        self.on_shape_changed(self.ui.radioButton_lowPass.isChecked())

        self.ui.comboBox_FilterType.currentIndexChanged.connect(self.on_impl_changed)

        self.ui.pushButton_FrequencyResponse.clicked.connect(self.show_frequency_response)
        self.ui.pushButton_Filter.clicked.connect(self.apply_filter)
        self.ui.pushButton_detectFreq.clicked.connect(self.detect_freq)

    def toggle_frame(self):
        if self.popup.isVisible():
            self.popup.hide()
        else:
            self.popup.show()

    def on_shape_changed(self, low_pass_checked):
        self.ui.groupBox_upperFreq.setEnabled(not low_pass_checked)

    def on_impl_changed(self):
        pass  # reserved for future per-type UI adjustments

    def is_fir(self):
        return self.ui.comboBox_FilterType.currentIndex() == 1

    def parse_channels(self):
        text = self.ui.lineEdit_selectedChannels.text().strip()
        print(text,flush=True)
        if not text:
            return []
        try:
            return [int(c.strip()) for c in text.split(',') if c.strip()]
        except ValueError:
            return []

    def get_filter_coeff(self, fs):
        """Return (coeff, kind) where kind is 'sos' or 'fir'."""
        low = self.ui.doubleSpinBox_lowerFreq.value()
        high = self.ui.doubleSpinBox_upperFreq.value()
        nyq = fs / 2.0
        band_pass = self.ui.radioButton_bandPass.isChecked()
        print('going filter coeff',flush=True)

        if band_pass:
            if high <= low:
                high = low + 1
            if high >= nyq:
                high = nyq - 1
        else:
            if low >= nyq:
                low = nyq -1

        if self.is_fir():
            if band_pass:
                b = firwin(_FIR_TAPS, [low, high], window='hamming',
                           pass_zero=False, fs=fs)
            else:
                b = firwin(_FIR_TAPS, low, window='hamming', fs=fs)
            return b, 'fir'
        else:
            if band_pass:
                sos = butter(_IIR_ORDER, [low, high], btype='band',
                             fs=fs, output='sos')
            else:
                sos = butter(_IIR_ORDER, low, btype='low',
                             fs=fs, output='sos')
            return sos, 'sos'

    def apply_coeff(self, coeff, kind, data):
        if kind == 'sos':
            return sosfiltfilt(coeff, data, axis=0)
        else:
            return filtfilt(coeff, [1.0], data, axis=0)

    def freq_response(self, coeff, kind, fs):
        if kind == 'sos':
            return sosfreqz(coeff, worN=2048, fs=fs)
        else:
            return freqz(coeff, worN=2048, fs=fs)

    def ensure_canvas(self):
        if self.canvas is not None:
            return
        fig = Figure(tight_layout=True)
        fig.patch.set_facecolor('#2d2d2d')
        self.canvas = FigureCanvas(fig)
        layout = self.ui.widget_cutoff_freq.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.widget_cutoff_freq)
        layout.addWidget(self.canvas)

    def style_ax(self, ax, title):
        ax.set_facecolor('#19232d')
        ax.set_title(title, color='white', fontsize=9)
        ax.tick_params(colors='white', labelsize=7)
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        low = self.ui.doubleSpinBox_lowerFreq.value()
        high = self.ui.doubleSpinBox_upperFreq.value()
        ax.set_xlim(0, max(low,high)* 2)
        for spine in ax.spines.values():
            spine.set_edgecolor('#555555')
        ax.grid(True, alpha=0.2, color='white')

    def detect_freq(self):
        channels = self.parse_channels()
        if not channels:
            return

        ephys = self.MW.Ephys.ephys_data
        fs = float(ephys.read_data.analogsignals[0].sampling_rate)
        vis = self.MW.Ephys.VisEphys
        signal = ephys.read_data.analogsignals[0].load(
            time_slice=(vis.time_start, vis.time_end),
            channel_indexes=channels,
        )
        data = signal.magnitude  # (n_samples, n_channels)

        # average PSD across selected channels
        freqs, psd = welch(data[:, 0], fs=fs, nperseg=min(1024, data.shape[0]))
        for ch in range(1, data.shape[1]):
            _, p = welch(data[:, ch], fs=fs, nperseg=min(1024, data.shape[0]))
            psd += p
        psd /= data.shape[1]

        # find frequency range above 1% of peak power
        threshold = 0.01 * psd.max()
        above = np.where(psd >= threshold)[0]
        low_freq = float(freqs[above[0]])
        high_freq = float(freqs[above[-1]])

        self.ui.doubleSpinBox_lowerFreq.setValue(round(low_freq, 2))
        self.ui.doubleSpinBox_upperFreq.setValue(round(high_freq, 2))


    def show_frequency_response(self):
        ephys = self.MW.Ephys.ephys_data
        fs = float(ephys.read_data.analogsignals[0].sampling_rate)
        coeff, kind = self.get_filter_coeff(fs)
        print(coeff,flush=True)
        if coeff is None:
            return
        print(coeff,flush=True)
        w, h = self.freq_response(coeff, kind, fs)

        self.ensure_canvas()
        fig = self.canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(w, 20 * np.log10(np.abs(h) + 1e-12), color='#4fc3f7', linewidth=1.5)
        ax.set_xlabel('Frequency (Hz)', fontsize=8)
        ax.set_ylabel('Amplitude (dB)', fontsize=8)
        self.style_ax(ax, 'Frequency Response')
        self.canvas.draw()

    def apply_filter(self):
        channels = self.parse_channels()
        if not channels:
            return
        print('going apply filter',flush=True)
        ephys = self.MW.Ephys.ephys_data
        fs = float(ephys.read_data.analogsignals[0].sampling_rate)
        coeff, kind = self.get_filter_coeff(fs)
        if coeff is None:
            return

        vis = self.MW.Ephys.VisEphys
        signal = ephys.read_data.analogsignals[0].load(
            time_slice=(vis.time_start, vis.time_end),
            channel_indexes=channels,
        )
        raw = signal.magnitude          # (n_samples, n_channels)
        times = signal.times.magnitude
        filtered = self.apply_coeff(coeff, kind, raw)

        self.MW.ui.widget_pgEphys.plot_ephys(signal.times, filtered, channels)

        w, h = self.freq_response(coeff, kind, fs)

        self.ensure_canvas()
        fig = self.canvas.figure
        fig.clear()

        ax_freq = fig.add_subplot(2, 1, 1)
        ax_freq.plot(w, 20 * np.log10(np.abs(h) + 1e-12), color='#4fc3f7', linewidth=1.5)
        ax_freq.set_xlabel('Frequency (Hz)', fontsize=8)
        ax_freq.set_ylabel('dB', fontsize=8)
        self.style_ax(ax_freq, 'Frequency Response')

        ax_sig = fig.add_subplot(2, 1, 2)
        ax_sig.plot(times, raw[:, 0], color='#888888', linewidth=0.8, label='raw', alpha=0.7)
        ax_sig.plot(times, filtered[:, 0], color='#81c784', linewidth=1.0,
                    label=f'ch {channels[0]} filtered')
        ax_sig.set_xlabel('Time (s)', fontsize=8)
        ax_sig.set_ylabel('Amplitude', fontsize=8)
        ax_sig.legend(fontsize=7, facecolor='#2d2d2d', labelcolor='white', framealpha=0.6)
        self.style_ax(ax_sig, 'Filtered Signal')

        self.canvas.draw()
