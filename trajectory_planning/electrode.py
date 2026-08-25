# This Python file uses the following encoding: utf-8
import os
import numpy as np
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from mrid_utils.channel_mapper import plot_dwi_1D_cross_section
from utils.zoom import Zoom
from trajectory_planning.file_input_output import FileOutput
from gui_utils.busy_overlay import BusyOverlay
from paths_config import _paths

class ElecGeometry:
    def get_deepest_point(self):
        self.selecting_point = True
        self.coords_deepest_point[self.shank_number] = self.LoadMRI.slice_indices[0][::-1].copy()
        self.set_value(self.coords_deepest_point[self.shank_number].copy(),self.ui.spinBox_tp_deep_x,self.ui.spinBox_tp_deep_y,self.ui.spinBox_tp_deep_z)

        #draw deep green
        self.draw_point(self.coords_deepest_point[self.shank_number],(0,1,0),'deep')

        self.mri_deep[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_deepest_point[self.shank_number])) #xyz
        if self.mri_insert[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.selecting_point = False
        self.render()



    def get_insert_point(self):
        self.selecting_point = True
        self.coords_insert_point[self.shank_number] = self.get_point_at_edge(self.edge_mask, self.clicked_viewname)

        self.set_value(self.coords_insert_point[self.shank_number].copy(),self.ui.spinBox_tp_insert_x,self.ui.spinBox_tp_insert_y,self.ui.spinBox_tp_insert_z)

        #draw insert red
        self.draw_point(self.coords_insert_point[self.shank_number],(1,0,0),'insert')
        self.mri_insert[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_insert_point[self.shank_number])) #xyz
        if self.mri_deep[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.selecting_point = False
        self.render()



    def change_insert_point(self):
        self.coords_insert_point[self.shank_number] = [self.ui.spinBox_tp_insert_x.value()-1,self.ui.spinBox_tp_insert_y.value()-1,self.ui.spinBox_tp_insert_z.value()-1]
        self.draw_point(self.coords_insert_point[self.shank_number],(0,1,0),'insert')
        self.mri_insert[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_insert_point[self.shank_number]))
        if self.mri_deep[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.render()

    def change_deepest_point(self):
        self.coords_deepest_point[self.shank_number] = [self.ui.spinBox_tp_deep_x.value()-1,self.ui.spinBox_tp_deep_y.value()-1,self.ui.spinBox_tp_deep_z.value()-1]
        self.draw_point(self.coords_deepest_point[self.shank_number],(0,1,0),'deep')
        self.mri_deep[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_deepest_point[self.shank_number]))
        if self.mri_insert[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.render()

    def change_shank_parameters(self):
        if self.coords_deepest_point[self.shank_number] is not None and self.coords_insert_point[self.shank_number] is not None:
            self.create_channel_list()

        self.render()


    def create_channel_list(self):
        self.ui.groupBox_shank.setEnabled(True)
        self.ui.pushButton_coronalView.setEnabled(True)
        self.ui.pushButton_sagittalView.setEnabled(True)
        self.ui.pushButton_axialView.setEnabled(True)

        self.direction_atlas[self.shank_number] = (np.array(self.coords_insert_point[self.shank_number]) - np.array(self.coords_deepest_point[self.shank_number]))
        self.direction_atlas[self.shank_number] = self.direction_atlas[self.shank_number] / np.linalg.norm(self.direction_atlas[self.shank_number])
        physical_per_atlas_voxel = np.linalg.norm(self.direction_atlas[self.shank_number] * np.array(self.fixedImg.GetSpacing()))

        dfx_shank = self.dfx_shank_data.get(self.shank_number)
        if dfx_shank is not None:
            # Use the DXF-bent contact depths (distance from the deepest/tip
            # contact, in um) directly along the deepest->insert axis; the
            # lateral (X) bundling offset has no defined direction in 3D
            # (the probe's roll around this axis is unknown), so it is
            # collapsed/ignored here.
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
            self.atlas_shank_end[self.shank_number] = self.coords_deepest_point[self.shank_number] + (num_channels-1)*d_separation_atlas*self.direction_atlas[self.shank_number]
            self.channel_points[self.shank_number] = np.array([self.coords_deepest_point[self.shank_number] + i * d_separation_atlas * self.direction_atlas[self.shank_number] for i in range(num_channels)])

        # The insertion-refinement page (page_31) temporarily swaps the
        # displayed volume from the atlas to the subject's own MRI (see
        # _enter_mri_space_for_insertion) so the user can see the real
        # skull -- self.LoadMRI.renderers[0][view_name] is the MRI-space
        # renderer for the whole time picking_insertion_point is True, so
        # drawing this atlas-voxel-coordinate line onto it would place it
        # nonsensically. The numeric geometry above (direction_atlas,
        # channel_points, atlas_shank_end) is still needed live for the
        # PDF report though, so only the rendering is skipped here --
        # _return_to_atlas_space() re-runs this for every shank once
        # picking is done, drawing all of this properly.
        if not getattr(self.LoadMRI, 'picking_insertion_point', False):
            #line
            vtk_color = self.get_shank_vtk_color(self.shank_number)
            for view_name in 'axial','sagittal','coronal':
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

            # recenter=False here -- this is an automatic refresh after an edit
            # to the shank's own geometry (e.g. a 3D-window nudge), not the user
            # explicitly switching to this view, so keep whatever pan/zoom/
            # rotation they already have on it instead of snapping back to
            # centered on every single edit.
            if self.ui.stackedWidget_coronal.currentIndex() == 1: #coronal
                self.change_view_coronal(checked=False, recenter=False)
            if self.ui.stackedWidget_sagittal.currentIndex() == 1: #coronal
                self.change_view_sagittal(checked=False, recenter=False)
        atlas_values = [self.atlas_vol[tuple(np.round(p[::-1]).astype(int))] for p in self.channel_points[self.shank_number]]
        region_name = [self.tp_labels[val][4] for val in atlas_values]
        self.check_CA1_or_2(region_name,self.channel_points[self.shank_number],num_channels)
        self.check_region_to_avoid()
        self.check_shank_intersections()
        if hasattr(self, 'shank_sidebar'):
            self.shank_sidebar.refresh()
        if self.tp3d_window is not None:
            self.tp3d_window.refresh_shanks()


    def check_region_to_avoid(self):
        if not hasattr(self, 'region_to_avoid_img') or self.region_to_avoid_img is None:
            return
        hit = False
        deep = np.array(self.coords_deepest_point[self.shank_number])
        insert = np.array(self.coords_insert_point[self.shank_number])
        n_steps = int(np.max(np.abs(insert - deep))) + 1 #check every voxel
        samples = np.linspace(deep, insert, n_steps)
        for p in samples:
            idx = tuple(np.round(p[::-1]).astype(int))
            if self.region_to_avoid[idx] > 0:
                hit = True
                break
        if hit:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText(f"Shank {self.shank_number} passes through a region which should be avoided!")
            msg_box.addButton("OK", QMessageBox.ActionRole)
            msg_box.exec()


    def check_shank_intersections(self):
        """Warn if the current shank's deep->insert line crosses (or passes
        implausibly close to) any other shank's line -- two physical
        probes can't occupy the same space, so this is a real planning
        error, not just a soft "too close for comfort" hint. Same trigger
        point/style as check_region_to_avoid."""
        spacing = np.array(self.fixedImg.GetSpacing())
        deep = self.coords_deepest_point.get(self.shank_number)
        insert = self.coords_insert_point.get(self.shank_number)
        if deep is None or insert is None:
            return
        deep_mm = np.array(deep, dtype=float) * spacing
        insert_mm = np.array(insert, dtype=float) * spacing

        # Sub-voxel threshold: below this, the two shank lines are
        # effectively occupying the same physical location.
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

    @staticmethod
    def _segment_segment_distance(p1, p2, p3, p4):
        """Closest distance between 3D line segments p1->p2 and p3->p4
        (standard closest-point-between-segments construction)."""
        d1, d2, r = p2 - p1, p4 - p3, p1 - p3
        a, e, f = np.dot(d1, d1), np.dot(d2, d2), np.dot(d2, r)

        if a <= 1e-12 and e <= 1e-12:
            return float(np.linalg.norm(p1 - p3))
        if a <= 1e-12:
            s, t = 0.0, np.clip(f / e, 0.0, 1.0)
        else:
            c = np.dot(d1, r)
            if e <= 1e-12:
                t, s = 0.0, np.clip(-c / a, 0.0, 1.0)
            else:
                b = np.dot(d1, d2)
                denom = a * e - b * b
                s = np.clip((b * f - c * e) / denom, 0.0, 1.0) if abs(denom) > 1e-12 else 0.0
                t = (b * s + f) / e
                if t < 0.0:
                    t, s = 0.0, np.clip(-c / a, 0.0, 1.0)
                elif t > 1.0:
                    t, s = 1.0, np.clip((b - c) / a, 0.0, 1.0)

        closest1 = p1 + d1 * s
        closest2 = p3 + d2 * t
        return float(np.linalg.norm(closest1 - closest2))

    def check_CA1_or_2(self,regionNames,points,num_channels):
        if "Cornu ammonis 1" in regionNames:
            self.ui.pushButton_PyLdetection.setEnabled(True)

            minPixVal = 2e16
            pyrChIdx = 0
            dwi1Dsignal = np.zeros((num_channels,))

            for idx, point in enumerate(points):
                z, y, x = [int(c) for c in point]
                dwi1Dsignal[idx] = self.dwi[x, y, z]

                if regionNames[idx] == "Cornu ammonis 1":
                    if dwi1Dsignal[idx] < minPixVal:
                        minPixVal = dwi1Dsignal[idx]
                        pyrChIdx = idx

            plot_dwi_1D_cross_section(dwi1Dsignal,regionNames,pyrChIdx,num_channels,mplwidget=self.ui.tp_dwi1D_widget)
        else:
            self.ui.pushButton_PyLdetection.setEnabled(False)

    def show_canvas(self):
        if not hasattr(self, 'dwi_window'):
            self.dwi_window = QWidget()
            self.dwi_window.setWindowTitle("DWI 1D Cross Section")
            layout = QVBoxLayout(self.dwi_window)
            layout.addWidget(self.ui.tp_dwi1D_frame)

        self.dwi_window.show()
        self.dwi_window.raise_()

    # ------------------------------------------------------------------
    # Insertion-point refinement page (stackedWidget_trajectoryplanning
    # index 2, page_31) -- reached via pushButton_SaveTraj once every
    # shank has both a deepest and an insertion point from the page_6
    # workflow. That page_6 insertion point is an automatic guess (via
    # get_point_at_edge/edge_mask, now always the atlas's own brain-mask
    # outer border since skull segmentation is disconnected) -- this page
    # temporarily swaps the displayed volume back to the subject's own MRI
    # (the atlas has no skull at all) so the user can see the real skull
    # and correct it, by clicking directly along the shank's own fixed
    # trajectory line -- all done in native MRI voxel space (mri_deep/
    # mri_insert), converting back to an atlas-space equivalent
    # (coords_insert_point, via the approximate mri_to_atlas_via_lookup)
    # only for bookkeeping the rest of the app still reads.
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
        self.MW.overlay = BusyOverlay(self.MW, message="Loading MRI view, please wait…")
        self.MW.overlay.run(self._enter_insertion_refinement_page_continued)

    def _enter_insertion_refinement_page_continued(self):
        self._enter_mri_space_for_insertion()
        self._switch_insertion_shank_mri(0)

    def _enter_mri_space_for_insertion(self):
        """Swap the displayed volume from the atlas back to the subject's
        own resampled MRI working volume (the exact file movingImg_resampled
        was built from, and mri_deep/mri_insert are indexed against --
        NOT self.MW.data_pre_resampled, which is the original, non-resampled
        scan used elsewhere only for filename display) -- same restart_gui
        mechanism do_get_shank_line uses for the opposite direction.
        Destroys and rebuilds every 2D-view renderer/actor, so every
        atlas-space actor dict is reset here; _return_to_atlas_space (called
        once picking is done) does the same in reverse and redraws them
        properly."""
        self.MW.restart_gui(self._mri_working_volume_path, full_restart=False,
                             label_file=False, data_view='coronal')
        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.TrajPlanning = self
        self.LoadMRI.picking_insertion_point = True

        self.point_actor_bregma = {}
        self.point_actor_lambda = {}
        for shank_idx in self.coords_deepest_point:
            self.point_actor_deep[shank_idx] = {}
            self.point_actor_insert[shank_idx] = {}
            self.line_actor[shank_idx] = {}
            self.label_actor[shank_idx] = {}
        self._insertion_guide_actor = {}
        self._mri_marker_actor = {'deep': {}, 'insert': {}}

        # shank add/remove and the atlas-space combo/3D-view controls don't
        # make sense mid-refinement -- comboBox_insertion_shank/NEXT are the
        # only way to switch shanks while this page is up
        for w in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks,
                  self.ui.pushButton_addShank, self.ui.pushButton_removeShank,
                  self.ui.pushButton_coronalView, self.ui.pushButton_sagittalView,
                  self.ui.pushButton_axialView):
            w.setEnabled(False)

    def _return_to_atlas_space(self):
        """Swap the 2D-slice display back to the atlas once every shank's
        insertion point has been click-confirmed, and rebuild everything
        that was torn down entering MRI space (edge mask, atlas reference
        points, per-shank lines/channels) -- mirrors do_get_shank_line's
        own post-restart setup, minus the parts that are only valid to run
        once per session (signal connections, the one-time forbidden-
        region/skull-mask overlay reload, the insertion-step popup). Not
        needed for the PDF report itself -- see on_next_shank_clicked --
        only for continued interactive use of page_6/the 2D views."""
        path_main = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        self.MW.restart_gui(path_main, full_restart=False, label_file=True, data_view='coronal')
        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.TrajPlanning = self
        self.LoadMRI.picking_insertion_point = False
        self.tp_labels = self.LoadMRI.tp_labels
        self.update_voxel_spinbox_ranges()

        self.LoadMRI.tp_imgvtk = {}
        self.LoadMRI.tp_actor = {}
        self.LoadMRI.tp_renderer = {}
        self.create_edge_mask()
        self.draw_atlas_reference_points()

        self.point_actor_bregma = {}
        self.point_actor_lambda = {}
        for shank_idx in self.coords_deepest_point:
            self.point_actor_deep[shank_idx] = {}
            self.point_actor_insert[shank_idx] = {}
            self.line_actor[shank_idx] = {}
            self.label_actor[shank_idx] = {}
        self._insertion_guide_actor = {}
        self._mri_marker_actor = {'deep': {}, 'insert': {}}

        if not self._overlay_layers_reloaded:
            region_to_avoid_img = getattr(self, 'region_to_avoid_img', None)
            if region_to_avoid_img is not None:
                self.MW.FileLoader.layer_index += 1
                self.MW.FileLoader.initialize_file(region_to_avoid_img, self.MW.FileLoader.layer_index, 'coronal', 0)
            skull_mask_img = getattr(self, 'skull_mask_img', None)
            if skull_mask_img is not None:
                self.MW.FileLoader.layer_index += 1
                self.MW.FileLoader.initialize_file(
                    skull_mask_img, self.MW.FileLoader.layer_index, 'coronal', 0,
                    binary_color=(0.3, 0.3, 0.3), layer_label="Skull Mask", visibility_enabled=True)
            self._overlay_layers_reloaded = True

        # Vis3D itself is NOT rebuilt here -- its plotters live in their own
        # persistent widgets (vtkWidget_trajPlan_*), entirely separate from
        # LoadMRI.vtk_widgets/renderers (the ones restart_gui just tore down
        # and rebuilt above), and its own atlas meshes (background_small
        # etc.) were snapshotted once when it was first built -- it stays
        # perfectly valid across this whole atlas<->MRI round trip.
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
        # done refining -- land back on the main shank workspace instead of
        # leaving page_31's now-purposeless NEXT/Save-as-PDF controls up
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(1)

    def _switch_insertion_shank_mri(self, index):
        """comboBox_insertion_shank/NEXT's shank-switch handler while page_31
        is showing -- deliberately NOT select_shank (which assumes atlas
        space is displayed): syncs the other shank combos itself, flips the
        camera to this shank's current (native-MRI-space) insertion point,
        and redraws its markers/guide line."""
        self.shank_number = index
        for combo in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks,
                      self.ui.comboBox_insertion_shank):
            if combo.currentIndex() != index:
                combo.blockSignals(True)
                combo.setCurrentIndex(index)
                combo.blockSignals(False)

        insert = self.mri_insert.get(index)
        deep = self.mri_deep.get(index)
        if insert is not None:
            self.set_value(list(insert), self.ui.spinBox_insertion_x,
                            self.ui.spinBox_insertion_y, self.ui.spinBox_insertion_z)
            self._flip_cursor_to_point(insert)
        dist = 0.0
        if insert is not None and deep is not None:
            spacing = np.array(self.movingImg_resampled.GetSpacing())
            dist = float(np.linalg.norm((np.array(insert) - np.array(deep)) * spacing))
        self.ui.doubleSpinBox_distance_shank.setValue(dist)
        self.ui.spinBox_depth.setValue(dist)

        self._draw_insertion_guide_line_mri()
        self._refresh_next_shank_button()

    def _flip_cursor_to_point(self, point_xyz):
        """Jump the crosshair/cursor (all three 2D views) to an XYZ point in
        whichever volume is currently displayed -- the "camera flip" to
        wherever this shank's insertion point currently sits, so the user
        starts from a sensible reference instead of wherever they last
        happened to be looking. Also pans (without changing zoom) each
        view's camera to actually center on that point -- switching slice
        alone isn't enough if the view is zoomed in on a different spot,
        since the point could then land off-screen."""
        zyx = [int(round(c)) for c in reversed(list(point_xyz))]
        shape = self.LoadMRI.volumes[0].slices[0].shape
        zyx[0] = int(np.clip(zyx[0], 0, shape[0] - 1))
        zyx[1] = int(np.clip(zyx[1], 0, shape[1] - 1))
        zyx[2] = int(np.clip(zyx[2], 0, shape[2] - 1))
        self.LoadMRI.slice_indices[0] = zyx
        self.LoadMRI.update_slices(0, 'axial')  # also re-renders and refreshes point/line actors
        self.MW.Cursor.update_cursor_display(0)
        self.MW.Cursor.update_cursor_lines(0)

        for view_name in ('axial', 'coronal', 'sagittal'):
            renderer = self.LoadMRI.renderers[0][view_name]
            camera = renderer.GetActiveCamera()
            wx, wy = self._atlas_point_display_xy(point_xyz, view_name)
            old_fp = camera.GetFocalPoint()
            Zoom.recenter_camera_to_world_point(camera, (wx, wy, old_fp[2]))
            renderer.ResetCameraClippingRange()
        self.render()

    def _draw_insertion_guide_line_mri(self):
        """Dashed guide line (page_31 only), in the shank's own colour, from
        its deepest point out along its own fixed trajectory direction (in
        native MRI voxel space) to a bit past its current insertion point --
        the line pick_insertion_point_from_click constrains clicks to. Only
        the currently selected shank's guide/markers are shown at a time."""
        for actors in self._insertion_guide_actor.values():
            for view_name, actor in actors.items():
                self.LoadMRI.renderers[0][view_name].RemoveActor(actor)
        self._insertion_guide_actor = {}

        shank = self.shank_number
        deep = self.mri_deep.get(shank)
        insert = self.mri_insert.get(shank)
        if deep is None or insert is None:
            self.render()
            return

        deep_arr = np.array(deep, dtype=float)
        insert_arr = np.array(insert, dtype=float)
        seg = insert_arr - deep_arr
        base_t = float(np.linalg.norm(seg))
        direction = seg / base_t if base_t > 1e-9 else np.array([0.0, 0.0, 1.0])
        self._insertion_direction_mri[shank] = direction
        # extend a bit past the current insertion point so there's room to
        # click the true skull surface even if it sits slightly beyond
        # today's guess
        t_max = base_t * 1.3
        self._insertion_guide_t_max[shank] = t_max
        far_point = deep_arr + t_max * direction

        color = self.get_shank_vtk_color(shank)
        actors = {}
        for view_name in ('axial', 'sagittal', 'coronal'):
            p1 = self._atlas_point_display_xy(deep_arr, view_name)
            p2 = self._atlas_point_display_xy(far_point, view_name)
            actors[view_name] = self._draw_dotted_line(view_name, p1, p2, color=color)
        self._insertion_guide_actor[shank] = actors
        self._draw_mri_shank_markers()
        self.render()

    def _draw_mri_shank_markers(self):
        """Deep (green) / insert (red) point markers for the current shank
        on the MRI-space renderers -- self-contained (own actor dict)
        rather than reusing draw_point/point_actor_deep/point_actor_insert,
        since those track atlas-space markers and get reset/redrawn
        separately by _return_to_atlas_space."""
        for kind_actors in self._mri_marker_actor.values():
            for view_name, actor in kind_actors.items():
                self.LoadMRI.renderers[0][view_name].RemoveActor(actor)
        self._mri_marker_actor = {'deep': {}, 'insert': {}}

        shank = self.shank_number
        spacing = self.LoadMRI.volumes[0].spacing
        shape = self.LoadMRI.volumes[0].slices[0].shape
        for kind, color, point in (('deep', (0, 1, 0), self.mri_deep.get(shank)),
                                    ('insert', (1, 0, 0), self.mri_insert.get(shank))):
            if point is None:
                continue
            zyx = list(point)[::-1]
            for view_name in ('axial', 'sagittal', 'coronal'):
                if view_name == "axial":
                    center = [(shape[2]-1-zyx[2])*spacing[2], zyx[1]*spacing[1], 1.1]
                elif view_name == "coronal":
                    center = [(shape[2]-1-zyx[2])*spacing[2], zyx[0]*spacing[0], 1.1]
                else:
                    center = [(shape[1]-1-zyx[1])*spacing[1], zyx[0]*spacing[0], 1.1]

                polygon_source = vtkRegularPolygonSource()
                polygon_source.GeneratePolygonOn()
                polygon_source.SetNumberOfSides(100)
                polygon_source.SetRadius(0.1)
                polygon_source.SetCenter(center)
                mapper = vtkPolyDataMapper()
                mapper.SetInputConnection(polygon_source.GetOutputPort())
                actor = vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(*color)
                actor.GetProperty().SetOpacity(0.9)
                self.LoadMRI.renderers[0][view_name].AddActor(actor)
                self._mri_marker_actor[kind][view_name] = actor

    def pick_insertion_point_from_click(self):
        """Wired into CustomInteractorStyle.on_left_button_down
        (core/interactor_style.py) while LoadMRI.picking_insertion_point is
        True -- a plain click in any 2D view immediately sets this shank's
        insertion point, in native MRI voxel space, projected onto its own
        fixed trajectory line (mri_deep + the direction computed in
        _draw_insertion_guide_line_mri) instead of wherever was actually
        clicked, so the point can only ever slide along that line. The
        atlas-space equivalent (coords_insert_point) is recomputed via the
        approximate nearest-neighbour lookup so the rest of the app (region
        checks, PDF report) stays consistent."""
        shank = self.shank_number
        deep = self.mri_deep.get(shank)
        direction = self._insertion_direction_mri.get(shank)
        if deep is None or direction is None:
            return

        click_pt = np.array(self.LoadMRI.slice_indices[0][::-1], dtype=float)  # xyz, MRI voxel space
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
        self.coords_insert_point[shank] = [int(round(c)) for c in
                                            self.mri_to_atlas_via_lookup(self.mri_insert[shank])]

        self.set_value(list(self.mri_insert[shank]), self.ui.spinBox_insertion_x,
                        self.ui.spinBox_insertion_y, self.ui.spinBox_insertion_z)
        self._draw_mri_shank_markers()
        self.render()

        spacing = np.array(self.movingImg_resampled.GetSpacing())
        dist = float(np.linalg.norm((np.array(self.mri_insert[shank]) - np.array(self.mri_deep[shank])) * spacing))
        self.ui.doubleSpinBox_distance_shank.setValue(dist)
        self.ui.spinBox_depth.setValue(dist)

        # numeric-only while picking_insertion_point is True (see the guard
        # inside create_channel_list) -- keeps direction_atlas/channel_points
        # current for the PDF report without touching the (currently MRI-
        # displaying) atlas-space renderers
        self.create_channel_list()

        self._insertion_confirmed.add(shank)
        self._refresh_next_shank_button()

    def _refresh_next_shank_button(self):
        """pushButton_nextShank is dual-purpose: it cycles through shanks
        still awaiting a click-confirmed insertion point, then once every
        shank has one, relabels itself to trigger the actual PDF export
        (what pushButton_SaveTraj used to do directly)."""
        all_confirmed = (self.ui.comboBox_Shanks.count() > 0
                         and len(self._insertion_confirmed) >= self.ui.comboBox_Shanks.count())
        if all_confirmed:
            self.ui.pushButton_nextShank.setText("Save Trajectory \n as pdf")
        else:
            self.ui.pushButton_nextShank.setText("NEXT")

    def on_next_shank_clicked(self):
        count = self.ui.comboBox_Shanks.count()
        if count > 0 and len(self._insertion_confirmed) >= count:
            # The PDF report (capture_pages) needs neither the atlas 2D
            # display nor a rebuilt Vis3D -- its atlas-space panels already
            # come from Vis3D's own persistent, display-independent meshes/
            # plotters (see _return_to_atlas_space), and its MRI-space
            # panels come from dedicated off-screen plotters -- so open the
            # dialog immediately, still in MRI mode, instead of making the
            # user wait through a whole restart_gui round trip first just
            # to get to it. Swap back to the atlas afterward (needed for
            # continued interactive use of page_6/the 2D views, not for
            # this dialog) once the user is done with it either way.
            FileOutput(self.MW, self.MW.data_pre_resampled, parent=self.MW).exec()
            self.MW.overlay = BusyOverlay(self.MW, message="Returning to atlas view, please wait…")
            self.MW.overlay.run(self._return_to_atlas_space)
            return
        if count > 0:
            next_index = (self.shank_number + 1) % count
            self._switch_insertion_shank_mri(next_index)
