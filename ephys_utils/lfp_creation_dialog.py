# This Python file uses the following encoding: utf-8
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QSpinBox, QLabel,
    QPushButton, QGroupBox, QApplication,
)

from ephys_utils.downsample_filter_LFP import downsample_filter_LFP
from ephys.ephysrecording import EphysRecording
from gui_utils.busy_overlay import BusyOverlay

_DS_FACTOR = 10          # downsample factor is always 10 (e.g. 20 kHz -> 2 kHz)
_PASSBAND = 250          # Hz: lowpass passband edge (fixed, matches MATLAB)
_STOPBAND = 450        # Hz: passband -> stopband, so stopband = 250 + 200 = 450 Hz
_DEFAULT_ORDER = 600     # FIR order: ~100 dB attenuation for a 200 Hz transition at 20 kHz


class LFPCreationDialog(QDialog):
    """Confirm/correct the parameters read from the recording XML before
    creating the .lfp file.

    Fields default to what was parsed from the XML; the user can fix them if the
    XML is wrong, then click 'Create LFP file'. The target LFP sample rate is
    derived (acquisition rate / 10) and shown read-only.
    """

    def __init__(self, MW, ephys_data):
        super().__init__(MW)
        self.MW = MW
        self.ephys_data = ephys_data
        self.created = False

        self.setWindowTitle("Create LFP file")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)
        intro = QLabel(
            "Confirm the values read from the recording XML.\n"
            "Correct them if they are wrong, then create the LFP file.")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        form = QFormLayout()

        # --- editable fields ---
        self.spin_channels = QSpinBox()
        self.spin_channels.setRange(1, 4096)
        self.spin_channels.setValue(int(ephys_data.n_channels))
        form.addRow("Number of channels:", self.spin_channels)

        self.spin_acq = QSpinBox()
        self.spin_acq.setRange(1, 1_000_000)
        self.spin_acq.setValue(int(ephys_data.sample_rate))
        self.spin_acq.setSuffix(" Hz")
        form.addRow("Acquisition sample rate:", self.spin_acq)

        self.spin_order = QSpinBox()
        self.spin_order.setRange(2, 5000)
        self.spin_order.setValue(_DEFAULT_ORDER)
        form.addRow("Filter order:", self.spin_order)

        # --- derived / read-only fields ---
        form.addRow("Lowpass filter:",
                    QLabel(f"passband {_PASSBAND} Hz, stopband {_STOPBAND} Hz"))

        form.addRow("Downsample factor:", QLabel(f"{_DS_FACTOR}x"))

        self.label_lfp_rate = QLabel()
        form.addRow("Target LFP sample rate:", self.label_lfp_rate)

        layout.addLayout(form)

        # --- informational: channel layout (read-only) ---
        info = QGroupBox("Channel layout (read-only)")
        info_layout = QVBoxLayout(info)
        order_label = QLabel("Channel order: "
                             + ", ".join(str(c) for c in ephys_data.all_channels))
        order_label.setWordWrap(True)
        skipped = ephys_data.dead_channels
        skip_label = QLabel("Skipped channels: "
                            + (", ".join(str(c) for c in skipped) if skipped else "none"))
        skip_label.setWordWrap(True)
        info_layout.addWidget(order_label)
        info_layout.addWidget(skip_label)
        layout.addWidget(info)

        # --- button ---
        self.button_create = QPushButton("Create LFP file")
        self.button_create.clicked.connect(self.create_lfp)
        layout.addWidget(self.button_create)

        self.spin_acq.valueChanged.connect(self._update_lfp_rate)
        self._update_lfp_rate()

    def _update_lfp_rate(self):
        self.label_lfp_rate.setText(f"{self.spin_acq.value() // _DS_FACTOR} Hz")

    def create_lfp(self):
        num_channels = self.spin_channels.value()
        sample_rate = self.spin_acq.value()
        filter_order = self.spin_order.value()
        lfp_rate = sample_rate // _DS_FACTOR

        # hide the popup first so only the busy overlay is visible during creation
        self.hide()
        QApplication.processEvents()

        overlay = BusyOverlay(self.MW, "Creating LFP file, please wait…")
        overlay.setGeometry(self.MW.rect())
        overlay.raise_()
        overlay.show()
        QApplication.processEvents()
        try:
            raw_dir = os.path.dirname(self.ephys_data.file_path)
            dat_name = os.path.basename(self.ephys_data.file_path)
            downsample_filter_LFP(
                raw_dir, dat_name,
                num_channels=num_channels,
                sample_rate=sample_rate,
                cutoff=_PASSBAND,
                stopband=_STOPBAND,
                filter_order=filter_order,
            )
        finally:
            overlay.close()

        # keep the recording metadata consistent with the values actually used
        self.ephys_data.n_channels = num_channels
        self.ephys_data.sample_rate = sample_rate
        self.ephys_data.lfp_sample_rate = lfp_rate
        self.ephys_data.lfp_memmap = EphysRecording._load_lfp_memmap(
            self.ephys_data.lfp_path, num_channels)

        self.created = True
        self.accept()
