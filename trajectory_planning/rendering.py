# This Python file uses the following encoding: utf-8
import numpy as np
import vtk
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from core.image_layer import ImageLayer
from gui_utils.busy_overlay import BusyOverlay
from paths_config import _paths
from mrid_utils.atlas_registry import ATLASES, get_active_atlas_id

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

        def proceed():
            if not self.reload_atlas_view(atlas_id):
                self._sync_atlas_selector_widget()  # switch declined/failed -- revert the combo

        # BusyOverlay.run() defers fn (QTimer.singleShot) and discards its
        # return value -- reload_atlas_view's own True/False (whether the
        # switch actually happened) has to be checked from inside proceed()
        # now, not synchronously here, since run() itself always returns
        # immediately.
        atlas_name = ATLASES[atlas_id]['display_name']
        self.MW.overlay = BusyOverlay(
            self.MW, message=f"Switching to {atlas_name} atlas, please wait…")
        self.MW.overlay.run(proceed)

    def _atlas_plane_segment_in_view(self, view_name, normal, plane_point):
        """Voxel-space XYZ endpoints of the reference plane's crossing of
        the CURRENTLY DISPLAYED slice for view_name (None if it doesn't
        cross). Shared by update_atlas_plane_line (the coronal reference
        line) and compute_shank_reference_angle, which uses this same
        crossing as the coronal reference direction -- the raw
        bregma-lambda vector is ~degenerate there since bregma/lambda
        differ almost entirely along the AP axis, which coronal flattens
        out. Space-agnostic -- only reads self.LoadMRI/self.LoadMRI.
        slice_indices, so this works unchanged for RenderingMri too."""
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
        """Refresh the coronal reference-plane tilt indicator. Sagittal
        already has its own plain bregma-lambda line (atlas_bl_line_actor,
        drawn once in draw_atlas_reference_points); calling
        update_atlas_plane_line('sagittal') too used to draw a SECOND,
        separate line there (the plane's crossing of the current sagittal
        slice), overlapping/duplicating the first."""
        self.update_atlas_plane_line('coronal')

    def update_atlas_plane_line(self, view_name):
        """Where the bregma/lambda/misalignment reference plane crosses the
        CURRENTLY DISPLAYED coronal or sagittal slice -- a true 3D-plane
        intersection, not a naive point-to-point projection. Drawn as a
        dotted line. Since the intersection depends on which slice is
        showing, this needs to be called again whenever that slice changes
        (see LoadMRI.update_slices)."""
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

    @staticmethod
    def _line_intersection_2d(p1, d1, p2, d2):
        """2D point where line (p1 + t*d1) crosses line (p2 + s*d2), or
        None if they're ~parallel (no unique crossing)."""
        denom = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(denom) < 1e-9:
            return None
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / denom
        return p1 + t * d1

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
