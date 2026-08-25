# This Python file uses the following encoding: utf-8
"""
Self-contained "user-defined channel geometry" panel for electrode
localisation (core/electrode_localization.py's ChannelVariablesInput).

Reuses the same DXF-bending pipeline trajectory planning's Shank Geometry
panel uses (trajectory_planning/dfx_geometry.py calls the same
electrode2geometry functions), but built as a plain QWidget instead of a
mixin tied to form.ui widgets, since ChannelVariablesInput is built
entirely in code. Only the per-channel depth is read out here -- the
channel-ID/Neuroscope-XML mapping DfxGeometry also supports is irrelevant
to electrode localisation (channel_mapper.py only ever needs depths).
"""
import os

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox

from electrode2geometry.python.geometry_core import bend_dxf_probe_geometry

# Same palette convention as during_surgery/mri_preview.py's _SHANK_COLORS /
# trajectory_planning/shank.py's NEON_COLORS -- a plain local tuple list
# rather than importing either, to keep this panel dependency-free of both.
_TAG_COLORS = [
    (0, 255, 71), (255, 20, 147), (0, 191, 255),
    (255, 255, 0), (138, 0, 196), (255, 92, 0), (255, 255, 255),
]


def _make_double_spin(value, minimum, maximum, decimals=1):
    spin = QtWidgets.QDoubleSpinBox()
    spin.setDecimals(decimals)
    spin.setRange(minimum, maximum)
    spin.setValue(value)
    return spin


class DfxGeometryPanel(QtWidgets.QWidget):
    """One DXF-bending workspace, with a per-tag committed-geometry store
    (self.tag_geometry) analogous to DfxGeometry.dfx_shank_data being
    keyed per shank number in trajectory planning."""

    def __init__(self, roi_names, parent=None):
        super().__init__(parent)
        self.roi_names = roi_names
        self.dfx_file = ""
        self.dfx_result = None
        self.tag_geometry = {}  # roi_name -> Nx2 array (X um lateral, Y um depth-from-tip)

        layout = QtWidgets.QVBoxLayout(self)

        tag_row = QtWidgets.QHBoxLayout()
        tag_row.addWidget(QtWidgets.QLabel("Tag:"))
        self.combo_tag = QtWidgets.QComboBox()
        self.combo_tag.addItems(roi_names)
        tag_row.addWidget(self.combo_tag)
        self.label_status = QtWidgets.QLabel()
        tag_row.addWidget(self.label_status)
        tag_row.addStretch()
        layout.addLayout(tag_row)

        file_row = QtWidgets.QHBoxLayout()
        self.button_dxf = QtWidgets.QPushButton("Select DXF file...")
        self.button_dxf.clicked.connect(self.browse_dxf_file)
        file_row.addWidget(self.button_dxf)
        layout.addLayout(file_row)

        form = QtWidgets.QFormLayout()
        self.spin_um_per_unit = _make_double_spin(1.0, 0.0001, 1e6, decimals=4)
        self.spin_artificial_extension = _make_double_spin(3000.0, 0.0, 1e6)
        self.spin_first_bend_distance = _make_double_spin(150.0, 0.0, 1e6)
        self.spin_max_theta = _make_double_spin(45.0, 0.0, 90.0)
        self.spin_bundle_ratio = _make_double_spin(0.05, 0.0, 1.0, decimals=3)
        self.spin_bend_r1 = _make_double_spin(300.0, 0.0, 1e6)
        self.spin_bend_r2 = _make_double_spin(300.0, 0.0, 1e6)
        self.spin_arc_points = QtWidgets.QSpinBox()
        self.spin_arc_points.setRange(2, 10000)
        self.spin_arc_points.setValue(100)
        form.addRow("um per DXF unit", self.spin_um_per_unit)
        form.addRow("Artificial extension (um)", self.spin_artificial_extension)
        form.addRow("First bend distance (um)", self.spin_first_bend_distance)
        form.addRow("Max bend angle (deg)", self.spin_max_theta)
        form.addRow("Bundle ratio", self.spin_bundle_ratio)
        form.addRow("Bend radius 1 (um)", self.spin_bend_r1)
        form.addRow("Bend radius 2 (um)", self.spin_bend_r2)
        form.addRow("Arc points", self.spin_arc_points)
        layout.addLayout(form)

        button_row = QtWidgets.QHBoxLayout()
        self.button_run = QtWidgets.QPushButton("Run bending model")
        self.button_run.clicked.connect(self.run_bending)
        self.button_commit = QtWidgets.QPushButton("Use this geometry for tag")
        self.button_commit.clicked.connect(self.commit_geometry)
        button_row.addWidget(self.button_run)
        button_row.addWidget(self.button_commit)
        layout.addLayout(button_row)

        self.plot = pg.PlotWidget(background="k")
        self.plot.setAspectLocked(True)
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        self.plot.setLabel("bottom", "ML from center (um)")
        self.plot.setLabel("left", "Depth from tip (um)")
        self.plot.setMinimumHeight(220)
        layout.addWidget(self.plot)

        self.combo_tag.currentIndexChanged.connect(self._refresh_status)
        self._refresh_status()

    def _refresh_status(self):
        roi = self.combo_tag.currentText()
        if roi in self.tag_geometry:
            self.label_status.setText(f"({self.tag_geometry[roi].shape[0]} contacts committed)")
        else:
            self.label_status.setText("(no geometry committed yet)")

    def browse_dxf_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select the DXF file", "", "DXF files (*.dxf);;All files (*)")
        if not path:
            return
        self.dfx_file = path
        self.button_dxf.setText(os.path.basename(path))
        self.button_dxf.setToolTip(path)

    def run_bending(self):
        if not self.dfx_file:
            QMessageBox.warning(self, "No DXF file", "Please select a DXF file first.")
            return
        try:
            result = bend_dxf_probe_geometry(
                self.dfx_file,
                um_per_dxf_unit=self.spin_um_per_unit.value(),
                artificial_extension=self.spin_artificial_extension.value(),
                first_bend_distance=self.spin_first_bend_distance.value(),
                max_theta_deg=self.spin_max_theta.value(),
                bundle_ratio=self.spin_bundle_ratio.value(),
                bend_radius1=self.spin_bend_r1.value(),
                bend_radius2=self.spin_bend_r2.value(),
                arc_points=self.spin_arc_points.value())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Bending failed", str(exc))
            return
        self.dfx_result = result
        self._draw_geometry(result)

    def _draw_geometry(self, result):
        self.plot.clear()
        e_start = result["Electrode_Start"]
        e_stop = result["Electrode_Stop"]
        dash_pen = pg.mkPen((150, 150, 150), width=1, style=QtCore.Qt.PenStyle.DashLine)
        bent_pen = pg.mkPen((80, 160, 255), width=2)
        for i in range(e_start.shape[0]):
            self.plot.plot([e_start[i, 0], e_stop[i, 0]], [e_start[i, 1], e_stop[i, 1]], pen=dash_pen)
            self.plot.plot(result["xPaths"][i], result["yPaths"][i], pen=bent_pen)
        self.plot.plot(result["Bent_Stop"][:, 0], result["Bent_Stop"][:, 1],
                        pen=None, symbol="o", symbolBrush=(0, 220, 0), symbolSize=6)
        self.plot.autoRange(padding=0.1)

    def commit_geometry(self):
        if self.dfx_result is None:
            QMessageBox.warning(self, "Nothing to commit", "Run the bending model first.")
            return
        roi = self.combo_tag.currentText()
        self.tag_geometry[roi] = self.dfx_result["Bent_Stop"].copy()
        self._refresh_status()
        self._draw_overview()

    def _draw_overview(self):
        self.plot.clear()
        tags = sorted(self.tag_geometry)
        all_x = np.concatenate([self.tag_geometry[t][:, 0] for t in tags])
        x_spread = float(np.max(all_x) - np.min(all_x)) if all_x.size else 0.0
        offset_step = max(x_spread, 1.0) * 1.5
        for i, roi in enumerate(tags):
            geometry = self.tag_geometry[roi]
            color = _TAG_COLORS[i % len(_TAG_COLORS)]
            self.plot.plot(geometry[:, 0] + i * offset_step, geometry[:, 1], pen=None,
                            symbol="o", symbolBrush=color, symbolSize=8, name=roi)
        self.plot.autoRange(padding=0.1)

    def get_depths_um(self):
        """dict[roi_name, np.ndarray | None] of depth-from-tip (um) for
        every roi_name -- None for one still missing committed geometry."""
        depths = {}
        for roi in self.roi_names:
            geometry = self.tag_geometry.get(roi)
            depths[roi] = None if geometry is None else geometry[:, 1].copy()
        return depths
