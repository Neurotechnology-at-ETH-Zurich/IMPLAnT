# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets


class ShankSetupDialog(QtWidgets.QDialog):
    """Asked once, right before insertion-point selection: how many shanks
    the probe has, and whether each shank's contact geometry will be
    user-defined (DXF bending / Shank Geometry panel, non-uniform spacing)
    or pre-defined (equal spacing between electrodes)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shank Setup")
        self.setModal(True)

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

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_values(self):
        """Return (n_shanks, mode) with mode in {'uniform', 'custom'}."""
        mode = "custom" if self.radio_custom.isChecked() else "uniform"
        return self.spinBox_n_shanks.value(), mode
