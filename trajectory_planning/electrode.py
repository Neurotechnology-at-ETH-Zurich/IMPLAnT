# This Python file uses the following encoding: utf-8
import numpy as np
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from utils.zoom import Zoom
from trajectory_planning.file_input_output import FileOutput
from gui_utils.busy_overlay import BusyOverlay

class ElecGeometry:
    def change_shank_parameters(self):
        if self.coords_deepest_point[self.shank_number] is not None and self.coords_insert_point[self.shank_number] is not None:
            self.create_channel_list()

        self.render()


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
    def _enter_insertion_refinement_page_continued(self):
        self._enter_mri_space_for_insertion()
        self._switch_insertion_shank_mri(0)

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

        # Same reasoning as select_shank's own call (shank.py): switching
        # shanks here (page_31, insertion refinement) changes which insert
        # point the oblique constraint view(s) should be anchored on --
        # hasattr-guarded since this method is inherited unchanged by the
        # plain (non-MRI) TrajectoryPlanning too, which has no oblique
        # views at all.
        if hasattr(self, '_refresh_oblique_views_for_insert'):
            self._refresh_oblique_views_for_insert(index)

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
