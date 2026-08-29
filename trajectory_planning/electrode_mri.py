# This Python file uses the following encoding: utf-8
"""MRI-space override of ElecGeometry (trajectory_planning/electrode.py).

check_region_to_avoid (already space-agnostic -- works on whatever
coords_deepest_point/coords_insert_point/region_to_avoid currently are),
show_canvas, _refresh_next_shank_button, on_next_shank_clicked,
_switch_insertion_shank_mri, _flip_cursor_to_point,
_draw_insertion_guide_line_mri, _draw_mri_shank_markers are inherited
unchanged -- they already read mri_deep/mri_insert directly, which are now
just aliases of coords_deepest_point/coords_insert_point (see get/change_*_
point below), or are otherwise already space-agnostic.
"""

import numpy as np
from PySide6.QtWidgets import QMessageBox

from mrid_utils.channel_mapper import plot_dwi_1D_cross_section
from trajectory_planning.electrode import ElecGeometry
from paths_config import _paths


class ElecGeometryMri(ElecGeometry):
    def _apply_constraints(self, shank_number):
        """
        checkBox_constraint_90deg / checkBox_constraint_90deg_coronal:
        insert is always the anchor, so any setter that just moved insert
        OR deep re-snaps deep here to stay exactly perpendicular to
        bregma-lambda (constrain_shank_ap_to_zero) or exactly
        perpendicular to RL (constrain_shank_rl_to_zero). The two
        checkboxes are mutually exclusive (enforce_constraint_90deg/
        enforce_constraint_90deg_coronal unchecks the other one the
        moment either is checked, radio-button style), so at most one of
        ap_on/rl_on is ever true here -- this doesn't need to pick
        between them itself. No-op entirely if neither is checked.
        """
        ap_on = self.ui.checkBox_constraint_90deg.isChecked()
        rl_on = self.ui.checkBox_constraint_90deg_coronal.isChecked()
        if not ap_on and not rl_on:
            return
        if ap_on:
            self.constrain_shank_ap_to_zero(shank_number)
        if rl_on:
            self.constrain_shank_rl_to_zero(shank_number)
        if shank_number == self.shank_number:
            self.set_value(list(self.mri_deep[shank_number]), self.ui.spinBox_tp_deep_x, self.ui.spinBox_tp_deep_y, self.ui.spinBox_tp_deep_z)
        self.draw_point(self.mri_deep[shank_number], (0, 1, 0), 'deep')
        if shank_number == self.shank_number:
            if ap_on:
                self.update_oblique_coronal_view()
                self.update_oblique_coronal_crossing_line()
                self.ui.stackedWidget_coronal.setCurrentIndex(1)
            if rl_on:
                self.update_oblique_sagittal_view()
                self.update_oblique_sagittal_crossing_line()
                self.ui.stackedWidget_sagittal.setCurrentIndex(1)

    def _refresh_oblique_views_for_insert(self, shank_number):
        """Re-anchor the oblique constraint view(s) on this shank's
        current insert point (update_oblique_coronal_view/update_oblique_
        sagittal_view anchor there, falling back to bregma only if no
        insert point exists yet) the moment that insert point changes --
        called independently of _apply_constraints, whose own oblique-
        view refresh only runs once BOTH a deep and an insert point exist
        for this shank. Without this, checking a constraint checkbox
        before placing a deepest point (or moving the insert point during
        insertion refinement, which never touches mri_deep at all -- see
        pick_insertion_point_from_click) left the oblique view stuck
        showing the old anchor (or bregma) instead of the just-picked
        insert point.

        Also switches stackedWidget_coronal/stackedWidget_sagittal to the
        oblique page (index 1) -- same setCurrentIndex(1) enforce_
        constraint_90deg/_coronal do when the checkbox is first checked.
        Refreshing the content alone wasn't enough if that panel had
        somehow ended up back on the normal page (index 0) with the
        checkbox still checked: the constraint view needs to actually be
        the thing on screen the moment insertion is set, not just correct
        in the background."""
        if shank_number != self.shank_number:
            return
        if self.ui.checkBox_constraint_90deg.isChecked():
            self.update_oblique_coronal_view()
            self.update_oblique_coronal_crossing_line()
            self.ui.stackedWidget_coronal.setCurrentIndex(1)
        if self.ui.checkBox_constraint_90deg_coronal.isChecked():
            self.update_oblique_sagittal_view()
            self.update_oblique_sagittal_crossing_line()
            self.ui.stackedWidget_sagittal.setCurrentIndex(1)

    def enforce_constraint_90deg(self, checked):
        """checkBox_constraint_90deg.toggled: snap every already-placed
        shank to perpendicular the moment the box is checked, not just on
        the next drag. Also swaps the coronal panel to the oblique,
        true-AP-perpendicular reslice (stackedWidget_coronal page 1,
        vtkWidget_data_coronal_3, page_32) while checked, since the AP=0-
        constrained shank generally isn't contained in any single
        fixed-y axis-aligned coronal slice -- reverts to the normal
        coronal view (page 0) when unchecked. page_32 (index 1) used to
        hold the "clipped 3D view" feature (change_view_coronal's
        Vis3D.render_clipped, vtkWidget_trajPlan_1) -- that's been moved
        to page_10 (index 2, see change_view_coronal/create_channel_list)
        to make room.

        Mutually exclusive with checkBox_constraint_90deg_coronal --
        forcing AP to zero AND RL to zero simultaneously would leave no
        remaining direction for the shank (fully vertical, no freedom at
        all), so checking this one unchecks the other first, same as a
        radio button. setChecked(False) below re-enters enforce_
        constraint_90deg_coronal(False) synchronously (Qt direct
        connections), so its own oblique view/page is already reverted
        by the time this continues."""
        if checked and self.ui.checkBox_constraint_90deg_coronal.isChecked():
            self.ui.checkBox_constraint_90deg_coronal.setChecked(False)

        if checked:
            self.setup_oblique_coronal_view()
            self.update_oblique_coronal_view()
            self.update_oblique_coronal_crossing_line()
            self.ui.stackedWidget_coronal.setCurrentIndex(1)
        else:
            self.ui.stackedWidget_coronal.setCurrentIndex(0)
            self.hide_oblique_coronal_crossing_line()

        if not checked:
            return
        current_shank = self.shank_number
        for shank_number in sorted(self.mri_deep):
            if self.mri_deep.get(shank_number) is None or self.mri_insert.get(shank_number) is None:
                continue
            self.shank_number = shank_number
            self.constrain_shank_ap_to_zero(shank_number)
            self.set_value(list(self.mri_deep[shank_number]), self.ui.spinBox_tp_deep_x, self.ui.spinBox_tp_deep_y, self.ui.spinBox_tp_deep_z)
            self.draw_point(self.mri_deep[shank_number], (0, 1, 0), 'deep')
            self.calculate_distance(self.mri_deep[shank_number], self.mri_insert[shank_number])
            self.create_channel_list()
        self.shank_number = current_shank
        self.select_shank(self.shank_number)
        self.render()

    def enforce_constraint_90deg_coronal(self, checked):
        """checkBox_constraint_90deg_coronal.toggled: coronal-angle
        analogue of enforce_constraint_90deg -- snaps every already-
        placed shank to perpendicular-to-RL the moment the box is
        checked, not just on the next drag. Also swaps the sagittal panel
        to the oblique, true-RL-perpendicular reslice (stackedWidget_
        sagittal page 1, vtkWidget_data_sagittal_3, page_33) while
        checked, since the RL=0-constrained shank generally isn't
        contained in any single fixed-x axis-aligned sagittal slice --
        reverts to the normal sagittal view (page 0) when unchecked.
        page_33 (index 1) used to hold sagittal's own "clipped 3D view"
        feature -- moved to page_4 (index 2, see change_view_sagittal/
        create_channel_list), same reordering as checkBox_constraint_
        90deg's own page_32->page_10.

        Mutually exclusive with checkBox_constraint_90deg -- see that
        method's docstring."""
        if checked and self.ui.checkBox_constraint_90deg.isChecked():
            self.ui.checkBox_constraint_90deg.setChecked(False)

        if checked:
            self.setup_oblique_sagittal_view()
            self.update_oblique_sagittal_view()
            self.update_oblique_sagittal_crossing_line()
            self.ui.stackedWidget_sagittal.setCurrentIndex(1)
        else:
            self.ui.stackedWidget_sagittal.setCurrentIndex(0)
            self.hide_oblique_sagittal_crossing_line()

        if not checked:
            return
        current_shank = self.shank_number
        for shank_number in sorted(self.mri_deep):
            if self.mri_deep.get(shank_number) is None or self.mri_insert.get(shank_number) is None:
                continue
            self.shank_number = shank_number
            self.constrain_shank_rl_to_zero(shank_number)
            self.set_value(list(self.mri_deep[shank_number]), self.ui.spinBox_tp_deep_x, self.ui.spinBox_tp_deep_y, self.ui.spinBox_tp_deep_z)
            self.draw_point(self.mri_deep[shank_number], (0, 1, 0), 'deep')
            self.calculate_distance(self.mri_deep[shank_number], self.mri_insert[shank_number])
            self.create_channel_list()
        self.shank_number = current_shank
        self.select_shank(self.shank_number)
        self.render()

    def get_deepest_point(self):
        self.selecting_point = True
        self.coords_deepest_point[self.shank_number] = self.LoadMRI.slice_indices[0][::-1].copy()
        self.set_value(self.coords_deepest_point[self.shank_number].copy(), self.ui.spinBox_tp_deep_x, self.ui.spinBox_tp_deep_y, self.ui.spinBox_tp_deep_z)

        self.draw_point(self.coords_deepest_point[self.shank_number], (0, 1, 0), 'deep')

        # coords_deepest_point is already an MRI voxel index (the MRI never
        # stops being the displayed volume in this workflow) -- mri_deep is
        # kept as a plain alias, not re-derived via atlas_to_mri_coordinates
        # (that conversion only made sense when coords_* were atlas-voxel
        # coordinates), since several other methods (PDF report,
        # shank_sidebar, the insertion-refinement page) still read mri_deep/
        # mri_insert directly.
        self.mri_deep[self.shank_number] = list(self.coords_deepest_point[self.shank_number])
        if self.mri_insert[self.shank_number] is not None:
            self._apply_constraints(self.shank_number)
            self.calculate_distance(self.mri_deep[self.shank_number], self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.selecting_point = False
        self.render()

    def get_insert_point(self):
        self.selecting_point = True
        self.coords_insert_point[self.shank_number] = self.get_point_at_edge(self.edge_mask, self.clicked_viewname)

        self.set_value(self.coords_insert_point[self.shank_number].copy(), self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z)

        self.draw_point(self.coords_insert_point[self.shank_number], (1, 0, 0), 'insert')
        self.mri_insert[self.shank_number] = list(self.coords_insert_point[self.shank_number])
        if self.mri_deep[self.shank_number] is not None:
            self._apply_constraints(self.shank_number)
            self.calculate_distance(self.mri_deep[self.shank_number], self.mri_insert[self.shank_number])
            self.create_channel_list()
        else:
            self._refresh_oblique_views_for_insert(self.shank_number)

        self.selecting_point = False
        self.render()

    def change_insert_point(self):
        self.coords_insert_point[self.shank_number] = [self.ui.spinBox_tp_insert_x.value() - 1, self.ui.spinBox_tp_insert_y.value() - 1, self.ui.spinBox_tp_insert_z.value() - 1]
        self.draw_point(self.coords_insert_point[self.shank_number], (0, 1, 0), 'insert')
        self.mri_insert[self.shank_number] = list(self.coords_insert_point[self.shank_number])
        if self.mri_deep[self.shank_number] is not None:
            self._apply_constraints(self.shank_number)
            self.calculate_distance(self.mri_deep[self.shank_number], self.mri_insert[self.shank_number])
            self.create_channel_list()
        else:
            self._refresh_oblique_views_for_insert(self.shank_number)

        self.render()

    def change_deepest_point(self):
        self.coords_deepest_point[self.shank_number] = [self.ui.spinBox_tp_deep_x.value() - 1, self.ui.spinBox_tp_deep_y.value() - 1, self.ui.spinBox_tp_deep_z.value() - 1]
        self.draw_point(self.coords_deepest_point[self.shank_number], (0, 1, 0), 'deep')
        self.mri_deep[self.shank_number] = list(self.coords_deepest_point[self.shank_number])
        if self.mri_insert[self.shank_number] is not None:
            self._apply_constraints(self.shank_number)
            self.calculate_distance(self.mri_deep[self.shank_number], self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.render()

    def create_channel_list(self):
        self.ui.pushButton_coronalView.setEnabled(True)
        self.ui.pushButton_sagittalView.setEnabled(True)
        self.ui.pushButton_axialView.setEnabled(True)

        self.direction_atlas[self.shank_number] = (np.array(self.coords_insert_point[self.shank_number]) - np.array(self.coords_deepest_point[self.shank_number]))
        self.direction_atlas[self.shank_number] = self.direction_atlas[self.shank_number] / np.linalg.norm(self.direction_atlas[self.shank_number])
        physical_per_atlas_voxel = np.linalg.norm(self.direction_atlas[self.shank_number] * np.array(self.movingImg_resampled.GetSpacing()))

        dfx_shank = self.dfx_shank_data.get(self.shank_number)
        if dfx_shank is not None:
            depth_um = dfx_shank["geometry"][:, 1]
            offsets_atlas = (depth_um / 1000) / physical_per_atlas_voxel
            self.channel_points[self.shank_number] = (
                self.coords_deepest_point[self.shank_number]
                + offsets_atlas[:, None] * self.direction_atlas[self.shank_number])
            self.atlas_shank_end[self.shank_number] = self.channel_points[self.shank_number][
                np.argmax(depth_um)]
            num_channels = depth_um.shape[0]
        else:
            num_channels = self.ui.spinBox_tp_channels.value()
            d_separation_atlas = (self.ui.spinBox_tp_separation.value() / 1000) / physical_per_atlas_voxel
            self.atlas_shank_end[self.shank_number] = self.coords_deepest_point[self.shank_number] + (num_channels - 1) * d_separation_atlas * self.direction_atlas[self.shank_number]
            self.channel_points[self.shank_number] = np.array([self.coords_deepest_point[self.shank_number] + i * d_separation_atlas * self.direction_atlas[self.shank_number] for i in range(num_channels)])

        if not getattr(self.LoadMRI, 'picking_insertion_point', False):
            vtk_color = self.get_shank_vtk_color(self.shank_number)
            for view_name in 'axial', 'sagittal', 'coronal':
                if view_name in self.line_actor[self.shank_number]:
                    for a in self.line_actor[self.shank_number][view_name]:
                        self.LoadMRI.renderers[0][view_name].RemoveActor(a)
                    self.LoadMRI.renderers[0][view_name].RemoveActor(self.label_actor[self.shank_number][view_name])
                self.line_actor[self.shank_number][view_name], self.label_actor[self.shank_number][view_name] = self.draw_electrode_line(view_name, self.coords_deepest_point[self.shank_number], self.atlas_shank_end[self.shank_number], color=vtk_color)
                for a in self.line_actor[self.shank_number][view_name]:
                    self.LoadMRI.renderers[0][view_name].AddActor(a)
                self.LoadMRI.renderers[0][view_name].AddActor(self.label_actor[self.shank_number][view_name])
            self.render()
            if hasattr(self, 'atlas_bregma_coords'):
                self.update_shank_angle_display()
                self.update_coronal_plane_line()

            if self.ui.stackedWidget_coronal.currentIndex() == 2:
                self.change_view_coronal(checked=False, recenter=False)
            if self.ui.stackedWidget_sagittal.currentIndex() == 2:
                self.change_view_sagittal(checked=False, recenter=False)

        # region-name lookup now samples the atlas-labels-on-MRI-grid overlay
        # (mri_label_vol, built in TpRegistrationMri.build_mri_label_overlay)
        # instead of the atlas' own native-grid array (atlas_vol).
        mri_values = [self.mri_label_vol[tuple(np.round(p[::-1]).astype(int))] for p in self.channel_points[self.shank_number]]
        region_name = [self.tp_labels[val][4] for val in mri_values]
        self.check_CA1_or_2(region_name, self.channel_points[self.shank_number], num_channels)
        self.check_region_to_avoid()
        self.check_shank_intersections()
        if hasattr(self, 'shank_sidebar'):
            self.shank_sidebar.refresh()
        if self.tp3d_window is not None:
            self.tp3d_window.refresh_shanks()

    def check_shank_intersections(self):
        spacing = np.array(self.movingImg_resampled.GetSpacing())
        deep = self.coords_deepest_point.get(self.shank_number)
        insert = self.coords_insert_point.get(self.shank_number)
        if deep is None or insert is None:
            return
        deep_mm = np.array(deep, dtype=float) * spacing
        insert_mm = np.array(insert, dtype=float) * spacing

        TOUCH_DIST_MM = 0.05
        hit_shanks = []
        for other_idx, other_deep in self.coords_deepest_point.items():
            if other_idx == self.shank_number or other_deep is None:
                continue
            other_insert = self.coords_insert_point.get(other_idx)
            if other_insert is None:
                continue
            other_deep_mm = np.array(other_deep, dtype=float) * spacing
            other_insert_mm = np.array(other_insert, dtype=float) * spacing
            dist = self._segment_segment_distance(
                deep_mm, insert_mm, other_deep_mm, other_insert_mm)
            if dist < TOUCH_DIST_MM:
                hit_shanks.append(other_idx)

        if hit_shanks:
            shanks_str = ", ".join(str(i + 1) for i in sorted(hit_shanks))
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText(
                f"Shank {self.shank_number + 1} intersects with shank(s) {shanks_str}!")
            msg_box.addButton("OK", QMessageBox.ActionRole)
            msg_box.exec()

    def check_CA1_or_2(self, regionNames, points, num_channels):
        ca1_region_name = _paths.get('atlas_ca1_region_name', "Cornu ammonis 1")
        if ca1_region_name in regionNames and hasattr(self, 'dwi'):
            self.ui.pushButton_PyLdetection.setEnabled(True)

            minPixVal = 2e16
            pyrChIdx = 0
            dwi1Dsignal = np.zeros((num_channels,))

            for idx, point in enumerate(points):
                # self.dwi stays on the atlas' own native grid (see
                # TpRegistrationMri.do_get_shank_line's note) -- convert this
                # MRI-space channel point to its nearest atlas-voxel
                # equivalent via the existing dense correspondence lookup
                # (same approximation class already used elsewhere, e.g.
                # coord_transform.py's mri_grid_not_background_mask) instead
                # of indexing self.dwi with the MRI-space point directly.
                atlas_point = self.mri_to_atlas_via_lookup(point)
                z, y, x = [int(round(c)) for c in atlas_point]
                dwi1Dsignal[idx] = self.dwi[x, y, z]

                if regionNames[idx] == ca1_region_name:
                    if dwi1Dsignal[idx] < minPixVal:
                        minPixVal = dwi1Dsignal[idx]
                        pyrChIdx = idx

            plot_dwi_1D_cross_section(dwi1Dsignal, regionNames, pyrChIdx, num_channels, mplwidget=self.ui.tp_dwi1D_widget)
        else:
            self.ui.pushButton_PyLdetection.setEnabled(False)
            if hasattr(self.ui.tp_dwi1D_widget, 'canvas'):
                self.ui.tp_dwi1D_widget.canvas.figure.clear()
                self.ui.tp_dwi1D_widget.canvas.draw()

    # ------------------------------------------------------------------
    # Insertion-point refinement page (page_31). The MRI never stops being
    # the displayed volume in this workflow, so unlike ElecGeometry's
    # version there is no volume round-trip left to do here -- only the
    # "picking mode" bookkeeping (suppressing the normal shank-line redraw,
    # disabling shank add/remove while refining) remains. Since the
    # renderers are never torn down/rebuilt (no restart_gui call), any
    # actor left on screen must be explicitly removed here instead of just
    # forgotten via a dict reset -- see the RemoveActor loops in
    # _return_to_atlas_space below (ElecGeometry's version could just reset
    # those dicts, since restart_gui had already destroyed the actors along
    # with the whole renderer).

    def enter_insertion_refinement_page(self):
        missing = [idx + 1 for idx in sorted(self.coords_deepest_point)
                   if self.coords_deepest_point.get(idx) is None
                   or self.coords_insert_point.get(idx) is None
                   or self.direction_atlas.get(idx) is None]
        if missing:
            msg_box = QMessageBox(self.MW)
            msg_box.setWindowTitle("Insertion Points Incomplete")
            msg_box.setText(
                "Every shank needs both an insertion and a deepest point "
                "before continuing -- missing for shank(s): "
                + ", ".join(str(i) for i in missing))
            msg_box.addButton("OK", QMessageBox.ActionRole)
            msg_box.exec()
            return

        self._insertion_confirmed = set()
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(2)
        self._enter_mri_space_for_insertion()
        self._switch_insertion_shank_mri(0)

    def _enter_mri_space_for_insertion(self):
        self.LoadMRI.picking_insertion_point = True

        for w in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks,
                  self.ui.pushButton_addShank, self.ui.pushButton_removeShank,
                  self.ui.pushButton_coronalView, self.ui.pushButton_sagittalView,
                  self.ui.pushButton_axialView):
            w.setEnabled(False)

    def _return_to_atlas_space(self):
        self.LoadMRI.picking_insertion_point = False

        for actors in self._insertion_guide_actor.values():
            for view_name, actor in actors.items():
                self.LoadMRI.renderers[0][view_name].RemoveActor(actor)
        self._insertion_guide_actor = {}

        for kind_actors in self._mri_marker_actor.values():
            for view_name, actor in kind_actors.items():
                self.LoadMRI.renderers[0][view_name].RemoveActor(actor)
        self._mri_marker_actor = {'deep': {}, 'insert': {}}

        for idx in sorted(self.coords_deepest_point):
            self.shank_number = idx
            self.create_channel_list()
        self.init_page30_mirror()

        for w in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks,
                  self.ui.pushButton_addShank, self.ui.pushButton_removeShank,
                  self.ui.pushButton_coronalView, self.ui.pushButton_sagittalView,
                  self.ui.pushButton_axialView):
            w.setEnabled(True)
        self.select_shank(self.shank_number)
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(1)

    def _set_insertion_refinement_layers_visible(self, visible):
        """Toggle the "Brain Regions" (mri_label_vol, self.
        _mri_label_overlay_layer_index -- registration_mri.py's
        build_mri_label_overlay) and "Forbidden Regions" (self.
        _region_to_avoid_layer_index -- do_get_shank_line) overlays.
        Both are orientation aids for placing/constraining the shank
        earlier in the workflow; for the final skull-point click here, a
        clean, undistracted view of the raw MRI matters more than either.
        Same toggle_visibility(checked, visibility_btn) calls the
        intensity table's own eye-icon buttons drive, so the table stays
        in sync (icon, opacity-box enabled state) with this."""
        for layer_index in (getattr(self, '_mri_label_overlay_layer_index', None),
                             getattr(self, '_region_to_avoid_layer_index', None)):
            if layer_index is None:
                continue
            layer = self.LoadMRI.MW.Layers[0].get(layer_index)
            if layer is not None:
                layer.toggle_visibility(visible, getattr(layer, 'visibility_btn', None))

    def pick_insertion_point_from_click(self):
        shank = self.shank_number
        deep = self.mri_deep.get(shank)
        direction = self._insertion_direction_mri.get(shank)
        if deep is None or direction is None:
            return

        click_pt = np.array(self.LoadMRI.slice_indices[0][::-1], dtype=float)
        deep_arr = np.array(deep, dtype=float)
        t = float(np.dot(click_pt - deep_arr, direction))
        t_max = self._insertion_guide_t_max.get(shank)
        t = max(0.0, min(t, t_max)) if t_max is not None else max(0.0, t)
        proj = deep_arr + t * direction

        shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx, MRI shape
        proj[0] = np.clip(proj[0], 0, shape[2] - 1)
        proj[1] = np.clip(proj[1], 0, shape[1] - 1)
        proj[2] = np.clip(proj[2], 0, shape[0] - 1)
        self.mri_insert[shank] = [int(round(c)) for c in proj]
        # coords_insert_point is the same MRI-voxel space as mri_insert now --
        # no atlas-space lookup conversion needed (ElecGeometry's version
        # used mri_to_atlas_via_lookup here since coords_insert_point used
        # to be atlas-voxel).
        self.coords_insert_point[shank] = list(self.mri_insert[shank])

        self.set_value(list(self.mri_insert[shank]), self.ui.spinBox_insertion_x,
                        self.ui.spinBox_insertion_y, self.ui.spinBox_insertion_z)
        self._draw_mri_shank_markers()
        # This is the final skull-point click -- deliberately the OPPOSITE
        # of _refresh_oblique_views_for_insert's usual "open/refresh the
        # constraint view" behavior everywhere else: force back to the
        # plain coronal/sagittal pages (even if a constraint checkbox is
        # still checked from an earlier step) and hide the Brain Regions/
        # Forbidden Regions overlays, so the actual skull surface is
        # visible without oblique distortion or region-color clutter.
        #
        # Also exit the "3D visualisation" clipped view (pushButton_
        # coronalView/sagittalView, page index 2 -- change_view_coronal/
        # _sagittal in rendering.py) if either was active: setCurrentIndex
        # alone only changes what's on screen, not the toggle button's own
        # checked state, which is what actually drives that page (clicked,
        # not toggled -- see trajectory_planning.py's wiring) -- left
        # unsynced, the button would still read "3D view" while the panel
        # already shows the plain 2D page. Same pattern select_shank
        # (shank.py) already uses for this exact situation.
        self.ui.stackedWidget_coronal.setCurrentIndex(0)
        self.ui.stackedWidget_sagittal.setCurrentIndex(0)
        self.ui.pushButton_coronalView.setChecked(True)
        self.ui.pushButton_sagittalView.setChecked(True)
        self.hide_oblique_coronal_crossing_line()
        self.hide_oblique_sagittal_crossing_line()
        self._set_insertion_refinement_layers_visible(False)
        self.render()

        spacing = np.array(self.movingImg_resampled.GetSpacing())
        dist = float(np.linalg.norm((np.array(self.mri_insert[shank]) - np.array(self.mri_deep[shank])) * spacing))
        self.ui.doubleSpinBox_distance_shank.setValue(dist)
        self.ui.spinBox_depth.setValue(dist)

        self.create_channel_list()

        self._insertion_confirmed.add(shank)
        self._refresh_next_shank_button()
