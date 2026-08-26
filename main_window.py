# This Python file uses the following encoding: utf-8
# Important: You need to run the following command to generate the ui_form.py file: pyside6-uic form.ui -o ui_form.py
import os
import sys
# xcb (X11) is Linux-only -- forcing it unconditionally crashed PySide6 on
# macOS/Windows, which don't ship that plugin at all (they use their own
# native cocoa/windows plugins by default and don't need this override).
if sys.platform.startswith('linux'):
    os.environ.setdefault('QT_QPA_PLATFORM', 'xcb')
import warnings
# pandas 1.5.x calls np.find_common_type internally, which numpy 1.25+ deprecated.
# It's cosmetic (nothing breaks); silence just that one message, not all warnings.
warnings.filterwarnings(
    'ignore', message='np.find_common_type is deprecated',
    category=DeprecationWarning,
)
import json as _json
from paths_config import _base_dir, _exe_dir, _paths
_session_state_path = os.path.join(_exe_dir, 'last_session.json')
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_form import Ui_MainWindow
from utils.zoom import zoom_notifier
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog, QDockWidget
import SimpleITK as sitk
from gui_utils.busy_overlay import BusyOverlay
from PySide6 import QtWidgets
from ephys.init_ephys import InitEphys
from PySide6.QtCore import Qt, QCoreApplication, QResource, QSize
from PySide6.QtWidgets import QLayout
import qdarkstyle
from utils.zoom import Zoom
import shutil
from samri.samri_main import InitSAMRI,SAMRI_InputDialog,SAMRI_InputDock
from samri.samri_logging import LogAdapter,SamriWorker
import logging
from PySide6.QtWidgets import QWidget
from trajectory_planning.trajectory_planning import TrajectoryPlanning
from trajectory_planning.file_input_output import FileInput
from mrid_utils.atlas_fetch import ensure_atlas_available
from during_surgery.load_surgery_plan import LoadSurgeryPlan
from during_surgery.surgery_controller import SurgeryController
import vtk
import pandas as pd
from file_handling.loader import FileLoader
from file_handling.resample_data import ResampleData
from PySide6.QtGui import QIcon, QAction, QFont
from mrid_utils import atlas_switch
import subprocess
from PySide6.QtCore import QTimer
import datetime
from PySide6.QtWidgets import QProxyStyle, QStyle


class QuickTooltipStyle(QProxyStyle):
    """Shortens the hover delay before any tooltip appears, app-wide."""
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.SH_ToolTip_WakeUpDelay:
            return 150
        return super().styleHint(hint, option, widget, returnData)

class MainWindow(QMainWindow):
    """
    Main application window for MRI visualization.
    """
    def __init__(self, parent=None):
        """
        Initialize the main window
        """
        super().__init__(parent)
        self.resize_bool=True
        # per-file view state (slice position, zoom, ...), so switching back to an
        # already-visited main file restores its prior view instead of resetting it.
        # Plain in-memory dict, keyed by absolute file path -- gone on app close/kill.
        self._session_view_cache = {}
        # same idea for ephys recordings (time window, zoom, mode, highlighted channel)
        self._ephys_session_view_cache = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # nothing cached yet at startup -- hide until there's another file/recording to switch to
        #self.ui.comboBox_cache.setVisible(False)
        #self.ui.comboBox_cache_2.setVisible(False)
        #self.ui.comboBox_cache.activated.connect(self._switch_mri_from_cache)
        #self.ui.comboBox_cache_2.activated.connect(self._switch_ephys_from_cache)
        self.setWindowTitle("IMPLAnT")
        self.setWindowIcon(QIcon(os.path.join(_base_dir, "Icons/Github/IMPLAnT_quad.png")))
        # Lives for the whole app session (unlike TrajectoryPlanning, which
        # only exists while an MRI is loaded) -- see during_surgery/
        # surgery_controller.py for why the Surgery tab has no MRI/
        # TrajectoryPlanning dependency at all.
        self.surgery = SurgeryController(self)
        self.add_actions()
        self.ui.tabWidget.setCurrentIndex(0)

    def add_actions(self):
        """
        Initializes action triggers, GUI layout and setup UI elements.
        """
        #hide tab bars
        self.ui.tabWidget.tabBar().setVisible(False)
        self.ui.tabWidget_visualisation.tabBar().setVisible(False)
        self.ui.tabWidget_visualisation.setCurrentIndex(0)

        #only show one row of views and center the three visible widgets
        box = self.ui.page_3D
        layout = box.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)
        self.ui.groupBox_data2.setVisible(False)
        self.ui.groupBox_data1.setVisible(False)
        self.ui.heatmap_data0.setVisible(False)
        self.ui.groupBox_barcode.setVisible(False)
        self.ui.groupbox_legend0.setVisible(False)
        self.ui.contrast_data.setItemEnabled(0, True)
        self.ui.contrast_data.setCurrentIndex(0)
        self.ui.contrast_data.setItemEnabled(1, False)
        self.ui.contrast_data.setItemEnabled(2, False)
        self.ui.dockWidget_ephys.setVisible(False)
        self.ui.lineEdit_vis3D.setVisible(False)
        self.ui.frame_vis3D.setVisible(False)
        self.ui.textEdit_SAMRI_reg.setVisible(False)
        self.ui.stackedWidget_3d.setVisible(False)
        self.ui.stackedWidget_axial.setCurrentIndex(0)
        self.ui.stackedWidget_coronal.setCurrentIndex(0)
        self.ui.stackedWidget_sagittal.setCurrentIndex(0)
        self.ui.stackedWidget_dfx.setCurrentIndex(0)
        self.ui.stackedWidget_3d_tp.setCurrentIndex(0)
        self.ui.stackedWidget_3d_tp.currentChanged.connect(self._update_3d_tp_height_cap)
        self._update_3d_tp_height_cap(0)

        #resize to inital size
        self.resize(1600, 900)
        self.setMinimumSize(1500,800)

        # Connect all buttons to open file. Like the per-tab "Open Session"
        # actions below, these go through load_previous_session() first so
        # any of them can also reopen a recently-used file/session instead of
        # always starting a brand-new one.
        self.ui.actionOpen.triggered.connect(lambda: self.load_previous_session(['mri']))
        self.ui.actionOpen_ephys_Data.triggered.connect(lambda: self.load_previous_session(['ephys']))
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionNew_Window.triggered.connect(self.open_new_window)
        self.ui.actionStart_SAMRI_process.triggered.connect(lambda: self.load_previous_session(['samri']))
        self.ui.actionTrajectory_Planning_2.triggered.connect(lambda: self.load_previous_session(['trajectory']))
        self.ui.actionDuring_Surgery.triggered.connect(self.initialize_surgery)
        # Surgery tab's measured-mm bregma/lambda fields: "sag"/"cor"/"ax"
        # match the same sagittal/coronal/axial slice-index convention as
        # the voxel-cursor spinboxes elsewhere (x=sag=ML, y=cor=AP,
        # z=ax=DV) -- ax/DV must stay last, since reproject_target_to_null
        # (during_surgery/reprojection.py) assumes index 2 of the vector
        # it's given is the vertical axis.
        for sb in (self.ui.doubleSpinBox_sag_b, self.ui.doubleSpinBox_cor_b, self.ui.doubleSpinBox_ax_b,
                   self.ui.doubleSpinBox_sag_l, self.ui.doubleSpinBox_cor_l, self.ui.doubleSpinBox_ax_l):
            sb.valueChanged.connect(self.surgery.on_bregma_lambda_changed)
        # Same reset/perspective controls as the docked pre-op 3D view's own
        # resetCamera_vis3D/change_perspective_vis3D -- lambdas re-fetch
        # self.surgery.mri_preview each click rather than binding a method
        # reference now, since that property can rebuild its QtInteractor
        # after a full restart (see SurgeryController.mri_preview).
        self.ui.resetCamera_vis3D_2.clicked.connect(lambda: self.surgery.mri_preview.plotter.reset_camera())
        self.ui.change_perspective_vis3D_2.clicked.connect(lambda: self.surgery.mri_preview.toggle_perspective())
        self.ui.pushButton_questionmark.clicked.connect(self.show_step_instructions)
        self.ui.pushButton_questionmark_samri.clicked.connect(self.show_step_instructions)
        self.ui.pushButton_questionmark_2.clicked.connect(self.surgery.show_step_popup)
        self.ui.actionLoad_Prev_Session.triggered.connect(self.load_previous_session)
        # Not defined in form.ui -- created here rather than hand-editing
        # that generated file for one menu entry. Lets the user pick the
        # active reference atlas (see mrid_utils/atlas_registry.py) before
        # opening ephys/electrode localization; trajectory planning gets its
        # own live in-view switcher instead (TpRegistration.reload_atlas_view).
        self.ui.actionAtlas = QAction("Atlas…", self)
        self.ui.menuGUI.insertAction(self.ui.actionLoad_Prev_Session, self.ui.actionAtlas)
        self.ui.actionAtlas.triggered.connect(self.show_atlas_selector)
        # per-tab "Open Session" placeholders: 3D/4D Tools -> mri (filtered by
        # dimensionality), Ephys Analysis -> ephys, Surgery -> samri
        self.ui.actionOpen_Session_2.triggered.connect(lambda: self.load_previous_session(['mri'], is_4d=False))
        self.ui.actionOpen_Session.triggered.connect(lambda: self.load_previous_session(['mri'], is_4d=True))
        self.ui.actionOpen_Session_3.triggered.connect(lambda: self.load_previous_session(['ephys']))
        self.ui.actionOpen_Session_4.triggered.connect(lambda: self.load_previous_session(['samri']))

        # 3D Tools / 4D Tools / Ephys Analysis menu actions (besides "Open
        # Session") only do anything once ButtonsGUI_3D/4D or InitEphys
        # connects them, which only happens once a matching file is loaded --
        # grey them out until then instead of leaving them as silent no-ops.
        for action_name in ('actionRegister', 'actionResample', 'actionPaintbrush',
                             'actionSegmentation', 'actionMeasurement',
                             'actionStart_MRIDlabels', 'actionContrast_Adjustments',
                             'actionRippl_AI', 'actionTheta_Detection', 'actionLoad_Spike_Sorting'):
            getattr(self.ui, action_name).setEnabled(False)
        self.ui.menuElectrode_Localization.menuAction().setEnabled(False)

        # Re-render if tab changed
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)


    def _load_session_state(self):
        if not os.path.exists(_session_state_path):
            return {}
        try:
            with open(_session_state_path) as f:
                return _json.load(f)
        except (OSError, ValueError):
            return {}

    _SESSION_KIND_LABELS = {
        'mri': 'MRI', 'ephys': 'Ephys', 'samri': 'SAMRI',
        'trajectory': 'Trajectory Planning', 'overlay': 'Overlay Image',
    }
    _SESSION_HISTORY_LIMIT = 10

    def _confirm_replace_session(self, kind):
        """If a <kind> session is already active, ask before replacing it --
        loading another MRI file/ephys recording/SAMRI animal ID discards
        whatever's currently loaded. Returns True to proceed, False to cancel.
        A no-op (returns True) when nothing of that kind is active yet."""
        active = {
            'mri':   getattr(self, 'LoadMRI', None) is not None,
            'ephys': getattr(self, 'Ephys', None) is not None,
            'samri': getattr(self, 'Samri', None) is not None,
        }[kind]
        if not active:
            return True
        label = self._SESSION_KIND_LABELS[kind]
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(f"Replace current {label} session?")
        msg_box.setText(
            f"A {label} file/session is already loaded. Loading another will replace it.\n\n"
            "Continue?")
        btn_yes = msg_box.addButton("Continue", QMessageBox.ActionRole)
        msg_box.addButton("Cancel", QMessageBox.RejectRole)
        msg_box.exec()
        return msg_box.clickedButton() is btn_yes

    def _save_session_state(self, kind, **entry):
        """Record a recently-loaded MRI/ephys file or SAMRI animal ID in the
        rolling per-kind history (last _SESSION_HISTORY_LIMIT each) that
        'Load Prev. File' lets the user pick back from."""
        state = self._load_session_state()
        history = state.get(kind, [])
        dedup_key = entry.get('path') or entry.get('animal_id')
        history = [e for e in history if (e.get('path') or e.get('animal_id')) != dedup_key]
        entry['timestamp'] = datetime.datetime.now().isoformat(timespec='seconds')
        history.append(entry)
        state[kind] = history[-self._SESSION_HISTORY_LIMIT:]
        with open(_session_state_path, 'w') as f:
            _json.dump(state, f, indent=2)

    # kind -> the method that opens a brand-new file/session of that kind
    # (used by the per-tab pickers' "Load New File..." button)
    def _open_new_session(self, kind):
        {'mri': self.initialize_mri_session,
         'ephys': self.open_ephys_data,
         'samri': self.initialize_samri,
         'trajectory': self.initialize_trajectory_planning,
         'overlay': self.add_another_file}[kind]()

    def show_atlas_selector(self):
        atlas_switch.show_atlas_selector(self)

    def load_previous_session(self, kinds=None, is_4d=None):
        """
        Show a picker of previously loaded MRI/ephys files or SAMRI animal
        IDs. `kinds` restricts which type(s) are listed -- None (the File
        menu's global "Load Prev. File") shows all three; a single-element
        list (the per-tab "Open Session" actions) shows only that kind and
        adds a "Load New File..." button. `is_4d` further restricts 'mri'
        entries to only 3D or only 4D files, for the 3D/4D Tools menus.
        """
        single_kind = kinds[0] if kinds and len(kinds) == 1 else None
        kinds = kinds or list(self._SESSION_KIND_LABELS)
        state = self._load_session_state()
        entries = []
        for kind in kinds:
            for e in state.get(kind, []):
                if kind == 'mri' and is_4d is not None and bool(e.get('is_4d')) != is_4d:
                    continue
                entries.append((kind, e))
        entries.sort(key=lambda ke: ke[1].get('timestamp', ''), reverse=True)

        if not entries and single_kind is None:
            QMessageBox.information(
                self, "Load Previous Session", "No previous sessions were found.")
            return

        dlg = QtWidgets.QDialog(self)
        title = "Load Previous Session" if single_kind is None else \
            f"Load Previous {self._SESSION_KIND_LABELS[single_kind]} Session"
        dlg.setWindowTitle(title)
        dlg.resize(500, 400)
        layout = QtWidgets.QVBoxLayout(dlg)
        if not entries:
            layout.addWidget(QtWidgets.QLabel("No previous sessions found.", dlg))
        list_widget = QtWidgets.QListWidget(dlg)
        for kind, entry in entries:
            label = self._SESSION_KIND_LABELS[kind]
            if kind == 'samri':
                text = f"[{label}] Animal {entry.get('animal_id', '?')}"
            else:
                text = f"[{label}] {os.path.basename(entry.get('path', '?'))}"
            text += f"   —   {entry.get('timestamp', '')}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(Qt.UserRole, (kind, entry))
            list_widget.addItem(item)
        if entries:
            list_widget.setCurrentRow(0)
        list_widget.itemDoubleClicked.connect(lambda _: dlg.accept())
        layout.addWidget(list_widget)

        buttons = QtWidgets.QDialogButtonBox(parent=dlg)
        open_btn = buttons.addButton("Open", QtWidgets.QDialogButtonBox.AcceptRole)
        open_btn.setEnabled(bool(entries))
        load_new = {'flag': False}
        if single_kind is not None:
            new_btn = buttons.addButton("Load New File...", QtWidgets.QDialogButtonBox.ActionRole)
            def _load_new():
                load_new['flag'] = True
                dlg.accept()
            new_btn.clicked.connect(_load_new)
        buttons.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        if dlg.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        if load_new['flag']:
            self._open_new_session(single_kind)
            return

        item = list_widget.currentItem()
        if item is None:
            return
        kind, entry = item.data(Qt.UserRole)
        self._restore_session_entry(kind, entry)

    def _restore_session_entry(self, kind, entry):
        if kind == 'mri':
            path = entry.get('path')
            if not path or not os.path.exists(path):
                QMessageBox.warning(self, "File not found", f"MRI file no longer exists:\n{path}")
                return
            self.FileLoader = FileLoader(self)
            file_name, data_view = self.FileLoader.restore_file(path)
            if file_name is not None:
                zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
                if not self.FileLoader.is_4d:
                    Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)
                self.ui.comboBox_resamplefiles.addItem(os.path.basename(file_name))
                if self.FileLoader.is_4d:
                    self.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")
                tab_idx = 0 if self.FileLoader.is_4d else 1
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.data_4d_3d.setCurrentIndex(tab_idx)

        elif kind == 'ephys':
            path = entry.get('path')
            xml_path = path.replace('.dat', '.xml') if path else None
            if not path or not (os.path.exists(path) and os.path.exists(xml_path)):
                QMessageBox.warning(
                    self, "File not found",
                    f"Ephys file (or its matching .xml) no longer exists:\n{path}")
                return
            if not self._confirm_replace_session('ephys'):
                return
            if not ensure_atlas_available(self):
                return
            self.ui.dockWidget_ephys.setVisible(True)
            self.ui.stackedWidget_video.setCurrentIndex(1)
            self.ui.textEdit_ephys.setText(f"File loaded: \n {path}")
            self.ui.tabWidget.setCurrentIndex(3)
            self.overlay = BusyOverlay(self, message="Loading ephys data, please wait…")
            self.overlay.run(self.do_ephys_heavy, path)

        elif kind == 'samri':
            if not self.initialize_samri():
                return
            if entry.get('raw_base_samri'):
                self.ui.lineEdit_rawBase.setText(entry['raw_base_samri'])
            self.ui.lineEdit_animalid.setText(entry.get('animal_id', ''))

        elif kind == 'overlay':
            path = entry.get('path')
            if not path or not os.path.exists(path):
                QMessageBox.warning(self, "File not found", f"Overlay image no longer exists:\n{path}")
                return
            if not hasattr(self, 'LoadMRI') or not hasattr(self, 'FileLoader'):
                QMessageBox.information(
                    self, "No MRI loaded",
                    "Load a main MRI image before adding an overlay image.")
                return
            self.add_another_file(path=path, skip_dialog=True)

        elif kind == 'trajectory':
            path = entry.get('path')
            transform_path = entry.get('transform_path')
            if not path or not os.path.exists(path):
                QMessageBox.warning(self, "File not found", f"Trajectory planning image no longer exists:\n{path}")
                return
            if not transform_path or not os.path.exists(transform_path):
                QMessageBox.warning(
                    self, "File not found",
                    f"Registration transform no longer exists:\n{transform_path}\n\n"
                    "Please first do SAMRI Registration again.")
                return
            if not ensure_atlas_available(self):
                return
            data = (path, entry.get('another') or [], entry.get('spacing', 0.05))
            self.overlay = BusyOverlay(self, message="Initializing trajectory planning, please wait…")
            self.overlay.run(self.finish_trajectory_work, data, transform_path)

    def open_ephys_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open ephys Data File",
            _paths['raw_base'],
            "Data files (*.dat)"
        )

        #User cancelled
        if not file_name:
            return

        #pop up asking for the view if 4D data used
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Open Main File")
        msg_box.setText(f"Do you want to open the file \n {file_name}?")
        msg_box.addButton("Yes", QMessageBox.ActionRole)
        btn_no = msg_box.addButton("No, other File", QMessageBox.ActionRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.ActionRole)
        msg_box.exec()
        if msg_box.clickedButton()==btn_cancel:
            return
        elif msg_box.clickedButton()==btn_no:
            self.open_ephys_data()
            return

        # the recording's .xml (same name as the .dat) is required to load ephys data
        xml_path = file_name.replace('.dat', '.xml')
        if not os.path.exists(xml_path):
            QMessageBox.critical(
                self, "XML file not found",
                f"No matching XML file was found:\n{xml_path}\n\n"
                "The recording's .xml file (same name as the .dat) is required to "
                "load the ephys data. Please make sure it is in the same folder."
            )
            return

        if not self._confirm_replace_session('ephys'):
            return
        if not ensure_atlas_available(self):
            return

        self.ui.dockWidget_ephys.setVisible(True)
        self.ui.stackedWidget_video.setCurrentIndex(1)
        self.ui.textEdit_ephys.setText(f"File loaded: {file_name}")
        self.ui.tabWidget.setCurrentIndex(3)
        self.overlay = BusyOverlay(self, message="Loading ephys data, please wait…")
        self.overlay.run(self.do_ephys_heavy, file_name)

    def do_ephys_heavy(self, file_name):
        self.snapshot_ephys_view_state()
        self.Ephys = InitEphys(self, file_name)
        self.Ephys.open_dat(file_name)
        self.reapply_ephys_view_state(file_name)
        self._save_session_state('ephys', path=file_name)
        #self.refresh_ephys_cache_combo()
        #ask about the spike cluster plot once the busy overlay is gone
        QTimer.singleShot(0, self.Ephys.prompt_spike_sorting)

    def snapshot_ephys_view_state(self):
        """
        Remember the current ephys recording's view (time window, zoom, mode,
        highlighted channel) under its path in self._ephys_session_view_cache,
        so switching back to it later via reapply_ephys_view_state() restores
        this instead of the freshly-loaded default.
        """
        if not hasattr(self, 'Ephys') or self.Ephys is None:
            return
        ve = self.Ephys.VisEphys
        pg_widget = self.ui.widget_pgEphys
        file_path = self.Ephys.ephys_data.file_path
        self._ephys_session_view_cache[file_path] = {
            'time_start': ve.time_start,
            'time_end': ve.time_end,
            'mode': ve.current_mode,
            'x_range': (pg_widget.xMin, pg_widget.xMax),
            'y_range': (pg_widget.yMin, pg_widget.yMax),
            'ch_highlight': getattr(ve, 'ch_highlight', None),
        }

    def reapply_ephys_view_state(self, file_path):
        """
        Reapply the ephys view previously stored for file_path by
        snapshot_ephys_view_state(), if any. No-op the first time a file is
        opened (nothing cached yet).
        """
        state = self._ephys_session_view_cache.get(file_path)
        if state is None:
            return
        ve = self.Ephys.VisEphys
        pg_widget = self.ui.widget_pgEphys

        # mode first -- show_lfp()/show_broadband() each redraw at whatever
        # time window is currently set, so get the mode right before touching
        # time. Default mode after a fresh load is always 'broadband', so
        # only 'lfp' needs an explicit switch.
        if state['mode'] == 'lfp':
            ve.show_lfp()

        # time window
        duration = state['time_end'] - state['time_start']
        self.ui.spinBox_duration.blockSignals(True)
        self.ui.spinBox_duration.setValue(duration * 1000)
        self.ui.spinBox_duration.blockSignals(False)
        ve._goto_time(state['time_start'])

        # zoom -- pinned down last so the redraws above don't clobber it
        pg_widget.xMin, pg_widget.xMax = state['x_range']
        pg_widget.yMin, pg_widget.yMax = state['y_range']
        pg_widget.plot.setLimits(yMin=pg_widget.yMin, yMax=pg_widget.yMax,
                                  xMin=pg_widget.xMin, xMax=pg_widget.xMax)
        pg_widget.plot.setXRange(pg_widget.xMin, pg_widget.xMax)
        pg_widget.plot.setYRange(pg_widget.yMin, pg_widget.yMax)

        # highlighted channel
        ch_idx = state['ch_highlight']
        if ch_idx is not None and ch_idx in ve.ephys_lines:
            ve.highlight_channel(ch_idx)

    def refresh_ephys_cache_combo(self):
        """
        Repopulate comboBox_cache_2 with the ephys recordings that have a
        cached view state (i.e. every recording visited this session other
        than the one currently open). Hidden when there's nothing to switch
        to -- either no other recording was ever opened, or none has been
        left yet (nothing gets cached until you switch away from it).
        """
        #combo = self.ui.comboBox_cache_2
        current_path = self.Ephys.ephys_data.file_path if getattr(self, 'Ephys', None) else None
        combo.blockSignals(True)
        combo.clear()
        for path in self._ephys_session_view_cache:
            if path == current_path:
                continue
            combo.addItem(os.path.basename(path), path)
        combo.blockSignals(False)
        combo.setVisible(combo.count() > 0)

    def _switch_ephys_from_cache(self, index):
        path = self.ui.comboBox_cache_2.itemData(index)
        if path:
            self._restore_session_entry('ephys', {'path': path})


    def resizeEvent(self, event):
        """
        re-rendering of vtk widgets if GUI resizes
        """
        super().resizeEvent(event)
        # Call on_gui_resize to re-render the vtk widgets
        if self.resize_bool==True:
            self.on_gui_resize()

    def initialize_mri_session(self):
        """
        Open the initial User Dialog when the application starts.
        """
        self.FileLoader = FileLoader(self)
        file_name, data_view = self.FileLoader.open_user_dialog()
        if file_name is None:
            return
        self._save_session_state('mri', path=file_name, is_4d=self.FileLoader.is_4d)
        zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
        if not self.FileLoader.is_4d:
            Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)

        self.ui.comboBox_resamplefiles.addItem(os.path.basename(file_name)) #add to combobox for resampling
        if self.FileLoader.is_4d:
            self.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")
        else:
            data_view = "coronal"

        tab_idx = 0 if self.FileLoader.is_4d else 1
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.data_4d_3d.setCurrentIndex(tab_idx)


    def on_gui_resize(self):
        """
        Re-render VTK widgets when GUI size changes.
        """
        self.ui.vtkWidget_data_sagittal.GetRenderWindow().Render()
        self.ui.vtkWidget_data_coronal.GetRenderWindow().Render()
        self.ui.vtkWidget_data_axial.GetRenderWindow().Render()
        self.ui.vtkWidget_data_seg3D.GetRenderWindow().Render()
        self.ui.vtkWidget_data00.GetRenderWindow().Render()
        self.ui.vtkWidget_data01.GetRenderWindow().Render()
        self.ui.vtkWidget_data02.GetRenderWindow().Render()
        self.ui.vtkWidget_data03.GetRenderWindow().Render()
        self.ui.vtkWidget_legend0.GetRenderWindow().Render()
        self.ui.vtkWidget_data10.GetRenderWindow().Render()
        self.ui.vtkWidget_data11.GetRenderWindow().Render()
        self.ui.vtkWidget_data12.GetRenderWindow().Render()
        self.ui.vtkWidget_data13.GetRenderWindow().Render()
        self.ui.vtkWidget_legend1.GetRenderWindow().Render()
        self.ui.vtkWidget_data10.GetRenderWindow().Render()
        self.ui.vtkWidget_data11.GetRenderWindow().Render()
        self.ui.vtkWidget_data12.GetRenderWindow().Render()
        self.ui.vtkWidget_data13.GetRenderWindow().Render()
        self.ui.vtkWidget_legend2.GetRenderWindow().Render()
        self.ui.vtkWidget_trajPlan_1.GetRenderWindow().Render()
        #barcode sachen
        self.ui.vtkWidget_ephys.GetRenderWindow().Render()

        if hasattr(self, 'LoadMRI'):
            # the scale bar's length/position is computed from the render
            # window's pixel width (utils/scale_bar.py) -- it's only ever
            # recomputed on zoom (utils/zoom.py), so resizing the window
            # without zooming left it showing a stale, now-incorrect length.
            if hasattr(self.LoadMRI, 'scale_bar') and hasattr(self.LoadMRI, 'renderers'):
                for view_name, bar in self.LoadMRI.scale_bar.items():
                    renderer = self.LoadMRI.renderers.get(0, {}).get(view_name)
                    if renderer is not None:
                        bar.update_bar(renderer, view_name, length_cm=1.0)

            if hasattr(self.LoadMRI,'minimap') and not self.LoadMRI.volumes[0].is_4d:
                for data_index, layers in self.Layers.items():
                    #for layer_index, layer in layers.items():
                    img_vtk = layers[0].img_vtks["axial"][0]
                    self.LoadMRI.minimap.add_minimap('axial',img_vtk,0,self.LoadMRI.vtk_widgets[0]["axial"],0,data_3d=True)
                    img_vtk = layers[0].img_vtks["coronal"][0]
                    self.LoadMRI.minimap.add_minimap('coronal',img_vtk,0,self.LoadMRI.vtk_widgets[0]["coronal"],0,data_3d=True)
                    img_vtk = layers[0].img_vtks["sagittal"][0]
                    self.LoadMRI.minimap.add_minimap('sagittal',img_vtk,0,self.LoadMRI.vtk_widgets[0]["sagittal"],0,data_3d=True)
            else:
                if hasattr(self.LoadMRI, 'vtk_widgets') and hasattr(self.LoadMRI, 'minimap'):
                    #each data_index has exactly one view, in the order the views were loaded
                    for data_index, view_name in enumerate(self.LoadMRI.vtk_widgets[0].keys()):
                        #a view being added is registered before its layer exists
                        if data_index not in self.Layers or 0 not in self.Layers[data_index]:
                            continue
                        for image_index,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
                            if image_index not in self.LoadMRI.minimap.minimap_renderers or view_name not in vtk_widget_image:
                                continue
                            img_vtk = self.Layers[data_index][0].img_vtks[view_name][image_index]
                            self.LoadMRI.minimap.add_minimap(view_name,img_vtk,image_index,vtk_widget_image[view_name],data_index)


    def add_another_file(self,path=None,skip_dialog=False):
        """
        Triggered if another file is uploaded by the user, saves it as highest layer.
        skip_dialog=True re-adds `path` directly with no file picker/confirmation,
        for restoring a previously-added overlay via load_previous_session().
        """
        self.FileLoader.layer_index += 1
        print("path",path,flush=True)
        file_name, data_view = self.FileLoader.open_user_dialog(layer_index=self.FileLoader.layer_index,add_another_file=True,path=path,skip_dialog=skip_dialog)
        if file_name is None:
            return
        self._save_session_state('overlay', path=file_name)

        if not self.LoadMRI.volumes[0].is_4d:
            #add to registration combobox
            self.ui.comboBox_movingimg.addItem(os.path.basename(file_name))
            self.LoadMRI.combo_Regimgname = self.ui.comboBox_movingimg
            self.LoadMRI.movingimg_filename.append(file_name)
        else:
            img = sitk.ReadImage(file_name)
            vol = sitk.GetArrayFromImage(img)
            #add to intensity table
            keys = list(self.LoadMRI.vtk_widgets[0].keys())
            idx = keys.index(data_view)
            tabclass = self.LoadMRI.intensity_table[idx]
            tabclass.update_table(os.path.basename(file_name), vol,idx)
            self.ui.contrast_data.setItemEnabled(idx, False)



    def initialize_surgery(self):
        # Unlike initialize_samri below, this only switches tabs AFTER the
        # PDF picker is actually accepted -- clicking the menu action then
        # hitting Cancel should leave you wherever you were, not dropped
        # onto an empty Surgery tab with nothing loaded.
        #
        # Deliberately independent of LoadMRI/TrajectoryPlanning -- see
        # during_surgery/surgery_controller.py -- so no MRI/registration
        # state is required or touched here.
        dlg = LoadSurgeryPlan(self, parent=self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # indexOf rather than a hardcoded index -- the Surgery tab
            # currently sits at index 6, but that would silently go stale if
            # tabWidget's pages are ever reordered/added to in Designer.
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.indexOf(self.ui.surgery))

    def initialize_samri(self):
        #Pop up for bruker2bids
        if not self._confirm_replace_session('samri'):
            return False
        self.ui.tabWidget.setCurrentIndex(5)
        SAMRI_InputDialog(self)
        self.show_samri_step_popup()
        return True

    def fetch_data(self,samri_input):
        def work_init():
            self.Samri = InitSAMRI(samri_input)
        # Clean up previous worker if it exists
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.done.disconnect()
            self.worker.failed.disconnect()
            self.worker = None

        # Reinstall log adapter fresh
        if hasattr(self, 'log_adapter') and self.log_adapter:
            self.log_adapter.uninstall()

        self.log_adapter = LogAdapter(self.ui.plainTextEdit_SAMRI)
        self.log_adapter.install(level=logging.INFO)

        overlay = BusyOverlay(self, "Fetching data from server…")
        overlay.setGeometry(self.rect())
        overlay.raise_()
        overlay.show()
        QApplication.processEvents()

        self.worker = SamriWorker(work_init, self)
        self.worker.done.connect(lambda: logging.info("Ready for Biascorrection or Registration"))
        self.worker.done.connect(self._on_bruker2bids_done)
        self.worker.done.connect(overlay.close)
        self.worker.failed.connect(self._on_fetch_failed)
        self.worker.failed.connect(overlay.close)
        self.worker.start()

    def _on_fetch_failed(self, tb):
        logging.error(tb)
        tb_lower = tb.lower()
        if 'network is unreachable' in tb_lower or 'errno 101' in tb_lower:
            text = ("<b style='color:#e74c3c;'>Network unreachable.</b><br>"
                    "Could not connect to the SAMRI server — check your network "
                    "connection (e.g. VPN) and try again.")
        elif 'name resolution' in tb_lower or 'gaierror' in tb_lower:
            text = ("<b style='color:#e74c3c;'>Could not resolve the server address.</b><br>"
                    "This is not related to the Animal ID — the SAMRI server's hostname "
                    "could not be looked up. Check the server address in the SAMRI tab "
                    "and your network/VPN connection.")
        elif 'no data found on the server' in tb_lower:
            text = ("<b style='color:#e74c3c;'>Animal ID not found.</b><br>"
                    "No data matching this Animal ID was found on the server — "
                    "please check the name and try again.")
        else:
            text = "<b style='color:#e74c3c;'>Fetching data from the SAMRI server failed.</b>"
        # a failed fetch must not leave stale registration/biascorrection controls
        # enabled from an earlier, unrelated successful fetch
        self.ui.frame_samri.setEnabled(False)
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("SAMRI Fetch Failed")
        msg_box.setText(text)
        msg_box.setDetailedText(tb)
        msg_box.addButton("OK", QMessageBox.ActionRole)
        msg_box.setWindowFlags(msg_box.windowFlags() & ~Qt.MSWindowsFixedSizeDialogHint)
        msg_box.setSizeGripEnabled(True)
        msg_box.layout().setSizeConstraint(QLayout.SetNoConstraint)
        msg_box.exec()

    def _on_bruker2bids_done(self):
        #Pop up for registration
        self.ui.frame_samri.setEnabled(True)
        self.Samri_input = SAMRI_InputDock(self)
        self.Samri.output_filepath = ""
        self._save_session_state('samri', animal_id=self.Samri.animal_id, raw_base_samri=self.Samri.raw_base_samri)
        self.show_samri_step_popup()


    def start_registration(self,samri_input):
        if not ensure_atlas_available(self):
            return
        def work_registration():
            self.ui.dockWidget_ephys.setEnabled(False)
            self.Samri.output_filepath =  self.Samri.start_registration(samri_input)

        # Clean up previous worker if it exists
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.done.disconnect()
            self.worker.failed.disconnect()
            self.worker = None

        if samri_input['register']:
            csv_path = f"{self.Samri.bids_base}/results/generic_work/data_selection.csv"
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, index_col=0)

                idx = df.loc[df['session'] == samri_input['working_session'][0]].index[0] #original_path?
                path = f"{self.Samri.bids_base}/results/generic_work/_ind_type_{idx}/s_register"
                if os.path.exists(path):
                    #pop up asking for the view if 4D data used
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Registration found")
                    msg_box.setText("Registration already found!")
                    msg_box.addButton("Cancel", QMessageBox.ActionRole)
                    btn_ok = msg_box.addButton("Re-Run", QMessageBox.ActionRole)
                    msg_box.exec()
                    if msg_box.clickedButton()==btn_ok:
                        shutil.rmtree(path)
                    else:
                        return
            def on_registration_failed(tb, threads):
                logging.error(tb)
                oom_keywords = ['memoryerror', 'out of memory', 'cannot allocate', 'std::bad_alloc', 'killed']
                if any(kw in tb.lower() for kw in oom_keywords) and threads > 1:
                    new_threads = max(1, threads // 2)
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("SAMRI crashed (memory)")
                    msg_box.setText(
                        f"SAMRI ran out of memory with {threads} thread(s).\n"
                        f"Retry with {new_threads} thread(s)?"
                    )
                    btn_retry = msg_box.addButton("Retry", QMessageBox.ActionRole)
                    msg_box.addButton("Cancel", QMessageBox.ActionRole)
                    msg_box.exec()
                    if msg_box.clickedButton() == btn_retry:
                        samri_input['num_threads'] = new_threads
                        self.start_registration(samri_input)
                else:
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Registration failed")
                    msg_box.setText("Registration encountered an error.")
                    msg_box.setDetailedText(tb)
                    msg_box.addButton("OK", QMessageBox.ActionRole)
                    msg_box.setWindowFlags(msg_box.windowFlags() & ~Qt.MSWindowsFixedSizeDialogHint)
                    msg_box.setSizeGripEnabled(True)
                    msg_box.layout().setSizeConstraint(QLayout.SetNoConstraint)
                    msg_box.exec()

            self.worker = SamriWorker(work_registration, self)
            overlay = BusyOverlay(self, message="Registering, please wait…")
            overlay.setGeometry(self.rect())
            overlay.raise_()
            overlay.show()
            self.worker.done.connect(overlay.close)
            self.worker.done.connect(lambda: self._on_registration_done(samri_input))
            self.worker.failed.connect(overlay.close)
            self.worker.failed.connect(
                lambda tb: on_registration_failed(tb, samri_input['num_threads'])
            )
            self.worker.start()
        elif samri_input["biascorrection"]:
            def work_bias():
                self.ui.dockWidget_ephys.setEnabled(False)
                self.Samri.biascorrection(samri_input)

            if hasattr(self, 'worker') and self.worker is not None:
                try:
                    self.worker.done.disconnect()
                    self.worker.failed.disconnect()
                except Exception:
                    pass
                self.worker = None

            overlay = BusyOverlay(self, message="Bias correction, please wait…")
            overlay.setGeometry(self.rect())
            overlay.raise_()
            overlay.show()
            def _on_biascorrection_failed(tb):
                logging.error(tb)
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Bias correction failed")
                msg_box.setText("Bias correction encountered an error.")
                msg_box.setDetailedText(tb)
                msg_box.addButton("OK", QMessageBox.ActionRole)
                msg_box.setWindowFlags(msg_box.windowFlags() & ~Qt.MSWindowsFixedSizeDialogHint)
                msg_box.setSizeGripEnabled(True)
                msg_box.layout().setSizeConstraint(QLayout.SetNoConstraint)
                msg_box.exec()

            self.worker = SamriWorker(work_bias, self)
            self.worker.done.connect(overlay.close)
            self.worker.done.connect(self._on_biascorrection_done)
            self.worker.failed.connect(overlay.close)
            self.worker.failed.connect(_on_biascorrection_failed)
            self.worker.start()

    def _copy_sub_to_data(self):
        """Copy DATA/Samri Registration/animal_id/bids/sub-animal_id → DATA/sub-animal_id."""
        try:
            src = os.path.join(self.Samri.bids_base, 'bids', f'sub-{self.Samri.animal_id}')
            dst = os.path.join(self.Samri.data_base, f'sub-{self.Samri.animal_id}')

            # SAMRI only ever writes data_selection.csv into its nipype work
            # cache (bids_base/results/generic_work/); copy it alongside the
            # subject's raw bids data too, so it travels with sub-<id> into
            # the copytree below instead of being left behind in the cache.
            csv_src = os.path.join(self.Samri.bids_base, 'results', 'generic_work', 'data_selection.csv')
            if os.path.exists(csv_src) and os.path.exists(src):
                shutil.copy(csv_src, os.path.join(src, 'data_selection.csv'))

            if os.path.exists(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        except Exception as e:
            logging.error(f"Failed to copy sub folder to DATA: {e}")

    def _on_registration_done(self, samri_input):
        self._copy_sub_to_data()

        verify_overlay = BusyOverlay(self, message="Verifying atlas registration…")
        verify_overlay.setGeometry(self.rect())
        verify_overlay.raise_()
        verify_overlay.show()
        QApplication.processEvents()

        transform_path = (
            f"{self.Samri.bids_base}/bids/sub-{self.Samri.animal_id}"
            f"/ses-{samri_input['working_session'][0]}/registration/output_Composite.h5"
        )
        success = os.path.exists(transform_path) and os.path.getsize(transform_path) > 0

        verify_overlay.close()

        msg = QMessageBox(self)
        if success:
            msg.setWindowTitle("Registration complete")
            msg.setText("Atlas registration was successful.")
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Registration verification failed")
            msg.setText(
                "SAMRI finished but no transformation file was found — "
                "atlas registration may not have completed correctly."
            )
        btn_ok = msg.addButton("OK", QMessageBox.ActionRole)
        btn_ok.setMinimumWidth(200)
        msg.exec()

        if success:
            # visualize_results() -> restart_gui() (VTK teardown/rebuild) ->
            # initialize_file() -> resample_tofit() (a real sitk BSpline
            # resample) all run synchronously on this (GUI) thread -- unlike
            # the registration itself, none of this is on a worker thread,
            # so without an overlay here the UI just silently freezes for
            # however long that takes, right after telling the user
            # registration already finished.
            self.overlay = BusyOverlay(self, message="Loading registered image…")
            self.overlay.run(self.Samri.visualize_results, self, logging)


    def _on_biascorrection_done(self):
        self._copy_sub_to_data()
        msg = QMessageBox(self)
        msg.setWindowTitle("Bias correction complete")
        msg.setText("Done with Biascorrection")
        msg.addButton("OK", QMessageBox.ActionRole)
        msg.exec()

    def initialize_trajectory_planning(self):
        if not ensure_atlas_available(self):
            return
        dlg = FileInput(self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dlg.get_values()

            folder = os.path.dirname(os.path.dirname(data[0]))
            transformPath = f"{folder}/registration/output_Composite.h5"
            if not os.path.exists(transformPath):
                msg_box = QMessageBox()
                msg_box.setWindowTitle("No Transformation File found")
                msg_box.setText("No Transformation File found, please first do SAMRI Registration.")
                msg_box.addButton("OK", QMessageBox.ActionRole)
                msg_box.exec()
                self.initialize_samri()
                return

            self._save_session_state(
                'trajectory', path=data[0], another=data[1], spacing=data[2],
                transform_path=transformPath)
            self.overlay = BusyOverlay(self, message="Initializing trajectory planning, please wait…")
            self.overlay.run(self.finish_trajectory_work,data, transformPath)

    def show_step_instructions(self):
        """
        pushButton_questionmark: re-show the current workflow's step-by-step
        instructions. Covers Trajectory Planning (which already pops these up
        automatically as the user progresses; this just lets them bring the
        current step back up on demand) and SAMRI (fetch -> select session).
        """
        traj = getattr(getattr(self, 'LoadMRI', None), 'TrajPlanning', None)
        if traj is not None:
            traj.show_current_step_popup()
            return
        if self.ui.tabWidget.currentWidget() is self.ui.tab_samri:
            self.show_samri_step_popup()
            return
        QMessageBox.information(
            self, "Instructions",
            "Load an MRI file, then start Trajectory Planning from the Tools menu "
            "to see step-by-step instructions here.")

    def show_samri_step_popup(self):
        if self.ui.frame_samri.isEnabled():
            title = "Step 2: Select Session"
            steps = [
                "Pick the session to work with from the 'Working Session' dropdown.",
                "Set the registration key/sequence and task (coronal/sagittal/axial) as needed.",
                "Click 'Biascorrection' to bias-correct the selected session, or 'Register' "
                "to run registration.",
            ]
        else:
            title = "Step 1: Enter Animal ID and Fetch Data"
            steps = [
                "Enter the Animal ID, adjusting the raw data path, server and password if needed.",
                "Click 'Fetch' to download the raw data ('Continue' to use data already fetched "
                "locally, 'Re-fetch' to redownload it).",
                "Once fetching finishes, you'll be able to select a session to bias-correct "
                "or register.",
            ]
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText("\n".join(f"{i+1}. {s}" for i, s in enumerate(steps)))
        msg_box.addButton("OK", QMessageBox.ActionRole)
        msg_box.exec()

    def finish_trajectory_work(self, data, transformPath):
        resampled_path = f"{data[0][:-7]}_resampled{data[2]*1000:.10g}um.nii.gz"
        self.data_pre_resampled = data[0]
        if not os.path.exists(resampled_path):
            ResampleData.resampling50um_trajectoryPlanning(data[0], new_spacing_mm=data[2])
        if not hasattr(self,'LoadMRI'):
            self.FileLoader = FileLoader(self)
            self.FileLoader.is_4d = False #3d file
            self.FileLoader.initialize_file(resampled_path,0,'coronal',0)
            zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
            Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)
            self.ui.comboBox_resamplefiles.addItem(os.path.basename(resampled_path)) #add to combobox for resampling
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.data_4d_3d.setCurrentIndex(1)
        else:
            self.restart_gui(resampled_path,data_view='coronal')

        data = list(data)
        data[0] = resampled_path

        self.LoadMRI.TrajPlanning = TrajectoryPlanning(self,self.ui,data,transformPath)

        self.ui.stackedWidget_3d.setVisible(True)
        self.ui.stackedWidget_3d.setCurrentIndex(0)
        box = self.ui.page_3D
        layout = box.layout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 1)

        #self.overlay.close()

    def open_new_window(self):
        subprocess.Popen([sys.executable] + sys.argv)


    def _update_3d_tp_height_cap(self, index):
        """stackedWidget_3d_tp's two pages need very different heights --
        page_29 (just the 3D-view toggle buttons) is compact, page_30
        (Cursor Position/Deepest Point/Insertion Point/Intensity group
        boxes) needs much more room. A single static maximumSize left
        enough headroom for page_30 that page_29 showed a lot of dead
        white space, but too little for page_30 let its content's minimum
        height exceed the cap, which Qt showed as real widget overlap
        rather than a clean shrink."""
        self.ui.stackedWidget_3d_tp.setMaximumSize(QSize(16777215, 200 if index == 0 else 350))

    def restart_gui(self, file_name, full_restart=True, label_file=False, data_view='coronal'):
        """
        Restart GUI if new main image is loaded.
        """
        if hasattr(self,'LoadMRI'):
            #deactivate interactor
            for image_index,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
                for view_name, vtk_widget in vtk_widget_image.items():
                    interactor = vtk_widget.GetRenderWindow().GetInteractor()
                    interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
            #delete measurement actors
            if hasattr(self,'Measurement'):
                for view_name, line_actor,line_slice_index,text_actor,_,dashed_lines,points in self.Measurement.measurement_lines:
                    renderer = self.Measurement.measurement_renderer[view_name]
                    renderer.RemoveActor(line_actor)
                    text_actor.SetVisibility(0)
                    renderer.RemoveActor(dashed_lines[1])
                    renderer.RemoveActor(dashed_lines[3])
                    renderer.RemoveActor(points[2])
                self.Measurement.measurement_lines = []
            for idx in self.LoadMRI.minimap.minimap_renderers:
                for vn in self.LoadMRI.minimap.minimap_renderers[idx]:
                    self.LoadMRI.minimap.minimap_renderers[idx][vn].RemoveAllViewProps()
                self.LoadMRI.minimap.minimap_renderers[idx] = {}
            for idx in self.LoadMRI.renderers:
                for vn in self.LoadMRI.renderers[idx]:
                    self.LoadMRI.renderers[idx][vn].RemoveAllViewProps()
                self.LoadMRI.renderers[idx] = {}

            for data_index in range(len(self.LoadMRI.vtk_widgets[0])):
                if hasattr(self.LoadMRI, f"intensity_table{data_index}"):
                    intensity_class = self.LoadMRI.intensity_table[data_index]
                    intensity_class.table.viewport().removeEventFilter(self)
            #remove cursor and minimap connections
            for key in ["scroll_0", "scroll_1", "scroll_2"]:
                try:
                    self.LoadMRI.cursor_ui[key].valueChanged.disconnect()
                except RuntimeError:
                    pass
            if not self.LoadMRI.volumes[0].is_4d: #3d
                self.ui.spinBox_x_data3d.valueChanged.disconnect()
                self.ui.spinBox_y_data3d.valueChanged.disconnect()
                self.ui.spinBox_z_data3d.valueChanged.disconnect()
                for idx in 0,1,2:
                    getattr(self.ui, f"go_down_data3d{idx}").clicked.disconnect()
                    getattr(self.ui, f"go_up_data3d{idx}").clicked.disconnect()
                    getattr(self.ui, f"go_right_data3d{idx}").clicked.disconnect()
                    getattr(self.ui, f"go_left_data3d{idx}").clicked.disconnect()
            else:    #4d
                # The widgets of all three data views exist in the .ui, but only
                # the loaded ones ever got connected (Cursor.init_widgets and
                # initialize_zoom_controls run per data view), and disconnect()
                # raises RuntimeError on a signal with no connections — same
                # reason the scroll bars above are wrapped.
                def _disconnect(signal):
                    try:
                        signal.disconnect()
                    except RuntimeError:
                        pass

                for image_index in 0,1,2:
                    for axis in ('x','y','z'):
                        _disconnect(self.LoadMRI.cursor_ui[f"spin_{axis}{image_index}"].valueChanged)
                    #self.LoadMRI.cursor_ui[f"spin_y_data{image_index}"].valueChanged.disconnect()
                    #self.LoadMRI.cursor_ui[f"spin_z_data{image_index}"].valueChanged.disconnect()
                    for idx in 0,1,2:
                        _disconnect(getattr(self.ui, f"go_down_data{idx}{image_index}").clicked)
                        _disconnect(getattr(self.ui, f"go_up_data{idx}{image_index}").clicked)
                        _disconnect(getattr(self.ui, f"go_right_data{idx}{image_index}").clicked)
                        _disconnect(getattr(self.ui, f"go_left_data{idx}{image_index}").clicked)

            #remove old renderers
            for image_index,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
                for view_name, vtk_widget in vtk_widget_image.items():
                    ren_win = vtk_widget.GetRenderWindow()
                    ren_coll = ren_win.GetRenderers()

                    renderers_to_remove = [ren_coll.GetItemAsObject(i) for i in range(ren_coll.GetNumberOfItems())]

                    for old_renderer in renderers_to_remove:
                        ren_win.RemoveRenderer(old_renderer)


            # Disconnect any important signals
            if hasattr(self.LoadMRI, "minimap"):
                try:
                    zoom_notifier.factorChanged.disconnect(self.LoadMRI.minimap.create_small_rectangle)
                except RuntimeError:
                    pass

        for dock_name in ("dock_paintbrush4d", "dock_segmentation", "dockWidget_ephys",
                          "dock_paintbrush", "dock_measurement"):
            dock = self.findChild(QDockWidget, dock_name)
            if dock:
                dock.close()
                if full_restart:
                    dock.deleteLater()

        # TrajectoryPlanning3DWindow (trajectory_planning_3d/window.py) sets
        # no objectName -- just a window title -- so it can't be found via
        # findChild(QDockWidget, name) like the docks above; go through
        # TrajPlanning.tp3d_window directly instead (None if the 3D window
        # was never opened this session).
        tp = getattr(self.LoadMRI, 'TrajPlanning', None) if hasattr(self, 'LoadMRI') and self.LoadMRI is not None else None
        tp3d_window = getattr(tp, 'tp3d_window', None)
        if tp3d_window is not None:
            tp3d_window.close()
            if full_restart:
                tp3d_window.deleteLater()

        if full_restart:
            # only tear down widget_pgEphys's plot when self.ui is about to be
            # rebuilt below -- otherwise this permanently kills its ViewBox
            # since the same widget_pgEphys is kept around
            existing_layout = QWidget.layout(self.ui.widget_pgEphys)   # call as unbound
            if existing_layout is not None:
                QWidget().setLayout(existing_layout)

        # Clear stored references
        self.LoadMRI = None

        #restart GUI
        if full_restart:
            from ui_form import Ui_MainWindow
            self.resize_bool=False
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.add_actions()
            self.show()
            # setupUi() creates a brand new stackedWidget_3d_tp with none of
            # __init__'s signal connections -- reconnect this one or its
            # height cap silently reverts to the .ui's static default.
            self.ui.stackedWidget_3d_tp.currentChanged.connect(self._update_3d_tp_height_cap)
            self._update_3d_tp_height_cap(self.ui.stackedWidget_3d_tp.currentIndex())

        QApplication.processEvents()
        self.resize_bool=True

        #self.LoadMRI = LoadMRI(self)
        image = sitk.ReadImage(file_name)
        volume = sitk.GetArrayFromImage(image)
        self.FileLoader = FileLoader(self)
        if volume.ndim==4:
            self.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")
            self.FileLoader.is_4d = True
        else:
            self.FileLoader.is_4d = False #3d file
        self.FileLoader.initialize_file(file_name,0,data_view,0,full_restart=full_restart,label_file=label_file)
        self.ui.data_4d_3d.setCurrentIndex(0 if self.FileLoader.is_4d else 1)
        self.ui.tabWidget.setCurrentIndex(0)

        zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
        Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0][data_view], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)
        #the widgets have a size only after the rebuilt UI has been laid out, so build the minimaps now
        QApplication.processEvents()
        self.on_gui_resize()
        return

    def snapshot_view_state(self):
        """
        Remember the current main file's view (slice position, zoom) under its
        path in self._session_view_cache, so switching back to it later via
        reapply_view_state() restores this instead of the freshly-loaded default.
        """
        if not hasattr(self, 'LoadMRI') or self.LoadMRI is None:
            return
        file_path = self.LoadMRI.volumes[0].file_path
        self._session_view_cache[file_path] = {
            'slice_indices': {idx: list(val) for idx, val in self.LoadMRI.slice_indices.items()},
            'zoom_factor': Zoom.global_zoom_factor,
            'tab_index': self.ui.tabWidget.currentIndex(),
        }

    def reapply_view_state(self, file_path):
        """
        Reapply the view previously stored for file_path by snapshot_view_state(),
        if any. No-op the first time a file is opened (nothing cached yet).
        """
        state = self._session_view_cache.get(file_path)
        if state is None:
            return

        for data_index, (z, y, x) in state['slice_indices'].items():
            if data_index not in self.LoadMRI.slice_indices:
                continue
            self.Cursor.scroll_slice('axial', 0, data_index, val=z)
            self.Cursor.scroll_slice('coronal', 0, data_index, val=y)
            self.Cursor.scroll_slice('sagittal', 0, data_index, val=x)

        if Zoom.global_zoom_factor:
            relative_factor = state['zoom_factor'] / Zoom.global_zoom_factor
            Zoom.zoom(relative_factor, self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets, 0, data_3d=True)

    def refresh_mri_cache_combo(self):
        """
        Repopulate comboBox_cache with the MRI files that have a cached view
        state (i.e. every file visited this session other than the one
        currently open). Hidden when there's nothing to switch to -- either
        no other file was ever opened, or none has been left yet (nothing
        gets cached until you switch away from it).
        """
        combo = self.ui.comboBox_cache
        current_path = self.LoadMRI.volumes[0].file_path if getattr(self, 'LoadMRI', None) else None
        combo.blockSignals(True)
        combo.clear()
        for path in self._session_view_cache:
            if path == current_path:
                continue
            combo.addItem(os.path.basename(path), path)
        combo.blockSignals(False)
        combo.setVisible(combo.count() > 0)

    def _switch_mri_from_cache(self, index):
        path = self.ui.comboBox_cache.itemData(index)
        if path:
            self._restore_session_entry('mri', {'path': path})

    def quit(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    # Register the .qrc file dynamically

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "resources.rcc")
    os.chdir(os.path.dirname(__file__))

    QResource.registerResource(file_path)
    #to mix vtk and QtQuick3D
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setStyle(QuickTooltipStyle(app.style()))
    # app-wide default text size -- widgets with their own explicit QFont
    # (various setFont(...) calls in ui_form.py, from Qt Designer) keep
    # whatever size they were set to; this only raises the baseline for
    # everything else.
    default_font = app.font()
    default_font.setPointSize(12)
    app.setFont(default_font)
    #dark mode
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6() + """
        QLineEdit:!read-only:enabled, QTextEdit[readOnly="false"]:enabled, QPlainTextEdit[readOnly="false"]:enabled,
        QSpinBox[readOnly="false"]:enabled, QDoubleSpinBox[readOnly="false"]:enabled, QComboBox:enabled {
            background-color: #204060;
            border: 1px solid #3d8ec9;
            color: #ffffff;
        }
        QComboBox:enabled::drop-down {
            border-left: 1px solid #3d8ec9;
        }
    """)
    app.setApplicationName("IMPLAnT")
    app.setWindowIcon(QIcon(os.path.join(_base_dir, "Icons/Github/IMPLAnT_quad.png")))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

