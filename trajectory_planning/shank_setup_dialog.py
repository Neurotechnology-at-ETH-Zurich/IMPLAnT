# This Python file uses the following encoding: utf-8
import os

from PySide6 import QtWidgets

from electrode2geometry.python.geometry_core import parse_neuroscope_xml


class ShankSetupDialog(QtWidgets.QDialog):
    """Asked once, right before insertion-point selection: how many shanks
    the probe has, and whether each shank's contact geometry will be
    user-defined (DXF bending / Shank Geometry panel, non-uniform spacing)
    or pre-defined (equal spacing between electrodes).

    In user-defined mode, a Neuroscope XML (the same format the Shank
    Geometry panel's own "Browse XML" reads via parse_neuroscope_xml) can
    optionally be loaded here up front -- its channel groups both set
    "Number of shanks" directly (one group == one shank) and get carried
    into TrajectoryPlanning's own dfx_xml_groups/dfx_xml_file/
    dfx_xml_nchannels (see registration.py's get_shank_line), so each
    shank's channel numbers are already filled in by the time its DXF
    bending is run (dfx_geometry.py's refresh_dfx_channel_display), instead
    of needing "Browse XML" clicked again once inside that panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shank Setup")
        self.setModal(True)

        self.xml_path = None
        self.xml_groups = []
        self.xml_nchannels = 0

        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()
        self.spinBox_n_shanks = QtWidgets.QSpinBox()
        self.spinBox_n_shanks.setRange(1, 32)
        self.spinBox_n_shanks.setValue(1)
        form.addRow("Number of shanks", self.spinBox_n_shanks)
        layout.addLayout(form)

        layout.addWidget(QtWidgets.QLabel("Contact geometry:"))
        self.radio_uniform = QtWidgets.QRadioButton(
            "Pre-defined - equal spacing between electrodes")
        self.radio_custom = QtWidgets.QRadioButton(
            "User-defined - import each shank's geometry "
            "(Shank Geometry / DXF bending)")
        self.radio_custom.setChecked(True)
        layout.addWidget(self.radio_uniform)
        layout.addWidget(self.radio_custom)

        xml_layout = QtWidgets.QHBoxLayout()
        self.pushButton_xml = QtWidgets.QPushButton("Load Neuroscope XML…")
        self.pushButton_xml.setToolTip(
            "Optional: sets \"Number of shanks\" from the XML's channel "
            "groups and pre-fills every shank's channel numbers in the "
            "Shank Geometry panel.")
        self.pushButton_xml.clicked.connect(self._browse_xml)
        xml_layout.addWidget(self.pushButton_xml)
        layout.addLayout(xml_layout)
        self.radio_uniform.toggled.connect(self._update_xml_button_visibility)
        self.radio_custom.toggled.connect(self._update_xml_button_visibility)
        self._update_xml_button_visibility()

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _update_xml_button_visibility(self):
        # Only "custom" (user-defined) mode has a Shank Geometry panel to
        # feed channel groups into -- "uniform" mode's channels are just a
        # count/separation, set on stackedWidget_geometry's other page.
        self.pushButton_xml.setVisible(self.radio_custom.isChecked())

    def _browse_xml(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select the Neuroscope XML file", "",
            "Neuroscope XML (*.xml);;All files (*)")
        if not path:
            return
        try:
            groups, n_channels, _skip = parse_neuroscope_xml(path)
        except Exception as exc:  # noqa: BLE001
            QtWidgets.QMessageBox.critical(self, "XML parse failed", str(exc))
            return
        if not groups:
            QtWidgets.QMessageBox.warning(
                self, "Empty XML", "No channel groups were found in the XML.")
            return

        self.xml_path = path
        self.xml_groups = groups
        self.xml_nchannels = n_channels
        self.pushButton_xml.setText(os.path.basename(path))
        self.pushButton_xml.setToolTip(path)
        # One channel group per shank -- editable afterward, in case the
        # XML groups don't line up 1:1 with physical shanks for this probe.
        self.spinBox_n_shanks.setValue(len(groups))

    def get_values(self):
        """Return (n_shanks, mode, xml_path, xml_groups, xml_nchannels)
        with mode in {'uniform', 'custom'}. xml_path is None (xml_groups
        empty, xml_nchannels 0) if no XML was loaded here."""
        mode = "custom" if self.radio_custom.isChecked() else "uniform"
        return (self.spinBox_n_shanks.value(), mode,
                self.xml_path, self.xml_groups, self.xml_nchannels)
