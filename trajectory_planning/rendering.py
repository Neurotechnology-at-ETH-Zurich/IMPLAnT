# This Python file uses the following encoding: utf-8
import numpy as np
import os
import nibabel as nib
import SimpleITK as sitk
import vtk
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from scipy import ndimage
import sys
from PySide6.QtCore import QTimer
from core.image_layer import ImageLayer
from paths_config import _paths
from mrid_utils import atlas_switch
from mrid_utils.atlas_registry import ATLASES, get_active_atlas_id
from trajectory_planning.visualisation3D import Visualisation3D

class Rendering:
    def render(self):
        for _,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                widget.GetRenderWindow().Render()

    def check_points_in_slice(self):
        # runs unconditionally on every cursor move (core/load_MRI_file.py's
        # update_slices) -- while the insertion-refinement page has swapped
        # the displayed volume to the subject's own MRI, coords_insert_point/
        # coords_deepest_point (atlas voxel coordinates) would get redrawn
        # onto that MRI-space renderer, at nonsensical positions.
        # pick_insertion_point_from_click/_draw_mri_shank_markers already
        # keep that page's own markers/guide line up to date.
        if getattr(self.LoadMRI, 'picking_insertion_point', False):
            return
        for view_name in 'axial','sagittal','coronal':
            renderer = self.LoadMRI.renderers[0][view_name]

            # hide deep/insert actors for all non-selected shanks
            for shank_idx in self.point_actor_deep:
                if shank_idx != self.shank_number:
                    if view_name in self.point_actor_deep[shank_idx]:
                        renderer.RemoveActor(self.point_actor_deep[shank_idx][view_name])
                    if view_name in self.point_actor_insert.get(shank_idx, {}):
                        renderer.RemoveActor(self.point_actor_insert[shank_idx][view_name])

            point_actors = [self.point_actor_bregma,self.point_actor_lambda,self.point_actor_insert[self.shank_number],self.point_actor_deep[self.shank_number]]
            coordinates =  [self.coords_bregma,self.coords_lambda,self.coords_insert_point[self.shank_number],self.coords_deepest_point[self.shank_number]]

            for point_actor, coordinate in zip(point_actors,coordinates):
                if coordinate is None:
                    continue
                coordinate = coordinate[::-1]
                if view_name in point_actor:
                    renderer.RemoveActor(point_actor[view_name])
                    if view_name=='axial':
                        if coordinate[0] == self.LoadMRI.slice_indices[0][0]:
                            renderer.AddActor(point_actor[view_name])
                    elif view_name=='sagittal':
                        if coordinate[2] == self.LoadMRI.slice_indices[0][2]:
                            renderer.AddActor(point_actor[view_name])
                    elif view_name=='coronal':
                        if coordinate[1] == self.LoadMRI.slice_indices[0][1]:
                            renderer.AddActor(point_actor[view_name])

            if self.atlas_shank_end[self.shank_number] is not None and self.coords_deepest_point[self.shank_number] is not None:
                if view_name in self.line_actor[self.shank_number]:
                    for a in self.line_actor[self.shank_number][view_name]:
                        self.LoadMRI.renderers[0][view_name].RemoveActor(a)
                    self.LoadMRI.renderers[0][view_name].RemoveActor(self.label_actor[self.shank_number][view_name])
                self.line_actor[self.shank_number][view_name], self.label_actor[self.shank_number][view_name] = self.draw_electrode_line(view_name, self.coords_deepest_point[self.shank_number], self.atlas_shank_end[self.shank_number], color=self.get_shank_vtk_color(self.shank_number))
                for a in self.line_actor[self.shank_number][view_name]:
                    self.LoadMRI.renderers[0][view_name].AddActor(a)
                self.LoadMRI.renderers[0][view_name].AddActor(self.label_actor[self.shank_number][view_name])



    def _set_bregma_lambda_visible(self, visible):
        """Toggle the Step 1 bregma/lambda markers (picked on the animal's
        own MRI, drawn by draw_point) -- used to hide them once the user
        moves on to painting forbidden areas, since they're just clutter
        at that point and the atlas isn't loaded yet anyway."""
        for actor_dict in (self.point_actor_bregma, self.point_actor_lambda):
            for actor in actor_dict.values():
                actor.SetVisibility(visible)
        self.render()

    def draw_point(self,point,color,label,radius=0.1):
        spacing = self.LoadMRI.volumes[0].spacing
        shape = self.LoadMRI.volumes[0].slices[0].shape
        point = point[::-1]  # xyz -> zyx once before loop
        for view_name in 'axial','sagittal','coronal':
            renderer = self.LoadMRI.renderers[0][view_name]

            if label == 'bregma' and view_name in self.point_actor_bregma:
                renderer.RemoveActor(self.point_actor_bregma[view_name])
            elif label == 'lambda' and view_name in self.point_actor_lambda:
                renderer.RemoveActor(self.point_actor_lambda[view_name])
            elif label == 'deep' and view_name in self.point_actor_deep[self.shank_number]:
                renderer.RemoveActor(self.point_actor_deep[self.shank_number][view_name])
            elif label == 'insert' and view_name in self.point_actor_insert[self.shank_number]:
                renderer.RemoveActor(self.point_actor_insert[self.shank_number][view_name])
            elif not label == 'bregma' and not label == 'lambda' and not label == 'deep' and not label == 'insert':
                if label in self.point_actor_channels[view_name]:
                    renderer.RemoveActor(self.point_actor_channels[view_name][label])

            if view_name == "axial":      # z fixed -> (x,y)
                center = [(shape[2]-1-point[2])*spacing[2],point[1]*spacing[1],1.1]
            elif view_name == "coronal": # y fixed -> (z,x)
                center = [(shape[2]-1-point[2])*spacing[2],point[0]*spacing[0],1.1]
            elif view_name == "sagittal":# x fixed -> (y,z)
                center = [(shape[1]-1-point[1])*spacing[1],point[0]*spacing[0],1.1]

            polygonSource = vtkRegularPolygonSource()
            polygonSource.GeneratePolygonOn()
            polygonSource.SetNumberOfSides(100)
            polygonSource.SetRadius(radius)
            polygonSource.SetCenter(center)

            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(polygonSource.GetOutputPort())

            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*color)
            actor.GetProperty().SetOpacity(0.9)

            renderer.AddActor(actor)
            if label == 'bregma':
                self.point_actor_bregma[view_name] = actor
            elif label == 'lambda':
                self.point_actor_lambda[view_name] = actor
            elif label == 'insert':
                self.point_actor_insert[self.shank_number][view_name] = actor
            elif label == 'deep':
                self.point_actor_deep[self.shank_number][view_name] = actor
            else:
                self.point_actor_channels[view_name][label] = actor

        self.check_points_in_slice()


    def _atlas_point_display_xy(self, point_xyz, view_name):
        """In-plane (x_display, y_display) for an atlas-space XYZ point in
        the given 2D view, using the same projection as draw_point()."""
        spacing = self.LoadMRI.volumes[0].spacing
        shape = self.LoadMRI.volumes[0].slices[0].shape
        point = list(point_xyz)[::-1]  # xyz -> zyx
        if view_name == "axial":     # z fixed -> (x,y)
            return (shape[2]-1-point[2])*spacing[2], point[1]*spacing[1]
        elif view_name == "coronal":   # y fixed -> (z,x)
            return (shape[2]-1-point[2])*spacing[2], point[0]*spacing[0]
        else:                        # sagittal, x fixed -> (y,z)
            return (shape[1]-1-point[1])*spacing[1], point[0]*spacing[0]

    def _draw_dotted_line(self, view_name, p1_xy, p2_xy, color=(1, 1, 0), height=1.05):
        renderer = self.LoadMRI.renderers[0][view_name]
        line = vtk.vtkLineSource()
        line.SetPoint1(p1_xy[0], p1_xy[1], height)
        line.SetPoint2(p2_xy[0], p2_xy[1], height)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetLineWidth(1)
        actor.GetProperty().SetLineStipplePattern(0xF0F0)  # dashed, same pattern as core/measurement.py
        actor.GetProperty().SetLineStippleRepeatFactor(10)
        renderer.AddActor(actor)
        return actor

    def _draw_atlas_marker(self, view_name, point_xyz, color):
        renderer = self.LoadMRI.renderers[0][view_name]
        cx, cy = self._atlas_point_display_xy(point_xyz, view_name)

        polygonSource = vtkRegularPolygonSource()
        polygonSource.GeneratePolygonOn()
        polygonSource.SetNumberOfSides(100)
        polygonSource.SetRadius(0.1)
        polygonSource.SetCenter([cx, cy, 1.1])

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(polygonSource.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetOpacity(0.9)
        renderer.AddActor(actor)
        return actor

    def _draw_atlas_point_label(self, view_name, point_xyz, label_text, color):
        """Small text tag (e.g. 'B'/'L') anchored at the marker's own world
        position, offset slightly so it doesn't sit on top of the dot."""
        renderer = self.LoadMRI.renderers[0][view_name]
        cx, cy = self._atlas_point_display_xy(point_xyz, view_name)
        text = vtk.vtkTextActor()
        text.SetInput(label_text)
        text.GetTextProperty().SetColor(*color)
        text.GetTextProperty().SetFontSize(11)
        text.GetTextProperty().BoldOn()
        text.GetPositionCoordinate().SetCoordinateSystemToWorld()
        text.GetPositionCoordinate().SetValue(cx + 0.15, cy + 0.15, 1.1)
        renderer.AddActor(text)
        return text

    def _draw_legend_text(self, view_name, legend_text, color, legend_y):
        renderer = self.LoadMRI.renderers[0][view_name]
        text = vtk.vtkTextActor()
        text.SetInput(legend_text)
        text.GetTextProperty().SetColor(*color)
        text.GetTextProperty().SetFontSize(14)
        text.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
        text.GetPositionCoordinate().SetValue(0.02, legend_y)
        renderer.AddActor2D(text)
        return text

    def draw_atlas_reference_points(self):
        """Fixed atlas bregma/lambda (the hardcoded registration reference
        points, not the ones the user picks on the animal's own MRI) as
        persistent yellow markers plus a colour legend, shown on every
        2D slice once the atlas becomes the active volume for the
        insertion/deepest-point step. Unlike draw_point()'s bregma/lambda,
        these aren't tied to one particular slice (check_points_in_slice
        doesn't know about them), since they're a fixed anatomical
        reference rather than something picked on a specific slice.

        Also draws:
        - sagittal: a dotted bregma-lambda reference line (the classic
          stereotaxic AP tilt reference), used by update_shank_angle_display
          to report the angle between it and the selected shank.
        - coronal: the centroid of every atlas voxel labelled corpus
          callosum (index 67) as a third point, joined to bregma by a
          dotted reference line.
        """
        self.atlas_ref_actor = {}
        self.atlas_ref_actor['bregma'] = {
            vn: self._draw_atlas_marker(vn, self.atlas_bregma_coords, (1, 1, 0))
            for vn in ('sagittal', 'coronal')
        }
        self.atlas_ref_actor['lambda'] = {
            vn: self._draw_atlas_marker(vn, self.atlas_lambda_coords, (1, 1, 0))
            for vn in ('sagittal', 'coronal')
        }
        self.atlas_ref_label = {
            'bregma': {
                vn: self._draw_atlas_point_label(vn, self.atlas_bregma_coords, "B", (1, 1, 0))
                for vn in ('sagittal', 'coronal')
            },
            'lambda': {
                vn: self._draw_atlas_point_label(vn, self.atlas_lambda_coords, "L", (1, 1, 0))
                for vn in ('sagittal', 'coronal')
            },
        }
        # one legend entry for the pair, not one per point
        for vn in ('sagittal', 'coronal'):
            self._draw_legend_text(vn, "— Atlas Bregma-Lambda", (1, 1, 0), 0.95)

        self.atlas_bl_line_actor = self._draw_dotted_line(
            'sagittal',
            self._atlas_point_display_xy(self.atlas_bregma_coords, 'sagittal'),
            self._atlas_point_display_xy(self.atlas_lambda_coords, 'sagittal'),
            color=(1, 1, 0))

        self.atlas_plane_actors = {}
        # bregma/lambda/cc are all the same kind of value here: MRI-derived,
        # warped into atlas space purely for this display (get_cc_mri_mean
        # forward-transforms the atlas's own CC voxels into this subject's
        # MRI space, averages, then converts that mean back to atlas space
        # via the same lookup as bregma/lambda -- not the atlas's own native
        # CC centroid computed directly from atlas_vol).
        self.atlas_cc_centroid = tuple(self.get_cc_mri_mean())
        self.atlas_ref_actor['corpus_callosum'] = {
            'coronal': self._draw_atlas_marker('coronal', self.atlas_cc_centroid, (1, 1, 0))
        }
        self._draw_legend_text('coronal', "● Corpus Callosum", (1, 1, 0), 0.90)
        # coronal's reference line is the bregma-lambda-CC PLANE's own
        # crossing of the current coronal slice (update_atlas_plane_line/
        # update_coronal_plane_line), not a naive bregma-CC chord -- a
        # straight line between just two of the three points defining
        # the plane isn't the plane's cross-section at all. That
        # function used to bail until a shank existed (see the removed
        # guard in update_atlas_plane_line); now it draws immediately,
        # same as sagittal's bregma-lambda line above.
        self.update_coronal_plane_line()

        self.render()

    def _ensure_atlas_selector_widget(self):
        """Populates and wires form.ui's own comboBox_atlas (page_30,
        self.ui.frame / self.ui.gridLayout_177, next to its lineEdit_83
        "Atlas" label) the first time this page is shown, letting the user
        switch atlases while looking at one (see reload_atlas_view) --
        reads that real, hand-placed widget instead of creating/inserting a
        new combo into the same grid layout at runtime, which collided
        with the already-placed pushButton_sagittalView/coronalView."""
        if hasattr(self.ui, '_atlas_selector_wired'):
            self._atlas_ids = list(ATLASES.keys())
            self._sync_atlas_selector_widget()
            return
        self.ui._atlas_selector_wired = True
        self._atlas_ids = list(ATLASES.keys())
        for atlas_id in self._atlas_ids:
            self.ui.comboBox_atlas.addItem(ATLASES[atlas_id]['display_name'])
        self._sync_atlas_selector_widget()
        self.ui.comboBox_atlas.currentIndexChanged.connect(self._on_atlas_selector_changed)

    def _sync_atlas_selector_widget(self):
        current_id = get_active_atlas_id(_paths)
        if current_id in self._atlas_ids:
            self.ui.comboBox_atlas.blockSignals(True)
            self.ui.comboBox_atlas.setCurrentIndex(self._atlas_ids.index(current_id))
            self.ui.comboBox_atlas.blockSignals(False)

    def _on_atlas_selector_changed(self, index):
        atlas_id = self._atlas_ids[index]
        if atlas_id == get_active_atlas_id(_paths):
            return
        if not self.reload_atlas_view(atlas_id):
            self._sync_atlas_selector_widget()  # switch declined/failed -- revert the combo

    def reload_atlas_view(self, atlas_id):
        """Switches to atlas_id and redraws this already-open atlas view in
        place -- replays the atlas-loading portion of
        TpRegistration.do_get_shank_line against the newly selected atlas
        instead of a full re-entry into trajectory planning. Returns False
        (leaving the previous atlas showing) if the user cancels the fetch
        or it fails."""
        if not atlas_switch.switch_active_atlas(atlas_id, self.MW):
            return False

        current_view = getattr(self.LoadMRI, 'data_view', 'coronal')
        path_main = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        self.MW.restart_gui(path_main, full_restart=False, label_file=True, data_view=current_view)
        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.TrajPlanning = self
        self.tp_labels = self.LoadMRI.tp_labels
        self.update_voxel_spinbox_ranges()

        # unlike the initial load, always rebuild -- the new atlas's
        # geometry/labels differ from whatever tg_edge_mask was built from
        self.LoadMRI.tp_imgvtk = {}
        self.LoadMRI.tp_actor = {}
        self.LoadMRI.tp_renderer = {}
        self.create_edge_mask()

        # re-anchor the atlas<->MRI coordinate machinery (coord_transform.py)
        # against the new atlas volume -- same call trajectory_planning.py's
        # __init__ made initially, reusing the same (unaffected -- both
        # atlases share one coordinate grid) registration transform. The
        # dense lookup table and corpus-callosum-mean caches built on top of
        # it are now stale and must be dropped, not just their inputs
        # refreshed, since they're only ever (re)built lazily via hasattr
        # guards.
        self.movingidx_bregma, self.movingidx_lambda, _ = self.get_atlas_coords(
            self.LoadMRI.volumes[0], self.transform_path)
        for stale_attr in ('_bl_lookup_atlas', '_bl_lookup_mri', '_bl_lookup_tree',
                           '_bl_lookup_stride', '_bl_lookup_grid_shape',
                           '_bl_lookup_mri_grid', '_bl_lookup_interpolator',
                           '_cc_mean_mri', '_cc_mean_atlas',
                           '_mri_not_background_mask', '_mri_not_background_mask_key'):
            if hasattr(self, stale_attr):
                delattr(self, stale_attr)

        self.Vis3D = Visualisation3D(self.MW)

        if hasattr(self, 'dwi'):
            del self.dwi
        if _paths.get('atlas_dwi'):
            dwi_path = os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
            nii_dwi = nib.load(dwi_path)
            dwi = np.asanyarray(nii_dwi.dataobj)
            self.dwi = dwi[:, :, :, 0]

        self.draw_atlas_reference_points()
        self._sync_atlas_selector_widget()
        QTimer.singleShot(0, self.render)
        return True

    def _atlas_plane_normal_and_point(self):
        """Normal (unit vector) and a point (both in physical mm) of the
        plane through atlas bregma, lambda and the corpus-callosum
        centroid -- three non-collinear points needed since bregma/lambda
        alone only fix a line, not a plane."""
        spacing = np.array(self.fixedImg.GetSpacing())
        b = np.array(self.atlas_bregma_coords) * spacing
        l = np.array(self.atlas_lambda_coords) * spacing
        c = np.array(self.atlas_cc_centroid) * spacing
        normal = np.cross(l - b, c - b)
        norm = np.linalg.norm(normal)
        if norm < 1e-9:
            return None, None
        return normal / norm, b

    def _atlas_plane_segment(self, normal, plane_point, fixed_idx, fixed_voxel,
                              free_a_idx, free_b_idx, extent_a, extent_b):
        """Voxel-space XYZ endpoints of the atlas plane's FULL crossing of
        the slice fixed at axis fixed_idx = fixed_voxel -- clipped to the
        actual image rectangle [0,extent_a-1] x [0,extent_b-1], so the
        line spans edge-to-edge across the atlas instead of a short dash
        near the center. Standard line-vs-rectangle clipping: solve the
        line equation coef_a*a + coef_b*b = k against each of the four
        rectangle edges, keep whichever intersections actually land within
        the rectangle -- there are exactly two whenever the line crosses
        it at all (a plane parallel to this slice, or one that just
        doesn't reach it, has none/one)."""
        spacing = np.array(self.fixedImg.GetSpacing())  # xyz
        d = np.dot(normal, plane_point)  # normal.P = d for any P on the plane
        k = d - normal[fixed_idx] * (fixed_voxel * spacing[fixed_idx])
        coef_a = normal[free_a_idx] * spacing[free_a_idx]
        coef_b = normal[free_b_idx] * spacing[free_b_idx]
        if max(abs(coef_a), abs(coef_b)) < 1e-9:
            return None  # plane is ~parallel to this slice -- no single crossing line

        max_a, max_b = extent_a - 1, extent_b - 1
        eps = 1e-6
        candidates = []
        if abs(coef_b) > 1e-9:
            for a in (0.0, max_a):
                b = (k - coef_a * a) / coef_b
                if -eps <= b <= max_b + eps:
                    candidates.append((a, min(max(b, 0.0), max_b)))
        if abs(coef_a) > 1e-9:
            for b in (0.0, max_b):
                a = (k - coef_b * b) / coef_a
                if -eps <= a <= max_a + eps:
                    candidates.append((min(max(a, 0.0), max_a), b))

        # dedupe near-identical points (the line passing exactly through a
        # corner hits two edges at once)
        uniq = []
        for pt in candidates:
            if not any(abs(pt[0] - u[0]) < eps and abs(pt[1] - u[1]) < eps for u in uniq):
                uniq.append(pt)
        if len(uniq) < 2:
            return None  # doesn't cross this slice's rectangle at all

        # >2 candidates only happens right at/near a corner -- the two
        # farthest-apart points are the true entry/exit through the rectangle
        best_pair, best_dist = None, -1
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                dist = np.hypot(uniq[i][0] - uniq[j][0], uniq[i][1] - uniq[j][1])
                if dist > best_dist:
                    best_dist, best_pair = dist, (uniq[i], uniq[j])

        endpoints = []
        for a, b in best_pair:
            p = [0.0, 0.0, 0.0]
            p[fixed_idx], p[free_a_idx], p[free_b_idx] = fixed_voxel, a, b
            endpoints.append(tuple(p))
        return endpoints

    def _atlas_plane_segment_in_view(self, view_name, normal, plane_point):
        """Voxel-space XYZ endpoints of the atlas bregma/lambda/CC plane's
        crossing of the CURRENTLY DISPLAYED slice for view_name (None if it
        doesn't cross). Shared by update_atlas_plane_line (the "Atlas
        plane" caption/arc) and update_shank_angle_display, which uses this
        same crossing as the coronal reference direction -- the raw
        bregma-lambda vector is ~degenerate there since bregma/lambda
        differ almost entirely along the AP axis, which coronal flattens
        out."""
        shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx
        # coronal: Y fixed, X/Z free (voxel-axis indices 0/2 in XYZ).
        # sagittal: X fixed, Y/Z free (voxel-axis indices 1/2 in XYZ).
        if view_name == 'coronal':
            fixed_idx, free_a_idx, free_b_idx = 1, 0, 2
            fixed_voxel = self.LoadMRI.slice_indices[0][1]
            extent_a, extent_b = shape[2], shape[0]
        else:
            fixed_idx, free_a_idx, free_b_idx = 0, 1, 2
            fixed_voxel = self.LoadMRI.slice_indices[0][2]
            extent_a, extent_b = shape[1], shape[0]
        return self._atlas_plane_segment(normal, plane_point, fixed_idx, fixed_voxel,
                                          free_a_idx, free_b_idx, extent_a, extent_b)

    def update_coronal_plane_line(self):
        """Refresh the atlas-plane tilt indicator -- coronal only. Sagittal
        already has its own plain bregma-lambda line (atlas_bl_line_actor,
        drawn once in draw_atlas_reference_points); calling
        update_atlas_plane_line('sagittal') too used to draw a SECOND,
        separate line there (the plane's crossing of the current sagittal
        slice), overlapping/duplicating the first."""
        self.update_atlas_plane_line('coronal')

    def update_atlas_plane_line(self, view_name):
        """Where the plane through atlas bregma/lambda/corpus-callosum
        crosses the CURRENTLY DISPLAYED coronal or sagittal slice -- a true
        3D-plane intersection, not a naive point-to-point projection (which
        would wrongly conflate the AP separation between bregma and the
        different-Y corpus-callosum centroid into an apparent DV/ML tilt).
        Drawn as a short dotted line (a tenth of the slice's in-plane
        extent) plus a white angle caption and arc showing its tilt off
        the horizontal (true-cut) direction. Since the intersection
        depends on which slice is showing, this needs to be called again
        whenever that slice changes (see LoadMRI.update_slices)."""
        if not hasattr(self, 'atlas_plane_actors'):
            self.atlas_plane_actors = {}
        actors = self.atlas_plane_actors.setdefault(view_name, {'line': None, 'text': None})
        if not hasattr(self, 'LoadMRI') or view_name not in self.LoadMRI.renderers.get(0, {}):
            return
        # atlas bregma/lambda and this plane indicator only belong on the
        # final (post-restart, atlas-space) insertion/deepest-point step --
        # not while still on the subject's own MRI (bregma/lambda picking,
        # forbidden-areas painting), which stays on
        # stackedWidget_trajectoryplanning page 0.
        if self.ui.stackedWidget_trajectoryplanning.currentIndex() != 1:
            renderer = self.LoadMRI.renderers[0][view_name]
            for key in ('line', 'text'):
                old = actors[key]
                if old is not None:
                    renderer.RemoveActor(old)
                    actors[key] = None
            return
        if getattr(self, 'atlas_cc_centroid', None) is None:
            return
        normal, plane_point = self._atlas_plane_normal_and_point()
        renderer = self.LoadMRI.renderers[0][view_name]
        for key in ('line', 'text'):
            old = actors[key]
            if old is not None:
                renderer.RemoveActor(old)
                actors[key] = None
        if normal is None:
            return

        segment = self._atlas_plane_segment_in_view(view_name, normal, plane_point)
        if segment is None:
            return  # this plane barely crosses this particular slice at all
        p1_xyz, p2_xyz = segment

        p1_xy = self._atlas_point_display_xy(p1_xyz, view_name)
        p2_xy = self._atlas_point_display_xy(p2_xyz, view_name)


        actors['line'] = self._draw_dotted_line(view_name, p1_xy, p2_xy)
        self.render()

    def update_shank_angle_display(self):
        """Angle between the currently selected shank's insert-deep line and
        the atlas stereotaxic reference, shown on BOTH the sagittal and
        coronal views (previously sagittal-only -- see
        _update_shank_angle_display_view for per-view details). Call after
        the shank line changes (create_channel_list) or the selected shank
        changes (select_shank)."""
        for view_name in ('sagittal', 'coronal'):
            self._update_shank_angle_display_view(view_name)

    def compute_shank_reference_angle(self, view_name, shank_number=None):
        """Angle (0-180 deg) between the given shank's (defaults to the
        currently selected shank, self.shank_number, if not passed)
        deep->insert line and the atlas stereotaxic reference in
        view_name, plus the raw vectors/frame info needed to draw it --
        shared by the 2D caption/arc (_update_shank_angle_display_view)
        and its 3D counterpart (visualisation3D's _draw_shank_angle_
        indicator) so this math exists in exactly one place. The explicit
        shank_number lets the PDF-report export compute each shank's own
        angle while looping over shanks other than the one currently
        selected in the GUI -- without it every exported page silently
        showed the angle of whichever shank happened to be selected when
        the export button was clicked, not the shank actually captured.

        Sagittal reference = the true 3D bregma-lambda vector, projected
        into the sagittal (y, z) plane -- well-resolved there, since
        bregma/lambda differ mostly along those two axes.
        Coronal reference = the atlas bregma-lambda-CC plane's own
        crossing of the CURRENTLY DISPLAYED coronal slice (the same line
        update_atlas_plane_line draws, via _atlas_plane_segment_in_view) --
        the raw bregma-lambda vector is unusable here since bregma/lambda
        differ almost entirely along the AP axis, which coronal flattens
        to ~zero length. That crossing's direction is oriented to agree in
        sign with the (tiny but non-zero) coronal-projected bregma-lambda
        vector, so "toward lambda" means the same thing in both views.

        ref_2d and shank_2d are both returned in the same raw/unflipped
        mm-diff frame (NOT this view's mirrored display frame) -- callers
        needing display-space vectors/points must apply their own flip.

        The angle is always the raw angle (0-180 deg) between these two
        CONSISTENTLY oriented vectors -- deliberately NOT folded to the
        acute angle, since folding makes e.g. a 170 deg and a 10 deg tilt
        display the same number with no way to tell which side the shank
        actually leans toward. Returns None if not computable (no shank/
        bregma/lambda/CC yet, or degenerate vectors)."""
        if shank_number is None:
            shank_number = self.shank_number
        insert = self.coords_insert_point.get(shank_number)
        deep = self.coords_deepest_point.get(shank_number)
        if insert is None or deep is None or getattr(self, 'atlas_bregma_coords', None) is None:
            return None

        spacing = np.array(self.fixedImg.GetSpacing())
        proj = (1, 2) if view_name == 'sagittal' else (0, 2)
        deep_vox = np.array(deep, dtype=float)

        # if the shank's first electrode contact sits exactly on the marked
        # deepest point, use the last electrode contact as the insertion
        # point for the angle/arc instead of the marked insertion point --
        # the angle should reflect the shank's real physical extent, not
        # just where the user happened to click.
        insert_vox = np.array(insert, dtype=float)
        channel_points = self.channel_points.get(shank_number)
        if channel_points is not None and len(channel_points) > 0:
            first_electrode_vox = np.array(channel_points[0], dtype=float)
            if np.allclose(first_electrode_vox, deep_vox):
                insert_vox = np.array(channel_points[-1], dtype=float)
        bl_vec = (np.array(self.atlas_lambda_coords) - np.array(self.atlas_bregma_coords)) * spacing
        shank_vec = (insert_vox - deep_vox) * spacing
        shank_2d = shank_vec[list(proj)]  # raw/unflipped mm-diff frame

        if view_name == 'sagittal':
            ref_2d = bl_vec[list(proj)]  # same raw/unflipped frame as shank_2d
            ref_point_vox = np.array(self.atlas_bregma_coords, dtype=float)  # a point ON the reference line
        else:
            ref_2d = None
            ref_point_vox = None
            if getattr(self, 'atlas_cc_centroid', None) is not None:
                normal, plane_point = self._atlas_plane_normal_and_point()
                if normal is not None:
                    segment = self._atlas_plane_segment_in_view(view_name, normal, plane_point)
                    if segment is not None:
                        # raw voxel-diff*spacing, matching shank_2d's frame --
                        # NOT _atlas_point_display_xy, which bakes in this
                        # view's display flip and would silently mix frames
                        # with shank_2d/bl_2d (mirrored vs. not), corrupting
                        # both the angle and the arc drawn from it
                        seg_vec = (np.array(segment[1]) - np.array(segment[0])) * spacing
                        ref_2d = seg_vec[list(proj)]
                        ref_point_vox = np.array(segment[0], dtype=float)  # a point ON the reference line
                        bl_2d = bl_vec[list(proj)]
                        if np.linalg.norm(bl_2d) > 1e-9 and np.dot(ref_2d, bl_2d) < 0:
                            ref_2d = -ref_2d  # keep "toward lambda" the same sign in both views
            if ref_2d is None:
                return None

        denom = np.linalg.norm(ref_2d) * np.linalg.norm(shank_2d)
        if denom == 0:
            return None
        cos_theta = np.clip(np.dot(ref_2d, shank_2d) / denom, -1, 1)
        angle = np.degrees(np.arccos(cos_theta))
        if view_name == 'sagittal':
            # bregma->lambda vs. deep->insert, as computed above, comes out
            # as the supplement of the angle that actually matches what's
            # shown on screen -- take the other side of the same straight
            # line (still the full 0-180 range, so still not the acute-fold
            # ambiguity this whole computation was written to avoid).
            angle = 180 - angle

        # The angle actually DISPLAYED/labelled is the MRI-space roll/pitch
        # (shank's angle to the bregma-lambda-CC-anchored planes -- same
        # source as the PDF report, see compute_shank_roll_pitch_mri),
        # not the atlas-space angle just computed above: insertion happens
        # into the real animal, not the atlas, and the nonlinear SyN
        # registration between the two spaces does not preserve angles, so
        # the atlas-space number would not match the physically meaningful
        # one. ref_2d/shank_2d/deep_vox/insert_vox/ref_point_vox stay in
        # atlas-voxel terms below regardless, since those still drive the
        # arc/line actually drawn onto this (atlas-space) view.
        roll_pitch = self.compute_shank_roll_pitch_mri(shank_number)
        if roll_pitch is not None:
            angle = roll_pitch[1] if view_name == 'sagittal' else roll_pitch[0]

        return {
            'angle': angle, 'proj': proj, 'spacing': spacing,
            'ref_2d': ref_2d, 'shank_2d': shank_2d,
            'deep_vox': deep_vox, 'insert_vox': insert_vox,
            'ref_point_vox': ref_point_vox,
        }

    @staticmethod
    def _line_intersection_2d(p1, d1, p2, d2):
        """2D point where line (p1 + t*d1) crosses line (p2 + s*d2), or
        None if they're ~parallel (no unique crossing)."""
        denom = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(denom) < 1e-9:
            return None
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / denom
        return p1 + t * d1

    def _update_shank_angle_display_view(self, view_name):
        """Caption anchored near the shank's own insert end in view_name
        (same world-space-attachment technique as draw_electrode_line's
        shank label) -- i.e. inside the brain, next to the shank itself,
        near the skull-surface end where the reference line it's measured
        against actually is, not a fixed-corner screen overlay and not the
        shank's plain midpoint (which can sit far from that reference with
        no visible relation to what the angle is comparing against). Angle
        math lives in compute_shank_reference_angle; this just draws it."""
        if not hasattr(self, 'LoadMRI') or view_name not in self.LoadMRI.renderers.get(0, {}):
            return
        renderer = self.LoadMRI.renderers[0][view_name]
        if not hasattr(self, 'shank_angle_text_actors'):
            self.shank_angle_text_actors = {}
        if not hasattr(self, 'shank_angle_arc_actors'):
            self.shank_angle_arc_actors = {}
        old_actor = self.shank_angle_text_actors.get(view_name)
        if old_actor is not None:
            renderer.RemoveActor(old_actor)
            self.shank_angle_text_actors[view_name] = None
        old_arc = self.shank_angle_arc_actors.get(view_name)
        if old_arc is not None:
            renderer.RemoveActor(old_arc)
            self.shank_angle_arc_actors[view_name] = None

        result = self.compute_shank_reference_angle(view_name)
        if result is None:
            self.render()
            return
        angle, proj, spacing = result['angle'], result['proj'], result['spacing']
        ref_2d, shank_2d = result['ref_2d'], result['shank_2d']
        deep_vox, insert_vox = result['deep_vox'], result['insert_vox']
        ref_point_vox = result['ref_point_vox']
        flip_axis = proj[0]  # this view's mirrored display axis: Y for sagittal, X for coronal

        # display-space deep/insert points (this view's mirrored axis
        # flipped), using the exact same projection draw_electrode_line
        # uses for its own label
        shape = np.array(self.fixedImg.GetSize())  # xyz
        a, b = deep_vox.copy(), insert_vox.copy()
        a[flip_axis] = shape[flip_axis] - 1 - a[flip_axis]
        b[flip_axis] = shape[flip_axis] - 1 - b[flip_axis]
        anchor = a + 0.5 * (b - a)
        pos = (anchor * spacing)[list(proj)]  # fallback if the arc can't be computed below
        deep_disp = (a * spacing)[list(proj)]
        insert_disp = (b * spacing)[list(proj)]

        # arc centered where the shank line actually CROSSES the reference
        # line (not at the deepest point -- that sits ON the shank line but
        # generally nowhere near the reference line, so an arc centered
        # there doesn't visually connect to either line). Both direction
        # vectors get the same single-axis sign flip into this view's
        # mirrored display frame -- that leaves the angle between them
        # unchanged (dot product is invariant under a consistent flip).
        flip = np.array([-1.0, 1.0])
        shank_dir, ref_dir = shank_2d * flip, ref_2d * flip
        shank_norm, ref_norm = np.linalg.norm(shank_dir), np.linalg.norm(ref_dir)
        view_angle = None  # this view's own (atlas-space) angle, set below if computable
        if shank_norm > 1e-9 and ref_norm > 1e-9 and ref_point_vox is not None:
            shank_dir, ref_dir = shank_dir / shank_norm, ref_dir / ref_norm
            if view_name == 'sagittal':
                # compute_shank_reference_angle reports 180-minus-the-raw
                # angle between ref_2d/shank_2d for sagittal (see its
                # docstring); keep ref_dir consistent with that supplement.
                ref_dir = -ref_dir

            ref_point = ref_point_vox.copy()
            ref_point[flip_axis] = shape[flip_axis] - 1 - ref_point[flip_axis]
            ref_point_disp = (ref_point * spacing)[list(proj)]

            arc_center = self._line_intersection_2d(deep_disp, shank_dir, ref_point_disp, ref_dir)
            if arc_center is None:
                arc_center = deep_disp  # lines ~parallel -- no real crossing, fall back

            # Point1 = i - (i-d)/2 = (i+d)/2, where i = vector from
            # arc_center to the insertion point and d = vector from
            # arc_center to the deepest point -- i.e. arc_center's vector
            # straight to the midpoint between insertion and deepest point
            # (equivalently: Point1 IS that midpoint). radius is just this
            # vector's own length -- one real, concrete point, no separate
            # "toward deep" direction plus an independently-averaged
            # distance.
            i_vec = insert_disp - arc_center
            d_vec = deep_disp - arc_center
            p1_vec = i_vec - (i_vec - d_vec) / 2
            radius = max(np.linalg.norm(p1_vec), 1e-6)
            point1_dir = p1_vec / radius

            # Point2 = ref_dir itself (already a unit vector, already
            # oriented consistently -- see the sagittal/coronal sign
            # handling above) -- NOT point1_dir rotated by the displayed
            # `angle`. `angle` is compute_shank_roll_pitch_mri's MRI-space
            # number, which since that function switched to a true line-
            # to-plane angle (see its docstring) can be a completely
            # different, much larger value than the geometric angle
            # between point1_dir/ref_dir actually drawn in this atlas-
            # space picture -- forcing the sweep to equal it (previously
            # via a rotation-sign heuristic here) produced arcs that
            # opened the wrong way or didn't visually reach the reference
            # line at all. Drawing directly between the two real vectors
            # is unambiguous and always geometrically correct; the
            # (possibly quite different) true MRI-space number is still
            # shown in the caption text below, not abandoned.
            point2_dir = ref_dir
            view_angle = float(np.degrees(np.arccos(np.clip(np.dot(point1_dir, ref_dir), -1.0, 1.0))))
            if view_angle > 90.0:
                # the reference is a LINE, not a directed ray (its "toward
                # lambda" sign above is just a cross-view convention) -- so
                # the angle actually worth showing/drawing is the shank's
                # acute angle to that line, not whichever of the two
                # supplementary angles the arbitrary sign happened to pick.
                # Flipping point2_dir to the opposite ray keeps the arc
                # anchored on the same real reference line while sweeping
                # through the acute wedge instead of the obtuse one.
                view_angle = 180.0 - view_angle
                point2_dir = -point2_dir

            arc = vtk.vtkArcSource()
            arc.SetCenter(arc_center[0], arc_center[1], 1.13)
            arc.SetPoint1(arc_center[0] + point1_dir[0] * radius, arc_center[1] + point1_dir[1] * radius, 1.13)
            arc.SetPoint2(arc_center[0] + point2_dir[0] * radius, arc_center[1] + point2_dir[1] * radius, 1.13)
            arc.SetResolution(20)
            arc_mapper = vtk.vtkPolyDataMapper()
            arc_mapper.SetInputConnection(arc.GetOutputPort())
            arc_actor = vtk.vtkActor()
            arc_actor.SetMapper(arc_mapper)
            arc_actor.GetProperty().SetColor(1, 1, 1)
            arc_actor.GetProperty().SetLineWidth(2)
            renderer.AddActor(arc_actor)
            self.shank_angle_arc_actors[view_name] = arc_actor

            # label position = the arc's own angle bisector (halfway
            # between Point1 and Point2, direction-wise), at roughly the
            # same distance from arc_center as the arc itself (radius) --
            # no separate scaling factor. point1_dir/point2_dir summed and
            # renormalized; falls back to a perpendicular of point1_dir
            # only in the degenerate case where they're exactly opposite
            # (a 180 degree sweep, where the sum cancels to zero).
            bisector_vec = point1_dir + point2_dir
            bisector_norm = np.linalg.norm(bisector_vec)
            if bisector_norm > 1e-9:
                bisector_dir = bisector_vec / bisector_norm
            else:
                bisector_dir = np.array([-point1_dir[1], point1_dir[0]])
            pos = arc_center + bisector_dir * radius

        caption_text = f"{angle:.1f}°(MRI)"
        #if view_angle is not None:
        #    # angle (MRI space, true value) and view_angle (this atlas-
        #    # space picture's own geometric angle) can legitimately differ
        #    # -- the atlas<->MRI registration is a nonlinear warp that
        #    # doesn't preserve angles -- so show both rather than letting
        #    # the arc's own visible span silently contradict one hidden
        #    # number.
        #    caption_text += f" ({view_angle:.1f}° Atlas)"
        caption = vtk.vtkCaptionActor2D()
        caption.SetCaption(caption_text)
        caption.SetAttachmentPoint(pos[0], pos[1], 1.15)
        caption.BorderOff()
        caption.LeaderOff()
        caption.GetCaptionTextProperty().SetColor(1, 1, 1)
        caption.GetCaptionTextProperty().SetFontSize(30)
        caption.GetCaptionTextProperty().SetBold(True)
        caption.GetCaptionTextProperty().ShadowOff()
        caption.GetCaptionTextProperty().BoldOff()
        caption.SetPosition(3, 3)
        caption.SetWidth(0.12)
        caption.SetHeight(0.035)
        renderer.AddActor(caption)
        self.shank_angle_text_actors[view_name] = caption

        self.render()

    def draw_electrode_line(self, view_name, point_a, point_b, color=(1,1,1), height=1.1):
        spacing = np.array(self.fixedImg.GetSpacing())  # x,y,z
        shape = np.array(self.fixedImg.GetSize())
        a = np.array(point_a, dtype=float)  # XYZ voxels
        b = np.array(point_b, dtype=float)
        if view_name == "axial" or view_name == "coronal":
            a[0] = shape[0]-1-a[0]
            b[0] = shape[0]-1-b[0]
        elif view_name == "sagittal":
            a[1] = shape[1]-1-a[1]
            b[1] = shape[1]-1-b[1]

        perp = {'coronal': (1, 1), 'sagittal': (0, 2), 'axial': (2, 0)}
        axis, slice_dim = perp[view_name]
        slice_idx = self.LoadMRI.slice_indices[0][slice_dim]
        proj = {'coronal': (0,2), 'sagittal': (1,2), 'axial': (0,1)}
        xi, yi = proj[view_name]

        pa = a * spacing
        pb = b * spacing
        mid = (pa + pb) / 2

        # dim projected line — always visible
        dim_line = vtk.vtkLineSource()
        dim_line.SetPoint1(pa[xi], pa[yi], height - 0.1)
        dim_line.SetPoint2(pb[xi], pb[yi], height - 0.1)
        dim_mapper = vtk.vtkPolyDataMapper()
        dim_mapper.SetInputConnection(dim_line.GetOutputPort())
        dim_actor = vtk.vtkActor()
        dim_actor.SetMapper(dim_mapper)
        dim_actor.GetProperty().SetColor(*color)
        dim_actor.GetProperty().SetOpacity(0.4)
        dim_actor.GetProperty().SetLineWidth(3)
        actors = [dim_actor]

        # bright clipped line — only when slice intersects
        denom = b[axis] - a[axis]
        if abs(denom) < 1e-6:
            # line is parallel to the slice plane — bright only if it lies within it
            if abs(a[axis] - slice_idx) <= 0.5:
                t_min, t_max = 0.0, 1.0
            else:
                t_min, t_max = 0.0, 0.0
        else:
            t_min = ((slice_idx - 0.5) - a[axis]) / denom
            t_max = ((slice_idx + 0.5) - a[axis]) / denom
            if t_min > t_max:
                t_min, t_max = t_max, t_min
        t_min = max(0.0, t_min)
        t_max = min(1.0, t_max)

        if t_min < t_max:
            p1 = (a + t_min * (b - a)) * spacing
            p2 = (a + t_max * (b - a)) * spacing
            bright_line = vtk.vtkLineSource()
            bright_line.SetPoint1(p1[xi], p1[yi], height)
            bright_line.SetPoint2(p2[xi], p2[yi], height)
            bright_mapper = vtk.vtkPolyDataMapper()
            bright_mapper.SetInputConnection(bright_line.GetOutputPort())
            bright_actor = vtk.vtkActor()
            bright_actor.SetMapper(bright_mapper)
            bright_actor.GetProperty().SetColor(*color)
            bright_actor.GetProperty().SetLineWidth(6)
            actors.append(bright_actor)

        caption = vtk.vtkCaptionActor2D()
        caption.SetCaption(f"Shank {self.shank_number+1}")
        caption.SetAttachmentPoint(mid[xi], mid[yi], height)
        caption.BorderOff()
        caption.LeaderOff()
        caption.GetCaptionTextProperty().SetColor(*color)
        caption.GetCaptionTextProperty().SetFontSize(7)
        caption.GetCaptionTextProperty().ShadowOff()
        caption.GetCaptionTextProperty().BoldOff()
        caption.SetPosition(3, 3)
        caption.SetWidth(0.1)
        caption.SetHeight(0.03)

        return actors, caption


    def visualize_regionname(self,region_name,view_name,indices):
        # reuse line renderer if exists
        shape = self.LoadMRI.volumes[0].slices[0].shape
        voxel = [0,0]
        if view_name=='axial': #xy
            voxel[0]=(shape[2]-indices[2])*self.LoadMRI.volumes[0].spacing[2]
            voxel[1]=indices[1]*self.LoadMRI.volumes[0].spacing[1]
        elif view_name=='coronal': #xz
            voxel[0]=(shape[2]-indices[2])*self.LoadMRI.volumes[0].spacing[2]
            voxel[1]=indices[0]*self.LoadMRI.volumes[0].spacing[0]
        elif view_name=='sagittal': #yz
            voxel[0]=(shape[1]-indices[1])*self.LoadMRI.volumes[0].spacing[1]
            voxel[1]=indices[0]*self.LoadMRI.volumes[0].spacing[0]

        if view_name not in self.LoadMRI.tp_renderer: # not in renderer_window:
            for vn in 'axial','coronal','sagittal':
                vtk_widget = self.LoadMRI.vtk_widgets[0][vn]
                self.LoadMRI.tp_renderer[vn] = vtk.vtkRenderer()
                vtk_widget.GetRenderWindow().SetNumberOfLayers(3)
                vtk_widget.GetRenderWindow().AddRenderer(self.LoadMRI.tp_renderer[vn])
                self.LoadMRI.tp_renderer[vn].SetLayer(1)
                self.LoadMRI.tp_renderer[vn].SetActiveCamera(vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera())

        #Delete previous text
        for vn in 'axial','coronal','sagittal':
            if vn in self.text_actor:
                tp_renderer = self.LoadMRI.tp_renderer[vn]
                tp_renderer.RemoveActor(self.text_actor[vn])

        tp_renderer = self.LoadMRI.tp_renderer[view_name]
        # Convert voxel to physical coordinates
        text_point = np.array([
            voxel[0],
            voxel[1],
            1.1
        ])

        #Create Text
        color = (1,1,1)
        text_actor = vtk.vtkBillboardTextActor3D()
        text_actor.SetInput(f"{region_name}")
        text_actor.SetPosition(text_point)
        text_actor.GetTextProperty().SetColor(*color)
        text_actor.GetTextProperty().SetFontSize(10)
        text_actor.GetTextProperty().BoldOn()
        text_actor.GetTextProperty().SetJustificationToCentered()

        self.text_actor[view_name] = text_actor
        tp_renderer.AddActor(text_actor) #REGION NAME

        self.render()


    def show_brainregion(self,checked):
        self.show_label = checked
        if not checked:
            #Delete previous text
            for vn in 'axial','coronal','sagittal':
                if vn in self.text_actor:
                    tp_renderer = self.LoadMRI.tp_renderer[vn]
                    tp_renderer.RemoveActor(self.text_actor[vn])

    def create_edge_mask(self):
        file_name = os.path.join(_paths['atlas_folder'], _paths['atlas_mask'])
        image = sitk.ReadImage(file_name)
        array = sitk.GetArrayFromImage(image)
        #array = self.LoadMRI.volumes[0].slices[0].copy()
        fg = array > 0
        fg_filled = ndimage.binary_fill_holes(fg)
        struct = np.ones((3, 3, 3), dtype=bool)
        eroded = ndimage.binary_erosion(fg_filled, structure=struct)
        border = fg_filled & ~eroded
        edge_mask = border.astype(np.uint8)
        self.edge_mask = edge_mask

        # Shared with every other overlay-adding call site (region_to_avoid_
        # img below, add_another_file, ...) instead of len(Layers[0]),
        # which only tracks layers added via THAT counter and can collide
        # with (silently overwrite) whichever Layers[0][layer_index] slot
        # this picks once anything else has used self.MW.FileLoader.
        # layer_index in the meantime -- see rendering_mri.py's identical
        # fix for the MRI-space version of this same method.
        self.MW.FileLoader.layer_index += 1
        layer_index = self.MW.FileLoader.layer_index
        # Attach LUT for contrast and brightness
        vminmax_perc = [0, 1] #reset
        vmin, vmax = np.percentile(edge_mask.copy(), [vminmax_perc[0]*100, vminmax_perc[1]*100])
        lut_vtk = vtk.vtkLookupTable()
        lut_vtk.SetNumberOfTableValues(2)
        lut_vtk.SetTableRange(0,1)
        lut_vtk.SetTableValue(0,0,0,0,0.4)
        lut_vtk.SetTableValue(1,1,1,1,1.0)
        lut_vtk.Build()

        self.LoadMRI.MW.Layers[0][layer_index] = ImageLayer(
            volume={0: edge_mask},  # same array reference — mutations are picked up automatically
            spacing=self.LoadMRI.volumes[0].spacing,
            view_names=['axial', 'coronal', 'sagittal'],
            slice_indices=self.LoadMRI.slice_indices[0],
            is_4d=False,
            render_fct=self.LoadMRI.render,
            vtk_dtype=vtk.VTK_UNSIGNED_CHAR,
            interpolation='nearest',
            opacity=1,
            lut = lut_vtk,
        )
        self.LoadMRI.setup_layer('coronal', 0, layer_index,visibility_at_start=False)

        # register it in the intensity table too. Skipping this used to
        # silently desync every layer added afterward (region-to-avoid,
        # ...): their layer_index (= len(Layers[0]) at creation
        # time) kept counting this layer, but the table's own row counter
        # never did, so each later row's visibility/opacity controls ended
        # up wired to the WRONG actual layer, one off from the row they
        # were sitting in.
        self.LoadMRI.MW.Layers[0][layer_index].visibility_btn = self.LoadMRI.intensity_table[0].update_table(
            "Brain Edge", edge_mask, 0, layer_index, visibility_enabled=False)



    def change_view_coronal(self,checked,recenter=True):
        if checked:
            # coronal view
            self.ui.stackedWidget_coronal.setCurrentIndex(0) #coronal
        else:
            # page 2 (page_10) -- the clipped-3D-view page used to be page 1
            # (page_32), but that slot now holds the oblique-reslice widget
            # for checkBox_constraint_90deg (see ElecGeometryMri.
            # enforce_constraint_90deg), so this got moved to page 2.
            self.ui.stackedWidget_coronal.setCurrentIndex(2)
            axis_y = np.array([0,1,0])
            direction = self.direction_atlas[self.shank_number]
            normal = axis_y - np.dot(axis_y, direction) * direction
            normal /= np.linalg.norm(normal)

            if normal[1]<0:
                normal *= -1

            self.Vis3D.render_clipped(normal,'coronal',self.shank_number,recenter=recenter)


    def change_view_sagittal(self,checked,recenter=True):
        if checked:
            # sagittal view
            self.ui.stackedWidget_sagittal.setCurrentIndex(0) #sagittal
        else:
            # page 2 (page_4) -- the clipped-3D-view page used to be page 1
            # (page_33), but that slot now holds the oblique-reslice widget
            # for checkBox_constraint_90deg_coronal (see ElecGeometryMri.
            # enforce_constraint_90deg_coronal), so this got moved to page 2,
            # same reordering as change_view_coronal's own page_32->page_10.
            self.ui.stackedWidget_sagittal.setCurrentIndex(2)
            axis_x = np.array([1,0,0]) #x-axis #(0,0,1)
            direction = self.direction_atlas[self.shank_number] #xyz
            normal = axis_x - np.dot(axis_x, direction) * direction
            normal /= np.linalg.norm(normal)
            if normal[0]>0:
                normal *= -1

            self.Vis3D.render_clipped(normal,'sagittal',self.shank_number,recenter=recenter)

    def change_view_axial(self,checked):
        if checked:
            # axial view
            self.ui.stackedWidget_axial.setCurrentIndex(0) #axial
        else:
            self.ui.stackedWidget_axial.setCurrentIndex(1) ##CHANGE TO 1
            normal = np.array([0,0,1]) #normal = np.array(axis_x) - np.dot(axis_x, direction) * direction
            atlas_z = self.fixedImg.GetSize()[2]
            if not hasattr(self, 'axial_slider_connected'):
                self.ui.horizontalSlider_axial3D.setRange(0, atlas_z - 1)
                self.ui.horizontalSlider_axial3D.setValue(self.coords_deepest_point[self.ui.comboBox_Shanks.currentIndex()][2])
                self.ui.horizontalSlider_axial3D.valueChanged.connect(self.update_axial_depth)
                self.axial_slider_connect = True
            depth = self.ui.horizontalSlider_axial3D.value()

            self.Vis3D.render_clipped(normal,'axial',self.shank_number,depth=depth)


    def update_axial_depth(self, depth):
        normal = np.array([0,0,1]) #normal = np.array(axis_x) - np.dot(axis_x, direction) * direction
        self.Vis3D.render_clipped(normal,'axial',self.shank_number,depth=depth)
