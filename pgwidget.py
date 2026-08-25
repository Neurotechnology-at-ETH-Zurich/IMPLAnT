# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenu
import pyqtgraph as pg
import numpy as np
from ephys.visualisationEphys import EVENT_STYLES
from PySide6.QtCore import Qt
from PySide6.QtCore import QRectF
from PySide6.QtGui import QKeySequence,QShortcut
from PySide6 import QtGui

class ClickablePlotWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.PgWidget = parent  # reference to your PgEphysWidget
        self.setFocusPolicy(Qt.StrongFocus)  # needed for Enter/Escape while editing
        self.scroll_time = False
        self.zooming = False
        self.measurement = False
        self.timeline = False
        self.rect_item = None
        self.timeline_item = None
        self.measurement_text = {}
        self.edit_time_text = None  # follows the cursor while editing an event


    def eventFilter(self, obj, event):
        if hasattr(event, 'button') and event.button() == Qt.MiddleButton:
            return True  # block middle button entirely
        return super().eventFilter(obj, event)

    def mouseDoubleClickEvent(self, event):
        ve = getattr(self.PgWidget, 'VisEphys', None)
        if ve is not None and ve.is_editing_event():
            super().mouseDoubleClickEvent(event)
            return

        # double right click zooms out one step (same as the zoom out button)
        if event.button() == Qt.RightButton:
            self.scroll_time = False  # the first click of the pair started time scrolling
            self.PgWidget.zoomReset()
            event.accept()
            return

        vb = self.getViewBox()
        pos = vb.mapSceneToView(event.position())
        x = pos.x()
        y = pos.y()
        # Pass event up to main widget
        channel_idx = self.PgWidget.find_closest_line(x, y)

        point = self.PgWidget.VisEphys.Vis3D.coords_list[channel_idx]
        self.PgWidget.VisEphys.Vis3D.show_coords(point)
        self.PgWidget.VisEphys.highlight_channel(channel_idx)

        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            event.accept()
            return

        # while editing an event, the plot's own pan/zoom/measure logic is
        # frozen — events go straight to the scene so the region can be dragged
        ve = getattr(self.PgWidget, 'VisEphys', None)
        if ve is not None and ve.is_editing_event():
            if event.button() == Qt.RightButton:
                menu = QMenu(self.PgWidget.MW)
                finish_action = menu.addAction("Finish editing")
                cancel_action = menu.addAction("Cancel editing")
                action = menu.exec(event.globalPosition().toPoint())
                if action == finish_action:
                    ve.finish_edit_event(commit=True)
                    self._hide_edit_time()
                elif action == cancel_action:
                    ve.finish_edit_event(commit=False)
                    self._hide_edit_time()
                return
            super().mousePressEvent(event)  # let the region boundaries drag
            return

        if event.button() == Qt.RightButton:
            # check if clicking inside a ripple / theta region → context menu
            if ve is not None:
                pos_view = self.plotItem.vb.mapSceneToView(event.pos())
                x = pos_view.x()
                hit = ve.event_at(x)
                if hit is not None:
                    kind, _ = hit
                    label = EVENT_STYLES[kind]['label']
                    menu = QMenu(self.PgWidget.MW)
                    edit_action = menu.addAction("Edit start/end time")
                    delete_action = menu.addAction(f"Delete {label}")
                    action = menu.exec(event.globalPosition().toPoint())
                    if action == delete_action:
                        ve.delete_event_at(kind, x)
                    elif action == edit_action:
                        ve.start_edit_event(kind, x)
                    return  # don't start time-scrolling
            self.scroll_time = True
            self.pos_original = event.globalPos()

        elif event.button() == Qt.LeftButton:
            if self.PgWidget.MW.ui.pushButton_measurement.isChecked():
                self.measurement = True
            elif self.PgWidget.MW.ui.pushButton_timeline.isChecked():
                self.timeline = True
            else:
                self.zooming = True
            self.pos_original = self.plotItem.vb.mapSceneToView(event.pos())

    def mouseReleaseEvent(self, event):
        ve = getattr(self.PgWidget, 'VisEphys', None)
        if ve is not None and ve.is_editing_event():
            super().mouseReleaseEvent(event)  # finish the region drag
            return
        if event.button() == Qt.RightButton:
            self.scroll_time = False
        elif event.button() == Qt.LeftButton:
            pos = self.plotItem.vb.mapSceneToView(event.pos())
            if self.zooming:
                diff_x = self.PgWidget.xMax - self.PgWidget.xMin
                diff_y = self.PgWidget.yMax - self.PgWidget.yMin
                if self.rect_item is not None:
                    self.removeItem(self.rect_item)
                if abs(pos.x() - self.pos_original.x()) < diff_x/75 and abs(pos.y() - self.pos_original.y()) < diff_y/75:
                    self.zooming = False
                    return
                if pos.x() > self.pos_original.x():
                    self.PgWidget.xMin = max(self.pos_original.x(),self.PgWidget.VisEphys.time_start)
                    self.PgWidget.xMax = min(pos.x(),self.PgWidget.VisEphys.time_end)

                else:
                    self.PgWidget.xMin = max(pos.x() ,self.PgWidget.VisEphys.time_start)
                    self.PgWidget.xMax = min(self.pos_original.x(),self.PgWidget.VisEphys.time_end)

                if not self.PgWidget.MW.ui.pushButton_selectTime.isChecked():
                    if pos.y() > self.pos_original.y():
                        self.PgWidget.yMin = max(self.pos_original.y(),-self.PgWidget.slot_height)
                        self.PgWidget.yMax = min(pos.y(), (len(self.PgWidget.MW.Ephys.ephys_data.all_channels)-1) * self.PgWidget.slot_height)
                    else:
                        self.PgWidget.yMin = max(pos.y(),-self.PgWidget.slot_height)
                        self.PgWidget.yMax = min(self.pos_original.y(), (len(self.PgWidget.MW.Ephys.ephys_data.all_channels)-1) * self.PgWidget.slot_height)
                self.PgWidget.plot.setLimits(yMin=self.PgWidget.yMin, yMax=self.PgWidget.yMax,xMin=self.PgWidget.xMin,xMax=self.PgWidget.xMax)
                self.PgWidget.plot.setXRange(self.PgWidget.xMin,self.PgWidget.xMax)
                self.PgWidget.plot.setYRange(self.PgWidget.yMin,self.PgWidget.yMax)

                self.zooming = False
                self.rect_item = None
            elif self.measurement:
                self.measurement =False
                for idx in list(self.measurement_text.keys()):
                        self.removeItem(self.measurement_text.pop(idx))
                if hasattr(self,"plot_points"):
                    self.removeItem(self.plot_points)
                    del self.plot_points
                self.removeItem(self.rect_item)
                self.rect_item = None
            elif self.timeline:
                self.removeItem(self.timeline_item)
                if hasattr(self,'timeline_text'):
                    self.removeItem(self.timeline_text)
                self.timeline =False
                self.timeline_item = None
                # also hide the mirrored cursor on the spike raster / spectrogram
                ve = getattr(self.PgWidget, 'VisEphys', None)
                ruster = getattr(ve, 'spike_ruster', None)
                if ruster is not None:
                    ruster.clear_timeline()
                for spec in getattr(ve, 'spectrograms', []):
                    spec.clear_timeline()
                csd = getattr(ve, 'csd_widget', None)
                if csd is not None:
                    csd.clear_timeline()


    def mouseMoveEvent(self, event):
        ve = getattr(self.PgWidget, 'VisEphys', None)
        if ve is not None and ve.is_editing_event():
            pos = self.plotItem.vb.mapSceneToView(event.pos())
            self._show_edit_time(pos)
            super().mouseMoveEvent(event)  # drag the region boundary
            return
        if self.scroll_time:
            pos = event.globalPos()  # position on screen
            delta = pos-self.pos_original
            self.pos_original = pos  # per-frame delta, not cumulative
            if delta.x() != 0:  # horizontal scroll
                ve = self.PgWidget.VisEphys
                # move the window as a fixed-width block, clamped to the recording
                # bounds so it can't invert / go negative (mmap needs length > 0)
                duration = ve.time_end - ve.time_start
                t_min = float(ve.Ephys.ephys_data.t_start.magnitude)
                t_max = float(ve.Ephys.ephys_data.t_stop.magnitude)
                new_start = ve.time_start + delta.x() / 1000
                new_start = max(t_min, min(new_start, t_max - duration))
                if new_start == ve.time_start:
                    super().mouseMoveEvent(event)
                    return  # already at an edge — nothing to redraw
                ve.time_start = new_start
                ve.time_end = new_start + duration
                self.PgWidget.xMin = ve.time_start
                self.PgWidget.xMax = ve.time_end
                signal = self.PgWidget.VisEphys.Ephys.ephys_data.read_data.analogsignals[0].load(time_slice=(self.PgWidget.VisEphys.time_start,self.PgWidget.VisEphys.time_end),channel_indexes=self.PgWidget.displayed_channels)
                self.PgWidget.VisEphys.displayed_channels,self.PgWidget.VisEphys.ephys_lines = self.PgWidget.plot_ephys(signal.times, signal.magnitude, self.PgWidget.displayed_channels)
                if self.PgWidget.VisEphys.Vis3D.table_excel.currentRow() != -1:
                    self.PgWidget.VisEphys.highlight_channel(ch_idx=self.PgWidget.VisEphys.Vis3D.table_excel.currentRow())

                #change slots
                self.PgWidget.MW.ui.spinBox_startMin.blockSignals(True)
                self.PgWidget.MW.ui.spinBox_startS.blockSignals(True)
                self.PgWidget.MW.ui.spinBox_startMs.blockSignals(True)
                self.PgWidget.MW.ui.horizontalSlider_ephys.blockSignals(True)
                time_start_min = int(self.PgWidget.VisEphys.time_start/60)
                time_start_sec = int(self.PgWidget.VisEphys.time_start - time_start_min*60)
                time_start_ms = int((self.PgWidget.VisEphys.time_start - time_start_min*60-time_start_sec)*1000)
                self.PgWidget.MW.ui.horizontalSlider_ephys.setValue(self.PgWidget.VisEphys.time_start*1000) #ms
                self.PgWidget.MW.ui.spinBox_startMin.setValue(time_start_min) #min
                self.PgWidget.MW.ui.spinBox_startS.setValue(time_start_sec) #sec
                self.PgWidget.MW.ui.spinBox_startMs.setValue(time_start_ms) #ms
                self.PgWidget.MW.ui.horizontalSlider_ephys.blockSignals(False)
                self.PgWidget.MW.ui.spinBox_startMin.blockSignals(False)
                self.PgWidget.MW.ui.spinBox_startS.blockSignals(False)
                self.PgWidget.MW.ui.spinBox_startMs.blockSignals(False)

                ruster = getattr(ve, 'spike_ruster', None)
                if ruster is not None:
                    ruster.update_view(ve.time_start, ve.time_end)
                ve.update_spectrogram()
        elif self.zooming:
            pos = self.plotItem.vb.mapSceneToView(event.pos())
            #pos_scene = self.plotItem.vb.mapViewToScene(pos)
            #pos_original_scene = self.plotItem.vb.mapViewToScene(self.pos_original)
            if hasattr(self, '_last_pos') and abs(pos.x() - self._last_pos.x()) < 1e-6 and abs(pos.y() - self._last_pos.y()) < 1e-6:
                return
            self._last_pos = pos
            # draw new rect
            if self.rect_item is None:
                self.rect_item = pg.QtWidgets.QGraphicsRectItem()
                self.rect_item.setPen(pg.mkPen('w'))
                self.rect_item.setBrush(pg.mkBrush(255, 255, 255, 50))
                self.addItem(self.rect_item)

            if not self.PgWidget.MW.ui.pushButton_selectTime.isChecked():
                self.rect_item.setRect(QRectF(
                    self.pos_original.x(), self.pos_original.y(),
                    pos.x() - self.pos_original.x(),
                    pos.y() - self.pos_original.y()
                ).normalized())
            else:
                self.rect_item.setRect(QRectF(
                    self.pos_original.x(), self.PgWidget.yMin,
                    pos.x() - self.pos_original.x(),
                    self.PgWidget.yMax-self.PgWidget.yMin
                ).normalized())

        elif self.timeline:
            pos = self.plotItem.vb.mapSceneToView(event.pos())
            if self.timeline_item is None:
                self.timeline_item = pg.QtWidgets.QGraphicsLineItem()
                self.timeline_item.setPen(pg.mkPen('w'))
                self.addItem(self.timeline_item)

                self.timeline_text = pg.TextItem(color='w', anchor=(0, 1),fill=pg.mkBrush(0, 0, 0, 150),border=pg.mkPen('w', width=1))
                self.timeline_text.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
                self.addItem(self.timeline_text)

            self.timeline_item.setLine(pos.x(), self.PgWidget.yMin, pos.x(), self.PgWidget.yMax)
            mins = int(pos.x() // 60)
            secs = int(pos.x() % 60)
            ms = int((pos.x() % 1) * 1000)
            self.timeline_text.setText(f"Time: {mins}:{secs:02d}.{ms:03d}, {(pos.x()):.3f} sec")
            self.timeline_text.setPos(self.PgWidget.xMin, self.PgWidget.yMin)

            # mirror the timeline cursor onto the spike raster and spectrogram
            # (shared time axis)
            ve = getattr(self.PgWidget, 'VisEphys', None)
            ruster = getattr(ve, 'spike_ruster', None)
            if ruster is not None:
                ruster.set_timeline(pos.x())
            for spec in getattr(ve, 'spectrograms', []):
                spec.set_timeline(pos.x())
            csd = getattr(ve, 'csd_widget', None)
            if csd is not None:
                csd.set_timeline(pos.x())



        elif self.measurement:
            pos = self.plotItem.vb.mapSceneToView(event.pos())

            if self.rect_item is None:
                # draw new rect
                self.rect_item = pg.QtWidgets.QGraphicsRectItem()
                self.rect_item.setPen(pg.mkPen('r'))
                self.rect_item.setBrush(pg.mkBrush(255, 255, 255, 50))  # semi-transparent
                self.addItem(self.rect_item)

            self.rect_item.setRect(QRectF(
                self.pos_original.x(), self.pos_original.y(),
                pos.x() - self.pos_original.x(),
                pos.y() - self.pos_original.y()
            ).normalized())

            self.measure_from_pos(pos)


        super().mouseMoveEvent(event)

    def _show_edit_time(self, pos):
        """Draw a small label at the cursor showing the time under it, so the
        user can read the event's new start/end while dragging."""
        if self.edit_time_text is None:
            self.edit_time_text = pg.TextItem(
                color='w', anchor=(0, 1), fill=pg.mkBrush(0, 0, 0, 150),
                border=pg.mkPen(0, 200, 255, width=1),
            )
            self.edit_time_text.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
            self.addItem(self.edit_time_text)
        mins = int(pos.x() // 60)
        secs = int(pos.x() % 60)
        ms = int((pos.x() % 1) * 1000)
        self.edit_time_text.setText(f"{mins}:{secs:02d}.{ms:03d}, {pos.x():.3f} sec")
        self.edit_time_text.setPos(pos.x(), pos.y())

    def _hide_edit_time(self):
        if self.edit_time_text is not None:
            self.removeItem(self.edit_time_text)
            self.edit_time_text = None

    def keyPressEvent(self, event):
        ve = getattr(self.PgWidget, 'VisEphys', None)
        if ve is not None and ve.is_editing_event():
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                ve.finish_edit_event(commit=True)
                self._hide_edit_time()
                event.accept()
                return
            if event.key() == Qt.Key_Escape:
                ve.finish_edit_event(commit=False)
                self._hide_edit_time()
                event.accept()
                return
        super().keyPressEvent(event)


    def measure_from_pos(self,pos):
        # get the times
        t1 = pos.x() if pos.x() < self.pos_original.x() else self.pos_original.x()
        t2 = self.pos_original.x() if pos.x() < self.pos_original.x() else pos.x()

        # get the data
        y1 = pos.y() if pos.y() < self.pos_original.y() else self.pos_original.y()
        y2 = self.pos_original.y() if pos.y() < self.pos_original.y() else pos.y()

        steps = np.arange(y1+self.PgWidget.slot_height*0.1, y2-self.PgWidget.slot_height*0.1, self.PgWidget.slot_height)
        channels_measurement = []
        line_indices = []
        for y_datapoint in steps:
            idx = self.PgWidget.find_closest_line(pos.x(), y_datapoint)
            channel_idx = self.PgWidget.MW.Ephys.ephys_data.all_channels[idx]
            if channel_idx in self.PgWidget.displayed_channels and channel_idx not in channels_measurement:
                channels_measurement.append(channel_idx)
                line_indices.append(idx)

        if channels_measurement == [] or abs(t2-t1)<1e-4:
            return

        signal = self.PgWidget.VisEphys.Ephys.ephys_data.read_data.analogsignals[0].load(time_slice=(t1,t2),channel_indexes=channels_measurement)

        points_x = []
        points_y = []


        for idx,ch_idx in enumerate(channels_measurement):
            signal_data = signal.magnitude[:, idx]
            ch_max = np.max(signal_data)
            ch_min = np.min(signal_data)
            # signal.times are quantities in seconds, but the stored signal_times
            # are plain floats; strip units here so the subtraction below doesn't
            # raise a dimensionless-vs-seconds conversion error
            t_max = float(signal.times[np.argwhere(signal_data==ch_max)[0][0]])
            t_min = float(signal.times[np.argwhere(signal_data==ch_min)[0][0]])
            diff_y_uV = (ch_max-ch_min)*0.195
            signal_times, ch_norm, offset = self.PgWidget.lines_values[line_indices[idx]]
            values = ch_norm + offset
            signal_times = np.asarray(signal_times, dtype=float)
            y_max=values[np.argmin(np.abs(signal_times - t_max))]
            y_min=values[np.argmin(np.abs(signal_times - t_min))]
            points_x.append(t_max)
            points_x.append(t_min)
            points_y.append(y_max)
            points_y.append(y_min)

            mins = abs(int(float(t_max-t_min) // 60))
            secs = abs(int(float(t_max-t_min) % 60))
            ms = abs(int((float(t_max-t_min) % 1) * 1000))

            if idx not in self.measurement_text:
                self.measurement_text[idx] = pg.TextItem(
                    color='w', anchor=(0, 1), fill=pg.mkBrush(0, 0, 0, 150),
                    border=pg.mkPen('w', width=1),
                )
                self.addItem(self.measurement_text[idx])

            diff_y = self.PgWidget.yMax -self.PgWidget.yMin #diff_y/20
            print(self.PgWidget.yMin + idx*diff_y/(len(self.PgWidget.MW.Ephys.ephys_data.all_channels) * self.PgWidget.slot_height)*2,flush=True)
            self.measurement_text[idx].setText(f"Ch {ch_idx}: {mins}:{secs:02d}.{ms:03d} min, {(diff_y_uV):.3f} uV")
            self.measurement_text[idx].setPos(self.PgWidget.xMin, self.PgWidget.yMin + idx*diff_y/(len(self.PgWidget.MW.Ephys.ephys_data.all_channels) * self.PgWidget.slot_height)*2) #*0.015
            self.measurement_text[idx].setFont(QtGui.QFont("Arial", self.height()*0.015, QtGui.QFont.Bold))

        # Remove leftover items if channel count decreased
        for idx in list(self.measurement_text.keys()):
            if idx >= len(channels_measurement):
                self.removeItem(self.measurement_text.pop(idx))

        if hasattr(self, "plot_points"):
            self.plot_points.setData(points_x, points_y)
        else:
            self.plot_points = self.plot(points_x, points_y, pen=None, symbol='o')
        # -> get ms and uV


class PgWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        # Layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Single plot widget
        self.plot = ClickablePlotWidget(self) #pg.PlotWidget()
        self.plot.setBackground('k')  # black background
        self.plot.showAxis('bottom', show=False)  # hide x-axis
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        self.layout.addWidget(self.plot)
        self.plot.getViewBox().setMenuEnabled(False)
        self.plot.getViewBox().setMouseEnabled(x=False, y=False)
        self.plot.hideButtons()

        # Store plotted lines
        self.lines = {}
        self.displayed_channels = []

        self.slot_height = 1.0
        self.amplitude = 1.5

        # digitalin (camera/LED TTL) rows drawn below the channel stack, one
        # slot each -- 0 when the loaded recording has no digitalin.dat.
        self.n_digitalin_rows = 0
        self._channel_yticks = []
        self._digitalin_yticks = []
        self._digitalin_lines = []
        self._digitalin_separator = None

    def base_ymin(self):
        """yMin with room for the digitalin rows (if any) below channel 0 --
        use this instead of a bare -self.slot_height wherever yMin gets reset,
        or the digitalin traces get clipped off the bottom of the plot.
        The extra +1 (only when there are digitalin rows at all) accounts
        for plot_digitalin's own one-channel-space gap before its separator."""
        extra_gap = 1 if self.n_digitalin_rows else 0
        return -(1 + self.n_digitalin_rows + extra_gap) * self.slot_height


    def init_PgWidget_class(self, VisEphys,MW):
        self.MW = MW
        self.VisEphys = VisEphys
        #self.ui.pushButton_openfile100um.clicked.connect(lambda: self.LoadMRI.Resample.open_as_new_file(self,self.MW))
        self.MW.ui.pushButtonAmp_plus.clicked.connect(lambda: self.change_amplitude(+0.2))
        self.MW.ui.pushButtonAmp_minus.clicked.connect(lambda: self.change_amplitude(-0.2))

        self.MW.ui.dockWidget_ephys.topLevelChanged.connect(self.on_dock_floating_changed)

        #ctrl D ctrl I
        ctrl_d = QShortcut(QKeySequence("Ctrl+D"), self.MW.ui.dockWidget_ephys)
        ctrl_d.setContext(Qt.ApplicationShortcut)
        ctrl_d.activated.connect(self.MW.ui.pushButtonAmp_minus.click)
        ctrl_i = QShortcut(QKeySequence("Ctrl+I"), self.MW.ui.dockWidget_ephys)
        ctrl_i.setContext(Qt.ApplicationShortcut)
        ctrl_i.activated.connect(self.MW.ui.pushButtonAmp_plus.click)

        self.xMin = self.VisEphys.time_start
        self.xMax = self.VisEphys.time_end
        self.n_digitalin_rows = 2 if self.MW.Ephys.ephys_data.digitalin is not None else 0
        self.yMin = self.base_ymin()
        self.yMax = len(self.MW.Ephys.ephys_data.all_channels) * self.slot_height

    def on_dock_floating_changed(self, floating):
        if floating:
            self.MW.ui.dockWidget_ephys.showFullScreen()

    def change_amplitude(self,val):
        self.amplitude = max(0.01,self.amplitude+val)

        for index, line in self.lines.items():
            if line is None:
                continue
            signal_times, ch_norm, offset = self.lines_values[index]
            line.setData(signal_times, ch_norm * self.amplitude + offset)



    def plot_ephys(self,signal_times, signal_data, channels,clear=True):
        """
        signal_times: 1D array of times (seconds)
        signal_data: 2D array (samples x channels)
        channels: list of channel indices to display
        slot_height: vertical offset per channel
        """
        if clear:
            self.plot.clear()
            # plot.clear() already destroyed the actual digitalin line items --
            # drop the stale references/ticks too, so a caller that redraws
            # without a follow-up plot_digitalin() (e.g. filter_data.py's
            # preview) doesn't leave "Camera"/"LED" tick labels with nothing
            # plotted next to them.
            self._digitalin_lines = []
            self._digitalin_yticks = []
        else:
            #remove all lines
            for line in self.lines.values():
                self.plot.removeItem(line)

        show_all = self.MW.ui.pushButton_showChannels.isChecked()

        self.lines = {}
        self.displayed_channels = []
        self.lines_values = {}
        self.signal_data = signal_data
        self.signal_times = signal_times

        n_samples, n_channels = signal_data.shape

        for index,_ in enumerate(self.MW.Ephys.ephys_data.all_channels):
            self.lines[index] = None
            self.lines_values[index] = None

        for i,ch_idx in enumerate(channels):
            index = self.MW.Ephys.ephys_data.all_channels.index(ch_idx)

            # offset each channel with space for deselected channels or not (depending on user input)
            if show_all:
                offset = (len(self.MW.Ephys.ephys_data.all_channels)-1-index) * self.slot_height
            else:
                offset = (len(channels)-1-i) * self.slot_height

            ch = signal_data[:, i]
            if ch.size==0:
                continue

            # normalize each channel independently to [-0.5, 0.5]
            ch_range = ch.max() - ch.min()
            ch_norm = (ch - ch.mean()) / ch_range

            # offset and plot
            max_idx = self.VisEphys.Vis3D.atlaslabelsdf['IDX'].max()
            j = self.VisEphys.Vis3D.chMap.index(ch_idx)
            channel_id = self.VisEphys.Vis3D.points_data['Channel'].iloc[j]
            rgba = self.VisEphys.Vis3D.cmap(channel_id / max_idx)
            r, g, b,a = rgba

            pen = pg.mkPen(color=(int(r*255), int(g*255), int(b*255),int(a*255)), width=1.0) #0.5)
            line = self.plot.plot(signal_times, ch_norm * self.amplitude + offset, pen=pen)

            self.displayed_channels.append(ch_idx)
            self.lines[index] = line
            self.lines_values[index] = (signal_times, ch_norm, offset)
            i+=1

        # y-axis ticks in the center of each channel slot
        if show_all:
            yticks = [((len(self.MW.Ephys.ephys_data.all_channels)-1-index) * self.slot_height, str(ch)) for index, ch in enumerate(self.MW.Ephys.ephys_data.all_channels)]
        else:
            yticks = [((len(channels)-1-index) * self.slot_height, str(ch)) for index, ch in enumerate(channels)]
            self.yMax = len(self.displayed_channels) * self.slot_height

        self._channel_yticks = yticks
        self._apply_yticks()
        self.plot.setLimits(yMin=self.yMin, yMax=self.yMax,xMin=self.xMin,xMax=self.xMax)
        self.plot.setXRange(self.xMin,self.xMax)
        self.plot.setYRange(self.yMin,self.yMax)

        return self.displayed_channels,self.lines

    def _apply_yticks(self):
        self.plot.getAxis('left').setTicks([self._channel_yticks + self._digitalin_yticks])

    def plot_digitalin(self, times, camera_state, led_state):
        """Draws the camera-shutter and LED TTL lines (see ephys/digitalin.py)
        as two extra rows below channel 0 -- call right after plot_ephys()
        each time the plot redraws for a new time window (plot_ephys's own
        clear() already dropped any previous digitalin lines/ticks)."""
        for line in self._digitalin_lines:
            self.plot.removeItem(line)
        self._digitalin_lines = []
        self._digitalin_yticks = []
        if self._digitalin_separator is not None:
            self.plot.removeItem(self._digitalin_separator)
            self._digitalin_separator = None

        if times.size == 0:
            self._apply_yticks()
            return

        # one extra channel-space of empty gap between the channel stack and
        # the digitalin rows, so the separator/rows below don't crowd channel 0
        gap = self.slot_height

        # separator sits in the middle of the empty gap between channel 0's
        # slot and the digitalin rows' slots.
        self._digitalin_separator = pg.InfiniteLine(
            pos=-0.5 * self.slot_height - gap / 2, angle=0, movable=False,
            pen=pg.mkPen(color=(120, 120, 120), width=1, style=Qt.DashLine))
        self.plot.addItem(self._digitalin_separator)

        # occupies most (not all) of its slot's height, centered on the slot,
        # same visual language as the channel traces above it
        margin = 0.1 * self.slot_height
        span = self.slot_height - 2 * margin
        for row, (label, state, color) in enumerate((
            ('Camera', camera_state, (200, 200, 200)),
            ('LED', led_state, (255, 165, 0)),
        )):
            # slot centers sit at integer multiples of slot_height, same
            # convention plot_ephys uses above zero for the channel stack
            offset = -(row + 1) * self.slot_height - gap
            pen = pg.mkPen(color=color, width=1.0)
            line = self.plot.plot(times, (state - 0.5) * span + offset, pen=pen)
            self._digitalin_lines.append(line)
            self._digitalin_yticks.append((offset, label))

        self._apply_yticks()


    def find_closest_line(self, x_click, y_click):
        closest_line = None
        min_distance = float('inf')

        for i, val in self.lines_values.items():
            if val is None:
                continue
            x, y1,y2 = val
            y = y1+y2
            if len(x) == 0:
                continue
            # find nearest time index (x may be a neo quantity or plain ndarray)
            x_arr = x.magnitude if hasattr(x, 'magnitude') else np.asarray(x)
            idx = np.searchsorted(x_arr, x_click)
            idx = np.clip(idx, 0, len(x_arr) - 1)

            y_at_x = y[idx]

            # compare vertical distance ONLY
            distance = abs(y_at_x - y_click)

            if distance < min_distance:
                min_distance = distance
                closest_line = i

        return closest_line

    def zoomReset(self):
        self.xMin = self.VisEphys.time_start
        self.xMax = self.VisEphys.time_end
        self.yMin = self.base_ymin()
        self.yMax = len(self.MW.Ephys.ephys_data.all_channels) * self.slot_height

        self.plot.setLimits(yMin=self.yMin, yMax=self.yMax,xMin=self.xMin,xMax=self.xMax)
        self.plot.setXRange(self.xMin,self.xMax)
        self.plot.setYRange(self.yMin,self.yMax)


    def zoomOut(self):
        self.xMin = max(self.xMin-0.1,self.VisEphys.time_start)
        self.xMax = min(self.xMax+0.1,self.VisEphys.time_end)
        self.yMin = max(self.yMin-self.slot_height,-self.slot_height)
        self.yMax = min(self.yMax+self.slot_height, len(self.MW.Ephys.ephys_data.all_channels) * self.slot_height)

        self.plot.setLimits(yMin=self.yMin, yMax=self.yMax,xMin=self.xMin,xMax=self.xMax)
        self.plot.setXRange(self.xMin,self.xMax)
        self.plot.setYRange(self.yMin,self.yMax)

