# This Python file uses the following encoding: utf-8
import os

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout

from electrode2geometry.python.geometry_core import (
    bend_dxf_probe_geometry, read_electrode_centroids, parse_neuroscope_xml,
    write_kilosort_json, parse_channel_text)
from trajectory_planning.shank import NEON_COLORS, _make_color_icon


class DfxGeometry:
    """
    Shank Geometry panel: bends a DXF electrode drawing toward a V-tip
    bundle (electrode2geometry's bending model), lets each shank's bent
    geometry be added to an assembled probe, and exports that probe as a
    Kilosort-style JSON.
    """

    def init_dfx_geometry(self):
        self.dfx_file = ""
        self.dfx_xml_file = ""
        self.dfx_result = None
        self.dfx_n_contacts = None
        self.dfx_xml_groups = []
        self.dfx_xml_nchannels = 0
        self.dfx_shank_data = {}  # shank_number -> {"geometry", "channels", "dxf_file", "result"}

        self.dfx_plot = pg.PlotWidget(background="k")
        self.dfx_plot.setAspectLocked(True)
        self.dfx_plot.showGrid(x=True, y=True, alpha=0.3)
        self.dfx_plot.setLabel("bottom", "ML from center (µm)")
        self.dfx_plot.setLabel("left", "DV (µm)")
        self.dfx_plot.addLegend()
        dfx_layout = QVBoxLayout(self.ui.widget_dfx)
        dfx_layout.setContentsMargins(0, 0, 0, 0)
        dfx_layout.addWidget(self.dfx_plot)

        self.ui.stackedWidget_dfx.setCurrentIndex(0)
        self.ui.pushButton_geometry_dfx.clicked.connect(self.show_dfx_panel)
        self.ui.pushButton_geometry_dfx.clicked.connect(self.show_geometry_step_popup)
        self.ui.pushButton_dfx_ok.clicked.connect(self.hide_dfx_panel)
        self.ui.pushButton_dfx.clicked.connect(self.browse_dfx_file)
        self.ui.pushButton_xml.clicked.connect(self.browse_dfx_xml)
        self.ui.pushButton_dfx_run.clicked.connect(self.run_dfx_bending)
        self.ui.pushButton_plot_probe.clicked.connect(self.add_dfx_shank)
        self.ui.pushButton_export.clicked.connect(self.export_dfx_json)
        self.ui.checkBox_defaultchannels.toggled.connect(self.update_default_channels)

        # Mirrors comboBox_Shanks so a shank can be picked without leaving
        # this panel; both stay in sync via select_shank (shank.py).
        self.ui.comboBox_geometry_shanks.addItem("Shank 1")
        self.ui.comboBox_geometry_shanks.setItemData(0, 0)
        self.ui.comboBox_geometry_shanks.setItemIcon(0, _make_color_icon(0))
        self.ui.comboBox_geometry_shanks.currentIndexChanged.connect(self.select_shank)

    def show_dfx_panel(self):
        self.ui.stackedWidget_dfx.setCurrentIndex(1)
        # If the current shank already has committed geometry, show the
        # final assembled-probe overview (same as right after "Plot Probe"),
        # not the single-shank bending curves; otherwise leave whatever
        # in-progress run is already showing.
        data = self.dfx_shank_data.get(self.shank_number)
        if data is not None:
            self.dfx_result = data["result"]
            self.dfx_n_contacts = data["result"]["Bent_Stop"].shape[0]
            self.draw_dfx_probe_overview()
        elif self.dfx_result is not None:
            self.draw_dfx_geometry(self.dfx_result)

    def hide_dfx_panel(self):
        self.show_insertion_step_popup()
        self.ui.stackedWidget_dfx.setCurrentIndex(0)
        self.ui.stackedWidget_3d.setVisible(True)
        # restore its column so the layout matches the normal (non-hidden)
        # trajectory-planning view (same stretches used elsewhere on show)
        layout = self.ui.page_3D.layout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 1)

        # user-defined geometry is set up per-shank via the dropdown above,
        # so whichever shank was last being bent/reviewed here is likely
        # not shank 1 -- land back on shank 1 (same convention as
        # get_shank_line's own post-setup reset in registration.py) instead
        # of leaving insertion/deepest-point picking pointed at whatever
        # shank happened to be selected when "OK" was clicked.
        self.ui.comboBox_Shanks.setCurrentIndex(0)
        self.select_shank(0)

    def browse_dfx_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self.MW, "Select the DXF file", "",
            "DXF files (*.dxf);;All files (*)")
        if not path:
            return
        self.dfx_file = path
        self.ui.pushButton_dfx.setText(os.path.basename(path))
        self.ui.pushButton_dfx.setToolTip(path)

        # Contact count only depends on the DXF's contours, not on the
        # bending parameters, so the default channel list can already be
        # shown now instead of waiting for "Run bending model".
        try:
            centroids = read_electrode_centroids(
                path, um_per_dxf_unit=self.ui.spinBox_um_per_unit.value())
        except Exception:  # noqa: BLE001
            return
        self.dfx_n_contacts = centroids.shape[0]
        self._fill_default_channel_text(self.dfx_n_contacts)

    def browse_dfx_xml(self):
        path, _ = QFileDialog.getOpenFileName(
            self.MW, "Select the Neuroscope XML file", "",
            "Neuroscope XML (*.xml);;All files (*)")
        if not path:
            return
        try:
            groups, n_channels, _skip = parse_neuroscope_xml(path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self.MW, "XML parse failed", str(exc))
            return
        if not groups:
            QMessageBox.warning(self.MW, "Empty XML",
                                "No channel groups were found in the XML.")
            return

        self.dfx_xml_file = path
        self.dfx_xml_groups = groups
        self.dfx_xml_nchannels = n_channels
        self.ui.pushButton_xml.setText(os.path.basename(path))

        idx = min(self.shank_number, len(groups) - 1)
        self.ui.textEdit_channels_xml.setPlainText(
            " ".join(str(int(c)) for c in groups[idx]))
        self.ui.checkBox_defaultchannels.setChecked(False)

    def run_dfx_bending(self):
        if not self.dfx_file:
            QMessageBox.warning(self.MW, "No DXF file",
                                "Please select a DXF file first.")
            return
        if not os.path.isfile(self.dfx_file):
            QMessageBox.critical(self.MW, "File missing",
                                 f"DXF file not found:\n{self.dfx_file}")
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
            QMessageBox.critical(self.MW, "Bending failed", str(exc))
            return

        self.dfx_result = result
        self.dfx_n_contacts = result["Bent_Stop"].shape[0]
        self._fill_default_channel_text(self.dfx_n_contacts)
        self.draw_dfx_geometry(result)

    def _fill_default_channel_text(self, n):
        self.ui.textEdit_channels_xml.setPlainText(" ".join(str(i) for i in range(n)))

    def update_default_channels(self):
        """Re-fill with 0..n-1 when the checkbox is (re-)checked. Does
        nothing on uncheck, so it never clobbers manually typed channels."""
        if self.dfx_n_contacts is None or not self.ui.checkBox_defaultchannels.isChecked():
            return
        self._fill_default_channel_text(self.dfx_n_contacts)

    def refresh_dfx_channel_display(self):
        """Called from select_shank (shank.py) whenever the current shank
        changes, so the panel shows that shank's already-committed channel
        list (if "Plot Probe" was already used for it) instead of leaving
        the previous shank's text behind. Signals are blocked while setting
        the checkbox so this doesn't trigger update_default_channels() and
        overwrite the text with the (possibly unrelated) current run's
        default list."""
        data = self.dfx_shank_data.get(self.shank_number)
        self.ui.checkBox_defaultchannels.blockSignals(True)
        if data is None:
            self.ui.textEdit_channels_xml.clear()
            self.ui.checkBox_defaultchannels.setChecked(True)
        else:
            channels = data["channels"]
            self.ui.textEdit_channels_xml.setPlainText(
                " ".join(str(int(c)) for c in channels))
            self.ui.checkBox_defaultchannels.setChecked(
                bool(np.array_equal(channels, np.arange(channels.size))))
        self.ui.checkBox_defaultchannels.blockSignals(False)

        # Show the final assembled-probe overview again (same as right
        # after "Plot Probe") if this shank already has committed geometry,
        # instead of leaving the previous shank's view on screen under the
        # new shank's channel list.
        if data is not None:
            self.dfx_result = data["result"]
            self.dfx_n_contacts = data["result"]["Bent_Stop"].shape[0]
            self.draw_dfx_probe_overview()
        else:
            self.dfx_result = None
            self.dfx_n_contacts = None
            self.dfx_plot.clear()

    def _resolve_channels(self, n):
        """Channel-ID array for `n` contacts from the checkbox/text box, or
        None (after warning) if a manually entered list doesn't match."""
        if self.ui.checkBox_defaultchannels.isChecked():
            return np.arange(n)
        channels = parse_channel_text(self.ui.textEdit_channels_xml.toPlainText())
        if channels.size != n:
            QMessageBox.warning(
                self.MW, "Count mismatch",
                f"Channel count ({channels.size}) does not match the "
                f"number of contacts in this run ({n}).")
            return None
        return channels

    def add_dfx_shank(self):
        """Plot Probe": commit the current bend result as this shank's
        geometry, then redraw the whole assembled probe (all shanks so far,
        colour-coded like the 3D view)."""
        if self.dfx_result is None:
            QMessageBox.warning(
                self.MW, "Nothing to add",
                "Run the bending model first, then Plot Probe to add it "
                "as this shank's geometry.")
            return

        geometry = self.dfx_result["Bent_Stop"]
        channels = self._resolve_channels(geometry.shape[0])
        if channels is None:
            return

        self.dfx_shank_data[self.shank_number] = {
            "geometry": geometry.copy(), "channels": channels,
            "dxf_file": self.dfx_file, "result": self.dfx_result}
        self.draw_dfx_probe_overview()

        # channel_points (read by the 2D shank line/table AND by
        # Visualisation3D's clipped 3D views) only gets (re)computed inside
        # create_channel_list -- without this call the 3D view would keep
        # showing the old uniform-spacing points until something else
        # (e.g. nudging a deep/insert spinbox) happened to re-trigger it.
        if (self.coords_deepest_point.get(self.shank_number) is not None
                and self.coords_insert_point.get(self.shank_number) is not None):
            self.create_channel_list()

    def draw_dfx_geometry(self, result):
        """Detailed preview of the current (not-yet-committed) bend run."""
        self.dfx_plot.clear()
        e_start = result["Electrode_Start"]
        e_stop = result["Electrode_Stop"]
        n = e_start.shape[0]

        dash_pen = pg.mkPen((150, 150, 150), width=1,
                            style=QtCore.Qt.PenStyle.DashLine)
        bent_pen = pg.mkPen((80, 160, 255), width=2)
        center_pen = pg.mkPen((255, 60, 60), width=2)

        for i in range(n):
            self.dfx_plot.plot([e_start[i, 0], e_stop[i, 0]],
                               [e_start[i, 1], e_stop[i, 1]], pen=dash_pen)
            self.dfx_plot.plot(result["xPaths"][i], result["yPaths"][i],
                               pen=bent_pen)

        self.dfx_plot.plot(
            [result["centerLineStart"][0], result["centerLineStop"][0]],
            [result["artificialY_um"], 0], pen=center_pen)
        self.dfx_plot.plot(e_start[:, 0], e_start[:, 1], pen=None,
                           symbol="o", symbolBrush=(0, 0, 0), symbolSize=6)
        self.dfx_plot.plot(e_stop[:, 0], e_stop[:, 1], pen=None,
                           symbol="o", symbolBrush=(230, 0, 230), symbolSize=6)
        self.dfx_plot.plot(result["Bent_Stop"][:, 0], result["Bent_Stop"][:, 1],
                           pen=None, symbol="o", symbolBrush=(0, 220, 0),
                           symbolSize=6)

        self._fit_and_limit_view()

    def draw_dfx_probe_overview(self):
        """Assembled multi-shank probe: final contact dots, colour-coded
        the same way each shank is coloured in the 3D view. Each shank gets
        a slight horizontal offset (display-only -- the stored/exported
        geometry is untouched) so overlapping/bundled shanks can still be
        told apart and compared side-by-side."""
        self.dfx_plot.clear()
        shank_order = sorted(self.dfx_shank_data)
        all_x = np.concatenate(
            [self.dfx_shank_data[s]["geometry"][:, 0] for s in shank_order])
        x_spread = float(np.max(all_x) - np.min(all_x)) if all_x.size else 0.0
        offset_step = max(x_spread, 1.0) * 1.5

        for plot_idx, shank_idx in enumerate(shank_order):
            geometry = self.dfx_shank_data[shank_idx]["geometry"]
            color = NEON_COLORS[self.shank_colors.get(shank_idx, 0)][1]
            x_offset = plot_idx * offset_step
            self.dfx_plot.plot(geometry[:, 0] + x_offset, geometry[:, 1], pen=None,
                               symbol="o", symbolBrush=color, symbolSize=8,
                               name=f"Shank {shank_idx + 1}")

        self._fit_and_limit_view()

    def _fit_and_limit_view(self):
        # Fit the view to what was just drawn, rather than keeping whatever
        # pan/zoom was left over from the previous plot...
        self.dfx_plot.autoRange(padding=0.1)

        # ...then cap how far the user can pan/zoom out beyond that, so the
        # shank(s) never get lost in an empty black viewport.
        view_box = self.dfx_plot.getViewBox()
        (xmin, xmax), (ymin, ymax) = view_box.viewRange()
        x_span, y_span = xmax - xmin, ymax - ymin
        x_pad, y_pad = x_span * 0.75, y_span * 0.75
        view_box.setLimits(xMin=xmin - x_pad, xMax=xmax + x_pad,
                           yMin=ymin - y_pad, yMax=ymax + y_pad,
                           maxXRange=x_span * 2.5, maxYRange=y_span * 2.5)

    def export_dfx_json(self):
        if not self.dfx_shank_data:
            QMessageBox.warning(
                self.MW, "Nothing to export",
                "Run the bending model and click 'Plot Probe' to add at "
                "least one shank first.")
            return

        geometries, channels_list, shanks_list = [], [], []
        for shank_idx in sorted(self.dfx_shank_data):
            data = self.dfx_shank_data[shank_idx]
            geometries.append(data["geometry"])
            channels_list.append(data["channels"])
            shanks_list.append(np.full(data["channels"].size, shank_idx + 1,
                                       dtype=int))

        geometry = np.vstack(geometries)
        channels = np.concatenate(channels_list)
        shank = np.concatenate(shanks_list)
        n_chan_total = (self.dfx_xml_nchannels if self.dfx_xml_nchannels > 0
                        else int(channels.max()) + 1)

        default_dir = os.path.dirname(self.dfx_file) if self.dfx_file else ""
        out_path, _ = QFileDialog.getSaveFileName(
            self.MW, "Export probe geometry",
            os.path.join(default_dir, "probe_geometry.json"),
            "JSON files (*.json)")
        if not out_path:
            return

        try:
            write_kilosort_json(out_path, channels, geometry, shank, n_chan_total)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self.MW, "Export failed", str(exc))
            return

        QMessageBox.information(
            self.MW, "Exported",
            f"Saved {channels.size} contacts across "
            f"{len(self.dfx_shank_data)} shank(s) to:\n{out_path}")
