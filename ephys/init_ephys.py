# This Python file uses the following encoding: utf-8
from ephys.visualisation3D import Visualisation3D
import os
from PySide6 import QtWidgets
import pandas as pd
import pyvista as pv
import numpy as np
from ephys.ephysrecording import EphysRecording
from ephys.mrid_info import MRIDInfo
from ephys.visualisationEphys import VisualisationEphys
import xml.etree.ElementTree as ET
from ephys.change_anatRegion import Change_AnatRegion
from ephys_utils.filter_data import FilterData
from ephys_utils.lfp_creation_dialog import LFPCreationDialog
from ephys_utils.spiking_ruster import SpikeRuster
from ephys_utils.lfp_spectrogram import LFPSpectrogram
from ephys_utils.csd_widget import CSDWidget
from ephys_utils.all_channels_spectrogram import AllChannelsSpectrogram
from ephys_utils import theta_detection
from ephys_utils.hierarchical_clustering import (
    build_activity_matrix, compute_correlation_matrix,
    hierarchical_clustering, load_custom_colormap
)
from gui_utils.busy_overlay import BusyOverlay
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt
import subprocess
import tempfile
import pathlib
import json
from PySide6.QtWidgets import QTableWidgetItem
import numpy
from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QLabel, QButtonGroup
from ephys.videoplayer import VideoPlayer


class _RotatedLabelAxis(pg.AxisItem):
    """Bottom axis whose tick labels are drawn rotated 90° (vertical)."""
    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):
        p.setRenderHint(p.RenderHint.Antialiasing, False)
        p.setRenderHint(p.RenderHint.TextAntialiasing, True)
        pen, p1, p2 = axisSpec
        p.setPen(pen)
        p.drawLine(p1, p2)
        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)
        if self.style['tickFont'] is not None:
            p.setFont(self.style['tickFont'])
        p.setPen(self.textPen())
        p.setClipRect(self.boundingRect().toAlignedRect())
        for rect, flags, text in textSpecs:
            p.save()
            cx, cy = rect.center().x(), rect.center().y()
            p.translate(cx, cy)
            p.rotate(-90)
            p.translate(-cx, -cy)
            p.drawText(rect, int(flags), text)
            p.restore()

##TODO
#os.path.join(filename[:-4] + '.xml')
#xml_file,flush=True)
#xml -> mapp, tells you the order
#- number of channels
#- 16bits -> int16 (plus und minus Werte)
#- Hz
#- groups… (each has their own visualisation window); ich glaube pro tag 1group
#- dead channels (if skip=1), aber option haben

class InitEphys:
    def __init__(self, MW,filename):
        self.MW = MW
        #self.first_time = True
        self.session_path = os.path.dirname(os.path.dirname(os.path.dirname(filename)))

        self.MW.ui.pushButton_anatRegion.clicked.connect(self.changeRegion)

        self.MW.ui.pushButton_AddVideo.clicked.connect(self.add_video)

        self.mrid_info = MRIDInfo.from_file(filename,self.session_path,group_idx=0)
        self.ephys_data = EphysRecording.from_file(filename,group_idx=0)

        self.Visualisation3D = Visualisation3D(self.session_path,self.MW,chMap=self.ephys_data.all_channels,Ephys=self)
        self.Visualisation3D.initialize_mridTag(self.mrid_info.mrid,chMap=self.ephys_data.all_channels)
        self.VisEphys = VisualisationEphys(self.MW,self.Visualisation3D,self)

        # No LFP file yet: confirm/correct the XML-parsed parameters, then create it.
        if self.ephys_data.lfp_memmap is None:
            LFPCreationDialog(self.MW, self.ephys_data).exec()

        self.MW.ui.pushButton_broadband.clicked.connect(self.VisEphys.show_broadband)
        self.MW.ui.pushButton_lfp.clicked.connect(self.VisEphys.show_lfp)
        self.MW.ui.actionRippl_AI.triggered.connect(self.detect_ripples)
        self.MW.ui.actionTheta_Detection.triggered.connect(self.detect_theta)
        self.MW.ui.actionLoad_Spike_Sorting.triggered.connect(lambda: self.load_spike_sorting())
        # only usable once ephys data is actually loaded (this method is that signal)
        self.MW.ui.actionRippl_AI.setEnabled(True)
        self.MW.ui.actionTheta_Detection.setEnabled(True)
        self.MW.ui.actionLoad_Spike_Sorting.setEnabled(True)

        # embed spike raster into widget_spike_ruster (reuse its existing layout)
        self.spike_ruster = SpikeRuster(self.MW.ui.widget_spike_ruster)
        raster_layout = self.MW.ui.widget_spike_ruster.layout()
        raster_layout.setContentsMargins(0, 0, 0, 0)
        raster_layout.addWidget(self.spike_ruster)
        self.VisEphys.spike_ruster = self.spike_ruster

        # one LFP spectrogram over the whole band, in the "Spectogram" tab of
        # tabWidget_LFP. Kept in a list because the timeline/channel-follow code
        # in pgwidget and VisEphys iterates VisEphys.spectrograms.
        container = self.MW.ui.widget_Spectogram_ripple
        self.lfp_spectrogram = LFPSpectrogram(
            container, label=getattr(self.MW.ui, 'lineEdit_ripple', None))
        spec_layout = container.layout()
        if spec_layout is None:
            spec_layout = QVBoxLayout(container)
        spec_layout.setContentsMargins(0, 0, 0, 0)
        spec_layout.addWidget(self.lfp_spectrogram)
        self.VisEphys.spectrograms = [self.lfp_spectrogram]

        # "Change Axis" flips the frequency axis log <-> linear (it re-runs the
        # CWT, because the analysed frequencies have to match the axis), and
        # "ColorMap" cycles jet <-> RdBu_r. Both buttons show the current state.
        self.MW.ui.pushButton_axisLog.setCheckable(True)
        self.MW.ui.pushButton_axisLog.setChecked(self.lfp_spectrogram.log_freq)
        self.MW.ui.pushButton_axisLog.toggled.connect(self._set_spectrogram_log_axis)
        self._set_spectrogram_log_axis(self.lfp_spectrogram.log_freq)

        self.MW.ui.pushButton_colorMap.clicked.connect(self._cycle_spectrogram_colormap)
        self.MW.ui.pushButton_colorMap.setText(
            f"ColorMap: {self.lfp_spectrogram.colormap_name}")

        # embed kCSD heatmap into widget_CSD
        self.csd_widget = CSDWidget(self.MW.ui.widget_CSD)
        csd_layout = self.MW.ui.widget_CSD.layout()
        if csd_layout is None:
            csd_layout = QVBoxLayout(self.MW.ui.widget_CSD)
        csd_layout.setContentsMargins(0, 0, 0, 0)
        csd_layout.addWidget(self.csd_widget)
        self.VisEphys.csd_widget = self.csd_widget

        # frequency x channel map at the middle of the visible window, in the
        # "Spectogram all Channels" tab
        container = self.MW.ui.widget_Spectogram_allChannels
        self.channel_spectrogram = AllChannelsSpectrogram(container)
        all_ch_layout = container.layout()
        if all_ch_layout is None:
            all_ch_layout = QVBoxLayout(container)
        all_ch_layout.setContentsMargins(0, 0, 0, 0)
        all_ch_layout.addWidget(self.channel_spectrogram)
        self.VisEphys.channel_spectrogram = self.channel_spectrogram

        # pushButton_allChannels_axis flips the all-channels map between linear
        # and log Hz on the x axis (it re-runs the CWT so the analysed
        # frequencies match the axis, like pushButton_axisLog does for the
        # single-channel spectrogram). The log axis is labelled 10, 20, 30 …
        self.MW.ui.pushButton_allChannels_axis.setCheckable(True)
        self.MW.ui.pushButton_allChannels_axis.setChecked(
            self.channel_spectrogram.log_freq)
        self.MW.ui.pushButton_allChannels_axis.toggled.connect(
            self._set_allChannels_log_axis)
        self._set_allChannels_log_axis(self.channel_spectrogram.log_freq)

        # pushButton_Timeframe_spectogram flips the all-channels map between
        # the current window and the session-wide ripple-triggered average
        # (±25 ms around every detected ripple), like Peter's MATLAB script.
        self.MW.ui.pushButton_Timeframe_spectogram.setCheckable(True)
        self.MW.ui.pushButton_Timeframe_spectogram.setChecked(
            self.channel_spectrogram.ripple_mode)
        self.MW.ui.pushButton_Timeframe_spectogram.toggled.connect(self._set_allChannels_ripple_mode)
        self._set_allChannels_ripple_mode(self.channel_spectrogram.ripple_mode)

        # ripple-triggered mode runs on a background thread (can take minutes on
        # a session with many ripples); block the buttons that would start an
        # overlapping run while one is in flight, mirroring the BusyOverlay it shows.
        self.channel_spectrogram.busyChanged.connect(self._set_allChannels_busy)

        btn_group = QButtonGroup(self.MW)
        btn_group.addButton(self.MW.ui.pushButton_broadband)
        btn_group.addButton(self.MW.ui.pushButton_lfp)
        self.MW.ui.pushButton_broadband.setChecked(True)

        btn_group = QButtonGroup(self.MW)
        btn_group.addButton(self.MW.ui.pushButton_zoomIn)
        btn_group.addButton(self.MW.ui.pushButton_timeline)
        btn_group.addButton(self.MW.ui.pushButton_selectTime)
        btn_group.addButton(self.MW.ui.pushButton_measurement)
        # timeline is the default tool. It has to be set explicitly: rubber-band
        # zoom is the `else` branch of the mode test in pgwidget.mousePressEvent,
        # so with nothing checked in this group a left drag always zooms.
        self.MW.ui.pushButton_timeline.setChecked(True)

        self.Filter = FilterData(MW)

        # default channels for the Filter popup (frame_filterchannels): the last two CA1 channels
        ca1_channels = self.Visualisation3D.get_last_ca1_channels(n=2)
        if ca1_channels:
            self.MW.ui.lineEdit_selectedChannels.setText(', '.join(str(c) for c in ca1_channels))

        # default frequency range: theta band
        self.MW.ui.doubleSpinBox_lowerFreq.setValue(4.0)
        self.MW.ui.doubleSpinBox_upperFreq.setValue(10.0)

        # live-update the heatmap colours when the limit changes (no re-clustering)
        self.MW.ui.doubleSpinBox_ClusterLimits.valueChanged.connect(self._update_cluster_clim)
        self.MW.ui.tabWidget_LFP.setCurrentIndex(0)

        self.MW.ui.horizontalSlider_ElectrodeRegion.valueChanged.connect(self.Visualisation3D.change_opacityRegionOfInterest)
        self.MW.ui.horizontalSlider_OtherRegions.valueChanged.connect(self.Visualisation3D.change_opacityOtherRegions)
        self.MW.ui.horizontalSlider_Background.valueChanged.connect(self.Visualisation3D.change_opacityBackground)
        self.MW.ui.tabWidget_ephys.setCurrentIndex(0)

    def _set_spectrogram_log_axis(self, checked):
        """pushButton_axisLog: log or linear frequency axis on the spectrogram."""
        self.lfp_spectrogram.set_log_frequency(checked)
        self.MW.ui.pushButton_axisLog.setText(
            "Axis: log Hz" if checked else "Axis: linear Hz")

    def _set_allChannels_log_axis(self, checked):
        """pushButton_allChannels_axis: log or linear frequency axis on the
        all-channels spectrogram."""
        self.channel_spectrogram.set_log_frequency(checked)
        self.MW.ui.pushButton_allChannels_axis.setText(
            "Axis: log Hz" if checked else "Axis: linear Hz")

    def _set_allChannels_ripple_mode(self, checked):
        """pushButton_Timeframe_spectogram: entire visible window vs.
        session-wide ripple-triggered average on the all-channels spectrogram."""
        self.channel_spectrogram.set_ripple_mode(checked)
        self.MW.ui.pushButton_Timeframe_spectogram.setText(
            "Timeframe: Around Ripple (±25ms)" if checked
            else "Timeframe: Entire Frame")

    def _set_allChannels_busy(self, busy):
        """channel_spectrogram.busyChanged: block the buttons that would start
        another ripple-triggered computation while one is already running."""
        self.MW.ui.pushButton_Timeframe_spectogram.setEnabled(not busy)
        self.MW.ui.pushButton_allChannels_axis.setEnabled(not busy)

    def _cycle_spectrogram_colormap(self):
        """pushButton_colorMap: step through LFPSpectrogram.COLORMAPS."""
        name = self.lfp_spectrogram.toggle_colormap()
        self.MW.ui.pushButton_colorMap.setText(f"ColorMap: {name}")

    def open_dat_newly(self,filename):
        self.ephys_data = EphysRecording.from_file(filename,self.mrid_info.xml_group_idx )

        self.Visualisation3D.index = self.mrid_info.xml_group_idx
        #self.mrid_info.mrid = list(self.mrid_info.mrid_coordinates.keys())[self.mrid_info.xml_group_idx]
        if self.Visualisation3D.spinbox is not None:
            self.Visualisation3D.spinbox.blockSignals(True)
        self.Visualisation3D.table_excel.blockSignals(True)
        self.Visualisation3D.initialize_mridTag(self.mrid_info.mrid,chMap=self.ephys_data.all_channels)
        if self.Visualisation3D.spinbox is not None:
            self.Visualisation3D.spinbox.blockSignals(False)
        self.Visualisation3D.fill_table(self.ephys_data.all_channels,self.ephys_data.dead_channels)
        self.Visualisation3D.table_excel.blockSignals(False)

        self.open_dat(filename,self.mrid_info.xml_group_idx)


    def open_dat(self,filename,group_idx=0):
        self.MW.ui.widget_pgEphys.init_PgWidget_class(self.VisEphys,self.MW)

        self.VisEphys.visualize_data(self.ephys_data.active_channels)
        self.Visualisation3D.manually_pick_point(point=[],idx=self.ephys_data.all_channels.index(self.ephys_data.active_channels[0]))
        self.Visualisation3D.plotter.enable_parallel_projection()

        self.load_existing_ripples()
        self.load_existing_theta()

        # compute the LFP spectrogram, CSD and all-channels spectrogram once now,
        # regardless of which tabWidget_LFP tab is in front -- so the first click
        # on any of them shows an already-computed map instead of the compute
        # happening right then
        self.VisEphys.prewarm_tabs()

        # tag/shank changed: re-filter the spike raster and the clustering that
        # is computed from it to the new group
        if getattr(self.spike_ruster, '_all_spike_units', None) is not None:
            region_map, color_map = self._channel_maps()
            self.spike_ruster.apply_group(region_map, color_map)
            self.spike_ruster.update_view(self.VisEphys.time_start, self.VisEphys.time_end)
            self.refresh_clustering()

    def _channel_maps(self):
        """For the currently selected group/tag, build:
          region_map : {channel_id: region_label}
          color_map  : {channel_id: (r,g,b,a)} matching the ephys trace colors
        Key order follows chMap (probe order)."""
        vis = self.Visualisation3D
        dead = set(self.ephys_data.dead_channels)
        region_map, color_map = {}, {}
        if getattr(vis, 'points_data', None) is not None and hasattr(vis, 'chMap'):
            max_idx = vis.atlaslabelsdf['IDX'].max()
            for i, ch in enumerate(vis.chMap):
                if ch in dead:
                    continue   # skip skipped channels
                region_map[ch] = str(vis.points_data.iloc[i]['Channel Label'])
                channel_id = vis.points_data['Channel'].iloc[i]
                r, g, b, a = vis.cmap(channel_id / max_idx)
                color_map[ch] = (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
        return region_map, color_map

    def refresh_spike_raster(self):
        """Re-filter the spike raster to the current channels (e.g. after a
        channel was skipped/unskipped). No-op if no spike data is loaded."""
        if getattr(self.spike_ruster, '_all_spike_units', None) is None:
            return
        region_map, color_map = self._channel_maps()
        self.spike_ruster.apply_group(region_map, color_map)
        self.spike_ruster.update_view(self.VisEphys.time_start, self.VisEphys.time_end)
        self.refresh_clustering()

    def refresh_clustering(self):
        """Recompute the hierarchical clustering for the units of the tag/shank
        that is selected now. The raster has to be re-filtered first, this works
        on the units it kept. No-op if there is nothing to cluster."""
        sr = getattr(self, 'spike_ruster', None)
        if sr is None or getattr(sr, '_spike_times', None) is None:
            return
        if len(sr._unit_ids) < 2:
            # nothing to correlate on this shank; drop the previous shank's
            # heatmap instead of leaving it up as if it belonged here
            self._clear_clustering()
            return
        self.run_hierarchical_clustering()

    def _clear_clustering(self):
        """Remove the clustering heatmap currently embedded, if any."""
        layout = self.MW.ui.widget_hierClustering.layout()
        for old in getattr(self, '_hier_widgets', []):
            if layout is not None:
                layout.removeWidget(old)
            old.setParent(None)
            old.deleteLater()
        self._hier_widgets = []

    def load_existing_ripples(self):
        """After ephys loading: if a saved ripple file exists, draw the events and
        jump to the ripple-navigation page (index 1); otherwise show the detection
        page (index 0)."""
        save_path = str(pathlib.Path(self.ephys_data.lfp_path).with_suffix('')) + '_ripples.npy'
        print(save_path,flush=True)
        if os.path.exists(save_path):
            events = numpy.load(save_path)
            self.VisEphys.draw_ripple_events(events, save_path=save_path)
            self.MW.ui.stackedWidget_ripplAI.setCurrentIndex(0)
        else:
            self.MW.ui.stackedWidget_ripplAI.setCurrentIndex(1)


    def change_xml_file(self,channel_idx:int,skip):
        tree = ET.parse(self.ephys_data.xml_path)
        root = tree.getroot()

        for idx, group in enumerate(root.findall('.//anatomicalDescription/channelGroups/group')):
            if idx == self.mrid_info.xml_group_idx:
                for ch in group.findall('channel'):
                    if int(ch.text) == int(channel_idx):
                        ch.set('skip', str(skip))
                        break

        tree.write(self.ephys_data.xml_path, xml_declaration=True, encoding="utf-8")

    def change_mridTAG_combobox(self):
        dialog = QDialog(self.MW)
        dialog.setWindowTitle("Select new MRID TAG")
        layout = QVBoxLayout()

        label = QLabel("Choose:")
        combo = QComboBox()
        combo_items = []
        for i, mrid in enumerate(self.mrid_info.mrid_coordinates):
            text = f"{mrid} (Channel Group: {i})"
            combo_items.append(text)

        combo.addItems(combo_items)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addWidget(QLabel("Please select in the Combobox the new Tag"))
        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            self.change_mridTAG(combo.currentIndex())


    def change_mridTAG(self,new_index):
        self.mrid_info.xml_group_idx = new_index
        self.mrid_info.mrid = list(self.mrid_info.mrid_coordinates.keys())[self.mrid_info.xml_group_idx] #'trio' #A->0

        overlay = BusyOverlay(self.MW, "Loading tag, please wait…")
        overlay.setGeometry(self.MW.rect())
        overlay.raise_()
        overlay.show()
        QApplication.processEvents()

        del self.Visualisation3D.chMap
        self.open_dat_newly(self.ephys_data.file_path)

        overlay.close()



    def changeRegion(self):
        dlg = Change_AnatRegion(self.MW)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_label_text = self.MW.ui.comboBox_ChangeanatRegion.currentText().split('(')[0].strip()
            points_electrodes_path = os.path.join(os.path.join(self.session_path,"analysed"),self.mrid_info.mrid,'channel_atlas_coordinates.xlsx')
            self.points_data = pd.read_excel(points_electrodes_path,header=0)

            new_index = self.Visualisation3D._label_to_atlas_index(new_label_text)
            new_label = self.Visualisation3D.atlaslabelsdf['LABEL'].values[new_index]
            new_idx = self.Visualisation3D.atlaslabelsdf['IDX'].values[new_index]

            # current channel comes from the selected table row (col 1 = channel number)
            row = self.Visualisation3D.table_excel.currentRow()
            channel_value = int(self.Visualisation3D.table_excel.item(row, 1).text())
            channel_numb = self.Visualisation3D.chMap.index(channel_value)

            self.points_data.loc[channel_numb,'Channel Label'] = new_label
            self.points_data.loc[channel_numb,'Channel'] = new_idx
            #save back in excel
            df = pd.DataFrame(self.points_data)
            excel_path = os.path.join(os.path.join(self.session_path,"analysed"),self.mrid_info.mrid,'channel_atlas_coordinates.xlsx')
            df.to_excel(excel_path, index=False)

            #change atlas incase new label was added
            if self.check_newlabel(new_idx):
                self.Visualisation3D.delete_volumes(self.mrid_info.mrid,new_idx,channel_numb)

            #update table with new label and new color table
            max_idx = self.Visualisation3D.atlaslabelsdf['IDX'].max()
            rgba = self.Visualisation3D.cmap(new_idx / max_idx)
            r, g, b,a = rgba
            color = QColor(r*255, g*255, b*255)
            item = QTableWidgetItem(str(new_label))
            self.MW.ui.tableWidget_ephys.setItem(channel_numb, 2, item)
            item = self.MW.ui.tableWidget_ephys.item(channel_numb, 1)
            item.setForeground(QBrush(color))
            item = self.MW.ui.tableWidget_ephys.item(channel_numb, 2)
            item.setForeground(QBrush(color))
            item = self.MW.ui.tableWidget_ephys.item(channel_numb, 3)
            item.setForeground(QBrush(color))

            # update plot color
            line = self.VisEphys.ephys_lines[channel_numb]
            current_pen = line.opts['pen']
            current_pen.setColor(QColor(int(r*255), int(g*255), int(b*255), int(a*255)))
            #pen = pg.mkPen(color=(int(r*255), int(g*255), int(b*255),int(a*255)), width=0.5)
            line.setPen(current_pen)


    def check_newlabel(self,new_idx):
        filepath = os.path.join(self.session_path,"analysed",'atlas-regions.nii.gz')
        mesh = pv.read(filepath)
        old_labels = np.unique(mesh.point_data['NIFTI'])
        new_labels = np.unique(self.points_data.iloc[:, 1].values) #self.points_data.iloc[:, -3:].values
        old_idx = self.Visualisation3D.atlaslabelsdf['IDX'].values[self.old_index_anatregion]
        if (old_labels == new_idx).any() and (new_labels == old_idx).any():
            return False
        else:
            self.Visualisation3D.create_atlas_region_file(self.mrid_info.mrid)
            return True



    def _default_pyl_channels(self, n=8):
        """The default ripple-detection channels: n CA1 channels centred on the
        pyramidal layer, padded to n if fewer are available."""
        ca1 = self.Visualisation3D.get_pyl_centered_channels(n=n)
        if not ca1:
            ca1 = list(self.ephys_data.active_channels[:n])
        ca1 = list(ca1)
        while 0 < len(ca1) < n:
            ca1.append(ca1[-1])
        return ca1

    def detect_ripples(self):
        if self.ephys_data.lfp_memmap is None:
            QtWidgets.QMessageBox.warning(self.MW, "No LFP", "LFP file not loaded.")
            return

        save_path = str(pathlib.Path(self.ephys_data.lfp_path).with_suffix('')) + '_ripples.npy'
        settings_path = str(pathlib.Path(self.ephys_data.lfp_path).with_suffix('')) + '_ripples_settings.json'

        # defaults: reuse the previously-saved detection settings if they exist,
        # otherwise centre on the detected CA1 pyramidal-layer channel
        saved = self._load_ripple_settings(settings_path)
        default_arch, default_threshold = 'CNN1D', 0.25
        default_above, default_below = 2, 5
        pyr_default = None
        if saved is not None:
            default_arch = saved.get('arch', 'CNN1D')
            default_threshold = saved.get('threshold', 0.25)
            default_above = saved.get('above', 2)
            default_below = saved.get('below', 5)
            pyr_default = saved.get('pyr')
        if pyr_default is None:
            pyr_default = self.Visualisation3D.get_pyl_channel()
        if pyr_default is None:
            active = self.ephys_data.active_channels
            pyr_default = active[len(active) // 2] if active else 0

        all_ch = self.ephys_data.all_channels
        ch_min, ch_max = min(all_ch), max(all_ch)

        dialog = QDialog(self.MW)
        dialog.setWindowTitle("Ripple detection")
        # non-modal + stay-on-top so it can be moved aside and the GUI behind it
        # (e.g. the channel table) stays visible and usable while it's open
        dialog.setModal(False)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout(dialog)

        # pyramidal-layer channel + N channels above/below → 8 total
        layout.addWidget(QLabel("Pyramidal-layer channel, plus channels above/below (8 total):"))
        ch_row = QtWidgets.QHBoxLayout()
        pyr_spin = QtWidgets.QSpinBox()
        pyr_spin.setRange(ch_min, ch_max)
        pyr_spin.setValue(int(pyr_default))
        above_spin = QtWidgets.QSpinBox()
        above_spin.setRange(0, 7)
        above_spin.setValue(int(default_above))
        below_spin = QtWidgets.QSpinBox()
        below_spin.setRange(0, 7)
        below_spin.setValue(int(default_below))
        reset_btn = QtWidgets.QPushButton("Reset to pyl")
        reset_btn.setToolTip("Reset the pyramidal channel to the detected one")
        for w in (QLabel("PyL ch:"), pyr_spin, QLabel("above:"), above_spin,
                  QLabel("below:"), below_spin, reset_btn):
            ch_row.addWidget(w)
        layout.addLayout(ch_row)
        layout.addWidget(QLabel("Channels used (upper → lower):"))
        channels_line = QtWidgets.QLineEdit()
        channels_line.setReadOnly(True)
        layout.addWidget(channels_line)

        def recompute():
            pyr, above, below = pyr_spin.value(), above_spin.value(), below_spin.value()
            chans = [pyr + k for k in range(-above, below + 1)]
            channels_line.setText(', '.join(str(c) for c in chans))

        # above + below is always 7 (→ 8 channels with the pyramidal one); moving
        # one spinbox moves the other so the total never changes
        def on_above(a):
            below_spin.blockSignals(True)
            below_spin.setValue(7 - a)
            below_spin.blockSignals(False)
            recompute()

        def on_below(b):
            above_spin.blockSignals(True)
            above_spin.setValue(7 - b)
            above_spin.blockSignals(False)
            recompute()

        pyr_spin.valueChanged.connect(lambda _: recompute())
        above_spin.valueChanged.connect(on_above)
        below_spin.valueChanged.connect(on_below)
        reset_btn.clicked.connect(
            lambda: pyr_spin.setValue(self.Visualisation3D.get_pyl_channel() or pyr_spin.value())
        )
        recompute()

        layout.addWidget(QLabel("Model:"))
        arch_combo = QtWidgets.QComboBox()
        arch_combo.addItems(["CNN1D", "CNN2D", "LSTM", "SVM", "XGBOOST"])
        arch_combo.setCurrentText(default_arch)
        layout.addWidget(arch_combo)
        layout.addWidget(QLabel("Threshold (0–1): lower catches more ripples, higher is more conservative:"))
        threshold_spin = QtWidgets.QDoubleSpinBox()
        threshold_spin.setRange(0.01, 0.99)
        threshold_spin.setSingleStep(0.05)
        threshold_spin.setDecimals(2)
        threshold_spin.setValue(default_threshold)
        layout.addWidget(threshold_spin)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        # if a ripple file already exists, warn that OK will overwrite it
        if os.path.exists(save_path):
            buttons.button(QDialogButtonBox.Ok).setText("Overwrite current file")

        def on_accept():
            # validate here so an invalid selection keeps the dialog open to fix
            channels = [int(c.strip()) for c in channels_line.text().split(',') if c.strip()]
            if len(channels) != 8:
                QtWidgets.QMessageBox.warning(
                    self.MW, "Channel error",
                    f"Need exactly 8 channels (got {len(channels)}). Set above + below = 7.")
                return
            missing = [c for c in channels if c not in all_ch]
            if missing:
                QtWidgets.QMessageBox.warning(
                    self.MW, "Channel error", f"Channel(s) not in the recording: {missing}")
                return
            dialog.accept()
            self._run_ripple_detection(
                channels, arch_combo.currentText(), threshold_spin.value(),
                save_path, settings_path,
                pyr_spin.value(), above_spin.value(), below_spin.value()
            )

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)

        # keep a reference so the non-modal dialog isn't garbage-collected
        self._ripple_dialog = dialog
        dialog.show()
        dialog.raise_()

    def _run_ripple_detection(self, channels, arch, threshold, save_path, settings_path,
                              pyr=None, above=2, below=5):
        # slice full LFP for selected channels, convert to float µV
        lfp_slice = self.ephys_data.lfp_memmap[channels, :].T.astype(numpy.float32) * 0.195

        with tempfile.TemporaryDirectory() as tmp:
            input_path  = str(pathlib.Path(tmp) / "lfp_in.npy")
            output_path = str(pathlib.Path(tmp) / "events_out.npy")
            numpy.save(input_path, lfp_slice)

            script = str(pathlib.Path(__file__).parent.parent / "rippl-AI" / "run_rippl.py")
            venv_python = str(pathlib.Path(__file__).parent.parent / ".venv10" / "bin" / "python3")

            overlay = BusyOverlay(self.MW, f"Running ripple detection ({arch})…")
            overlay.setGeometry(self.MW.rect())
            overlay.raise_()
            overlay.show()
            QApplication.processEvents()

            result = subprocess.run(
                [venv_python, script,
                 "--input",     input_path,
                 "--output",    output_path,
                 "--sf",        str(self.ephys_data.lfp_sample_rate),
                 "--arch",      arch,
                 "--threshold", str(threshold)],
                capture_output=True, text=True
            )
            overlay.close()
            print("---- run_rippl stdout ----\n", result.stdout, flush=True)
            print("---- run_rippl stderr ----\n", result.stderr, flush=True)

            if result.returncode != 0:
                QtWidgets.QMessageBox.critical(self.MW, "Detection failed", result.stderr[-1000:])
                return

            count_msg = result.stdout.strip().split('\n')[-1]
            events = numpy.load(output_path)

        # persist the settings used so a re-run (or reopening this session) pre-fills them
        self._save_ripple_settings(settings_path, channels, arch, threshold, pyr, above, below)

        self.MW.ui.stackedWidget_ripplAI.setCurrentIndex(0)
        self.VisEphys.draw_ripple_events(events, save_path=save_path)

        msg = QtWidgets.QMessageBox(self.MW)
        msg.setWindowTitle("Ripple detection")
        msg.setText(f"{count_msg}\n\nFalse positives can be deleted by right-clicking on a highlighted region.")
        msg.addButton("Close", QtWidgets.QMessageBox.RejectRole)
        rerun_btn = msg.addButton("Re-run", QtWidgets.QMessageBox.ActionRole)
        msg.exec()
        if msg.clickedButton() == rerun_btn:
            self.detect_ripples()

    def _load_ripple_settings(self, settings_path):
        """Return the saved ripple-detection settings dict, or None if absent/unreadable."""
        if not os.path.exists(settings_path):
            return None
        try:
            with open(settings_path) as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def _save_ripple_settings(self, settings_path, channels, arch, threshold,
                              pyr=None, above=2, below=5):
        """Persist the channels, pyramidal channel, above/below span, model and
        threshold used for ripple detection."""
        try:
            with open(settings_path, 'w') as f:
                json.dump({
                    "channels": [int(c) for c in channels],
                    "pyr": int(pyr) if pyr is not None else None,
                    "above": int(above),
                    "below": int(below),
                    "arch": arch,
                    "threshold": float(threshold),
                }, f, indent=2)
        except OSError:
            pass

    # ------------------------------------------------------------------
    # Theta detection
    # ------------------------------------------------------------------

    def _theta_paths(self):
        """(events .npy, full-result .npz, settings .json) for the loaded session.

        The .npy holds just the segments, because that is what the overlay reads
        and it keeps theta on the same contract as ripples. The .npz is the
        equivalent of the MATLAB .theta_info_new.mat struct — segments, filtered
        trace, phase and params in one container.
        """
        stem = str(pathlib.Path(self.ephys_data.lfp_path).with_suffix(''))
        return stem + '_theta.npy', stem + '_theta_info.npz', stem + '_theta_settings.json'

    def _probe_neighbour(self, channel, step):
        """The channel `step` positions away from `channel` along the probe.

        chMap (== all_channels) is in probe order and channel ids are not, so the
        adjacent contact is chMap[index(channel) + step] — never channel + step.
        Returns None at the ends of the probe.
        """
        probe_order = list(self.ephys_data.all_channels)
        try:
            pos = probe_order.index(channel) + step
        except ValueError:
            return None
        return probe_order[pos] if 0 <= pos < len(probe_order) else None

    def load_existing_theta(self):
        """After ephys loading: if a saved theta file exists, draw the segments and
        show the navigation page (index 0); otherwise show the 'run detection'
        page (index 1)."""
        save_path, info_path, _ = self._theta_paths()

        if os.path.exists(save_path):
            events = numpy.load(save_path)
            self.VisEphys.draw_theta_events(events, save_path=save_path)
            self.VisEphys.set_theta_cycles(self._theta_cycles_from_info(info_path))
            self.MW.ui.stackedWidget_theta.setCurrentIndex(0)
        else:
            self.MW.ui.stackedWidget_theta.setCurrentIndex(1)

    def _theta_cycles_from_info(self, info_path):
        """Cycle-boundary times (s) read back from the saved theta info, or None.

        Only the phase of the detection channel is needed, so the other arrays in
        the .npz are never decompressed. Boundaries are *not* restricted to the
        detected segments here — the overlay does that against the segments as
        they currently stand, so deleting or editing a segment moves its lines."""
        if not os.path.exists(info_path):
            return None
        try:
            with numpy.load(info_path, allow_pickle=False) as info:
                sel = int(info['sel_channel_idx']) if 'sel_channel_idx' in info else 0
                return theta_detection.theta_cycle_starts(
                    info['thetaPhase'], float(info['work_fs']), sel_channel_idx=sel)
        except (OSError, ValueError, KeyError) as exc:
            print(f"Could not read theta phase from {info_path}: {exc}", flush=True)
            return None

    def detect_theta(self):
        """Parameter dialog for theta detection on the LFP file."""
        lfp_path = self.ephys_data.lfp_path
        if not lfp_path or not os.path.exists(lfp_path):
            QtWidgets.QMessageBox.warning(
                self.MW, "No LFP file",
                "Theta detection runs on the LFP file, which was not found.\n"
                "Create it first using the 'Create LFP file' action.")
            return

        save_path, _, settings_path = self._theta_paths()
        saved = self._load_theta_settings(settings_path)

        # default: the last two CA1 channels in chMap order, the same pair the
        # filter popup uses. The deeper one drives detection, the other is its
        # neighbour one step up the probe.
        ca1 = self.Visualisation3D.get_last_ca1_channels(n=2)
        if ca1:
            default_ch, default_offset = ca1[-1], -1
        else:
            active = self.ephys_data.active_channels
            default_ch = active[len(active) // 2] if active else self.ephys_data.all_channels[0]
            default_offset = -1

        if saved is not None and saved.get('channel') is not None:
            default_ch = saved['channel']
            default_offset = int(saved.get('neighbour_offset', default_offset))

        def saved_or(key, fallback):
            return saved.get(key, fallback) if saved is not None else fallback

        all_ch = self.ephys_data.all_channels
        dialog = QDialog(self.MW)
        dialog.setWindowTitle("Theta detection")
        # non-modal + stay-on-top, same as the ripple dialog, so the channel
        # table behind it stays usable while picking a channel
        dialog.setModal(False)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(
            "Detection runs on the LFP file. Segments are kept where theta power\n"
            "dominates delta and the cycles are clean enough."))

        form = QtWidgets.QFormLayout()

        # detection channel and its neighbour sit on one row, with the resulting
        # channel pair spelled out on the right
        ch_spin = QtWidgets.QSpinBox()
        ch_spin.setRange(min(all_ch), max(all_ch))
        ch_spin.setValue(int(default_ch))

        offset_combo = QtWidgets.QComboBox()
        offset_combo.addItem("above", -1)
        offset_combo.addItem("below", +1)
        offset_combo.setCurrentIndex(0 if default_offset < 0 else 1)

        channels_line = QtWidgets.QLineEdit()
        channels_line.setReadOnly(True)
        channels_line.setMinimumWidth(110)

        ch_row = QtWidgets.QHBoxLayout()
        ch_row.addWidget(ch_spin)
        ch_row.addWidget(QLabel("second:"))
        ch_row.addWidget(offset_combo)
        ch_row.addStretch()
        ch_row.addWidget(QLabel("channels used:"))
        ch_row.addWidget(channels_line)
        form.addRow("Detection channel:", ch_row)

        def recompute():
            ch = ch_spin.value()
            neighbour = self._probe_neighbour(ch, offset_combo.currentData())
            channels_line.setText(
                f"{ch}, {neighbour}" if neighbour is not None else f"{ch}, — (probe end)")

        ch_spin.valueChanged.connect(lambda _: recompute())
        offset_combo.currentIndexChanged.connect(lambda _: recompute())
        recompute()

        def band_row(lo_default, hi_default, lo_min, hi_max):
            lo = QtWidgets.QDoubleSpinBox()
            lo.setRange(lo_min, hi_max)
            lo.setDecimals(1)
            lo.setSingleStep(0.5)
            lo.setValue(lo_default)
            hi = QtWidgets.QDoubleSpinBox()
            hi.setRange(lo_min, hi_max)
            hi.setDecimals(1)
            hi.setSingleStep(0.5)
            hi.setValue(hi_default)
            row = QtWidgets.QHBoxLayout()
            row.addWidget(lo)
            row.addWidget(QLabel("–"))
            row.addWidget(hi)
            return lo, hi, row

        f_theta = saved_or('f_theta', [6.0, 10.0])
        f_delta = saved_or('f_delta', [2.0, 3.0])
        theta_lo, theta_hi, theta_row = band_row(f_theta[0], f_theta[1], 0.5, 40.0)
        delta_lo, delta_hi, delta_row = band_row(f_delta[0], f_delta[1], 0.5, 40.0)
        form.addRow("Theta band (Hz):", theta_row)
        form.addRow("Delta band (Hz):", delta_row)

        ratio_spin = QtWidgets.QDoubleSpinBox()
        ratio_spin.setRange(0.1, 20.0)
        ratio_spin.setDecimals(2)
        ratio_spin.setSingleStep(0.1)
        ratio_spin.setValue(float(saved_or('th2d_ratio_threshold', 1.5)))
        form.addRow("Theta/delta ratio threshold:", ratio_spin)

        amp_spin = QtWidgets.QDoubleSpinBox()
        amp_spin.setRange(0.0, 5000.0)
        amp_spin.setDecimals(1)
        amp_spin.setValue(float(saved_or('amplitude_threshold', 60.0)))
        form.addRow("Min. peak amplitude (µV):", amp_spin)

        phase_spin = QtWidgets.QDoubleSpinBox()
        phase_spin.setRange(1.0, 180.0)
        phase_spin.setDecimals(1)
        phase_spin.setValue(float(saved_or('phase_threshold', 15.0)))
        form.addRow("Max. peak phase deviation (deg):", phase_spin)

        dur_spin = QtWidgets.QDoubleSpinBox()
        dur_spin.setRange(0.0, 60.0)
        dur_spin.setDecimals(2)
        dur_spin.setSingleStep(0.1)
        dur_spin.setValue(float(saved_or('duration_threshold', 0.5)))
        form.addRow("Min. segment duration (s):", dur_spin)

        consensus_box = QtWidgets.QCheckBox("Require theta in both channels")
        consensus_box.setToolTip(
            "Keep only the times where the theta/delta ratio is above threshold on\n"
            "both channels. Untick to detect on the detection channel alone, which\n"
            "is what the MATLAB does — the second channel is then only used for its\n"
            "phase trace.")
        consensus_box.setChecked(bool(saved_or('consensus', True)))
        form.addRow("", consensus_box)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)
        if os.path.exists(save_path):
            buttons.button(QDialogButtonBox.Ok).setText("Overwrite current file")

        def on_accept():
            channel = ch_spin.value()
            offset = offset_combo.currentData()
            if channel not in all_ch:
                QtWidgets.QMessageBox.warning(
                    self.MW, "Channel error",
                    f"Channel {channel} is not in the recording.")
                return
            neighbour = self._probe_neighbour(channel, offset)
            if neighbour is None:
                QtWidgets.QMessageBox.warning(
                    self.MW, "Channel error",
                    f"Channel {channel} is at the end of the probe — "
                    "flip the neighbour to the other side.")
                return
            if theta_lo.value() >= theta_hi.value() or delta_lo.value() >= delta_hi.value():
                QtWidgets.QMessageBox.warning(
                    self.MW, "Band error",
                    "Each band's lower edge must be below its upper edge.")
                return
            dialog.accept()
            self._run_theta_detection(
                channel, neighbour,
                (theta_lo.value(), theta_hi.value()),
                (delta_lo.value(), delta_hi.value()),
                ratio_spin.value(), amp_spin.value(),
                phase_spin.value(), dur_spin.value(),
                consensus_box.isChecked(),
            )

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)

        # keep a reference so the non-modal dialog isn't garbage-collected
        self._theta_dialog = dialog
        dialog.show()
        dialog.raise_()

    def _run_theta_detection(self, channel, neighbour, f_theta, f_delta, ratio,
                             amplitude, phase, duration, consensus):
        save_path, info_path, settings_path = self._theta_paths()
        channels = [channel, neighbour]

        overlay = BusyOverlay(self.MW, "Running theta detection…")
        overlay.setGeometry(self.MW.rect())
        overlay.raise_()
        overlay.show()
        QApplication.processEvents()
        try:
            result = theta_detection.detect_theta(
                self.ephys_data.lfp_path,
                self.ephys_data.n_channels,
                self.ephys_data.lfp_sample_rate,
                channels=channels,
                sel_channel_idx=0,       # channels[0] is the detection channel
                raw_sample_rate=self.ephys_data.sample_rate,
                f_theta=f_theta, f_delta=f_delta,
                th2d_ratio_threshold=ratio,
                amplitude_threshold=amplitude,
                phase_threshold=phase,
                duration_threshold=duration,
                consensus=consensus,
                progress=lambda m: print("theta:", m, flush=True),
            )
        except Exception as exc:                      # noqa: BLE001 - surfaced to the user
            QtWidgets.QMessageBox.critical(self.MW, "Detection failed", str(exc))
            return
        finally:
            overlay.close()

        events = result['segments_s']
        self._save_theta_info(info_path, result)
        self._save_theta_settings(settings_path, channel, result)

        self.MW.ui.stackedWidget_theta.setCurrentIndex(0)
        self.VisEphys.draw_theta_events(events, save_path=save_path)
        self.VisEphys.set_theta_cycles(theta_detection.theta_cycle_starts(
            result['theta_phase'], result['work_fs'],
            sel_channel_idx=result['sel_channel_idx']))

        total = float(numpy.sum(events[:, 1] - events[:, 0])) if len(events) else 0.0
        msg = QtWidgets.QMessageBox(self.MW)
        msg.setWindowTitle("Theta detection")
        msg.setText(
            f"{len(events)} theta segments detected ({total:.1f} s total).\n\n"
            "False positives can be deleted by right-clicking on a highlighted region.")
        msg.addButton("Close", QtWidgets.QMessageBox.RejectRole)
        rerun_btn = msg.addButton("Re-run", QtWidgets.QMessageBox.ActionRole)
        msg.exec()
        if msg.clickedButton() == rerun_btn:
            self.detect_theta()

    def _save_theta_info(self, info_path, result):
        """Write the full result, mirroring the MATLAB .theta_info_new.mat struct.

        theta_segments / thetaLFP / thetaPhase / params are all here, plus the
        segment boundaries in raw samples. The traces are stored at the
        acquisition rate (work_fs == sample_rate, decimation == 1), matching the
        MATLAB. Column order of the traces matches `channels`.
        """
        try:
            numpy.savez_compressed(
                info_path,
                theta_segments=result['segments_s'],
                theta_segments_samples=result['segments_samples'],
                thetaLFP=result['theta_lfp'],
                thetaPhase=result['theta_phase'],
                channels=numpy.asarray(result['channels']),
                sel_channel_idx=result['sel_channel_idx'],
                work_fs=result['work_fs'],
                decimation=result['decimation'],
                sample_rate=result['params']['sample_rate'],
                params=json.dumps(result['params']),
            )
        except OSError as exc:
            print(f"Could not write {info_path}: {exc}", flush=True)

    def _load_theta_settings(self, settings_path):
        """Return the saved theta-detection settings dict, or None if absent/unreadable."""
        if not os.path.exists(settings_path):
            return None
        try:
            with open(settings_path) as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def _save_theta_settings(self, settings_path, channel, result):
        """Persist the channels and parameters used, plus the rate the traces
        were saved at (work_fs == the raw sample rate; no decimation)."""
        probe_order = list(self.ephys_data.all_channels)
        channels = [int(c) for c in result['channels']]
        offset = probe_order.index(channels[1]) - probe_order.index(channels[0])
        try:
            with open(settings_path, 'w') as f:
                json.dump({
                    "channel": int(channel),
                    "neighbour_offset": int(offset),
                    "channels": channels,
                    "work_fs": float(result['work_fs']),
                    "decimation": int(result['decimation']),
                    **result['params'],
                }, f, indent=2)
        except OSError:
            pass

    def prompt_spike_sorting(self):
        """
        Asked once, right after the ephys data is loaded: load the spike cluster
        plot now, or later via Ephys Analysis -> Load Spike Sorting.

        Pre-filled with the `_res.mat` sitting next to the loaded .dat; the user
        can point at a different file instead.
        """
        dat_dir = os.path.dirname(self.ephys_data.file_path)
        candidate = os.path.splitext(self.ephys_data.file_path)[0] + '_res.mat'
        if not os.path.exists(candidate):
            candidate = ''

        dialog = QDialog(self.MW)
        dialog.setWindowTitle("Load spike cluster plot")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(
            "Load the spike sorting result now, so the spike cluster plot can be shown?"))

        file_edit = QtWidgets.QLineEdit(candidate)
        file_edit.setReadOnly(True)
        file_edit.setMinimumWidth(450)
        browse = QtWidgets.QPushButton("Choose other…")
        row = QtWidgets.QHBoxLayout()
        row.addWidget(file_edit)
        row.addWidget(browse)
        layout.addLayout(row)

        status = QLabel()
        status.setWordWrap(True)
        layout.addWidget(status)

        buttons = QDialogButtonBox()
        btn_ok = buttons.addButton(QDialogButtonBox.Ok)
        btn_later = buttons.addButton("Do Later", QDialogButtonBox.RejectRole)
        btn_later.setToolTip("Load it later via Ephys Analysis → Load Spike Sorting")
        layout.addWidget(buttons)

        def refresh():
            path = file_edit.text()
            btn_ok.setEnabled(bool(path) and os.path.exists(path))
            if not path:
                status.setText("No spike sorting file was found next to the recording.\n"
                               "Choose one, or load it later via Ephys Analysis → Load Spike Sorting.")
            elif not os.path.exists(path):
                status.setText("This file does not exist any more.")
            else:
                status.setText("Found next to the recording." if path == candidate
                               else "Using the file you selected.")

        def choose_other():
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                dialog, "Load JRCLUST result file",
                file_edit.text() or dat_dir, "MAT files (*.mat)"
            )
            if path:
                file_edit.setText(path)
                refresh()

        browse.clicked.connect(choose_other)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        refresh()

        if dialog.exec() == QDialog.Accepted and file_edit.text():
            self.load_spike_sorting(path=file_edit.text())

    def load_spike_sorting(self, path=None):
        """Load spike sorting data. Without `path` (menu action) the file is
        auto-detected and confirmed first."""
        if path:
            self._load_spike_sorting_file(path)
            return

        # auto-detect _res.mat in the same folder as the loaded .dat
        dat_stem = os.path.splitext(self.ephys_data.file_path)[0]
        candidate = dat_stem + '_res.mat'
        path = None

        if os.path.exists(candidate):
            msg = QtWidgets.QMessageBox(self.MW)
            msg.setWindowTitle("Spike sorting file found")
            msg.setText(f"Found:\n{os.path.basename(candidate)}\n\nLoad this file?")
            msg.setStyleSheet("QLabel { min-width: 400px; }")
            load_found  = msg.addButton("Load found file",  QtWidgets.QMessageBox.AcceptRole)
            choose_other = msg.addButton("Choose other…",   QtWidgets.QMessageBox.ActionRole)
            msg.addButton(QtWidgets.QMessageBox.Cancel)
            msg.exec()

            if msg.clickedButton() == load_found:
                path = candidate
            elif msg.clickedButton() == choose_other:
                path, _ = QtWidgets.QFileDialog.getOpenFileName(
                    self.MW, "Load JRCLUST result file",
                    os.path.dirname(self.ephys_data.file_path), "MAT files (*.mat)"
                )
            else:
                return
        else:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.MW, "Load JRCLUST result file",
                os.path.dirname(self.ephys_data.file_path), "MAT files (*.mat)"
            )

        if not path:
            return

        self._load_spike_sorting_file(path)

    def _load_spike_sorting_file(self, path):
        """Load the spike sorting result at `path` into the spike raster."""
        overlay = BusyOverlay(self.MW, "Loading spike sorting data…")
        overlay.setGeometry(self.MW.rect())
        overlay.raise_()
        overlay.show()
        QApplication.processEvents()

        try:
            region_map, color_map = self._channel_maps()

            prm_path = path[:-len('_res.mat')] + '.prm' if path.endswith('_res.mat') \
                else os.path.splitext(path)[0] + '.prm'
            self._spike_sorting_path = path

            self.spike_ruster.load_matlab_files(
                path, self.ephys_data.sample_rate,
                region_map, color_map,
                prm_path=prm_path,
            )
            self.spike_ruster.update_view(self.VisEphys.time_start, self.VisEphys.time_end)
            self.MW.ui.tabWidget_ephys.setCurrentIndex(2)

            self.run_hierarchical_clustering()
        except Exception as e:
            overlay.close()
            QtWidgets.QMessageBox.critical(self.MW, "Load failed", str(e))
            return

        overlay.close()

    def run_hierarchical_clustering(self):
        if self.spike_ruster._spike_times is None:
            QtWidgets.QMessageBox.warning(
                self.MW, "No spike data",
                "Load spike sorting data first (Ephys Analysis → Load Spike Sorting)."
            )
            return

        # heatmap colour limit (symmetric ±) from the spinbox
        clim_val = self.MW.ui.doubleSpinBox_ClusterLimits.value()
        clim = (-clim_val, clim_val)

        overlay = BusyOverlay(self.MW, "Computing hierarchical clustering…")
        overlay.setGeometry(self.MW.rect())
        overlay.raise_()
        overlay.show()
        QApplication.processEvents()

        try:
            sr = self.spike_ruster
            spike_times_samples = (sr._spike_times * self.ephys_data.sample_rate).astype(np.int64)

            activity, _ = build_activity_matrix(
                spike_times_samples, sr._spike_units,
                sr._unit_ids, self.ephys_data.sample_rate
            )
            corr_matrix = compute_correlation_matrix(activity)

            # try to load Peter's custom colormap; fall back to magma
            cmap_path = os.path.join(self.session_path, 'CustomColormap.mat')
            colormap = load_custom_colormap(cmap_path, key='CustomColormap3')

            region_map, color_map = self._channel_maps()
            cluster_labels, reordered = hierarchical_clustering(
                corr_matrix, list(sr._unit_labels)
            )
            unit_labels_reordered = [lbl for lbl, _ in cluster_labels]
            channels_reordered = [sr._unit_channel[int(sr._unit_ids[i])]
                                   for i in range(len(sr._unit_ids))]
        except Exception as e:
            overlay.close()
            QtWidgets.QMessageBox.critical(self.MW, "Clustering failed", str(e))
            return

        overlay.close()
        self._embed_clustering_heatmap(reordered, unit_labels_reordered, clim, colormap,
                                       channels_reordered=channels_reordered,
                                       region_map=region_map, color_map=color_map)

    def _embed_clustering_heatmap(self, reordered, unit_labels, clim, colormap,
                                  channels_reordered=None, region_map=None, color_map=None):
        """Embed the correlation matrix as a pyqtgraph ImageItem with its y-axis
        linked to the spike ruster so each neuron row is the same pixel height."""
        container = self.MW.ui.widget_hierClustering
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)

        for old in getattr(self, '_hier_widgets', []):
            layout.removeWidget(old)
            old.setParent(None)
            old.deleteLater()

        n = reordered.shape[0]

        pg_cmap = pg.colormap.get('berlin', source='matplotlib')
        if colormap is not None:
            raw = (colormap(np.linspace(0, 1, 256)) * 255).astype(np.uint8)
            pg_cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 256), color=raw)
        lut = pg_cmap.getLookupTable(0.0, 1.0, 256)

        bottom_axis = _RotatedLabelAxis(orientation='bottom')
        bottom_axis.setStyle(tickTextHeight=80)
        plot_widget = pg.PlotWidget(background='k', axisItems={'bottom': bottom_axis})
        plot = plot_widget.getPlotItem()
        plot.setMouseEnabled(x=False, y=False)
        plot.getViewBox().invertY(True)   # match spike ruster: unit 0 at top

        # tick labels: unit i sits at y=i (and x=i)
        ticks = [(i, unit_labels[i]) for i in range(n)]
        plot.hideAxis('bottom')
        plot.hideAxis('left')

        # pg.ImageItem expects data[col, row]; reordered is [row, col] — just transpose.
        # invertY(True) is inherited from the linked spike ruster view, no extra flip needed.
        img_data = reordered.T
        image_item = pg.ImageItem(img_data)
        image_item.setLookupTable(lut)
        image_item.setLevels([clim[0], clim[1]])
        image_item.setRect(-0.5, -0.5, n, n)
        plot.addItem(image_item)

        cbar = pg.ColorBarItem(
            values=(clim[0], clim[1]),
            colorMap=pg_cmap,
            label='Pearson r',
            interactive=False,
            pen='w',
        )
        cbar.setImageItem(image_item, insert_in=plot)
        self._hier_cbar = cbar

        # Brain-region boundary lines
        if channels_reordered and region_map and color_map:
            regions_ordered = [region_map.get(ch, '') for ch in channels_reordered]
            for i in range(1, len(regions_ordered)):
                if regions_ordered[i] != regions_ordered[i - 1]:
                    b = i - 0.5
                    color = color_map.get(channels_reordered[i], (255, 255, 255, 255))
                    pen = pg.mkPen(color=color, width=1.5)
                    plot.plot([-0.5, n - 0.5], [b, b], pen=pen)
                    plot.plot([b, b], [-0.5, n - 0.5], pen=pen)

        plot.setXRange(-0.5, n - 0.5, padding=0)
        plot.setYRange(-0.5, n - 0.5, padding=0)

        self._hier_widgets = [plot_widget]
        self._hier_image_item = image_item
        self._hier_plot = plot
        self._hier_channels_reordered = channels_reordered or []
        self._hier_highlight_items = []
        layout.addWidget(plot_widget)

    def _update_cluster_clim(self, val):
        if hasattr(self, '_hier_image_item'):
            self._hier_image_item.setLevels([-val, val])
        if hasattr(self, '_hier_cbar'):
            self._hier_cbar.setLevels(low=-val, high=val)

    def set_highlight_clustering(self, channel):
        """Highlight rows and columns for all units on `channel`."""
        plot = getattr(self, '_hier_plot', None)
        if plot is None:
            return
        for item in getattr(self, '_hier_highlight_items', []):
            plot.removeItem(item)
        self._hier_highlight_items = []

        channels = getattr(self, '_hier_channels_reordered', [])
        rows = [i for i, ch in enumerate(channels) if ch == channel]
        for row in rows:
            h_band = pg.LinearRegionItem(
                orientation='horizontal', movable=False,
                brush=pg.mkBrush(255, 255, 255, 50), pen=pg.mkPen(None))
            h_band.setRegion((row - 0.5, row + 0.5))
            h_band.setZValue(5)
            plot.addItem(h_band)
            v_band = pg.LinearRegionItem(
                orientation='vertical', movable=False,
                brush=pg.mkBrush(255, 255, 255, 50), pen=pg.mkPen(None))
            v_band.setRegion((row - 0.5, row + 0.5))
            v_band.setZValue(5)
            plot.addItem(v_band)
            self._hier_highlight_items += [h_band, v_band]

    def add_video(self):
        self.Video = VideoPlayer(self.MW)
        self.Video.add_video()




