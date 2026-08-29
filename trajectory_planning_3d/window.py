# This Python file uses the following encoding: utf-8
import os

import numpy as np
import SimpleITK as sitk
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QDockWidget, QHeaderView, QListWidgetItem, QTableWidgetItem, QVBoxLayout, QWidget
)

from gui_utils.busy_overlay import BusyOverlay
from trajectory_planning.shank import NEON_COLORS, _make_color_icon
from trajectory_planning_3d.add_region_dialog import AddRegionDialog
from ui_form_tp_3d import Ui_Form

pv.global_theme.background = 'black'

SHANK_LINE_WIDTH = 4
SHANK_LINE_WIDTH_SELECTED = 9
SHANK_TIP_EXTENSION_MM = 4.0  # how far the drawn line extends past the insertion point, outside the brain -- matches draw_electrode_lines' convention in trajectory_planning/visualisation3D.py
SHANK_CONTACT_DOT_SIZE = 6


class TrajectoryPlanning3DWindow(QDockWidget):
    """3D view of the atlas + planned shanks, opened alongside the main
    window by pushButton_tp_3d. A QDockWidget rather than a bare top-level
    widget: QMainWindow has native layout/geometry handling for dock
    widgets (docked or floating) that a hand-parented Qt.Window/Qt.Tool
    widget doesn't get -- the latter broke MW's own resizing. Starts
    floating so it behaves like its own window, usable at the same time as
    the main one, but can be dragged into the main window if wanted. Kept
    as a single persistent instance (see TrajectoryPlanning.open_3d_window)
    so region/shank visibility state and camera position survive being
    hidden and reopened."""

    def __init__(self, MW):
        super().__init__("Trajectory Planning — 3D View", MW)
        self.MW = MW
        self.tp = MW.LoadMRI.TrajPlanning

        content = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(content)
        self.setWidget(content)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        self.opacityRegions = 0.9
        self.opacityBackground = 0.5
        self.parallel_projection = True
        self.selected_shank_idx = None

        self.region_actors = {}          # atlas value -> vtk actor
        self.shank_actors = {}           # shank_idx -> vtk actor (shanks are always visible)
        self._region_meshes = {}         # atlas value -> cached pv mesh (or None)
        self._shank_region_cache = {}    # shank_idx -> [atlas vals it traverses], refreshed in refresh_shanks
        self._syncing = False            # guards against the table<->list resync re-triggering itself
        self._depth_peeling_enabled = False  # only turned on once 2+ translucent layers overlap
        self.background_actor = None
        self._armed_axis = None          # None, 'x', 'y', 'z', or 'trajectory' -- which axis the step buttons move
        self._camera_reset_pending = True  # one extra reset_camera() once actually shown -- see showEvent
        self._pending_nudge_steps = 0    # accumulated steps from rapid repeated clicks -- see _queue_nudge
        self._nudge_timer = QTimer(self)
        self._nudge_timer.setSingleShot(True)
        self._nudge_timer.timeout.connect(self._apply_pending_nudge)

        layout = QVBoxLayout(self.ui.vtkWidget_vis3D)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(self.ui.vtkWidget_vis3D)
        layout.addWidget(self.plotter)
        # Same per-frame render tuning already used for the orthogonal-view
        # plotters in trajectory_planning/visualisation3D.py -- MSAA and
        # depth peeling both cost real time on EVERY frame (not just once),
        # which is what actually makes plain camera rotation feel laggy;
        # SetDesiredUpdateRate lets VTK drop detail while the camera is
        # actively being dragged and restore it once it stops.
        self.plotter.render_window.SetMultiSamples(0)
        self.plotter.renderer.SetUseDepthPeeling(False)
        self.plotter.render_window.GetInteractor().SetDesiredUpdateRate(30)
        # depth peeling (see _update_depth_peeling) is deliberately NOT
        # enabled here -- it costs real per-frame render time (several
        # extra passes), so with just the background shell and the shanks
        # visible (nothing else translucent to sort against) it would only
        # slow down plain camera rotation for no benefit.

        self.ui.resetCamera_vis3D.clicked.connect(self.plotter.reset_camera)
        self.ui.change_perspective_vis3D.clicked.connect(self._toggle_perspective)
        self.ui.pushButton_add_region.clicked.connect(self._open_add_region_dialog)
        self.ui.pushButton_selectAll.clicked.connect(lambda: self._set_all_shank_rows(True))
        self.ui.pushButton_deselectAll.clicked.connect(lambda: self._set_all_shank_rows(False))
        self.ui.tableWidgetshank_legend.cellChanged.connect(self._on_shank_row_changed)
        self.ui.tableWidgetshank_legend.cellClicked.connect(self._on_shank_table_clicked)
        # the "Show" column's checkbox is the main way to toggle a shank's
        # regions -- the style's default indicator is tiny, so size it up
        # to something easier to click/see (a QTableWidgetItem's checkbox
        # is drawn by the style, not a real QCheckBox, so this has to go
        # through the item-view indicator selector rather than QCheckBox).
        self.ui.tableWidgetshank_legend.setStyleSheet(
            "QTableWidget::indicator { width: 22px; height: 22px; }")
        self.ui.listWidget_visible_regions.itemChanged.connect(self._on_region_item_changed)
        self.ui.comboBox_Shanks_tp3d.setEnabled(True)
        self.ui.comboBox_Shanks_tp3d.currentIndexChanged.connect(self._on_shank_combo_changed)

        self._axis_buttons = {
            'x': self.ui.pushButton_slicex_vis3D,          # sagittal
            'y': self.ui.pushButton_slicey_vis3D,          # coronal
            'z': self.ui.pushButton_slicez_vis3D,          # axial
            'trajectory': self.ui.pushButton_alongTraj,    # the shank's own insert->deep axis
            'roll': self.ui.pushButton_roll,               # rotate around the SI axis (see _nudge_shank)
            'pitch': self.ui.pushButton_pitch,             # rotate around the RL axis (see _nudge_shank)
        }
        for axis, btn in self._axis_buttons.items():
            btn.clicked.connect(lambda checked=False, ax=axis: self._toggle_axis_arm(ax))
        # x/y/z/trajectory already have a tooltip baked into form_tp_3d.ui --
        # roll/pitch don't, so add the matching wording here instead of
        # leaving those two the only unexplained buttons in the row.
        self.ui.pushButton_roll.setToolTip(
            "Select roll -- the step buttons below then rotate the selected shank's roll angle by that many degrees")
        self.ui.pushButton_pitch.setToolTip(
            "Select pitch -- the step buttons below then rotate the selected shank's pitch angle by that many degrees")
        self.ui.pushButton_stepBack10_vis3D.clicked.connect(lambda: self._queue_nudge(-10))
        self.ui.pushButton_stepBack1_vis3D.clicked.connect(lambda: self._queue_nudge(-1))
        self.ui.pushButton_stepFwd1_vis3D.clicked.connect(lambda: self._queue_nudge(1))
        self.ui.pushButton_stepFwd10_vis3D.clicked.connect(lambda: self._queue_nudge(10))
        self._update_axis_arm_ui()

        self.forbidden_area_actor = None
        self.ui.checkBox_forbiddenareas.toggled.connect(self._on_forbidden_areas_toggled)
        self.ui.checkBox_forbiddenareas.setToolTip("Hide the forbidden-area overlay in this 3D view")
        self._set_forbidden_area_visible(not self.ui.checkBox_forbiddenareas.isChecked())
        self._update_forbidden_area_checkbox_enabled()

        self.ui.checkBox_hideplanes.toggled.connect(self._on_hide_planes_toggled)
        self.ui.checkBox_hideplanes.setToolTip(
            "Hide the bregma-lambda-CC and bregma-lambda reference planes used to measure roll/pitch")

        # checkBox_constraint_90deg/_coronal live on the MAIN window (page_5
        # -- see ElecGeometryMri.enforce_constraint_90deg/_coronal), not
        # this docked window's own ui -- self.tp.ui is that same main-window
        # ui object (see TrajectoryPlanning.__init__).
        self.tp.ui.checkBox_constraint_90deg.toggled.connect(self._update_roll_pitch_enabled)
        self.tp.ui.checkBox_constraint_90deg_coronal.toggled.connect(self._update_roll_pitch_enabled)
        self._update_roll_pitch_enabled()

        self._rebuild_background_mesh()
        self._draw_landmarks_and_planes()
        self.plotter.add_axes()
        self.plotter.reset_camera()

        self.refresh_shanks()

    # ---- shank legend / combo -------------------------------------------------

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_shanks()
        self._maybe_reset_camera()
        # a single deferred attempt wasn't reliably enough -- being newly
        # added to a QMainWindow's dock layout can take more than one
        # event-loop pass to settle on a final size (addDockWidget +
        # resizeDocks doesn't necessarily finish before this fires), so
        # retry a few times; _maybe_reset_camera stops doing anything once
        # the first one that finds a real size succeeds.
        for delay_ms in (50, 200, 500):
            QTimer.singleShot(delay_ms, self._maybe_reset_camera)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._maybe_reset_camera()

    def _maybe_reset_camera(self):
        # reset_camera() run in __init__, before the widget was ever
        # actually shown/laid out, can end up with a degenerate camera (the
        # view showing black/nothing) -- redo it once there's a real size
        # to compute bounds against, whichever fires first: a resize to a
        # meaningful size, or one of the deferred retries from showEvent.
        if not self._camera_reset_pending:
            return
        if self.width() <= 10 or self.height() <= 10:
            return
        self._camera_reset_pending = False
        self.plotter.reset_camera()

    def closeEvent(self, event):
        # temporary instrumentation: closing this dock reportedly freezes
        # the GUI -- run from a terminal and see which of these actually
        super().closeEvent(event)

    def _current_shank_indices(self):
        """Which shanks actually exist right now, straight from
        comboBox_Shanks (the 2D view's own, always-correctly-maintained
        list) rather than self.tp.shank_colors -- remove_shank() doesn't
        clean that dict up, so its keys can still list shanks that were
        deleted."""
        combo = self.tp.ui.comboBox_Shanks
        return [combo.itemData(i) for i in range(combo.count())]

    def refresh_shanks(self):
        self._update_forbidden_area_checkbox_enabled()
        shank_indices = self._current_shank_indices()
        if self.selected_shank_idx not in shank_indices:
            self.selected_shank_idx = shank_indices[0] if shank_indices else None

        # Which shanks were "fully shown" (checkbox ticked) before
        # recomputing -- so a shank whose geometry just changed (moved
        # insert/deep point, different channel count, ...) keeps its
        # regions in sync with what it traverses NOW, not what it used to.
        table = self.ui.tableWidgetshank_legend
        previously_checked = {
            table.item(row, 2).data(Qt.UserRole) for row in range(table.rowCount())
            if table.item(row, 0).checkState() == Qt.Checked
        }
        previously_checked &= set(shank_indices)
        old_cache = self._shank_region_cache

        # compute_shank_regions samples the whole insert->deep line at ~voxel
        # resolution -- expensive, so do it once per refresh and let every
        # click-driven handler read from this cache instead of recomputing.
        self._shank_region_cache = {
            idx: [r['val'] for r in self.tp.compute_shank_regions(idx, self.tp.channel_points.get(idx, []))
                  if r['val'] != 0]  # atlas value 0 is "Clear Label" (background/unlabeled) -- never a real region
            for idx in shank_indices
        }

        # add newly-traversed regions, drop ones no longer traversed (unless
        # another still-checked shank still needs them)
        for idx in previously_checked:
            old_vals = set(old_cache.get(idx, []))
            new_vals = set(self._shank_region_cache.get(idx, []))
            for val in new_vals - old_vals:
                self._ensure_region_item(val, True)
            dropped = old_vals - new_vals
            if dropped:
                other_needed = set()
                for other_idx in previously_checked:
                    if other_idx != idx:
                        other_needed.update(self._shank_region_cache.get(other_idx, []))
                for val in dropped:
                    if val not in other_needed:
                        self._remove_region_item(val)

        self._populate_shank_table()
        self._populate_shank_combo()
        self._draw_all_shanks()
        self._draw_landmarks_and_planes()
        self._update_axis_indicator()

    def _populate_shank_table(self):
        table = self.ui.tableWidgetshank_legend
        table.blockSignals(True)
        table.clear()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Show", "Color", "Shank"])
        # checkbox/colour columns are small, fixed-content widgets -- let the
        # shank-name column take whatever width they don't use instead of
        # leaving empty space if the table is wider than its content (same
        # convention as gui_utils/intensity_table.py's layer-name column).
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        shank_indices = self._current_shank_indices()
        table.setRowCount(len(shank_indices))
        for row, idx in enumerate(shank_indices):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            vals = self._shank_region_vals(idx)
            fully_shown = bool(vals) and all(self._is_region_checked(v) for v in vals)
            checkbox_item.setCheckState(Qt.Checked if fully_shown else Qt.Unchecked)
            table.setItem(row, 0, checkbox_item)

            color_item = QTableWidgetItem()
            color_item.setFlags(Qt.ItemIsEnabled)
            r, g, b = NEON_COLORS[self.tp.shank_colors[idx]][1]
            color_item.setBackground(QColor(r, g, b))
            table.setItem(row, 1, color_item)

            name_item = QTableWidgetItem(f"Shank {idx + 1}")
            name_item.setFlags(Qt.ItemIsEnabled)
            name_item.setData(Qt.UserRole, idx)
            table.setItem(row, 2, name_item)
            if idx == self.selected_shank_idx:
                table.selectRow(row)
        # only the checkbox/color columns get resized to their content --
        # column 2 is QHeaderView.Stretch (above) and manages its own width
        # to fill whatever's left on its own; resizeColumnsToContents()
        # would force it back down to ITS content width on every refresh
        # too, undoing the stretch, and (combined with this table's
        # AdjustToContents sizeAdjustPolicy, which shrinks the whole widget
        # to match its columns' current widths) leaving the table visibly
        # narrower than the space it's actually been given.
        table.resizeColumnToContents(0)
        table.resizeColumnToContents(1)
        table.resizeRowsToContents()
        table.blockSignals(False)

    def _populate_shank_combo(self):
        combo = self.ui.comboBox_Shanks_tp3d
        combo.blockSignals(True)
        combo.clear()
        for idx in self._current_shank_indices():
            combo.addItem(f"Shank {idx + 1}")
            combo.setItemData(combo.count() - 1, idx)
            combo.setItemIcon(combo.count() - 1, _make_color_icon(self.tp.shank_colors[idx]))
            if idx == self.selected_shank_idx:
                combo.setCurrentIndex(combo.count() - 1)
        combo.blockSignals(False)

    def _select_shank(self, shank_idx, sync_combo, sync_table):
        """Single source of truth for "which shank is selected" -- drawn
        bolder in 3D, and kept in sync between the combobox and the legend
        table regardless of which one triggered the change. Only touches the
        previously- and newly-selected shanks' line width in place -- no
        need to rebuild every shank's mesh just to change which one is bold."""
        if shank_idx == self.selected_shank_idx:
            return
        self._flush_pending_nudge()
        previous_idx = self.selected_shank_idx
        self.selected_shank_idx = shank_idx
        for idx in (previous_idx, shank_idx):
            actor = self.shank_actors.get(idx)
            if actor is not None:
                width = SHANK_LINE_WIDTH_SELECTED if idx == self.selected_shank_idx else SHANK_LINE_WIDTH
                actor.GetProperty().SetLineWidth(width)
        self._update_angle_legend()
        self._update_axis_indicator()
        self.plotter.render()

        if sync_combo:
            combo = self.ui.comboBox_Shanks_tp3d
            combo_idx = combo.findData(shank_idx)
            if combo_idx != -1 and combo.currentIndex() != combo_idx:
                combo.blockSignals(True)
                combo.setCurrentIndex(combo_idx)
                combo.blockSignals(False)

        if sync_table:
            table = self.ui.tableWidgetshank_legend
            for row in range(table.rowCount()):
                if table.item(row, 2).data(Qt.UserRole) == shank_idx:
                    if table.currentRow() != row:
                        table.blockSignals(True)
                        table.selectRow(row)
                        table.blockSignals(False)
                    break

    def _on_shank_combo_changed(self, index):
        combo = self.ui.comboBox_Shanks_tp3d
        if index < 0:
            return
        shank_idx = combo.itemData(index)
        self._select_shank(shank_idx, sync_combo=False, sync_table=True)
        # select_shank is the 2D view's own single source of truth for
        # "which shank is selected" -- it syncs comboBox_Shanks,
        # comboBox_geometry_shanks, the color combo, spinboxes and the 2D
        # line colors itself, so picking a shank here updates every other
        # shank selector too, not just this window's own table/combo.
        if self.tp.shank_number != shank_idx:
            self.tp.select_shank(shank_idx)

        insert = self.tp.coords_insert_point.get(shank_idx)
        deep = self.tp.coords_deepest_point.get(shank_idx)
        if insert is None or deep is None:
            return
        spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        mid = (np.array(insert, dtype=float) + np.array(deep, dtype=float)) / 2 * spacing
        self.plotter.set_focus(mid)
        self.plotter.render()

    def _on_shank_table_clicked(self, row, column):
        """Clicking anywhere on a shank's row selects it (bolder in 3D,
        synced to the combobox); clicking a column other than the checkbox
        itself also flips that row's checkbox -- the checkbox cell already
        toggles natively on click, same convention as on_table_click in
        ephys/visualisation3D.py."""
        table = self.ui.tableWidgetshank_legend
        shank_idx = table.item(row, 2).data(Qt.UserRole)
        self._select_shank(shank_idx, sync_combo=True, sync_table=False)
        if column != 0:
            item = table.item(row, 0)
            item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)

    def _set_all_shank_rows(self, checked):
        table = self.ui.tableWidgetshank_legend
        state = Qt.Checked if checked else Qt.Unchecked
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item.checkState() != state:
                item.setCheckState(state)  # triggers _on_shank_row_changed

    def _shank_region_vals(self, shank_idx):
        return self._shank_region_cache.get(shank_idx, [])

    def _on_shank_row_changed(self, row, column):
        if column != 0 or self._syncing:
            return
        table = self.ui.tableWidgetshank_legend
        shank_idx = table.item(row, 2).data(Qt.UserRole)
        checked = table.item(row, 0).checkState() == Qt.Checked
        my_vals = self._shank_region_vals(shank_idx)

        if checked:
            for val in my_vals:
                self._ensure_region_item(val, True)
        else:
            # a region stays visible if some OTHER checked shank still needs it
            other_needed = set()
            for r in range(table.rowCount()):
                if r == row or table.item(r, 0).checkState() != Qt.Checked:
                    continue
                other_needed.update(self._shank_region_vals(table.item(r, 2).data(Qt.UserRole)))
            for val in my_vals:
                if val not in other_needed:
                    self._remove_region_item(val)

        self._resync_shank_checkboxes()

    def _resync_shank_checkboxes(self):
        """Keep every shank row's checkbox reflecting whether ALL of that
        shank's traversed regions are currently checked in
        listWidget_visible_regions -- so manually checking/unchecking a
        region in the list (the "other way round") is reflected back onto
        the shank table too, not just table -> list."""
        self._syncing = True
        try:
            table = self.ui.tableWidgetshank_legend
            for row in range(table.rowCount()):
                shank_idx = table.item(row, 2).data(Qt.UserRole)
                vals = self._shank_region_vals(shank_idx)
                fully_shown = bool(vals) and all(self._is_region_checked(v) for v in vals)
                item = table.item(row, 0)
                state = Qt.Checked if fully_shown else Qt.Unchecked
                if item.checkState() != state:
                    item.setCheckState(state)
        finally:
            self._syncing = False

    # ---- shank 3D actors -------------------------------------------------

    def _draw_all_shanks(self):
        """Shanks are always visible -- only which of their traversed regions
        get highlighted is togglable, via the legend table's checkboxes.
        Rebuilds every shank's line (cheap) so edits made elsewhere (e.g.
        dragging the insertion/deepest point) are picked up on refresh, and
        so the currently-selected shank redraws bolder. Also removes the
        actor for any shank that no longer exists (e.g. just deleted via
        remove_shank), which a plain rebuild-in-place wouldn't catch."""
        current = set(self._current_shank_indices())
        for idx in set(self.shank_actors) - current:
            self.plotter.remove_actor(f'shank_{idx}')
            self.plotter.remove_actor(f'shank_dots_{idx}')
            del self.shank_actors[idx]
        for idx in current:
            actor = self._build_shank_actor(idx)
            if actor is not None:
                self.shank_actors[idx] = actor
        self.plotter.render()

    def _current_space_insert_deep_mm(self, shank_idx):
        """This shank's insert/deep points, in MRI physical mm -- shared by
        _build_shank_actor and the landmark/plane drawing so both agree on
        exactly the same points. mri_insert/mri_deep are already MRI-grid
        voxel indices (electrode_mri.py's change_insert_point/
        change_deepest_point set them straight from the MRI-space spinbox
        values), so no atlas conversion is needed here."""
        insert = self.tp.mri_insert.get(shank_idx)
        deep = self.tp.mri_deep.get(shank_idx)
        if getattr(self.tp, 'movingImg_resampled', None) is None:
            return None, None
        spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        if insert is None or deep is None:
            return None, None
        return np.array(insert, dtype=float) * spacing, np.array(deep, dtype=float) * spacing

    def _current_space_channel_points_mm(self, shank_idx):
        """This shank's contact points, in MRI physical mm. channel_points
        is built (electrode_mri.py's create_channel_list) directly from
        coords_deepest_point/direction_atlas using movingImg_resampled's
        own spacing -- i.e. already MRI-grid voxel indices, same as
        mri_insert/mri_deep -- so this just scales by MRI spacing, no
        atlas_points_to_mri_indices warp needed."""
        pts = self.tp.channel_points.get(shank_idx)
        if pts is None or len(pts) == 0:
            return None
        if getattr(self.tp, 'movingImg_resampled', None) is None:
            return None
        spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        return np.asarray(pts, dtype=float) * spacing

    def _build_shank_actor(self, shank_idx):
        insert_mm, deep_mm = self._current_space_insert_deep_mm(shank_idx)
        if insert_mm is None or deep_mm is None:
            return None
        color = self.tp.get_shank_vtk_color(shank_idx)
        width = SHANK_LINE_WIDTH_SELECTED if shank_idx == self.selected_shank_idx else SHANK_LINE_WIDTH

        # extend the drawn line past the insertion point, outside the brain
        # -- same convention (and distance) as draw_electrode_lines in
        # trajectory_planning/visualisation3D.py, so a shank looks the same
        # way in both 3D views instead of stopping exactly at the skull.
        direction = insert_mm - deep_mm
        length = np.linalg.norm(direction)
        tip_mm = insert_mm + direction / length * SHANK_TIP_EXTENSION_MM if length > 1e-9 else insert_mm

        actor = self.plotter.add_mesh(
            pv.Line(deep_mm, tip_mm), color=color, line_width=width, name=f'shank_{shank_idx}',
            reset_camera=False, render=False)

        dots_name = f'shank_dots_{shank_idx}'
        channel_pts_mm = self._current_space_channel_points_mm(shank_idx)
        if channel_pts_mm is None:
            self.plotter.remove_actor(dots_name)
        else:
            self.plotter.add_mesh(
                pv.PolyData(channel_pts_mm.astype(np.float32)), color=color,
                point_size=SHANK_CONTACT_DOT_SIZE, name=dots_name,
                render_points_as_spheres=True, render=False, show_scalar_bar=False,
                reset_camera=False, pickable=False)
        return actor

    # ---- region list / meshes ---------------------------------------------

    def _open_add_region_dialog(self):
        name_to_idx = {
            label[4]: idx for idx, label in self.tp.tp_labels.items() if idx != 0
        }
        dlg = AddRegionDialog(list(name_to_idx.keys()), parent=self)
        if dlg.exec():
            name = dlg.selected_region_name()
            val = name_to_idx.get(name)
            if val is not None:
                self._ensure_region_item(val, True)

    def _find_region_item(self, val):
        lw = self.ui.listWidget_visible_regions
        for i in range(lw.count()):
            item = lw.item(i)
            if item.data(Qt.UserRole) == val:
                return item
        return None

    def _is_region_checked(self, val):
        item = self._find_region_item(val)
        return item is not None and item.checkState() == Qt.Checked

    def _remove_region_item(self, val):
        """Drop a region from listWidget_visible_regions entirely, rather
        than just unchecking it -- used when a shank stops needing a region
        (unchecked/removed/its geometry changed), since a stale unchecked
        entry left behind serves no purpose there. Manually unchecking a
        region directly in the list is a separate, deliberate action and
        still just hides it (see _on_region_item_changed)."""
        item = self._find_region_item(val)
        if item is None:
            return
        lw = self.ui.listWidget_visible_regions
        lw.takeItem(lw.row(item))
        self._set_region_visible(val, False)

    def _ensure_region_item(self, val, checked):
        if val == 0:
            return  # "Clear Label" -- background/unlabeled, never a real region to render
        lw = self.ui.listWidget_visible_regions
        item = self._find_region_item(val)
        if item is None:
            if not checked:
                return  # nothing to hide, nothing to add just to mark it unchecked
            label = self.tp.tp_labels.get(val)
            name = label[4] if label is not None else f"Region {val}"
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setData(Qt.UserRole, val)
            lw.blockSignals(True)
            item.setCheckState(Qt.Checked)
            lw.addItem(item)
            lw.blockSignals(False)
            self._set_region_visible(val, True)
        else:
            state = Qt.Checked if checked else Qt.Unchecked
            if item.checkState() != state:
                item.setCheckState(state)  # triggers _on_region_item_changed

    def _on_region_item_changed(self, item):
        if self._syncing:
            return
        self._set_region_visible(item.data(Qt.UserRole), item.checkState() == Qt.Checked)
        self._resync_shank_checkboxes()

    def _set_region_visible(self, val, visible):
        if visible:
            actor = self.region_actors.get(val)
            if actor is None:
                mesh = self._get_region_mesh(val)
                if mesh is None or mesh.n_points == 0:
                    return
                color = self.tp.tp_labels[val][:3]
                self.region_actors[val] = self.plotter.add_mesh(
                    mesh, color=color, opacity=self.opacityRegions, name=f'region_{val}')
            else:
                actor.SetVisibility(True)
        else:
            actor = self.region_actors.get(val)
            if actor is not None:
                actor.SetVisibility(False)
        self._update_depth_peeling()
        self.plotter.render()

    def _update_depth_peeling(self):
        """Depth peeling costs real per-frame render time (several extra
        passes) -- only worth paying once 2+ translucent surfaces actually
        overlap (the background shell plus 1+ visible regions). With just
        the background and the shanks visible, turn it back off so plain
        camera rotation stays cheap."""
        needs_peeling = any(a.GetVisibility() for a in self.region_actors.values())
        if self.forbidden_area_actor is not None and self.forbidden_area_actor.GetVisibility():
            needs_peeling = True
        plane_actor = self.plotter.actors.get('plane_bregma_lambda_roll')
        if plane_actor is not None and plane_actor.GetVisibility():
            needs_peeling = True  # the two reference planes are translucent whenever shown
        if needs_peeling and not self._depth_peeling_enabled:
            self.plotter.enable_depth_peeling()
            self._depth_peeling_enabled = True
        elif not needs_peeling and self._depth_peeling_enabled:
            self.plotter.disable_depth_peeling()
            self._depth_peeling_enabled = False

    def _update_forbidden_area_checkbox_enabled(self):
        """Nothing to hide/show if no forbidden-area mask was ever warped
        onto the atlas (region_to_avoid only gets set in
        TrajectoryPlanning.do_get_shank_line when a region_to_avoid_img
        exists) -- grey the checkbox out instead of leaving a control that
        looks actionable but silently does nothing."""
        has_data = getattr(self.tp, 'region_to_avoid', None) is not None
        self.ui.checkBox_forbiddenareas.setEnabled(has_data)

    def _on_forbidden_areas_toggled(self, checked):
        # checkBox_forbiddenareas reads "Hide Forbidden Areas" -- checked
        # means hide, so visible is the opposite.
        self._set_forbidden_area_visible(not checked)

    def _set_forbidden_area_visible(self, visible):
        region_to_avoid = getattr(self.tp, 'region_to_avoid', None)
        if visible:
            if region_to_avoid is None:
                return
            if self.forbidden_area_actor is None:
                # region_to_avoid lives on the MRI's own grid --
                # registration_mri.py's warp_red_areas paints it directly
                # onto the displayed MRI and never warps it into atlas
                # space -- same grid _build_mask_mesh now always assumes.
                mesh = self._build_mask_mesh(region_to_avoid > 0)
                if mesh is None or mesh.n_points == 0:
                    return
                self.forbidden_area_actor = self.plotter.add_mesh(
                    mesh, color='red', opacity=self.opacityRegions, name='forbidden_area')
            else:
                self.forbidden_area_actor.SetVisibility(True)
        elif self.forbidden_area_actor is not None:
            self.forbidden_area_actor.SetVisibility(False)
        self._update_depth_peeling()
        self.plotter.render()

    def _get_region_mesh(self, val):
        if val in self._region_meshes:
            return self._region_meshes[val]
        mesh = self._build_mask_mesh(self.tp.mri_label_vol == val)
        self._region_meshes[val] = mesh
        return mesh

    def _build_mask_mesh(self, mask_zyx):
        """Crop to the mask's own bounding box (+1 voxel padding) before
        handing it to VTK -- thresholding the WHOLE volume at full
        resolution just to extract one small mask is what makes the first
        toggle of any given region/mask slow, since it's typically a tiny
        fraction of the full volume. Shared by per-region meshes
        (mri_label_vol, the atlas-region-label overlay already resampled
        onto the MRI's own grid by TrajectoryPlanningMri.
        build_mri_label_overlay -- see registration_mri.py) and the
        forbidden-area mesh (region_to_avoid, painted directly onto the
        displayed MRI -- registration_mri.py's warp_red_areas) -- both
        already live on the MRI's own grid, so this just needs the MRI's
        own spacing, no cross-grid reprojection at all."""
        if not mask_zyx.any():
            return None
        zs, ys, xs = np.nonzero(mask_zyx)
        z0, z1 = max(int(zs.min()) - 1, 0), min(int(zs.max()) + 2, mask_zyx.shape[0])
        y0, y1 = max(int(ys.min()) - 1, 0), min(int(ys.max()) + 2, mask_zyx.shape[1])
        x0, x1 = max(int(xs.min()) - 1, 0), min(int(xs.max()) + 2, mask_zyx.shape[2])
        cropped_zyx = mask_zyx[z0:z1, y0:y1, x0:x1]

        mask_xyz = np.transpose(cropped_zyx, (2, 1, 0)).astype(np.uint8)
        spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        vol = pv.ImageData()
        vol.dimensions = np.array(mask_xyz.shape) + 1
        vol.spacing = spacing
        vol.origin = np.array([x0, y0, z0]) * spacing  # position the crop back where it belongs
        vol.cell_data['mask'] = mask_xyz.flatten(order='F')
        return vol.threshold(0.5, scalars='mask')

    # ---- background context mesh -------------------------------------------

    def _rebuild_background_mesh(self):
        """(Re)builds the background shell behind a BusyOverlay -- it's a
        real, ~seconds-long blocking operation (full-volume threshold +
        surface extraction + decimation + smoothing), so show a "loading"
        overlay while it runs instead of the window just appearing to
        hang."""
        BusyOverlay(self.widget(), "Loading atlas…").run(self._build_background_mesh)

    def _build_background_mesh(self, downsample=3):
        """Translucent context shell, built the same way as add_background in
        ephys/visualisation3D.py: threshold the volume, extract+clean+fill
        the outer surface, Taubin-smooth it, and cull the front faces so you
        can see the highlighted regions/shanks inside. Built directly on the
        MRI's own grid (mri_label_vol, the atlas-region-label overlay
        already resampled onto the MRI's own array shape by
        TrajectoryPlanningMri.build_mri_label_overlay -- see registration_
        mri.py) at the MRI's own spacing/origin, so the shell's vertex
        positions are true MRI physical-mm coordinates from the moment
        they're created -- no separate atlas->MRI warp step needed, just
        colour by the subject's own MRI intensity at those same positions."""
        mri_spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        data_zyx = self.tp.mri_label_vol[::downsample, ::downsample, ::downsample]
        data_xyz = np.transpose(data_zyx, (2, 1, 0))
        vol = pv.ImageData()
        vol.dimensions = np.array(data_xyz.shape) + 1
        vol.spacing = tuple(s * downsample for s in mri_spacing)
        vol.origin = (0.0, 0.0, 0.0)
        vol.cell_data['NIFTI'] = data_xyz.flatten(order='F')

        background = vol.threshold(value=0.5)
        background = background.extract_surface(algorithm='dataset_surface')
        background = background.clean().triangulate()
        background = background.fill_holes(hole_size=1e10)
        background = background.clean().triangulate()
        # this is just a translucent context shell, not something that needs
        # to be geometrically precise -- decimating BEFORE smoothing caps its
        # triangle count (which otherwise scales with atlas resolution) so
        # camera rotation stays cheap every frame; smoothing afterwards hides
        # the facets decimation introduces.
        background = background.decimate(0.75)
        smoothed = background.smooth_taubin(n_iter=50, pass_band=0.1)

        mesh_kwargs = dict(
            opacity=self.opacityBackground,
            style='surface',
            line_width=0.5,
            pickable=False,
            name='background',
            reset_camera=False,
            render=False,
            culling='front',
        )

        # Already true MRI physical-mm coordinates (vol was built at the
        # MRI's own spacing/origin above) -- just divide back to a voxel
        # index to sample this subject's own MRI intensity there.
        mri_arr = sitk.GetArrayFromImage(self.tp.movingImg_resampled)  # zyx
        mri_shape = mri_arr.shape
        idx = smoothed.points / mri_spacing  # (N,3) float xyz
        rounded = np.round(idx).astype(int)
        in_bounds = (
            (rounded[:, 0] >= 0) & (rounded[:, 0] < mri_shape[2]) &
            (rounded[:, 1] >= 0) & (rounded[:, 1] < mri_shape[1]) &
            (rounded[:, 2] >= 0) & (rounded[:, 2] < mri_shape[0])
        )
        clipped = np.clip(rounded, 0, np.array(mri_shape[::-1]) - 1)
        intensity = np.where(
            in_bounds, mri_arr[clipped[:, 2], clipped[:, 1], clipped[:, 0]], 0
        ).astype(float)
        smoothed.point_data['intensity'] = intensity
        # stretch contrast to the actual (non-background) intensity range
        # instead of mapping the raw scanner range 0..max onto gray --
        # otherwise real tissue, which rarely reaches the data's true max,
        # renders far darker than it needs to.
        nonzero = intensity[intensity > 0]
        clim = [float(np.percentile(nonzero, 1)), float(np.percentile(nonzero, 99))] if nonzero.size else None
        self.background_actor = self.plotter.add_mesh(
            smoothed, scalars='intensity', cmap='gray', clim=clim, show_scalar_bar=False, **mesh_kwargs)

    # ---- bregma/lambda landmarks + roll/pitch reference planes -------------

    _LANDMARK_ACTOR_NAMES = ('landmark_bregma', 'landmark_lambda')
    _PLANE_ACTOR_NAMES = ('plane_bregma_lambda_roll', 'plane_bregma_lambda_rl')
    _LANDMARK_AND_PLANE_ACTOR_NAMES = _LANDMARK_ACTOR_NAMES + _PLANE_ACTOR_NAMES

    def _current_space_bregma_lambda_mm(self):
        """Bregma/lambda points, in MRI physical mm -- shared by the plane
        drawing and the armed-axis indicator (for its roll/pitch rotation-
        axis line) so both agree on exactly the same points.
        coords_bregma/coords_lambda are always set by the time this window
        is usable (bregma/lambda selection is a mandatory earlier wizard
        step)."""
        spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        bregma = np.array(self.tp.coords_bregma, dtype=float) * spacing
        lam = np.array(self.tp.coords_lambda, dtype=float) * spacing
        return bregma, lam

    def _current_space_frame(self):
        """(ap_axis, rl_axis, si_axis), driven by the user's manually-
        dialed-in coronal misalignment angle (CoordTransform.
        ap_rl_si_frame_from_misalignment) -- matches compute_shank_
        roll_pitch_mri exactly, so this window's angle readouts always
        agree with the PDF report's."""
        spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
        bregma = np.array(self.tp.coords_bregma, dtype=float) * spacing
        lam = np.array(self.tp.coords_lambda, dtype=float) * spacing
        misalignment_deg = getattr(self.tp, 'coronal_misalignment_deg', 0.0)
        return self.tp.ap_rl_si_frame_from_misalignment(bregma, lam, misalignment_deg)

    def _draw_landmarks_and_planes(self):
        """Bregma/lambda landmark markers, plus the two reference planes
        compute_shank_roll_pitch_mri measures each shank's roll/pitch
        against (see _current_space_frame -- CoordTransform.
        ap_rl_si_frame_from_misalignment), purely so those angle numbers
        can be visually sanity-checked against an actual picture of the
        planes they describe. Yellow = the RL-SI plane (normal=AP) roll
        is measured within, as an angle from vertical (SI). Cyan = the
        AP-SI plane (normal=RL) pitch is measured within, as an angle
        from the AP line -- each plane's own reference LINE is what the
        angle is actually measured to (see _update_axis_indicator), not
        the plane itself; these planes just show where that line lives.
        checkBox_hideplanes hides just the two planes, leaving the
        landmark spheres visible."""
        for name in self._LANDMARK_AND_PLANE_ACTOR_NAMES:
            if name in self.plotter.actors:
                self.plotter.remove_actor(name, render=False)

        points = self._current_space_bregma_lambda_mm()
        if points is None:
            return
        bregma, lam = points

        frame = self._current_space_frame()
        if frame is None:
            return
        ap_axis, rl_axis, _si_axis = frame
        bl_dist = float(np.linalg.norm(lam - bregma))

        radius = max(bl_dist * 0.03, 0.05)
        for name, point, color in (
            ('landmark_bregma', bregma, 'red'),
            ('landmark_lambda', lam, 'green'),
        ):
            self.plotter.add_mesh(pv.Sphere(radius=radius, center=point), color=color, name=name, render=False)

        size = max(bl_dist * 3, 1.0)
        self.plotter.add_mesh(
            pv.Plane(center=bregma, direction=ap_axis, i_size=size, j_size=size),
            color='yellow', opacity=0.25, name='plane_bregma_lambda_roll', render=False)
        self.plotter.add_mesh(
            pv.Plane(center=bregma, direction=rl_axis, i_size=size, j_size=size),
            color='cyan', opacity=0.25, name='plane_bregma_lambda_rl', render=False)

        hide_planes = self.ui.checkBox_hideplanes.isChecked()
        for name in self._PLANE_ACTOR_NAMES:
            if name in self.plotter.actors:
                self.plotter.actors[name].SetVisibility(not hide_planes)

        self._update_depth_peeling()
        self._update_angle_legend()

    def _on_hide_planes_toggled(self, checked):
        for name in self._PLANE_ACTOR_NAMES:
            if name in self.plotter.actors:
                self.plotter.actors[name].SetVisibility(not checked)
        self._update_depth_peeling()
        self.plotter.render()

    _AXIS_INDICATOR_NAME = 'axis_indicator'

    @staticmethod
    def _dashed_line_mesh(p1, p2, n_dashes=16):
        """A dashed/dotted line from p1 to p2, built as alternating
        'on'/'off' segments -- VTK's own line stippling (SetLineStipple
        Pattern) doesn't render reliably on the modern OpenGL2 backend
        pyvista/VTK use here, so this fakes it geometrically instead."""
        p1 = np.asarray(p1, dtype=float)
        p2 = np.asarray(p2, dtype=float)
        t = np.linspace(0.0, 1.0, n_dashes * 2 + 1)
        points = p1[None, :] + t[:, None] * (p2 - p1)[None, :]
        lines = []
        for i in range(0, len(points) - 1, 2):
            lines.extend([2, i, i + 1])
        poly = pv.PolyData()
        poly.points = points
        poly.lines = np.array(lines)
        return poly

    @staticmethod
    def _dashed_arc_mesh(center, dir1, dir2, radius, n_dashes=16):
        """Dashed arc of the given radius around `center`, sweeping from
        dir1 to dir2 (both unit vectors from center) -- same alternating-
        segment trick as _dashed_line_mesh, just walking Rodrigues'
        rotation formula (dir1 rotated around the dir1 x dir2 axis) instead
        of a straight lerp. Returns None if dir1/dir2 are ~parallel (no
        well-defined sweep plane/direction)."""
        dir1 = np.asarray(dir1, dtype=float)
        dir2 = np.asarray(dir2, dtype=float)
        sweep = np.arccos(np.clip(np.dot(dir1, dir2), -1.0, 1.0))
        axis = np.cross(dir1, dir2)
        axis_norm = np.linalg.norm(axis)
        if sweep < 1e-6 or axis_norm < 1e-9:
            return None
        axis /= axis_norm
        t = np.linspace(0.0, sweep, n_dashes * 2 + 1)
        c, s = np.cos(t), np.sin(t)
        # Rodrigues' rotation formula, vectorized over every sample angle at once.
        rotated = (dir1[None, :] * c[:, None] + np.cross(axis, dir1)[None, :] * s[:, None]
                   + axis[None, :] * np.dot(axis, dir1) * (1 - c)[:, None])
        points = np.asarray(center, dtype=float)[None, :] + rotated * radius
        lines = []
        for i in range(0, len(points) - 1, 2):
            lines.extend([2, i, i + 1])
        poly = pv.PolyData()
        poly.points = points
        poly.lines = np.array(lines)
        return poly

    _AXIS_ANGLE_ARC_NAME = 'axis_angle_arc'

    def _update_axis_indicator(self):
        """Dotted line showing exactly what the step buttons are about to
        do, before pressing them: for x/y/z/trajectory, a line through the
        DEEP point (what those steps actually move) along the direction
        it'll move in; for roll/pitch, a line through the INSERTION point
        (the fixed pivot) along the rotation axis (SI for roll, RL for
        pitch) -- the line a rotation axis geometrically passes through --
        PLUS a dotted arc, for roll/pitch only, from the shank's current
        direction to its own projection onto the reference plane
        compute_shank_roll_pitch_mri measures it against (RL-normal plane
        for roll, SI-normal for pitch) -- i.e. a literal picture of the
        angle those buttons' legend number already reports, since the
        angle between a vector and its own projection onto a plane IS the
        angle between that vector and the plane. Cleared entirely whenever
        no axis is armed, no shank is selected, or the needed geometry/
        landmarks aren't available yet."""
        name = self._AXIS_INDICATOR_NAME
        arc_name = self._AXIS_ANGLE_ARC_NAME
        if name in self.plotter.actors:
            self.plotter.remove_actor(name, render=False)
        if arc_name in self.plotter.actors:
            self.plotter.remove_actor(arc_name, render=False)
        if self._armed_axis is None or self.selected_shank_idx is None:
            return
        insert_mm, deep_mm = self._current_space_insert_deep_mm(self.selected_shank_idx)
        if insert_mm is None or deep_mm is None:
            return
        shank_vec = insert_mm - deep_mm
        shank_dist = float(np.linalg.norm(shank_vec))
        if shank_dist <= 1e-9:
            return
        half_len = max(shank_dist, 1.0)
        shank_dir = shank_vec / shank_dist

        if self._armed_axis in ('x', 'y', 'z'):
            direction = np.zeros(3)
            direction['xyz'.index(self._armed_axis)] = 1.0
            anchor = deep_mm
        elif self._armed_axis == 'trajectory':
            direction = shank_dir
            anchor = deep_mm
        else:  # 'roll' / 'pitch'
            frame = self._current_space_frame()
            if frame is None:
                return
            ap_axis, rl_axis, si_axis = frame
            direction = si_axis if self._armed_axis == 'roll' else rl_axis
            anchor = insert_mm

            # roll = angle from vertical (SI), within the RL-SI plane,
            # dropping AP entirely; pitch = angle from the AP line, within
            # the AP-SI plane, dropping RL entirely (see
            # compute_shank_roll_pitch_mri) -- NOT the rotation axis
            # itself (`direction` above), which is the OTHER one of the
            # two axes.
            drop_axis = ap_axis if self._armed_axis == 'roll' else rl_axis
            reference_axis = si_axis if self._armed_axis == 'roll' else ap_axis
            shank_proj = shank_dir - np.dot(shank_dir, drop_axis) * drop_axis
            proj_norm = np.linalg.norm(shank_proj)
            if proj_norm > 1e-9:
                shank_proj /= proj_norm
                reference_dir = reference_axis if np.dot(shank_proj, reference_axis) >= 0 else -reference_axis
                arc_mesh = self._dashed_arc_mesh(
                    insert_mm, reference_dir, shank_proj, half_len * 0.6)
                if arc_mesh is not None:
                    self.plotter.add_mesh(arc_mesh, color='cyan', line_width=2, name=arc_name, render=False)

        self.plotter.add_mesh(
            self._dashed_line_mesh(anchor - direction * half_len, anchor + direction * half_len),
            color='orange', line_width=3, name=name, render=False)

    def _update_angle_legend(self):
        """On-screen roll/pitch readout for the currently selected shank --
        compute_shank_roll_pitch_mri, the same single source of truth used
        by the 2D views and the PDF report."""
        name = 'angle_legend'
        roll_pitch = (self.tp.compute_shank_roll_pitch_mri(self.selected_shank_idx)
                      if self.selected_shank_idx is not None else None)
        if roll_pitch is None:
            if name in self.plotter.actors:
                self.plotter.remove_actor(name, render=False)
            return

        roll_deg, pitch_deg = roll_pitch
        lines = [
            f"Shank {self.selected_shank_idx + 1}",
            f"roll:  {roll_deg:.1f}°",
            f"pitch: {pitch_deg:.1f}°",
        ]
        self.plotter.add_text(
            "\n".join(lines), position='upper_right', font_size=10, color='white', name=name)

    # ---- camera -------------------------------------------------------------

    def _toggle_perspective(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.parallel_projection:
            self.plotter.disable_parallel_projection()
            self.ui.change_perspective_vis3D.setIcon(
                QIcon(os.path.join(base_dir, "Icons", "ephys", "projection_prespective.png")))
            self.parallel_projection = False
        else:
            self.plotter.enable_parallel_projection()
            self.ui.change_perspective_vis3D.setIcon(
                QIcon(os.path.join(base_dir, "Icons", "ephys", "projection_parallel.png")))
            self.parallel_projection = True

    # ---- moving the selected shank ------------------------------------------

    _AXIS_LABELS = {
        'x': 'Sagittal (x)',
        'y': 'Coronal (y)',
        'z': 'Axial (z)',
        'trajectory': 'Along trajectory',
        'roll': 'Roll (deg)',
        'pitch': 'Pitch (deg)',
    }
    _ARMED_STYLE = "background-color: #e67e22; color: white;"

    def _update_roll_pitch_enabled(self, *_args):
        """checkBox_constraint_90deg/checkBox_constraint_90deg_coronal
        (main window -- see ElecGeometryMri.enforce_constraint_90deg/
        _coronal) lock the shank's AP or RL component to exactly zero,
        and re-enforce that lock on every subsequent deep/insert change
        (ElecGeometryMri._apply_constraints, which change_insert_point/
        change_deepest_point call -- the same path _nudge_shank drives).
        The roll/pitch buttons pivot the shank around the insertion point
        with no notion of either lock, so whatever a nudge just did gets
        partly undone/redistributed the moment that automatic re-snap
        runs -- a confusingly imprecise stand-in for what the button's
        own step size promises. Disable both while either constraint is
        active, rather than one-off-verify which rotation axis happens
        not to disturb which locked component (rotating around one
        in-plane axis can still perturb the locked one via the other
        in-plane component -- not reliably safe to leave enabled)."""
        constrained = (self.tp.ui.checkBox_constraint_90deg.isChecked()
                       or self.tp.ui.checkBox_constraint_90deg_coronal.isChecked())
        self.ui.pushButton_roll.setEnabled(not constrained)
        self.ui.pushButton_pitch.setEnabled(not constrained)
        if constrained and self._armed_axis in ('roll', 'pitch'):
            self._flush_pending_nudge()
            self._armed_axis = None
            self._update_axis_arm_ui()
            self._update_axis_indicator()
            self.plotter.render()

    def _toggle_axis_arm(self, axis):
        """Clicking one of the 6 axis buttons arms/disarms it -- only one
        axis is armed at a time, and the step buttons (<</</>/>>) move (or
        rotate) the selected shank along whichever one is currently
        armed."""
        self._flush_pending_nudge()
        self._armed_axis = None if self._armed_axis == axis else axis
        self._update_axis_arm_ui()
        self._update_axis_indicator()
        self.plotter.render()

    def _update_axis_arm_ui(self):
        for axis, btn in self._axis_buttons.items():
            btn.setStyleSheet(self._ARMED_STYLE if axis == self._armed_axis else "")
            # setStyleSheet("") correctly clears it internally right away,
            # but Qt doesn't always repaint to match -- force it, or a
            # button can stay visibly orange after being disarmed even
            # though its actual stylesheet is already back to empty.
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
        self.ui.label_selectedAxis_vis3D.setText(
            self._AXIS_LABELS[self._armed_axis] if self._armed_axis else "no axis selected")
        # the step strip only makes sense once an axis is armed -- keep it
        # out of the way otherwise instead of showing controls with nothing
        # to act on yet.
        self.ui.frame_axisNav_vis3D.setVisible(self._armed_axis is not None)

    _NUDGE_DEBOUNCE_MS = 200

    def _queue_nudge(self, steps):
        """Step buttons feed here instead of calling _nudge_shank directly --
        each click just accumulates its delta and (re)starts a short timer,
        so a burst of rapid clicks (e.g. holding a button, or double/triple-
        clicking) only pays for _nudge_shank's expensive redraw/region-check
        cascade once, after the user actually stops clicking, rather than
        once per click."""
        self._pending_nudge_steps += steps
        self._nudge_timer.start(self._NUDGE_DEBOUNCE_MS)

    def _apply_pending_nudge(self):
        steps = self._pending_nudge_steps
        self._pending_nudge_steps = 0
        if steps:
            self._nudge_shank(steps)

    def _flush_pending_nudge(self):
        """Apply (rather than silently drop) any nudge still waiting on the
        debounce timer before the armed axis or selected shank changes --
        otherwise those accumulated steps would apply to the wrong axis/
        shank once the timer finally fires."""
        if self._nudge_timer.isActive():
            self._nudge_timer.stop()
            self._apply_pending_nudge()

    def _nudge_shank(self, steps):
        """Move (or rotate) the selected shank by `steps` along whichever
        axis is currently armed. 'trajectory' (the shank's own insert->deep
        axis) slides only the DEEP point along it -- the entry point
        through the skull is fixed by definition of that axis, so it must
        not move. World x/y/z instead move the deep point sideways and
        then re-find where the (unchanged-direction) line now actually
        crosses the skull edge for the new insertion point, rather than
        just carrying the old insertion point's coordinate forward by the
        same delta -- a lateral shift means the old point is no longer
        necessarily ON the edge anymore. 'roll'/'pitch' pivot the shank
        around the (fixed) insertion point by `steps` DEGREES, not voxels
        -- see the dedicated branch below for why that changes only its
        own angle. Goes through the exact same spinBox_tp_insert_*/
        spinBox_tp_deep_* + change_insert_point/change_deepest_point path
        the 2D view itself uses, so everything downstream (redraw, region/
        angle recompute, this window's own refresh) happens exactly like a
        manual edit would."""
        if self._armed_axis is None or self.selected_shank_idx is None:
            return
        idx = self.selected_shank_idx
        insert = self.tp.coords_insert_point.get(idx)
        deep = self.tp.coords_deepest_point.get(idx)
        if insert is None or deep is None:
            return
        insert_arr = np.asarray(insert, dtype=float)
        deep_arr = np.asarray(deep, dtype=float)

        if self._armed_axis == 'trajectory':
            direction = self.tp.direction_atlas.get(idx)
            if direction is None:
                return
            new_deep = deep_arr + np.asarray(direction, dtype=float) * steps
            new_insert = insert_arr  # entry point through the skull stays put
        elif self._armed_axis in ('roll', 'pitch'):
            # Pivot around the INSERTION point (kept fixed, same convention
            # as 'trajectory') by `steps` degrees, rotating around the SI
            # axis for roll or the RL axis for pitch -- rotating a vector
            # around an axis leaves that vector's component ALONG the axis
            # unchanged. Roll = angle to the RL-normal plane (depends only
            # on the shank's RL component); rotating around SI leaves RL
            # fixed while mixing AP/SI, so it changes roll's own angle
            # without touching the RL component pitch is independent of.
            # Symmetrically, rotating around RL leaves the SI component
            # (pitch's own) fixed. So each button moves only its own angle.
            # coords_insert_point/coords_deepest_point are already MRI-grid
            # voxel indices (electrode_mri.py's change_insert_point/
            # change_deepest_point) -- use the same MRI-space frame
            # (ap_rl_si_frame_from_misalignment) compute_shank_roll_pitch_mri
            # does, so the nudge buttons actually move the angle the legend
            # displays.
            spacing = np.array(self.tp.movingImg_resampled.GetSpacing())
            bregma = np.array(self.tp.coords_bregma, dtype=float) * spacing
            lam = np.array(self.tp.coords_lambda, dtype=float) * spacing
            misalignment_deg = getattr(self.tp, 'coronal_misalignment_deg', 0.0)
            frame = self.tp.ap_rl_si_frame_from_misalignment(bregma, lam, misalignment_deg)
            if frame is None:
                return
            _ap_axis, rl_axis, si_axis = frame
            rotation_axis = si_axis if self._armed_axis == 'roll' else rl_axis

            # Rodrigues' rotation formula, applied in physical mm (spacing
            # can be anisotropic, so rotating raw voxel-index components
            # directly against a physical-space axis would be wrong).
            shank_vec_mm = (deep_arr - insert_arr) * spacing
            theta = np.radians(steps)
            c, s = np.cos(theta), np.sin(theta)
            rotated_mm = (shank_vec_mm * c + np.cross(rotation_axis, shank_vec_mm) * s
                          + rotation_axis * np.dot(rotation_axis, shank_vec_mm) * (1 - c))
            new_deep = insert_arr + rotated_mm / spacing
            new_insert = insert_arr  # pivot point -- the entry point stays put
        else:
            delta = np.zeros(3)
            delta['xyz'.index(self._armed_axis)] = steps
            new_deep = deep_arr + delta
            new_insert = self._find_new_insert_point(new_deep, insert_arr, deep_arr)

        # change_insert_point/change_deepest_point always act on the 2D
        # view's OWN current shank (self.tp.shank_number), not whichever one
        # is merely selected in this window -- make sure they agree first.
        if self.tp.shank_number != idx:
            self.tp.select_shank(idx)

        insert_boxes = (self.tp.ui.spinBox_tp_insert_x, self.tp.ui.spinBox_tp_insert_y, self.tp.ui.spinBox_tp_insert_z)
        deep_boxes = (self.tp.ui.spinBox_tp_deep_x, self.tp.ui.spinBox_tp_deep_y, self.tp.ui.spinBox_tp_deep_z)
        # spinboxes are 1-based, coords_insert_point/coords_deepest_point are
        # 0-based (see change_insert_point/change_deepest_point) -- blocked
        # while setting all 3 axes so change_insert_point only fires once,
        # via the explicit call below, with a fully-consistent new position
        # instead of 3 times with transiently-mixed old/new coordinates.
        for box, val in zip(insert_boxes, new_insert):
            box.blockSignals(True)
            box.setValue(int(round(val)) + 1)
            box.blockSignals(False)
        for box, val in zip(deep_boxes, new_deep):
            box.blockSignals(True)
            box.setValue(int(round(val)) + 1)
            box.blockSignals(False)

        self.tp.change_insert_point()
        self.tp.change_deepest_point()

    def _find_new_insert_point(self, new_deep, old_insert, old_deep):
        """After a sideways (x/y/z) nudge, march from the new deep point
        along the OLD (unchanged) insert direction and, of every point
        along that ray that's inside self.tp.edge_mask (the skull/brain
        boundary), take the one that's vertically highest -- largest Z,
        confirmed against the atlas's own NIfTI direction matrix (+1 on the
        Z axis, i.e. increasing Z is more superior/dorsal) -- instead of
        just carrying the old insertion point's coordinate forward by the
        same delta, which can leave it sitting off the edge after a lateral
        shift. Taking the highest point rather than the first one found
        matters because the skull mask can have a hole/gap partway up (a
        real foramen, or a segmentation defect); the true insertion point
        is always the topmost crossing, at the outer skull surface. Falls
        back to the naive translated point if there's no edge mask yet or
        no crossing is found in range."""
        edge_mask = getattr(self.tp, 'edge_mask', None)
        naive = new_deep + (old_insert - old_deep)
        direction = old_insert - old_deep
        dist = np.linalg.norm(direction)
        if edge_mask is None or dist < 1e-6:
            return naive
        direction = direction / dist
        max_dist = dist * 1.5  # a bit of slack in case the edge shifted further out
        topmost = None
        for t in np.linspace(0, max_dist, int(max_dist) + 1):
            p = new_deep + t * direction
            vidx = tuple(np.round(p[::-1]).astype(int))
            if all(0 <= vidx[i] < edge_mask.shape[i] for i in range(3)) and edge_mask[vidx]:
                if topmost is None or p[2] > topmost[2]:
                    topmost = p
        return topmost if topmost is not None else naive
