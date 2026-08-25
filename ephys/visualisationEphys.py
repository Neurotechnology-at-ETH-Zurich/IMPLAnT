# This Python file uses the following encoding: utf-8
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt
import os

# Overlay styling per event kind. Ripples are gold and theta green so both can
# be on screen at once and still be told apart; half_width is the starting
# half-span when the user adds one by hand (ripples are tens of ms, theta
# segments seconds).
EVENT_STYLES = {
    'ripple': {'label': 'ripple', 'brush': (255, 200, 0, 50),
               'pen': (255, 200, 0, 120), 'half_width': 0.025},
    'theta':  {'label': 'theta',  'brush': (0, 220, 120, 45),
               'pen': (0, 220, 120, 120), 'half_width': 0.25},
}

# Theta cycle boundaries: dotted verticals in the same green as the segments.
# Above ~8 Hz a cycle is 125 ms, so a long window can ask for thousands of
# lines — past this many they would be solid ink anyway, so the overlay is
# skipped instead of drawn (see _refresh_theta_cycles).
THETA_CYCLE_PEN = (0, 220, 120, 170)
MAX_THETA_CYCLE_LINES = 500


class VisualisationEphys:
    def __init__(self,MW,Vis3D,Ephys):
        self.MW = MW
        self.Vis3D = Vis3D
        self.Ephys = Ephys
        #self.Ephys.ephys_data.read_data = read_data
        self.total_ch_visible = 20
        duration = 0.5

        self.MW.ui.spinBox_startMin.setMaximum(int(self.Ephys.ephys_data.t_stop*60))
        self.MW.ui.spinBox_duration.setMaximum(int((self.Ephys.ephys_data.t_stop-self.Ephys.ephys_data.t_start)*1000))

        self.time_start = int(self.Ephys.ephys_data.t_stop/2)
        self.time_end = self.time_start + duration

        time_start_min = int(self.time_start/60)
        time_start_sec = int(self.time_start - time_start_min*60)
        time_start_ms = int((self.time_start - time_start_min*60-time_start_sec)*1000)
        self.MW.ui.spinBox_startMin.setValue(time_start_min) #min
        self.MW.ui.spinBox_startS.setValue(time_start_sec) #sec
        self.MW.ui.spinBox_startMs.setValue(time_start_ms) #ms
        self.MW.ui.spinBox_startMs.setMaximum(int((float(self.Ephys.ephys_data.t_stop.magnitude-self.Ephys.ephys_data.t_start.magnitude))*1000))
        self.MW.ui.spinBox_startS.setMaximum(int((float(self.Ephys.ephys_data.t_stop.magnitude-self.Ephys.ephys_data.t_start.magnitude))*1000))

        self.current_mode = 'broadband'
        # per kind ('ripple' / 'theta'): the (n_events, 2) second-based array set
        # after detection, its LinearRegionItems, its .npy path and its visibility
        self.events = {kind: None for kind in EVENT_STYLES}
        self._event_items = {kind: [] for kind in EVENT_STYLES}
        self._event_save_path = {kind: None for kind in EVENT_STYLES}
        self._events_visible = {kind: True for kind in EVENT_STYLES}
        # only one event is ever edited at a time, whatever its kind
        self._editing_region = None    # LinearRegionItem currently being edited
        self._editing_kind = None      # which kind that region belongs to
        self._editing_event_idx = None # its row in self.events[kind]
        self._editing_is_new = False   # True when editing a freshly-added event
        # theta cycle boundaries (ascending times in s, whole recording) and the
        # InfiniteLines currently drawn for the visible window
        self.theta_cycles = None
        self._theta_cycle_items = []
        self._theta_cycles_visible = True

        self.MW.ui.spinBox_duration.setValue(duration*1000)
        self.MW.ui.horizontalSlider_ephys.setMaximum(int((float(self.Ephys.ephys_data.t_stop.magnitude-self.Ephys.ephys_data.t_start.magnitude)-duration)*1000))
        self.MW.ui.horizontalSlider_ephys.setValue(self.time_start*1000) #sec

        self.MW.ui.spinBox_startMin.editingFinished.connect(self.change_start_end_time)
        self.MW.ui.spinBox_startS.editingFinished.connect(self.change_start_end_time)
        self.MW.ui.spinBox_startMs.editingFinished.connect(self.change_start_end_time)
        self.MW.ui.spinBox_duration.editingFinished.connect(self.change_start_end_time)
        self.MW.ui.horizontalSlider_ephys.valueChanged.connect(self.change_start_end_time_slider)

        self.MW.ui.pushButton_zoomOut.clicked.connect(self.MW.ui.widget_pgEphys.zoomOut)
        self.MW.ui.pushButton_zoomReset.clicked.connect(self.MW.ui.widget_pgEphys.zoomReset)
        self.MW.ui.pushButton_exportCSD.clicked.connect(self.export_csd)

        self.MW.ui.pushButton_next_rippl.clicked.connect(self.next_ripple)
        self.MW.ui.pushButton_prev_rippl.clicked.connect(self.prev_ripple)
        self.MW.ui.pushButton_addRipple.clicked.connect(self.add_ripple)

        self.MW.ui.checkBox_ripplAI.setChecked(True)
        self.MW.ui.checkBox_ripplAI.toggled.connect(self.set_ripple_visibility)

        self.MW.ui.pushButton_next_theta.clicked.connect(self.next_theta)
        self.MW.ui.pushButton_prev_theta.clicked.connect(self.prev_theta)
        self.MW.ui.pushButton_add_theta.clicked.connect(self.add_theta)

        self.MW.ui.checkBox_theta.setChecked(True)
        self.MW.ui.checkBox_theta.toggled.connect(self.set_theta_visibility)

        # optional: a "Cycles" checkbox next to the theta controls toggles the
        # dotted cycle boundaries. Without it in the .ui they are simply always on.
        self.MW.ui.checkBox_thetaCycles.toggled.connect(self.set_theta_cycle_visibility)

        self.MW.ui.pushButton_Timenext.clicked.connect(lambda: self.step_time(+0.5))
        self.MW.ui.pushButton_Timeprev.clicked.connect(lambda: self.step_time(-0.5))

        # create and electrode table
        self.Vis3D.table_excel = self.MW.ui.tableWidget_ephys
        self.Vis3D.fill_table(self.Ephys.ephys_data.all_channels,self.Ephys.ephys_data.dead_channels)
        self.Vis3D.table_excel.cellClicked.connect(self.Vis3D.on_table_click)


    def show_broadband(self):
        self.current_mode = 'broadband'
        vb = self.MW.ui.widget_pgEphys.plot.getViewBox()
        x_range, y_range = vb.viewRange()
        self.visualize_data(self.displayed_channels)
        self.MW.ui.widget_pgEphys.plot.setXRange(*x_range, padding=0)
        self.MW.ui.widget_pgEphys.plot.setYRange(*y_range, padding=0)

    def show_lfp(self):
        if self.Ephys.ephys_data.lfp_memmap is None:
            return
        self.current_mode = 'lfp'
        vb = self.MW.ui.widget_pgEphys.plot.getViewBox()
        x_range, y_range = vb.viewRange()
        self.visualize_data(self.displayed_channels)
        self.MW.ui.widget_pgEphys.plot.setXRange(*x_range, padding=0)
        self.MW.ui.widget_pgEphys.plot.setYRange(*y_range, padding=0)

    def visualize_data(self, channels):
        if self.time_start == self.time_end or channels == []:
            if channels == []:
                self.MW.ui.widget_pgEphys.plot.clear()
                self.displayed_channels = channels
                for index, _ in enumerate(self.Ephys.ephys_data.all_channels):
                    self.ephys_lines[index] = None
            return

        self.MW.ui.widget_pgEphys.xMin = self.time_start
        self.MW.ui.widget_pgEphys.xMax = self.time_end

        if self.current_mode == 'lfp' and self.Ephys.ephys_data.lfp_memmap is not None:
            sr = self.Ephys.ephys_data.lfp_sample_rate
            s0 = int(self.time_start * sr)
            s1 = int(self.time_end * sr)
            # lfp_memmap shape: (n_channels, n_lfp_samples); channel IDs == physical row indices
            raw_slice = self.Ephys.ephys_data.lfp_memmap[channels, s0:s1].T.astype(np.float32) * 0.195
            times = np.linspace(self.time_start, self.time_end, raw_slice.shape[0])
            self.displayed_channels, self.ephys_lines = self.MW.ui.widget_pgEphys.plot_ephys(times, raw_slice, channels)
        else:
            signal = self.Ephys.ephys_data.read_data.analogsignals[0].load(
                time_slice=(self.time_start, self.time_end), channel_indexes=channels)
            self.displayed_channels, self.ephys_lines = self.MW.ui.widget_pgEphys.plot_ephys(
                signal.times, signal.magnitude, channels)

        if self.Ephys.ephys_data.digitalin is not None:
            dtimes, camera_state, led_state = self.Ephys.ephys_data.digitalin.time_slice(
                self.time_start, self.time_end)
            self.MW.ui.widget_pgEphys.plot_digitalin(dtimes, camera_state, led_state)

        # highlight channel, even after time scrolling
        if self.Vis3D.table_excel.currentRow() != -1:
            self.highlight_channel(ch_idx=self.Vis3D.table_excel.currentRow())

        self._refresh_event_overlay()

        ruster = getattr(self, 'spike_ruster', None)
        if ruster is not None:
            ruster.update_view(self.time_start, self.time_end)

        self.update_spectrogram()
        self.update_csd()
        self.update_channel_spectrogram()

    def prewarm_tabs(self):
        """Force-compute the LFP spectrogram, CSD and all-channels spectrogram
        once regardless of which tabWidget_LFP tab is currently in front. Called
        once right after a file/tag finishes loading (see InitEphys.open_dat),
        so the first click on any of those tabs shows an already-computed map
        instead of triggering the compute right then."""
        self.update_spectrogram(force=True)
        self.update_csd(force=True)
        self.update_channel_spectrogram(force=True)

    def update_spectrogram(self, force=False):
        """Redraw the LFP spectrogram for the window currently shown in the ephys
        plot / spike raster. No-op until the widget is created."""
        channels = getattr(self, 'displayed_channels', []) or []

        for spec in getattr(self, 'spectrograms', []):
            channel = spec.channel
            if channel is None or (channels and channel not in channels):
                channel = channels[0] if channels else None

            spec.update_view(
                self.Ephys.ephys_data.lfp_memmap,
                self.Ephys.ephys_data.lfp_sample_rate,
                self.time_start, self.time_end, channel=channel,
                force=force,
            )

    def _csd_inputs(self):
        """Channels (displayed, minus dead) and their 1D depth positions (mm) —
        exactly what the CSD map is built from, so the display and the export
        share one source of truth. ele_pos_1d is atlas-derived when available,
        else None (the widget then falls back to uniform spacing)."""
        channels = getattr(self, 'displayed_channels', []) or []
        # drop dead/skipped channels: their flat or noisy LFP would otherwise
        # corrupt the kCSD interpolation and leave a bogus band in the map
        dead = set(getattr(self.Ephys.ephys_data, 'dead_channels', None) or [])
        channels = [ch for ch in channels if ch not in dead]

        ele_pos_1d = None
        coords_list = getattr(self.Vis3D, 'coords_list', None)
        chMap = getattr(self.Vis3D, 'chMap', None)
        if coords_list is not None and chMap is not None and len(channels) >= 2:
            ch_to_pos = {chMap[i]: coords_list[i] for i in range(len(chMap))}
            positions = np.array([ch_to_pos[ch] for ch in channels if ch in ch_to_pos])
            if positions.shape[0] == len(channels) and positions.shape[0] >= 2:
                # project onto first principal axis of the probe
                centered = positions - positions.mean(axis=0)
                _, _, Vt = np.linalg.svd(centered, full_matrices=False)
                depths = centered @ Vt[0]   # shape (n,)
                # orient so chMap[0] (surface entry) has the smallest value
                surface_ch = chMap[0]
                if surface_ch in channels:
                    surf_depth = depths[list(channels).index(surface_ch)]
                    if surf_depth > np.median(depths):
                        depths = -depths
                depths = depths - depths.min()
                ele_pos_1d = depths.reshape(-1, 1)
        return channels, ele_pos_1d

    def update_csd(self, force=False):
        """Recompute and redraw the kCSD heatmap. No-op until the widget is created."""
        csd = getattr(self, 'csd_widget', None)
        if csd is None:
            return

        channels, ele_pos_1d = self._csd_inputs()
        if len(channels) < 2:
            csd._clear()
            return

        csd.update_view(
            self.Ephys.ephys_data.lfp_memmap,
            self.Ephys.ephys_data.lfp_sample_rate,
            self.time_start, self.time_end,
            active_channels=channels,
            ele_pos_1d=ele_pos_1d,
            force=force,
        )

    def update_channel_spectrogram(self, force=False):
        """Redraw the frequency x channel wavelet map for the middle of the
        window currently shown in the ephys plot. Same channels and depth order
        as the CSD, so a feature sits on the same row in both. No-op until the
        widget is created."""
        spec = getattr(self, 'channel_spectrogram', None)
        if spec is None:
            return

        channels, ele_pos_1d = self._csd_inputs()
        if len(channels) < 2:
            spec._clear()
            return

        spec.update_view(
            self.Ephys.ephys_data.lfp_memmap,
            self.Ephys.ephys_data.lfp_sample_rate,
            self.time_start, self.time_end,
            active_channels=channels,
            ele_pos_1d=ele_pos_1d,
            ripple_events=self.events.get('ripple'),
            ripple_channels=self._ripple_detection_channels(),
            force=force,
        )

    def _ripple_detection_channels(self):
        """Channels rippl-AI detection was run on (saved alongside the ripple
        events at detection time), so the all-channels spectrogram's ripple
        mode can find each ripple's true peak instead of just its
        (start+end)/2 midpoint. None if ripples were never detected this
        session."""
        lfp_path = getattr(self.Ephys.ephys_data, 'lfp_path', None)
        if not lfp_path:
            return None
        settings_path = os.path.splitext(lfp_path)[0] + '_ripples_settings.json'
        settings = self.Ephys._load_ripple_settings(settings_path)
        return settings.get('channels') if settings else None

    def export_csd(self):
        """Solve the kCSD over the whole recording (same channels, geometry and
        cross-validated parameters as the on-screen map) and stream it to a raw
        float32 binary + JSON sidecar. Wired to pushButton_exportCSD."""
        from PySide6.QtWidgets import (QFileDialog, QProgressDialog, QMessageBox,
                                       QApplication)
        from PySide6.QtCore import Qt

        csd = getattr(self, 'csd_widget', None)
        if csd is None or self.Ephys.ephys_data.lfp_memmap is None:
            QMessageBox.warning(self.MW, 'Export CSD', 'No LFP data / CSD widget loaded.')
            return
        channels, ele_pos_1d = self._csd_inputs()
        if len(channels) < 2:
            QMessageBox.warning(self.MW, 'Export CSD',
                                'Need at least 2 live channels to export a CSD.')
            return

        path = os.path.join(os.path.dirname(dat_path),os.path.splitext(os.path.basename(dat_path))[0] + '_csd.bin')

        dlg = QProgressDialog('Exporting CSD…', 'Cancel', 0, 100, self.MW)
        dlg.setWindowModality(Qt.WindowModal)
        dlg.setMinimumDuration(0)
        dlg.setValue(0)

        def prog(frac):
            dlg.setValue(int(frac * 100))
            QApplication.processEvents()
            if dlg.wasCanceled():
                raise KeyboardInterrupt

        try:
            meta = csd.export_csd(
                self.Ephys.ephys_data.lfp_memmap,
                self.Ephys.ephys_data.lfp_sample_rate,
                channels, ele_pos_1d, path, progress=prog)
            dlg.setValue(100)
            QMessageBox.information(
                self.MW, 'Export CSD',
                f"Wrote {meta['shape'][0]}×{meta['shape'][1]} CSD (depth×time)\n"
                f"to {meta['bin_file']} (+ .json sidecar).")
        except KeyboardInterrupt:
            QMessageBox.information(self.MW, 'Export CSD', 'Export cancelled.')
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.MW, 'Export CSD', f'Export failed: {e}')
        finally:
            dlg.close()

    def change_start_end_time(self):
        self.time_start = min(self.MW.ui.spinBox_startMin.value()*60 + self.MW.ui.spinBox_startS.value() + self.MW.ui.spinBox_startMs.value()/1000,self.Ephys.ephys_data.t_stop.magnitude-self.MW.ui.spinBox_duration.value()/1000)

        self.time_end = self.time_start + self.MW.ui.spinBox_duration.value()/1000

        self.MW.ui.horizontalSlider_ephys.blockSignals(True)
        self.MW.ui.spinBox_startMin.blockSignals(True)
        self.MW.ui.spinBox_startS.blockSignals(True)
        self.MW.ui.spinBox_startMs.blockSignals(True)
        self.MW.ui.horizontalSlider_ephys.setMaximum(int((self.Ephys.ephys_data.t_stop.magnitude-self.Ephys.ephys_data.t_start.magnitude-self.MW.ui.spinBox_duration.value()/1000)*1000))
        self.MW.ui.horizontalSlider_ephys.setValue(self.time_start*1000) #ms
        time_start_min = int(self.time_start/60)
        time_start_sec = int(self.time_start - time_start_min*60)
        time_start_ms = int((self.time_start - time_start_min*60-time_start_sec)*1000)
        self.MW.ui.spinBox_startMin.setValue(time_start_min) #min
        self.MW.ui.spinBox_startS.setValue(time_start_sec) #sec
        self.MW.ui.spinBox_startMs.setValue(time_start_ms) #ms
        self.MW.ui.horizontalSlider_ephys.blockSignals(False)
        self.MW.ui.spinBox_startMin.blockSignals(False)
        self.MW.ui.spinBox_startS.blockSignals(False)
        self.MW.ui.spinBox_startMs.blockSignals(False)

        self.visualize_data(self.displayed_channels)

    def change_start_end_time_slider(self,val):
        self.MW.ui.spinBox_startMin.blockSignals(True)
        self.MW.ui.spinBox_startS.blockSignals(True)
        self.MW.ui.spinBox_startMs.blockSignals(True)
        time_start_min = int(self.MW.ui.horizontalSlider_ephys.value()/1000/60)
        time_start_sec = int(self.MW.ui.horizontalSlider_ephys.value()/1000 - time_start_min*60)
        time_start_ms = int((self.MW.ui.horizontalSlider_ephys.value()/1000- time_start_min*60-time_start_sec)*1000)
        self.MW.ui.spinBox_startMin.setValue(time_start_min) #min
        self.MW.ui.spinBox_startS.setValue(time_start_sec) #sec
        self.MW.ui.spinBox_startMs.setValue(time_start_ms) #ms
        self.MW.ui.spinBox_startMin.blockSignals(False)
        self.MW.ui.spinBox_startS.blockSignals(False)
        self.MW.ui.spinBox_startMs.blockSignals(False)

        self.time_start = self.MW.ui.spinBox_startMin.value()*60 + self.MW.ui.spinBox_startS.value() + self.MW.ui.spinBox_startMs.value()/1000
        self.time_end = self.time_start + self.MW.ui.spinBox_duration.value()/1000
        self.visualize_data(self.displayed_channels)

    # ------------------------------------------------------------------
    # Event overlay (ripples and theta segments share this machinery; the
    # per-kind wrappers further down are what the buttons connect to)
    # ------------------------------------------------------------------

    def draw_events(self, kind, events, save_path=None):
        """Store detected events of `kind`, save to file, and draw them."""
        self.events[kind] = events
        if save_path is not None:
            self._event_save_path[kind] = save_path
        self._save_events(kind)
        self._refresh_event_overlay(kind)

    def _save_events(self, kind):
        if self._event_save_path[kind] and self.events[kind] is not None:
            np.save(self._event_save_path[kind], self.events[kind])

    def event_at(self, x):
        """The event under time position x as (kind, index), or None.

        When kinds overlap — a ripple sitting inside a theta segment, which is
        the normal case — the narrower one wins, so right-clicking a ripple
        doesn't offer to delete the theta segment around it.
        """
        best = None
        for kind, events in self.events.items():
            if events is None or len(events) == 0:
                continue
            idxs = np.where((events[:, 0] <= x) & (events[:, 1] >= x))[0]
            for idx in idxs:
                span = events[idx, 1] - events[idx, 0]
                if best is None or span < best[0]:
                    best = (span, kind, int(idx))
        return (best[1], best[2]) if best is not None else None

    def delete_event_at(self, kind, x):
        """Delete the event of `kind` that contains time position x."""
        events = self.events[kind]
        if events is None:
            return
        mask = ~((events[:, 0] <= x) & (events[:, 1] >= x))
        self.events[kind] = events[mask]
        self._save_events(kind)
        self._refresh_event_overlay(kind)

    def is_editing_event(self):
        """True while the user is dragging an event's start/end boundaries."""
        return self._editing_region is not None

    def start_edit_event(self, kind, x):
        """Enter edit mode for the event of `kind` containing time x."""
        events = self.events[kind]
        if events is None or self.is_editing_event():
            return
        idxs = np.where((events[:, 0] <= x) & (events[:, 1] >= x))[0]
        if len(idxs) == 0:
            return
        self._begin_edit(kind, int(idxs[0]), is_new=False)

    def add_event(self, kind):
        """Add a new event in the middle of the current view and immediately
        drop into edit mode so the user can drag its start/end into place.
        Cancelling the edit removes the just-added event again."""
        if self.is_editing_event():
            return
        center = (self.time_start + self.time_end) / 2.0
        half = EVENT_STYLES[kind]['half_width']
        new_event = [[center - half, center + half]]
        events = self.events[kind]
        if events is None or len(events) == 0:
            self.events[kind] = np.array(new_event, dtype=float)
        else:
            self.events[kind] = np.vstack([events, new_event])
        self._refresh_event_overlay(kind)
        self._begin_edit(kind, len(self.events[kind]) - 1, is_new=True)

    def _begin_edit(self, kind, event_idx, is_new):
        """Make the region for events[kind][event_idx] draggable and freeze the
        rest of the ephys GUI so a stray pan/zoom can't tear it down mid-edit."""
        region = next(
            (r for r in self._event_items[kind]
             if getattr(r, '_event_idx', None) == event_idx),
            None,
        )
        if region is None:
            return

        # highlight and unlock only the region being edited
        region.setMovable(True)
        region.setBrush(pg.mkBrush(0, 200, 255, 60))
        region.setHoverBrush(pg.mkBrush(0, 200, 255, 90))
        for line in region.lines:
            line.setPen(pg.mkPen(0, 200, 255, 220, width=2))
            line.setHoverPen(pg.mkPen(0, 200, 255, 255, width=3))

        self._editing_region = region
        self._editing_kind = kind
        self._editing_event_idx = event_idx
        self._editing_is_new = is_new
        self._set_nav_controls_enabled(False)

    def finish_edit_event(self, commit=True):
        """Leave edit mode. When commit is True the dragged bounds are written
        back to the event array (and to disk); otherwise the edit is discarded
        (and a freshly-added event is removed again)."""
        region = self._editing_region
        if region is None:
            return
        kind = self._editing_kind
        changed = False
        if commit:
            start, end = sorted(region.getRegion())
            self.events[kind][self._editing_event_idx] = [start, end]
            changed = True
        elif self._editing_is_new:
            # discarding an event that was only just added → drop it again
            self.events[kind] = np.delete(self.events[kind], self._editing_event_idx, axis=0)
            changed = True

        self._editing_region = None
        self._editing_kind = None
        self._editing_event_idx = None
        self._editing_is_new = False
        self._set_nav_controls_enabled(True)
        if changed:
            self._save_events(kind)
        self._refresh_event_overlay()

    def _set_nav_controls_enabled(self, enabled):
        """Enable/disable the ephys navigation widgets so nothing rebuilds the
        plot (and drops the editable region) while an event is being edited."""
        for name in ('spinBox_startMin', 'spinBox_startS', 'spinBox_startMs',
                     'spinBox_duration', 'horizontalSlider_ephys',
                     'pushButton_next_rippl', 'pushButton_prev_rippl',
                     'pushButton_next_theta', 'pushButton_prev_theta',
                     'pushButton_Timenext', 'pushButton_Timeprev',
                     'pushButton_zoomOut', 'pushButton_zoomReset',
                     'pushButton_measurement', 'pushButton_timeline',
                     'pushButton_selectTime'):
            w = getattr(self.MW.ui, name, None)
            if w is not None:
                w.setEnabled(enabled)

    def set_event_visibility(self, kind, visible):
        """Show/hide the overlay regions of one kind."""
        self._events_visible[kind] = bool(visible)
        for item in self._event_items[kind]:
            item.setVisible(self._events_visible[kind])

    def _jump_to_event(self, kind, direction):
        """Center the view on the next (+1) / previous (-1) event of `kind`."""
        events = self.events[kind]
        if events is None or len(events) == 0:
            return

        duration = self.MW.ui.spinBox_duration.value() / 1000
        if kind=='theta':
            start_times = np.sort(events[:, 0])
        else: #rippls
            start_times = np.sort(events[:, 0] + (events[:, 1] - events[:, 0])/2)

        current_center = self.time_start + duration / 2.0
        eps = 1e-6

        if direction > 0:
            cand = start_times[start_times > current_center + eps]
        else:
            cand = start_times[start_times < current_center - eps]
        if len(cand) == 0:
            return  # no event in that direction

        target = cand[0] if direction > 0 else cand[-1]
        self._goto_time(target - duration/2.0)

    # --- ripple wrappers (what the rippl-AI buttons connect to) ---

    def draw_ripple_events(self, events, save_path=None):
        self.draw_events('ripple', events, save_path=save_path)

    def set_ripple_visibility(self, visible):
        self.set_event_visibility('ripple', visible)

    def next_ripple(self):
        self._jump_to_event('ripple', direction=+1)

    def prev_ripple(self):
        self._jump_to_event('ripple', direction=-1)

    def add_ripple(self):
        self.add_event('ripple')

    # --- theta wrappers ---

    def draw_theta_events(self, events, save_path=None):
        self.draw_events('theta', events, save_path=save_path)

    def set_theta_visibility(self, visible):
        self.set_event_visibility('theta', visible)

    def set_theta_cycles(self, cycles):
        """Store the cycle-boundary times (s) for the whole recording and redraw.

        `cycles` covers the full trace; which of its lines are shown is decided at
        draw time from the theta segments as they currently stand, so editing or
        deleting a segment updates the lines with it. None clears them."""
        self.theta_cycles = None if cycles is None else np.sort(np.asarray(cycles, dtype=float))
        self._refresh_theta_cycles()

    def set_theta_cycle_visibility(self, visible):
        self._theta_cycles_visible = bool(visible)
        for item in self._theta_cycle_items:
            item.setVisible(self._theta_cycles_visible)

    def _refresh_theta_cycles(self):
        """Redraw the dotted cycle boundaries for the visible window."""
        plot = self.MW.ui.widget_pgEphys.plot
        for item in self._theta_cycle_items:
            plot.removeItem(item)
        self._theta_cycle_items = []

        cycles = self.theta_cycles
        if cycles is None or len(cycles) == 0:
            return

        lo, hi = np.searchsorted(cycles, [self.time_start, self.time_end])
        times = cycles[lo:hi]

        # only inside the segments that survive in the overlay right now
        events = self.events['theta']
        if events is None or len(events) == 0:
            return
        seg = np.asarray(events, dtype=float).reshape(-1, 2)
        seg = seg[np.argsort(seg[:, 0])]
        idx = np.searchsorted(seg[:, 0], times, side='right') - 1
        times = times[(idx >= 0) & (times <= seg[np.clip(idx, 0, None), 1])]

        if len(times) > MAX_THETA_CYCLE_LINES:
            return  # window too wide for the lines to mean anything

        pen = pg.mkPen(*THETA_CYCLE_PEN, width=2, style=Qt.DotLine)
        for t in times:
            line = pg.InfiniteLine(pos=float(t), angle=90, pen=pen, movable=False)
            line.setVisible(self._theta_cycles_visible)
            plot.addItem(line, ignoreBounds=True)
            self._theta_cycle_items.append(line)

    def next_theta(self):
        self._jump_to_event('theta', direction=+1)

    def prev_theta(self):
        self._jump_to_event('theta', direction=-1)

    def add_theta(self):
        self.add_event('theta')

    def step_time(self, fraction):
        """Shift the ephys window by `fraction` of the current duration.

        Half a window (±0.5) keeps the second half of the old view on screen, so
        nothing crossing the edge is missed while scanning through the trace."""
        duration = self.MW.ui.spinBox_duration.value() / 1000
        self._goto_time(self.time_start + fraction * duration)

    def _goto_time(self, new_start):
        """Move the ephys view so it starts at new_start (seconds), keeping the
        current duration, and sync the spinboxes/slider without retriggering them."""
        duration = self.MW.ui.spinBox_duration.value() / 1000
        min_start = self.Ephys.ephys_data.t_start.magnitude
        max_start = self.Ephys.ephys_data.t_stop.magnitude - duration
        new_start = max(min_start, min(new_start, max_start))

        self.time_start = new_start
        self.time_end = new_start + duration

        widgets = (self.MW.ui.horizontalSlider_ephys, self.MW.ui.spinBox_startMin,
                   self.MW.ui.spinBox_startS, self.MW.ui.spinBox_startMs)
        for w in widgets:
            w.blockSignals(True)
        time_start_min = int(new_start / 60)
        time_start_sec = int(new_start - time_start_min * 60)
        time_start_ms = int((new_start - time_start_min * 60 - time_start_sec) * 1000)
        self.MW.ui.spinBox_startMin.setValue(time_start_min)
        self.MW.ui.spinBox_startS.setValue(time_start_sec)
        self.MW.ui.spinBox_startMs.setValue(time_start_ms)
        self.MW.ui.horizontalSlider_ephys.setValue(int(new_start * 1000))
        for w in widgets:
            w.blockSignals(False)

        self.visualize_data(self.displayed_channels)

    def _refresh_event_overlay(self, kind=None):
        """Rebuild the overlay regions for one kind, or all kinds when kind is None."""
        # never rebuild while an edit is in progress — that would drop the
        # movable region the user is dragging
        if self.is_editing_event():
            return

        plot = self.MW.ui.widget_pgEphys.plot
        t0, t1 = self.time_start, self.time_end

        for k in ([kind] if kind is not None else list(EVENT_STYLES)):
            for item in self._event_items[k]:
                plot.removeItem(item)
            self._event_items[k] = []

            events = self.events[k]
            if events is None or len(events) == 0:
                continue

            style = EVENT_STYLES[k]
            for idx in range(len(events)):
                start, end = events[idx]
                if end < t0 or start > t1:
                    continue
                region = pg.LinearRegionItem(
                    values=(start, end),
                    brush=pg.mkBrush(*style['brush']),
                    pen=pg.mkPen(*style['pen']),
                    movable=False,
                )
                region._event_idx = idx  # map back to events[k] for editing
                region.setVisible(self._events_visible[k])
                plot.addItem(region)
                self._event_items[k].append(region)

        if kind is None or kind == 'theta':
            self._refresh_theta_cycles()

    def highlight_channel(self,ch_idx):
        if self.ephys_lines[ch_idx] is None:
            return
        pen_current = self.ephys_lines[ch_idx].opts['pen']

        if pen_current.widthF() == 3.0:
            return  # already highlighted

        # reset all lines to default
        for idx, line in self.ephys_lines.items():
            if line is None:
                continue
            current_pen = line.opts['pen']
            current_pen.setWidthF(1.0)
            line.setPen(current_pen)

        # highlight clicked line
        current_pen = self.ephys_lines[ch_idx].opts['pen']
        current_pen.setWidthF(3.0)
        self.ephys_lines[ch_idx].setPen(current_pen)

        self.Vis3D.table_excel.selectRow(ch_idx)

        self.ch_highlight = ch_idx

        channel_id = self.Ephys.ephys_data.all_channels[ch_idx]

        # mirror the highlight onto the spike raster and clustering
        ruster = getattr(self, 'spike_ruster', None)
        if ruster is not None:
            ruster.set_highlight(channel_id)
        self.Ephys.set_highlight_clustering(channel_id)

        # ... and onto the CSD map, where the channel's LFP trace turns white
        csd = getattr(self, 'csd_widget', None)
        if csd is not None:
            csd.set_highlight(channel_id)

        # ... and onto the all-channel wavelet map, which marks the channel's row
        spec = getattr(self, 'channel_spectrogram', None)
        if spec is not None:
            spec.set_highlight(channel_id)

        # the spectrograms follow the highlighted channel
        specs = [s for s in getattr(self, 'spectrograms', []) if s.channel != channel_id]
        if specs:
            for spec in specs:
                spec.set_channel(channel_id)
            self.update_spectrogram()



