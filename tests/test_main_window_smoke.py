# This Python file uses the following encoding: utf-8
"""
Smoke/regression tests for MainWindow's extension API (register_tab,
register_menu_action, load_split_ui, register_session_loaded_callback,
register_module) and the dock-closing/memory-eviction work built on top of
it -- see CONTRIBUTING.md's "Adding your own tab/tool to MainWindow" section
for the API itself.

These codify checks that were, until this suite existed, only ever run by
hand (construct MainWindow offscreen, inspect it, throw the script away) --
several real bugs during this codebase's own tab-extraction work (a missing
import, a broken icon path, a tab-count regression) were only caught because
someone remembered to manually repeat that check after each change. This
suite exists so that stops being necessary.

Deliberately construction/control-flow level only -- see conftest.py's `mw`
fixture docstring for why (no display here, and real VTK needs one). Nothing
here loads an actual MRI/ephys/SAMRI file or renders anything; a handful of
tests fake just enough of LoadMRI's shape (via unittest.mock.MagicMock) to
exercise the surrounding Python logic without touching real VTK objects.
Anything that actually renders still needs a manual check against the real
app (CONTRIBUTING.md's "Testing" section).
"""
from unittest.mock import MagicMock

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget


ORIGINAL_TAB_TITLES = [
    "MRI Images",
    "Popups for Time-Series Data",
    "Popups for Time-Series Data II",
    "Ephys",
    "Popups for ephys",
    "SAMRI",
    "Intraoperative",
]


def test_constructs_without_exception(mw):
    assert mw is not None


def test_original_tab_layout_preserved(mw):
    """The 4 tabs split out of form.ui into standalone .ui files (tab_ephys,
    tab_samri, surgery, plus the earlier popup tabs) must land back in
    exactly their original order/titles once load_split_ui/register_tab
    re-attach them."""
    assert mw.ui.tabWidget.count() == len(ORIGINAL_TAB_TITLES)
    titles = [mw.ui.tabWidget.tabText(i) for i in range(mw.ui.tabWidget.count())]
    assert titles == ORIGINAL_TAB_TITLES


def test_split_tab_widgets_resolve_by_original_name(mw):
    """self.ui.<name> must keep working for every tab split out of form.ui --
    load_split_ui flattens the sub-form's widgets onto self.ui by name, so a
    tab renamed during extraction (e.g. Designer's default "Form") instead
    of kept as its original objectName would silently break this."""
    for name in ("tab_ephys", "tab_samri", "surgery"):
        assert hasattr(mw.ui, name), f"self.ui.{name} did not resolve"


def test_promoted_and_native_widgets_resolve(mw):
    """Widgets promoted in Designer (QVTKRenderWindowInteractor, QVideoWidget)
    or dynamically reparented into docks (native="true" containers) must
    survive a tab's move into its own .ui file the same way plain widgets
    do."""
    for name in ("vtkWidget_ephys", "widget_video", "widget", "widget_axialView"):
        assert hasattr(mw.ui, name), f"self.ui.{name} did not resolve"


def test_icons_load(mw):
    """Icons set via a relative file path (not a .qrc resource) get rewritten
    by Designer relative to wherever a widget's .ui file now lives when it's
    moved into a new one -- this is what actually broke during this
    project's own tab extractions, twice. Guards against it regressing on
    the next one."""
    for name in ("pushButton_questionmark_2", "pushButton_questionmark_samri",
                 "change_perspective_vis3D_2"):
        icon = getattr(mw.ui, name).icon()
        assert not icon.isNull(), f"{name}'s icon failed to load"


def test_extension_api_present(mw):
    for method in ("register_tab", "register_menu_action", "load_split_ui",
                   "register_session_loaded_callback", "register_module"):
        assert callable(getattr(mw, method, None)), f"MainWindow.{method} missing"


def test_register_module_plain_name(mw):
    class Foo:
        pass
    foo = Foo()
    mw.register_module('some_test_module', foo)
    assert mw.some_test_module is foo
    assert mw._registered_modules['some_test_module'] is foo


def test_register_module_dotted_name(mw):
    """register_module('LoadMRI.TrajPlanning', ...) must set the attribute on
    self.LoadMRI, not on self -- TrajPlanning only exists while an MRI is
    loaded, and several places look it up via self.LoadMRI.TrajPlanning."""
    mw.LoadMRI = MagicMock()
    traj = MagicMock()
    mw.register_module('LoadMRI.TrajPlanning', traj)
    assert mw.LoadMRI.TrajPlanning is traj
    assert mw._registered_modules['LoadMRI.TrajPlanning'] is traj


def test_close_tool_docks_detaches_on_full_restart(mw):
    """A dock closed during a full restart (an actual self.ui rebuild) must
    be immediately unreachable via findChild -- otherwise a subsequent
    initialize_paintbrush/_measurement/_segmentation's own "does this dock
    already exist" check can resurrect the stale one, wired to the
    just-replaced self.ui/LoadMRI, instead of building a fresh one."""
    dock = QDockWidget('Measurement', mw)
    dock.setObjectName('dock_measurement')
    mw.addDockWidget(Qt.RightDockWidgetArea, dock)
    mw._close_tool_docks(full_restart=True)
    assert mw.findChild(QDockWidget, 'dock_measurement') is None


def test_close_tool_docks_full_restart_false_just_hides(mw):
    """Switching workflows (not rebuilding self.ui) should close the dock
    without detaching it -- its content still belongs to the same self.ui."""
    dock = QDockWidget('Measurement', mw)
    dock.setObjectName('dock_measurement')
    mw.addDockWidget(Qt.RightDockWidgetArea, dock)
    mw._close_tool_docks(full_restart=False)
    assert mw.findChild(QDockWidget, 'dock_measurement') is dock


def test_free_previous_workflow_state_clears_ephys_and_samri(mw):
    mw.Samri = object()
    mw.register_module('Samri', mw.Samri)
    mw._free_previous_workflow_state('ephys')
    assert mw.Samri is None
    assert 'Samri' not in mw._registered_modules, "stale registry entry after freeing Samri"

    mw.Ephys = object()
    mw.register_module('Ephys', mw.Ephys)
    mw._free_previous_workflow_state('samri')
    assert mw.Ephys is None
    assert 'Ephys' not in mw._registered_modules, "stale registry entry after freeing Ephys"


def test_free_previous_workflow_state_calls_teardown(mw):
    calls = []

    class FakeModule:
        def teardown(self):
            calls.append('called')

    mw.Samri = FakeModule()
    mw._free_previous_workflow_state('ephys')
    assert calls == ['called']


def test_free_previous_workflow_state_leaves_surgery_alone(mw):
    """SurgeryController is deliberately session-long -- never freed by a
    workflow switch, unlike Ephys/Samri."""
    mw.surgery = object()
    mw._free_previous_workflow_state('ephys')
    assert mw.surgery is not None


def test_evict_load_mri_noop_without_loadmri(mw):
    assert not hasattr(mw, 'LoadMRI')
    mw._evict_load_mri()  # must not raise


def test_evict_load_mri_skips_when_trajectory_planning_active(mw):
    """Evicting LoadMRI while trajectory planning is active would throw away
    expensive-to-rebuild state just because the user peeked at another tab
    -- must be a no-op in that case."""
    fake = MagicMock()
    fake.TrajPlanning = MagicMock()
    mw.LoadMRI = fake
    mw._evict_load_mri()
    assert mw.LoadMRI is fake


def test_evict_load_mri_frees_and_snapshots_view_state(mw):
    class FakeVolume:
        is_4d = True
        file_path = '/tmp/mrid_gui_test_fake_file.nii.gz'

    fake = MagicMock()
    fake.vtk_widgets = {0: {'axial': MagicMock(), 'coronal': MagicMock(), 'sagittal': MagicMock()}}
    fake.minimap.minimap_renderers = {0: {'axial': MagicMock()}}
    fake.renderers = {0: {'axial': MagicMock()}}
    cursor_ui = {'scroll_0': MagicMock(), 'scroll_1': MagicMock(), 'scroll_2': MagicMock()}
    for i in range(3):
        for axis in ('x', 'y', 'z'):
            cursor_ui[f'spin_{axis}{i}'] = MagicMock()
    fake.cursor_ui = cursor_ui
    fake.volumes = [FakeVolume()]
    fake.TrajPlanning = None
    mw.LoadMRI = fake

    mw._evict_load_mri()
    assert mw.LoadMRI is None
    assert FakeVolume.file_path in mw._session_view_cache


def test_teardown_load_mri_pops_trajplanning_registry_entry(mw):
    class FakeVolume:
        is_4d = True
        file_path = '/tmp/mrid_gui_test_fake_file2.nii.gz'

    fake = MagicMock()
    fake.vtk_widgets = {0: {'axial': MagicMock()}}
    fake.minimap.minimap_renderers = {0: {'axial': MagicMock()}}
    fake.renderers = {0: {'axial': MagicMock()}}
    cursor_ui = {'scroll_0': MagicMock(), 'scroll_1': MagicMock(), 'scroll_2': MagicMock()}
    for i in range(3):
        for axis in ('x', 'y', 'z'):
            cursor_ui[f'spin_{axis}{i}'] = MagicMock()
    fake.cursor_ui = cursor_ui
    fake.volumes = [FakeVolume()]
    traj = MagicMock()
    traj.tp3d_window = None
    fake.TrajPlanning = traj
    mw.LoadMRI = fake
    mw._registered_modules['LoadMRI.TrajPlanning'] = traj

    mw._teardown_load_mri(delete_windows=True)
    assert mw.LoadMRI is None
    assert 'LoadMRI.TrajPlanning' not in mw._registered_modules, \
        "stale registry entry after LoadMRI teardown"


def test_measurement_teardown_clears_state(mw):
    from core.measurement import Measurement
    m = Measurement(MagicMock(), None)
    m.measurement_lines = ['fake']
    mw.register_module('Measurement', m)
    mw._teardown_registered_modules()
    assert m.measurement_lines == []


def test_finish_mri_load_updates_ui_and_notifies(mw):
    mw.LoadMRI = MagicMock()
    notified = []
    mw._notify_session_loaded = lambda kind: notified.append(kind)

    mw._finish_mri_load('/tmp/some_4d_file.nii.gz', 'axial', is_4d=True)

    assert notified == ['mri']
    assert mw.ui.comboBox_resamplefiles.itemText(0) == 'some_4d_file.nii.gz'
    assert mw.ui.groupBox_data0.title() == 'View: AXIAL'
    assert mw.ui.data_4d_3d.currentIndex() == 0
    assert mw.ui.tabWidget.currentIndex() == 0
