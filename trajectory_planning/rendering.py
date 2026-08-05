# This Python file uses the following encoding: utf-8
import numpy as np
import os
import SimpleITK as sitk
import vtk
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from scipy import ndimage
import sys
import json as _json
from core.image_layer import ImageLayer
_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)

class Rendering:
    def render(self):
        for _,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                widget.GetRenderWindow().Render()

    def check_points_in_slice(self):
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

    def show_edge_mask(self):
        checked = self.ui.pushButton_edgemask.isChecked()
        self.LoadMRI.MW.Layers[0][self.layer_index].toggle_visibility(checked,None)
        if checked:
            self.ui.pushButton_edgemask.setText('Hide \n highlighted Points')
        else:
            self.ui.pushButton_edgemask.setText('Highlight Points \n on Brain Edge')


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

        layer_index = len(self.LoadMRI.MW.Layers[0])
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
        self.layer_index = layer_index



    def change_view_coronal(self,checked):
        if checked:
            # coronal view
            self.ui.stackedWidget_coronal.setCurrentIndex(0) #coronal
        else:
            self.ui.stackedWidget_coronal.setCurrentIndex(1) #CHANGE TO 1
            axis_y = np.array([0,1,0])
            direction = self.direction_atlas[self.shank_number]
            normal = axis_y - np.dot(axis_y, direction) * direction
            normal /= np.linalg.norm(normal)

            if normal[1]<0:
                normal *= -1

            self.Vis3D.render_clipped(normal,'coronal',self.shank_number)


    def change_view_sagittal(self,checked):
        if checked:
            # sagittal view
            self.ui.stackedWidget_sagittal.setCurrentIndex(0) #sagittal
        else:
            self.ui.stackedWidget_sagittal.setCurrentIndex(1) #CHANGE TO 1
            axis_x = np.array([1,0,0]) #x-axis #(0,0,1)
            direction = self.direction_atlas[self.shank_number] #xyz
            normal = axis_x - np.dot(axis_x, direction) * direction
            normal /= np.linalg.norm(normal)
            if normal[0]>0:
                normal *= -1

            self.Vis3D.render_clipped(normal,'sagittal',self.shank_number)

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
