# This Python file uses the following encoding: utf-8
"""
Adapts trajectory planning's own Shank Geometry widget (page_24, inside
stackedWidget_dfx/page_3D -- defined once in form.ui) for 4D electrode
localisation's ChannelVariablesInput / ElectrodeLoc._show_geometry_page
flow, instead of rebuilding an equivalent panel from scratch in code.
stackedWidget_dfx is a single widget instance shared with trajectory
planning (TrajectoryPlanning and ElectrodeLoc both receive the same
MainWindow.ui) -- ElectrodeLoc._show_geometry_page reparents it out of
page_3D for the duration of this panel's use, and trajectory planning's
DfxGeometry.reclaim_dfx_widget rewires it back to itself afterwards.
"""
import os

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtWidgets import QFileDialog, QMessageBox

from electrode2geometry.python.geometry_core import bend_dxf_probe_geometry
from trajectory_planning.dfx_geometry import ensure_dfx_plot
from trajectory_planning.shank import NEON_COLORS, _make_color_icon


class Dfx4DGeometry:
    """One DXF-bending session over page_24, keyed per ROI tag
    (self.tag_geometry) instead of per shank. page_24's channel-ID/
    Neuroscope-XML controls are hidden for the duration -- channel_mapper.py
    only ever needs each tag's depths, not a channel mapping."""

    def __init__(self, ui, roi_names):
        self.ui = ui
        self.roi_names = list(roi_names)
        self.dfx_file = ""
        self.dfx_result = None
        self.dfx_n_contacts = None
        self.tag_geometry = {}  # roi_name -> {"geometry": Nx2 array, "result": dict}
        self.current_tag = self.roi_names[0]

        self.dfx_plot = ensure_dfx_plot(self.ui.widget_dfx)

        combo = self.ui.comboBox_geometry_shanks
        combo.blockSignals(True)
        combo.clear()
        for i, roi in enumerate(self.roi_names):
            combo.addItem(_make_color_icon(i % len(NEON_COLORS)), roi)
        combo.blockSignals(False)

        for signal, slot in (
            (self.ui.pushButton_dfx.clicked, self.browse_dfx_file),
            (self.ui.pushButton_dfx_run.clicked, self.run_dfx_bending),
            (self.ui.pushButton_plot_probe.clicked, self.commit_tag_geometry),
            (self.ui.comboBox_geometry_shanks.currentIndexChanged, self.select_tag),
        ):
            try:
                signal.disconnect()
            except (TypeError, RuntimeError):
                pass
            signal.connect(slot)

        # Channel/XML controls don't map to anything here (get_depths_um
        # only reads geometry Y) -- hidden rather than removed, so
        # DfxGeometry.reclaim_dfx_widget can simply show them again.
        self.ui.pushButton_xml.setVisible(False)
        self.ui.textEdit_channels_xml.setVisible(False)
        self.ui.checkBox_defaultchannels.setVisible(False)

        self.ui.stackedWidget_dfx.setCurrentIndex(1)
        self.select_tag(0)

    def select_tag(self, index):
        self.current_tag = self.roi_names[index]
        data = self.tag_geometry.get(self.current_tag)
        if data is None:
            self.dfx_result = None
            self.dfx_n_contacts = None
            self.dfx_plot.clear()
        else:
            self.dfx_result = data["result"]
            self.dfx_n_contacts = data["result"]["Bent_Stop"].shape[0]
            self._draw_overview()

    def browse_dfx_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self.ui.pushButton_dfx.window(), "Select the DXF file", "",
            "DXF files (*.dxf);;All files (*)")
        if not path:
            return
        self.dfx_file = path
        self.ui.pushButton_dfx.setText(os.path.basename(path))
        self.ui.pushButton_dfx.setToolTip(path)

    def run_dfx_bending(self):
        if not self.dfx_file:
            QMessageBox.warning(self.ui.pushButton_dfx_run.window(), "No DXF file",
                                 "Please select a DXF file first.")
            return
        try:
            result = bend_dxf_probe_geometry(
                self.dfx_file,
                um_per_dxf_unit=self.ui.spinBox_um_per_unit.value(),
                artificial_extension=self.ui.spinBox_artificial_extension.value(),
                first_bend_distance=self.ui.spinBox_first_bend_distance.value(),
                max_theta_deg=self.ui.spinBox_max_bend_angle.value(),
                bundle_ratio=self.ui.doubleSpinBox_bundle_ratio.value(),
                bend_radius1=self.ui.spinBox_bend_r1.value(),
                bend_radius2=self.ui.spinBox_bend_r2.value(),
                arc_points=self.ui.spinBox_arc_points.value())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self.ui.pushButton_dfx_run.window(), "Bending failed", str(exc))
            return
        self.dfx_result = result
        self.dfx_n_contacts = result["Bent_Stop"].shape[0]
        self._draw_geometry(result)

    def _draw_geometry(self, result):
        """Detailed preview of the current (not-yet-committed) bend run."""
        self.dfx_plot.clear()
        e_start = result["Electrode_Start"]
        e_stop = result["Electrode_Stop"]
        dash_pen = pg.mkPen((150, 150, 150), width=1, style=QtCore.Qt.PenStyle.DashLine)
        bent_pen = pg.mkPen((80, 160, 255), width=2)
        for i in range(e_start.shape[0]):
            self.dfx_plot.plot([e_start[i, 0], e_stop[i, 0]], [e_start[i, 1], e_stop[i, 1]], pen=dash_pen)
            self.dfx_plot.plot(result["xPaths"][i], result["yPaths"][i], pen=bent_pen)
        self.dfx_plot.plot(result["Bent_Stop"][:, 0], result["Bent_Stop"][:, 1],
                            pen=None, symbol="o", symbolBrush=(0, 220, 0), symbolSize=6)
        self.dfx_plot.autoRange(padding=0.1)

    def commit_tag_geometry(self):
        """"Plot Probe": commit the current bend result as this tag's
        geometry, then redraw the whole assembled overview (all tags
        committed so far)."""
        if self.dfx_result is None:
            QMessageBox.warning(self.ui.pushButton_plot_probe.window(), "Nothing to add",
                                 "Run the bending model first, then Plot Probe to commit it.")
            return
        self.tag_geometry[self.current_tag] = {
            "geometry": self.dfx_result["Bent_Stop"].copy(), "result": self.dfx_result}
        self._draw_overview()

    def _draw_overview(self):
        """Assembled multi-tag overview, each tag offset horizontally
        (display-only) so overlapping/bundled tags can be told apart --
        same technique as DfxGeometry.draw_dfx_probe_overview."""
        self.dfx_plot.clear()
        tags = sorted(self.tag_geometry)
        if not tags:
            return
        all_x = np.concatenate([self.tag_geometry[t]["geometry"][:, 0] for t in tags])
        x_spread = float(np.max(all_x) - np.min(all_x)) if all_x.size else 0.0
        offset_step = max(x_spread, 1.0) * 1.5
        for i, roi in enumerate(tags):
            geometry = self.tag_geometry[roi]["geometry"]
            color = NEON_COLORS[i % len(NEON_COLORS)][1]
            self.dfx_plot.plot(geometry[:, 0] + i * offset_step, geometry[:, 1], pen=None,
                                symbol="o", symbolBrush=color, symbolSize=8, name=roi)
        self.dfx_plot.autoRange(padding=0.1)

    def get_depths_um(self):
        """dict[roi_name, np.ndarray | None] of depth-from-tip (um) for
        every roi_name -- None for one still missing committed geometry."""
        depths = {}
        for roi in self.roi_names:
            data = self.tag_geometry.get(roi)
            depths[roi] = None if data is None else data["geometry"][:, 1].copy()
        return depths
