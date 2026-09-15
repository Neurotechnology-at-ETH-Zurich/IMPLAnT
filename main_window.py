# This Python file uses the following encoding: utf-8
# Important: You need to run the following command to generate the ui_form.py file: pyside6-uic form.ui -o ui_form.py
import multiprocessing
import os
import sys

# Standalone worker-subprocess dispatch (--ripple-worker, --samri-worker,
# ...): must run and exit before any GUI import (PySide6/VTK/SimpleITK etc)
# -- see worker_dispatch.py's module docstring for why. Split into its own
# module purely to keep this file's top from being ~170 lines of repetitive
# per-worker dispatch blocks; no behavior change.
import worker_dispatch
worker_dispatch.maybe_run_worker_and_exit()

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
from paths_config import _base_dir, _exe_dir, _paths, get_raw_base
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
from ephys.ui_dock_ephys import Ui_Dock_ephys
from ephys.ui_tab_main_ephys import Ui_tab_ephys
from ephys.ui_tab_popups_ephys import Ui_tab as Ui_tab_popups_ephys
from gui_utils.ui_tab_popups_time_series import Ui_tab_15 as Ui_tab_popups_time_series
from file_handling.ui_tab_popups_time_series_ii import Ui_tab_6 as Ui_tab_popups_time_series_ii
from intraoperative.ui_tab_intraoperative import Ui_Form as Ui_tab_surgery
from samri.ui_tab_samri import Ui_tab_samri
from PySide6.QtCore import Qt, QCoreApplication, QResource, QSize
from PySide6.QtWidgets import QLayout
import qdarkstyle
from utils.zoom import Zoom
import shutil
from samri.samri_main import InitSAMRI,SAMRI_InputDialog,SAMRI_InputDock,SamriCancelToken
from samri.samri_logging import LogAdapter
from gui_utils.busy_worker import BusyWorker, show_worker_error
import logging
from PySide6.QtWidgets import QWidget
from trajectory_planning.trajectory_planning import TrajectoryPlanning
from trajectory_planning.trajectory_planning_mri import TrajectoryPlanningMri
from trajectory_planning.file_input_output import FileInput
from mrid_utils.atlas_fetch import ensure_atlas_available
from intraoperative.load_surgery_plan import LoadSurgeryPlan
from intraoperative.surgery_controller import SurgeryController
from pypdf import PdfReader
import pandas as pd
from file_handling.loader import FileLoader
from PySide6.QtGui import QIcon, QAction, QFont
from mrid_utils import atlas_switch
import subprocess
import tempfile
from PySide6.QtCore import QTimer
import datetime
from PySide6.QtWidgets import QProxyStyle, QStyle


class QuickTooltipStyle(QProxyStyle):
    """Shortens the hover delay before any tooltip appears, app-wide."""
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.SH_ToolTip_WakeUpDelay:
            return 300
        return super().styleHint(hint, option, widget, returnData)


def _run_trajectory_worker_subprocess(payload):
    """Runs the trajectory-planning resample step (trajectory_planning/
    trajectory_worker.py) in a separate OS process instead of in this one --
    mirrors samri/samri_main.py's _run_worker_subprocess. Always called from
    _resample_for_trajectory_planning, which only ever runs inside a
    BusyWorker QThread (never the GUI thread), so blocking here on the child
    via proc.wait() is fine.

    On a non-zero exit, raises RuntimeError with the last ~4000 characters of
    combined stdout/stderr, same tail-slicing convention as
    samri_main.py's _run_worker_subprocess."""
    frozen = getattr(sys, 'frozen', False)
    worker_dir = getattr(sys, '_MEIPASS', _base_dir)
    script = os.path.join(worker_dir, 'trajectory_planning', 'trajectory_worker.py')
    cmd = [sys.executable, '--trajectory-worker'] if frozen else [sys.executable, script]

    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, 'input.json')
        output_path = os.path.join(tmp, 'output.json')
        with open(input_path, 'w') as f:
            _json.dump(payload, f)

        cmd = cmd + ['--input', input_path, '--output', output_path]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.stdout:
            print(proc.stdout, end='', flush=True)

        if proc.returncode != 0:
            outcome = 'was killed' if proc.returncode < 0 else f'failed (exit code {proc.returncode})'
            tail = (proc.stdout + proc.stderr)[-4000:]
            raise RuntimeError(f"Trajectory planning resample subprocess {outcome}.\n{tail}")

        with open(output_path) as f:
            return _json.load(f)


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
        # register_session_loaded_callback()'s registry -- see the Extension
        # API block above register_tab below.
        self._session_loaded_callbacks = {}
        # register_module()'s registry -- see the Extension API block below.
        self._registered_modules = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_split_ui(Ui_Dock_ephys, self.ui.dockWidget_ephys.setWidget)
        # tabWidget pages split out of form.ui: after setupUi, tabWidget only
        # has [0]PostSurgery. Re-inserting at these original tabWidget
        # indices, in ascending order, then appending tab_samri/surgery last
        # (in that order), restores the original 7-tab layout: 0 PostSurgery,
        # 1 tab_15, 2 tab_6, 3 tab_ephys, 4 tab, 5 tab_samri, 6 surgery.
        self.load_split_ui(
            Ui_tab_popups_time_series,
            lambda w: self.register_tab(w, "Popups for Time-Series Data", index=1),
        )
        self.load_split_ui(
            Ui_tab_popups_time_series_ii,
            lambda w: self.register_tab(w, "Popups for Time-Series Data II", index=2),
        )
        self.load_split_ui(
            Ui_tab_ephys,
            lambda w: self.register_tab(w, "Ephys", index=3),
        )
        self.load_split_ui(
            Ui_tab_popups_ephys,
            lambda w: self.register_tab(w, "Popups for ephys", index=4),
        )
        # tab_samri and surgery (Intraoperative tab) were originally the last
        # two in form.ui's static tab order -- appending them here, in this
        # order (no index, same as addTab), lands them back at the end,
        # matching their original positions.
        self.load_split_ui(
            Ui_tab_samri,
            lambda w: self.register_tab(w, "SAMRI"),
        )
        self.load_split_ui(
            Ui_tab_surgery,
            lambda w: self.register_tab(w, "Intraoperative"),
        )
        # nothing cached yet at startup -- hide until there's another file/recording to switch to
        #self.ui.comboBox_cache.setVisible(False)
        #self.ui.comboBox_cache_2.setVisible(False)
        #self.ui.comboBox_cache.activated.connect(self._switch_mri_from_cache)
        #self.ui.comboBox_cache_2.activated.connect(self._switch_ephys_from_cache)
        self.setWindowTitle("IMPLAnT")
        self.setWindowIcon(QIcon(os.path.join(_base_dir, "Icons/Github/IMPLAnT_quad.png")))
        # Lives for the whole app session (unlike TrajectoryPlanning, which
        # only exists while an MRI is loaded) -- see intraoperative/
        # surgery_controller.py for why the Intraoperative tab has no MRI/
        # TrajectoryPlanning dependency at all. Registered (not just assigned)
        # as the pilot for the module registry described in the Extension API
        # block below -- see register_module()'s docstring for why this one
        # needed no teardown() to be added.
        self.register_module('surgery', SurgeryController(self))
        self.add_actions()
        self.ui.tabWidget.setCurrentIndex(0)

    def load_split_ui(self, ui_class, attach):
        """
        Extension API (see CONTRIBUTING.md): loads a Designer form built as
        its own standalone .ui file (e.g. ephys/dock_ephys.ui) and attaches
        its top-level widget via `attach(content_widget)` -- a dock's
        setWidget, or `lambda w: self.register_tab(w, "My Tool")`. The
        form's widgets are flattened onto self.ui (a `pushButton_go` in it
        becomes self.ui.pushButton_go), as if built into form.ui directly.
        Returns the generated Ui_* instance (rarely needed).
        """
        # Parented to self (a real top-level window) from the start, rather
        # than left parentless until attach() reparents it below: a widget
        # built while genuinely parentless is briefly top-level itself, and
        # if it (or a descendant, e.g. a native="true" VTK-hosting widget --
        # see intraoperative/tab_intraoperative.ui's `widget`) gets its
        # platform window created during that window, Qt can later warn
        # "QWidgetWindow(...) must be a top level window" once attach()
        # reparents it into its real, non-top-level home (a tab/dock).
        # Harmless in practice, but avoidable -- attach() below still
        # reparents content into its actual final home either way.
        content = QWidget(self)
        sub_ui = ui_class()
        sub_ui.setupUi(content)
        attach(content)
        # setupUi names the container after the original page/dock widget (e.g. "page_3D") --
        # expose it under that name too, so self.ui.<original_name> keeps working, not just
        # self.ui.<name-of-a-child-inside-it>.
        setattr(self.ui, content.objectName(), content)
        for name, value in vars(sub_ui).items():
            if not name.startswith("_"):
                setattr(self.ui, name, value)
        return sub_ui

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

        #resize to inital size, clamped to whatever screen we're actually on
        # (1600x900/1500x800 min don't fit smaller laptop displays otherwise)
        screen_geo = QApplication.primaryScreen().availableGeometry()
        self.resize(min(1600, screen_geo.width()), min(900, screen_geo.height()))
        self.setMinimumSize(min(1500, screen_geo.width()), min(800, screen_geo.height()))

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
        self.ui.actionIntraoperative.triggered.connect(lambda: self.load_previous_session(['surgery']))
        # Intraoperative tab's measured-mm bregma/lambda fields: "sag"/"cor" match
        # the same sagittal/coronal slice-index convention as the voxel-
        # cursor spinboxes elsewhere (x=sag=ML/RL, y=cor=AP) -- DV/"ax" was
        # dropped entirely (no longer measured), so reproject_target_to_null
        # (intraoperative/reprojection.py) is now a pure 2D (ML/RL, AP)
        # reprojection with no vertical/leveling component.
        for sb in (self.ui.doubleSpinBox_sag_b, self.ui.doubleSpinBox_cor_b,
                   self.ui.doubleSpinBox_sag_l, self.ui.doubleSpinBox_cor_l):
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
        # opening electrode localization, which has no in-view switcher of
        # its own; trajectory planning and the ephys 3D view instead get
        # their own live in-view switchers (TpRegistration.reload_atlas_view,
        # Visualisation3D.reload_atlas_view in ephys/visualisation3D.py).
        self.ui.actionAtlas = self.register_menu_action(
            self.ui.menuGUI, "Atlas…",
            triggered=self.show_atlas_selector,
            before=self.ui.actionLoad_Prev_Session,
        )
        # per-tab "Open Session" placeholders: Structural/Time-Series Tools -> mri (filtered by
        # dimensionality), Ephys Analysis -> ephys, Surgery -> samri
        self.ui.actionOpen_Session_2.triggered.connect(lambda: self.load_previous_session(['mri'], is_4d=False))
        self.ui.actionOpen_Session.triggered.connect(lambda: self.load_previous_session(['mri'], is_4d=True))
        self.ui.actionOpen_Session_3.triggered.connect(lambda: self.load_previous_session(['ephys']))
        self.ui.actionOpen_Session_4.triggered.connect(lambda: self.load_previous_session(['samri']))

        # Structural Tools / Time-Series Tools / Ephys Analysis menu actions (besides "Open
        # Session") only do anything once ButtonsGUI_Structural/4D or InitEphys
        # connects them, which only happens once a matching file is loaded --
        # grey them out until then instead of leaving them as silent no-ops.
        for action_name in ('actionRegister', 'actionResample', 'actionPaintbrush',
                             'actionSegmentation', 'actionMeasurement',
                             'actionStart_MRIDlabels', 'actionContrast_Adjustments',
                             'actionRippl_AI', 'actionTheta_Detection', 'actionLoad_Spike_Sorting'):
            getattr(self.ui, action_name).setEnabled(False)
        self.ui.menuElectrode_Localization.menuAction().setEnabled(False)

        # Re-render if tab changed
        #self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self.unsetCursor()

    # ------------------------------------------------------------------
    # Extension API -- see CONTRIBUTING.md's "Adding your own tab/tool to
    # MainWindow" for the short version and the built-in-tabs caveat.
    # ------------------------------------------------------------------

    def register_tab(self, widget, title, index=None):
        """
        Add `widget` (built in Designer, not with runtime addWidget() calls --
        see CONTRIBUTING.md) as a new page of self.ui.tabWidget. `index`
        inserts at that position instead of appending. Returns the tab index
        -- the tab bar is hidden, so switch to it later via
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.indexOf(widget)),
        not a hardcoded number (indices shift as tabs are added).
        """
        if index is None:
            self.ui.tabWidget.addTab(widget, title)
        else:
            self.ui.tabWidget.insertTab(index, widget, title)
        return self.ui.tabWidget.indexOf(widget)

    def register_menu_action(self, menu, text, triggered=None, before=None, enabled=True):
        """
        Add a new QAction to an existing menu (self.ui.menuGUI, ...), same as
        self.ui.actionAtlas in add_actions() above. `before`: an existing
        QAction to insert in front of (else appended). `triggered`: connected
        to the action's triggered signal if given. `enabled=False`: starts
        greyed out, same convention as actionRegister/actionResample/... in
        add_actions() (several built-ins do nothing until a file loads).
        Returns the QAction.
        """
        action = QAction(text, self)
        if before is not None:
            menu.insertAction(before, action)
        else:
            menu.addAction(action)
        if triggered is not None:
            action.triggered.connect(triggered)
        if not enabled:
            action.setEnabled(False)
        return action

    def register_session_loaded_callback(self, kind, callback):
        """
        Get notified once a session of the given `kind` finishes loading
        (not when it starts), instead of hooking the load paths yourself.
        `kind`: 'mri'/'ephys'/'samri'/'trajectory'/'surgery' (same vocabulary
        as load_previous_session(kinds=...)). Registering the same kind more
        than once is fine; a raising callback is logged, others still run.

        Gotchas, not obvious from the call sites alone:
        - 'mri' fires from 4 separate places (initialize_mri_session,
          _restore_session_entry, restart_gui, and finish_trajectory_work's
          first-load branch) -- they don't share a helper today.
        - a successful SAMRI *registration* fires 'mri', not 'samri' (it
          ends by reloading the image via restart_gui) -- 'samri' only fires
          for fetch/biascorrection (_on_bruker2bids_done/
          _on_biascorrection_done).
        - 'trajectory' fires after 'mri' for the same load (finish_
          trajectory_work calls/is called alongside an 'mri' load) -- expect
          both, in that order.
        - 'surgery' fires from SurgeryController.load_plan()
          (intraoperative/surgery_controller.py), not from this file --
          that's the one place both load paths (here and load_surgery_plan.py)
          converge.
        """
        self._session_loaded_callbacks.setdefault(kind, []).append(callback)

    def _notify_session_loaded(self, kind):
        for callback in self._session_loaded_callbacks.get(kind, []):
            try:
                callback()
            except Exception:
                logging.exception(
                    "register_session_loaded_callback callback for %r failed", kind)

    def register_module(self, name, module):
        """
        Register a feature-module controller under `name` instead of just
        assigning self.<name> = module. Currently registered: 'surgery'
        (__init__), 'Ephys' (do_ephys_heavy), 'Samri' (fetch_data),
        'ButtonsGUI_Structural'/'ButtonsGUI_TimeSeries' (file_handling/
        loader.py), 'LoadMRI.TrajPlanning' (finish_trajectory_work),
        'Measurement' (gui_utils/buttons_gui_structural.py's
        measurement_function) -- re-registering (a new file/recording/plan
        replacing the previous one) is expected and just overwrites the entry.

        `name` can be dotted (e.g. 'LoadMRI.TrajPlanning') for a module that
        naturally lives on an attribute other than self -- TrajPlanning is
        self.LoadMRI.TrajPlanning, not self.TrajPlanning, since it only
        exists while an MRI is loaded and several places already look it up
        that way (e.g. restart_gui's teardown, show_step_instructions). Only
        the last segment is set; everything before it (self.LoadMRI here)
        must already exist.

        - self.<name> (or the target named by the dotted path) is set to
          `module`, so every existing reference (self.surgery, self.Ephys,
          self.LoadMRI.TrajPlanning, ...) keeps working unchanged.
        - if `module` defines `teardown()`, it's called with no arguments
          from restart_gui(), before self.ui is replaced (see
          _teardown_registered_modules). 'Measurement' is the one module
          above that actually defines one (core/measurement.py) -- it just
          resets its own measurement_lines bookkeeping; the VTK side (its
          separate overlay renderer per view) is already covered by
          teardown_load_mri()'s renderer-wide sweep. 'surgery'/'Ephys'/
          'Samri'/'ButtonsGUI_*'/'LoadMRI.TrajPlanning' still don't define
          one: restart_gui doesn't touch Ephys/Samri/ButtonsGUI_* at all, and
          LoadMRI/TrajPlanning's actual per-restart cleanup is restart_gui's
          own hand-written VTK/signal teardown (core/load_MRI_file.py's
          teardown_load_mri()), not routed through this registry. Registering
          those is for discoverability (self._registered_modules lists every
          live controller), not because any cleanup was replaced.
        """
        target = self
        *parents, attr = name.split('.')
        for part in parents:
            target = getattr(target, part)
        setattr(target, attr, module)
        self._registered_modules[name] = module

    def _teardown_registered_modules(self):
        """Calls teardown() on every registered module that defines one (see
        register_module) -- from restart_gui(), before self.ui is replaced."""
        for name, module in self._registered_modules.items():
            self._call_module_teardown(name, module)

    def _call_module_teardown(self, name, module):
        """Calls module.teardown() if it defines one, logging (not raising)
        on failure. Shared by _teardown_registered_modules (restart_gui's
        full replace) and _free_previous_workflow_state (leaving a workflow
        for a different one) -- the two places a registered module gets
        discarded, so a teardown() fires the same way regardless of which
        path discarded it."""
        teardown = getattr(module, 'teardown', None)
        if teardown is not None:
            try:
                teardown()
            except Exception:
                logging.exception("teardown() failed for registered module %r", name)

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
        'surgery': 'Surgery',
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
        # Close any lingering tool dock (paintbrush/measurement/segmentation/
        # ephys) whenever the user starts a different kind of session --
        # 'overlay' is excluded since it adds to the CURRENT main image
        # rather than switching away from it. restart_gui() (reached via the
        # 'mri' branch) also does this itself with full_restart=True (a
        # proper detach, since self.ui is being rebuilt there); this call is
        # what covers ephys/samri/trajectory/surgery, and the very first
        # 'mri' load (which never reaches restart_gui at all).
        if kind != 'overlay':
            self._close_tool_docks(full_restart=False)
            self._free_previous_workflow_state(kind)
        {'mri': self.initialize_mri_session,
         'ephys': self.open_ephys_data,
         'samri': self.initialize_samri,
         'trajectory': self.initialize_trajectory_planning,
         'overlay': self.add_another_file,
         'surgery': self.initialize_surgery}[kind]()

    def show_atlas_selector(self):
        atlas_switch.show_atlas_selector(self)

    def load_previous_session(self, kinds=None, is_4d=None):
        """
        Show a picker of previously loaded MRI/ephys files or SAMRI animal
        IDs. `kinds` restricts which type(s) are listed -- None (the File
        menu's global "Load Prev. File") shows all three; a single-element
        list (the per-tab "Open Session" actions) shows only that kind and
        adds a "Load New File..." button. `is_4d` further restricts 'mri'
        entries to only 3D or only 4D files, for the Structural/Time-Series Tools menus.
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
        dlg.resize(1000, 400)
        layout = QtWidgets.QVBoxLayout(dlg)
        if not entries:
            layout.addWidget(QtWidgets.QLabel("No previous sessions found.", dlg))
        list_widget = QtWidgets.QListWidget(dlg)
        for kind, entry in entries:
            label = self._SESSION_KIND_LABELS[kind]
            if kind == 'samri':
                text = f"[{label}] Animal {entry.get('animal_id', '?')}"
            else:
                path = entry.get('path', '?')
                folder = os.path.basename(os.path.dirname(path))
                text = f"[{label}] {folder}/{os.path.basename(path)}"
            text += f"   —   {entry.get('timestamp', '')}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(Qt.UserRole, (kind, entry))
            item.setToolTip(entry.get('path', ''))
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
            # SAMRI's "new" action (initialize_samri) doesn't load a file at
            # all -- it starts a fresh registration session (raw data
            # folder/animal ID) -- so "Load New File..." is misleading there.
            new_btn_text = "Start New Session" if single_kind == 'samri' else "Load New File..."
            new_btn = buttons.addButton(new_btn_text, QtWidgets.QDialogButtonBox.ActionRole)
            def _load_new():
                load_new['flag'] = True
                dlg.accept()
            new_btn.clicked.connect(_load_new)
        buttons.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        for btn in buttons.buttons():
            btn.setMinimumHeight(36)
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
        # Same reasoning as _open_new_session above: close lingering tool
        # docks and free the previous workflow's heavy state whenever
        # restoring any kind of session except 'overlay'.
        if kind != 'overlay':
            self._close_tool_docks(full_restart=False)
            self._free_previous_workflow_state(kind)
        if kind == 'mri':
            path = entry.get('path')
            if not path or not os.path.exists(path):
                QMessageBox.warning(self, "File not found", f"MRI file no longer exists:\n{path}")
                return
            self.FileLoader = FileLoader(self)
            file_name, data_view = self.FileLoader.restore_file(path)
            if file_name is not None:
                self._finish_mri_load(file_name, data_view, self.FileLoader.is_4d)

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
            self._start_trajectory_planning_work(data, transform_path)

        elif kind == 'surgery':
            path = entry.get('path')
            if not path or not os.path.exists(path):
                QMessageBox.warning(self, "File not found", f"Surgery plan report no longer exists:\n{path}")
                return
            try:
                reader = PdfReader(path)
                attachment = reader.attachments["trajectory_planning_data.json"][0]
            except (KeyError, IndexError, FileNotFoundError):
                QMessageBox.critical(
                    self, "No trajectory data found",
                    "This PDF has no embedded trajectory data -- it may have "
                    "been saved before this feature was added, or isn't a "
                    "trajectory report.")
                return
            except Exception as exc:
                QMessageBox.critical(self, "Could not read PDF", str(exc))
                return
            data = _json.loads(attachment)
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.indexOf(self.ui.surgery))
            self.overlay = BusyOverlay(self, message="Loading surgery plan, please wait…")
            self.overlay.run(self.surgery.load_plan, data, pdf_path=path)

    def open_ephys_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open ephys Data File",
            get_raw_base(self),
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
        self.register_module('Ephys', InitEphys(self, file_name))
        self.Ephys.open_dat(file_name)
        self.reapply_ephys_view_state(file_name)
        self._save_session_state('ephys', path=file_name)
        #self.refresh_ephys_cache_combo()
        #ask about the spike cluster plot once the busy overlay is gone
        QTimer.singleShot(0, self.Ephys.prompt_spike_sorting)
        self._notify_session_loaded('ephys')

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
        combo = self.ui.comboBox_cache_2
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
        self._finish_mri_load(file_name, data_view, self.FileLoader.is_4d)

    def _finish_mri_load(self, file_name, data_view, is_4d):
        """
        Shared tail for the two places a plain MRI (re)load finishes without
        going through restart_gui()'s full-UI-rebuild path --
        initialize_mri_session (brand new file) and _restore_session_entry
        (reopening a recent one): connects the zoom notifier to the new
        minimap, fits the coronal view to window for 3D data, adds the file
        to the resample combobox, sets the 4D view title if needed, and
        switches to the default tab/view.

        restart_gui() (core/load_MRI_file.py) and finish_trajectory_work()'s
        first-load branch do something similar but not identical -- not
        folded in here, since forcing them to match this exactly would
        change real behavior, not just remove duplication (e.g. restart_gui
        doesn't currently add the file to comboBox_resamplefiles at all,
        unlike every other load path -- worth checking whether that's
        deliberate).
        """
        zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
        if not is_4d:
            Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)

        self.ui.comboBox_resamplefiles.addItem(os.path.basename(file_name)) #add to combobox for resampling
        if is_4d:
            self.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")

        tab_idx = 0 if is_4d else 1
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.data_4d_3d.setCurrentIndex(tab_idx)
        self._notify_session_loaded('mri')


    def on_gui_resize(self):
        """
        Re-render VTK widgets when GUI size changes.
        """
        for widget in (
            self.ui.vtkWidget_data_sagittal, self.ui.vtkWidget_data_coronal, self.ui.vtkWidget_data_axial,
            self.ui.vtkWidget_data_seg3D,
            self.ui.vtkWidget_data00, self.ui.vtkWidget_data01, self.ui.vtkWidget_data02, self.ui.vtkWidget_data03,
            self.ui.vtkWidget_legend0,
            self.ui.vtkWidget_data10, self.ui.vtkWidget_data11, self.ui.vtkWidget_data12, self.ui.vtkWidget_data13,
            self.ui.vtkWidget_legend1,
            self.ui.vtkWidget_data10, self.ui.vtkWidget_data11, self.ui.vtkWidget_data12, self.ui.vtkWidget_data13,
            self.ui.vtkWidget_legend2,
            self.ui.vtkWidget_trajPlan_1,
            self.ui.vtkWidget_ephys,  # barcode sachen
        ):
            # A widget can be hidden (a different tab or stacked-widget page
            # active) while still existing -- Render()ing it while unmapped
            # can hang the GL driver on an X11/DRI3 buffer-swap wait that
            # never arrives (confirmed via gdb backtrace: blocked in
            # vtkXOpenGLRenderWindow::MakeCurrent -> loader_dri3_get_buffers
            # -> xcb_wait_for_special_event), freezing the whole GUI -- see
            # trajectory_planning/rendering.py's identical guard.
            if widget.isVisible():
                widget.GetRenderWindow().Render()

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
        # onto an empty Intraoperative tab with nothing loaded.
        #
        # Deliberately independent of LoadMRI/TrajectoryPlanning -- see
        # intraoperative/surgery_controller.py -- so no MRI/registration
        # state is required or touched here.
        dlg = LoadSurgeryPlan(self, parent=self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # indexOf rather than a hardcoded index -- the Intraoperative tab
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
            self.register_module('Samri', InitSAMRI(samri_input))
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

        self.worker = BusyWorker(work_init, self)
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
        self._notify_session_loaded('samri')


    def start_registration(self,samri_input):
        if not ensure_atlas_available(self):
            return

        if samri_input['register']:
            from samri import memory_guard
            atlas_path = os.path.join(samri_input['atlas_folder'], _paths['atlas_template'])
            try:
                ok, required_gb, avail_gb = memory_guard.check(atlas_path)
            except Exception:
                ok = True
            if not ok:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Low memory for registration")
                msg_box.setText(
                    f"This registration is estimated to need ~{required_gb:.0f}GB of free RAM, "
                    f"but only ~{avail_gb:.0f}GB is currently available.\n\n"
                    "Running anyway risks the registration (and possibly the whole "
                    "application) being killed by the system if memory runs out.\n\n"
                    "To free up memory before proceeding:\n"
                    "  • Close unused applications (web browsers and IDEs are usually "
                    "the biggest RAM users)\n"
                    "  • Restart this application if it's been open a long time\n"
                    "  • Reboot the computer if it's been on for many days -- long "
                    "uptimes accumulate memory that a simple app close won't release"
                )
                btn_proceed = msg_box.addButton("Proceed anyway", QMessageBox.ActionRole)
                msg_box.addButton("Cancel", QMessageBox.ActionRole)
                msg_box.exec()
                if msg_box.clickedButton() != btn_proceed:
                    return

        cancel_token = SamriCancelToken()

        def work_registration():
            self.ui.dockWidget_ephys.setEnabled(False)
            self.Samri.output_filepath = self.Samri.start_registration(
                samri_input, on_progress=self.worker.progress.emit, cancel_token=cancel_token)

        # Clean up previous worker if it exists
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.done.disconnect()
            self.worker.failed.disconnect()
            self.worker = None

        if samri_input['register']:
            csv_path = f"{self.Samri.bids_base}/results/generic_work/data_selection.csv"
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, index_col=0)

                # data_selection.csv is left over from whichever run last wrote it --
                # it can predate the session selected here (a previous attempt for a
                # different session, or one that matched no scans at all), so there's
                # no guarantee it has a row for this session. Skip the "already
                # registered" check rather than crashing on an empty match: if this
                # session was never in it, there's nothing to check for yet either.
                # A run that crashed before finishing bids_data_selection (e.g. the
                # pandas/pybids column-naming mismatch) can also leave this file with
                # no columns at all, not just no matching rows -- guard for that too.
                matches = df.loc[df['session'] == samri_input['working_session'][0]] if 'session' in df.columns else df.iloc[0:0]
                if not matches.empty:
                    idx = matches.index[0] #original_path?
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

            self.worker = BusyWorker(work_registration, self)
            overlay = BusyOverlay(self, message="Registering, please wait…", cancellable=True)
            overlay.setGeometry(self.rect())
            overlay.raise_()
            overlay.show()
            overlay.cancelled.connect(cancel_token.cancel)
            self.worker.progress.connect(overlay.set_message, Qt.QueuedConnection)
            self.worker.done.connect(overlay.close)
            self.worker.done.connect(lambda: self._on_registration_done(samri_input))
            self.worker.failed.connect(overlay.close)
            self.worker.failed.connect(
                lambda tb: on_registration_failed(tb, samri_input['num_threads'])
            )
            self.worker.cancelled.connect(overlay.close)
            self.worker.cancelled.connect(lambda: logging.info("Registration cancelled."))
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

            self.worker = BusyWorker(work_bias, self)
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
        # _copy_sub_to_data is plain filesystem I/O (shutil copy/copytree) --
        # no Qt/VTK object is touched, so unlike visualize_results below it's
        # safe to run off the GUI thread instead of freezing it silently for
        # however long the copy of a subject's data takes.
        copy_overlay = BusyOverlay(self, message="Copying registration results, please wait…")
        copy_overlay.setGeometry(self.rect())
        copy_overlay.raise_()
        copy_overlay.show()

        def on_copy_done():
            copy_overlay.close()
            self._verify_and_finish_registration(samri_input)

        def on_copy_failed(tb):
            copy_overlay.close()
            show_worker_error(self, "Copying registration results failed", tb)

        self._copy_worker = BusyWorker(self._copy_sub_to_data, self)
        self._copy_worker.done.connect(on_copy_done)
        self._copy_worker.failed.connect(on_copy_failed)
        self._copy_worker.start()

    def _verify_and_finish_registration(self, samri_input):
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
        self._notify_session_loaded('samri')

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
            self._start_trajectory_planning_work(data, transformPath)

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

    def _start_trajectory_planning_work(self, data, transformPath):
        """Shows the overlay, runs the (potentially first-time-only, real)
        resampling step off the GUI thread, then runs the rest of
        finish_trajectory_work (VTK/GUI rebuild) once that's done. Shared by
        initialize_trajectory_planning and the "trajectory" branch of
        load_previous_session -- both used to just do
        overlay.run(self.finish_trajectory_work, data, transformPath)."""
        overlay = BusyOverlay(self, message="Initializing trajectory planning, please wait…")
        overlay.setGeometry(self.rect())
        overlay.raise_()
        overlay.show()

        # keep re-asserting the overlay on top for the same reason
        # BusyOverlay.run() does (see its docstring/comment there): on every
        # run after the first, finish_trajectory_work's sync GUI rebuild
        # below goes through restart_gui(), which rebuilds mw.ui from
        # scratch (setupUi/show()/processEvents()) -- those freshly
        # (re)painted VTK widgets are new siblings of the overlay and slip
        # in front of a one-off raise_() the moment they repaint.
        keepalive = QTimer(self)
        keepalive.timeout.connect(lambda: (overlay.raise_(), overlay.repaint()))
        keepalive.start(100)

        result = {}

        def work():
            result['resampled_path'] = self._resample_for_trajectory_planning(data)

        def on_done():
            # keep the overlay up through the VTK/GUI rebuild too -- that part
            # is still fully synchronous and can take a while (FileLoader.
            # initialize_file, restart_gui, building TrajectoryPlanningMri),
            # so closing it before this would leave that whole stretch with
            # no overlay at all, same mistake as prewarm_tabs
            self.finish_trajectory_work(data, transformPath, result['resampled_path'])
            keepalive.stop()
            overlay.close()

        def on_failed(tb):
            keepalive.stop()
            overlay.close()
            show_worker_error(self, "Trajectory planning setup failed", tb)

        self._traj_resample_worker = BusyWorker(work, self)
        self._traj_resample_worker.done.connect(on_done)
        self._traj_resample_worker.failed.connect(on_failed)
        self._traj_resample_worker.start()

    def _resample_for_trajectory_planning(self, data):
        """Runs the resample step (trajectory_planning/trajectory_worker.py)
        in a separate OS process instead of in this one -- same reasoning as
        SAMRI's registration/biascorrection (see samri_main.py's
        _run_worker_subprocess): a heavy first-time 25/50um resample no
        longer shares the GUI process's memory footprint. Called from
        _start_trajectory_planning_work's BusyWorker thread (never the GUI
        thread), so blocking here on the subprocess is fine. Returns
        resampled_path; a no-op (the file already exists) after the first
        call for a given path/spacing."""
        payload = {'file_path': data[0], 'spacing': data[2]}
        result = _run_trajectory_worker_subprocess(payload)
        return result['resampled_path']

    def finish_trajectory_work(self, data, transformPath, resampled_path):
        self.data_pre_resampled = data[0]
        if not hasattr(self,'LoadMRI'):
            self.FileLoader = FileLoader(self)
            self.FileLoader.is_4d = False #3d file
            self.FileLoader.initialize_file(resampled_path,0,'coronal',0)
            zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
            Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)
            self.ui.comboBox_resamplefiles.addItem(os.path.basename(resampled_path)) #add to combobox for resampling
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.data_4d_3d.setCurrentIndex(1)
            self._notify_session_loaded('mri')
        else:
            self.restart_gui(resampled_path,data_view='coronal')

        data = list(data)
        data[0] = resampled_path

        self.register_module('LoadMRI.TrajPlanning', TrajectoryPlanningMri(self,self.ui,data,transformPath))

        self.ui.stackedWidget_3d.setVisible(True)
        self.ui.stackedWidget_3d.setCurrentIndex(0)
        box = self.ui.page_3D
        layout = box.layout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 1)
        self._notify_session_loaded('trajectory')

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

    def _free_previous_workflow_state(self, new_kind):
        """
        Leaving 'samri'/'ephys' for a different kind of session frees their
        heavy backing objects (self.Samri/self.Ephys) instead of leaving them
        alive in memory for the rest of the app session -- calling
        teardown() on each first (see _call_module_teardown) if it defines
        one, same as restart_gui's full replace does via
        _teardown_registered_modules. Moving to 'ephys',
        'samri' or 'surgery' (none of which need the main image) additionally
        evicts self.LoadMRI itself -- see _evict_load_mri() -- since that's
        usually the single biggest thing in memory (VTK renderers/actors for
        3 views plus a minimap, not just the volume data). Safe to do
        unconditionally here: BusyOverlay blocks all navigation while any of
        this background work (fetch/registration/biascorrection, ephys file
        load) is actually running, so this is never reached mid-job.

        'mri'/'trajectory'/'overlay' are excluded from the Samri/Ephys half:
        'overlay' doesn't leave anything of its own to free, and switching TO
        'mri'/'trajectory' obviously shouldn't free the very state you're
        switching to. SurgeryController is never freed at all -- deliberately
        session-long, see its own docstring.

        Whatever's freed here can still be reopened later via "Load Previous
        Session" -- _save_session_state() already recorded what's needed to
        rebuild it (animal_id/raw_base_samri for samri, the file path for
        ephys/mri) at the point each one finished loading; reopening just
        means re-fetching/re-reading/re-rendering rather than resuming the
        exact in-memory state.

        Also pops the freed entry out of self._registered_modules -- setting
        self.Samri/self.Ephys to None alone would leave the registry still
        holding a reference to the discarded instance (self._registered_
        modules['Samri'] pointing at a "freed" object that self.Samri no
        longer does), which both misrepresents "every live controller" and
        keeps that instance from actually being garbage-collected.
        """
        if new_kind != 'samri' and getattr(self, 'Samri', None) is not None:
            self._archive_samri_log()
            self._call_module_teardown('Samri', self.Samri)
            if getattr(self, 'log_adapter', None):
                self.log_adapter.uninstall()
                self.log_adapter = None
            self.Samri = None
            self._registered_modules.pop('Samri', None)

        if new_kind != 'ephys' and getattr(self, 'Ephys', None) is not None:
            self._call_module_teardown('Ephys', self.Ephys)
            self.Ephys = None
            self._registered_modules.pop('Ephys', None)

        if new_kind in ('ephys', 'samri', 'surgery'):
            self._evict_load_mri()

    def _archive_samri_log(self):
        """
        Writes plainTextEdit_SAMRI's accumulated log (fetch/registration/
        biascorrection progress and errors, captured live by LogAdapter) to
        <exe_dir>/logs/ before self.Samri is freed -- otherwise that record
        just disappears once the widget is next cleared/reused, with nothing
        left to show for it. Then clears the widget so the next SAMRI
        session starts with a blank log instead of appending to the old one.
        """
        text = self.ui.plainTextEdit_SAMRI.toPlainText()
        if not text.strip():
            return
        logs_dir = os.path.join(_exe_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        animal_id = getattr(self.Samri, 'animal_id', 'unknown')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(logs_dir, f"samri_{animal_id}_{timestamp}.log")
        with open(path, 'w') as f:
            f.write(text)
        self.ui.plainTextEdit_SAMRI.clear()

    def _close_tool_docks(self, full_restart):
        """
        Close the ephys dock and any of the lazily-created tool docks
        (paintbrush/measurement/segmentation -- see gui_utils/
        buttons_gui_structural.py's "check if it exists already" pattern)
        that happen to be open.

        Called from _open_new_session/_restore_session_entry (starting or
        restoring ANY session -- mri/ephys/samri/trajectory/surgery, not just
        an MRI reload: e.g. switching to SAMRI or trajectory planning while
        the paintbrush/measurement/segmentation dock is open must close it
        too, not just replacing the main image) and from restart_gui() itself
        (replacing an existing main image, where self.ui is actually rebuilt).

        `full_restart=True` (restart_gui's case) also detaches the dock right
        now instead of just scheduling deleteLater(): that alone leaves it a
        findable, visible child of MainWindow until the deferred deletion
        actually runs, so a later initialize_paintbrush/_measurement/
        _segmentation's own "does this dock already exist" findChild check
        could resurrect the stale one (wired to the just-replaced self.ui/
        LoadMRI) instead of building a fresh one. removeDockWidget() takes it
        out of the dock layout immediately; setParent(None) makes it
        unreachable via findChild() immediately too; deleteLater() still
        handles the actual C++ destruction, just no longer on anything that
        matters visually. `full_restart=False` (self.ui is not being rebuilt)
        just closes it -- nothing needs detaching since the dock and its
        content keep belonging to the same self.ui.
        """
        for dock_name in ("dock_paintbrush4d", "dock_segmentation", "dockWidget_ephys",
                          "dock_paintbrush", "dock_measurement"):
            dock = self.findChild(QDockWidget, dock_name)
            if dock:
                dock.close()
                if full_restart:
                    self.removeDockWidget(dock)
                    dock.setParent(None)
                    dock.deleteLater()

    def _teardown_load_mri(self, delete_windows):
        """Delegates to core/load_MRI_file.py's teardown_load_mri() -- see
        there for what this actually does and why it lives there now."""
        from core.load_MRI_file import teardown_load_mri
        teardown_load_mri(self, delete_windows)

    def _evict_load_mri(self):
        """Delegates to core/load_MRI_file.py's evict_load_mri()."""
        from core.load_MRI_file import evict_load_mri
        evict_load_mri(self)

    def restart_gui(self, file_name, full_restart=True, label_file=False, data_view='coronal'):
        """
        Restart GUI if new main image is loaded. Delegates to
        core/load_MRI_file.py's restart_gui() -- kept as a method here since
        it's the documented external entry point (samri/samri_main.py,
        file_handling/loader.py, file_handling/metadata.py,
        file_handling/resample_data.py all call
        self.restart_gui(...)/MW.restart_gui(...)).
        """
        from core.load_MRI_file import restart_gui as _restart_gui_impl
        _restart_gui_impl(self, file_name, full_restart=full_restart, label_file=label_file, data_view=data_view)

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
        self.close()

    def closeEvent(self, event):
        from gui_utils.busy_worker import any_running
        if any_running():
            reply = QMessageBox.question(
                self, "Background task running",
                "A background task (registration, resampling, spectrogram, ripple "
                "detection, ...) is still running. Quitting now will abandon it. "
                "Quit anyway?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return
        event.accept()
        # A BusyWorker's run_callable has no cancellation point, so there is no
        # graceful way to wait for it -- QApplication.quit() alone only stops the
        # Qt event loop, leaving that QThread's native thread still executing
        # Python code underneath, which keeps the process alive (sometimes for as
        # long as the callable takes to finish on its own). Hard-exit instead; any
        # child processes it left behind (nipype/ProcessPoolExecutor) get reaped by
        # the next launch's reap_stale_instances(), same as a crash would be.
        os._exit(0)


if __name__ == "__main__":
    # Required for a frozen (PyInstaller) build on Windows: multiprocessing's
    # default 'spawn' start method there re-invokes this same exe to bootstrap
    # each worker (nipype's MultiProc plugin, electrode_localization.py's
    # ProcessPoolExecutor); without this, each "worker" would instead relaunch
    # the whole GUI from scratch. Must be the first thing that runs. A no-op
    # on Linux/macOS (default start method there is 'fork', which doesn't
    # re-invoke the executable), so this is a self-contained safety net that
    # can't affect the dev workflow.
    multiprocessing.freeze_support()

    from gui_utils.instance_guard import reap_stale_instances, register_instance, start_heartbeat, unregister_instance
    # Kill any other launch's process tree that's dead or (like the render()
    # hangs found while debugging a SAMRI run) alive but frozen -- before
    # this instance claims any of its own resources.
    reap_stale_instances()
    _instance_pid_file = register_instance()

    # Register the .qrc file dynamically

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "resources.rcc")
    os.chdir(os.path.dirname(__file__))

    QResource.registerResource(file_path)
    #to mix vtk and QtQuick3D
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    _instance_heartbeat_timer = start_heartbeat(app, _instance_pid_file)
    app.aboutToQuit.connect(lambda: unregister_instance(_instance_pid_file))
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
    # GNOME Shell (esp. under Wayland) resolves the taskbar/dash/alt-tab icon
    # by matching this app id to an installed .desktop file's Icon=, not by
    # reading the pixmap passed to setWindowIcon below -- without it, running
    # from source (where the process is python3, not IMPLAnT.desktop's Exec
    # target) shows a generic icon even though the QIcon itself loads fine.
    app.setDesktopFileName("IMPLAnT")
    app.setWindowIcon(QIcon(os.path.join(_base_dir, "Icons/Github/IMPLAnT_quad.png")))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

