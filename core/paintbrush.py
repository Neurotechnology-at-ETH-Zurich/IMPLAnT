# This Python file uses the following encoding: utf-8

import vtk
import numpy as np
from PySide6.QtGui import  QColor
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray,vtkPolyData
from core.image_layer import ImageLayer

class Paintbrush:
    """
    Paintbrush tool for voxel-wise annotation on MRI volumes.
    Supports square and round brushes, paint-over logic, and overlay rendering.
    """
    def __init__(self,LoadMRI):
        """Initialiye paintbrush tool"""
        super().__init__()
        self.LoadMRI = LoadMRI

        #default brush type is squared and red label and all lable scan be overpainted
        self.brush_type= 'square'
        self.brush_color = "red"
        self.paintover_color = "white"
        self.histogram_color = "all anat"
        self.LoadMRI.heatmap = False #cursor in 4th image visible
        self.LoadMRI.paint = False

        self.brush_actors = {}
        self.label_volume_index = 0
        self.last_roi_indices = set()
        self.layer_index = {}
        self.label_volume = {}
        self.seg_volume = {}
        for idx in range(len(self.LoadMRI.vtk_widgets)):
            self.label_volume[idx] = np.zeros_like(self.LoadMRI.volumes[0].slices[0], dtype=np.uint8)
            self.seg_volume[idx] = np.zeros_like(self.LoadMRI.volumes[0].slices[0], dtype=np.uint8)


    def start_paintbrush(self,is_4d=False,histogram_needed=True):
        """
        Initialize label volume and setup overlay tables for each view.
        """
        self.histogram_needed = histogram_needed
        for idx in range(len(self.LoadMRI.vtk_widgets)):
            if idx  in self.layer_index:
                continue
            # Store Layer
            layer_index = len(self.LoadMRI.MW.Layers[idx])
            lut = self.setup_lut()
            if is_4d:
                vol = {0: self.label_volume[idx], 1: self.label_volume[idx], 2: self.label_volume[idx]}
            else:
                vol = {0: self.label_volume[idx]}
            self.LoadMRI.MW.Layers[idx][layer_index] = ImageLayer(
                volume=vol,  # same array reference — mutations are picked up automatically
                spacing=self.LoadMRI.volumes[0].spacing,
                view_names=self.LoadMRI.MW.Layers[idx][0].view_names, #['axial', 'coronal', 'sagittal'],
                slice_indices=self.LoadMRI.slice_indices[0],
                is_4d=is_4d,
                render_fct=self.LoadMRI.render,
                vtk_dtype=vtk.VTK_UNSIGNED_CHAR,
                interpolation='nearest',
                opacity=0.5,
                lut = lut,
                flip=True,
            )
            self.layer_index[idx] = layer_index
            if not self.LoadMRI.volumes[0].is_4d:
                self.LoadMRI.setup_layer('coronal',idx,layer_index) ##data_view
            else:
                self.LoadMRI.setup_layer(self.LoadMRI.MW.Layers[0][0].view_names,idx,layer_index)
                intensity_filename = 'Segmentation Mask'
                self.LoadMRI.intensity_table[0].update_table(intensity_filename, vol[0],0,layer_index,visibility_enabled=False)


    def set_size(self,var:int):
        """
        Set brush size and update GUI sliders.
        """
        self.size = var
        self.LoadMRI.brush['size'].setEnabled(False)
        self.LoadMRI.brush['size_slider'].setEnabled(False)
        self.LoadMRI.brush['size'].setValue(self.size)
        self.LoadMRI.brush['size_slider'].setValue(self.size)
        self.LoadMRI.brush['size'].setEnabled(True)
        self.LoadMRI.brush['size_slider'].setEnabled(True)


    def mouse_moves(self,paintbrush_pos:tuple[int, int, int],filled:bool,view_name:str,data_index):
        """
        Called whenever the mouse moves. Paints overlay at voxel coordinates.
        Uses current brush size and color.
        """
        self.mouse_pos = paintbrush_pos

        # Create square / circle
        self.get_paint_settings(filled,view_name,paintbrush_pos,data_index)

        if not filled:
            self.LoadMRI.render()
            return

        label_value = self.color_combobox.index(self.brush_color)
        paintover_value = self.color_paintover.index(self.paintover_color)

        # Determine voxel radius according to view spacing
        if paintbrush_pos is not None:
            z, y, x = map(int, paintbrush_pos)
        else:
            return
        nz, ny, nx = self.label_volume[data_index].shape
        half = int(self.size // 2)
        region = [0]
        if self.brush_type == 'square':
            if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d: # XY plane, spacing Z ignored
                x0, x1 = max(0, x-half), min(nx - 1, x +half+ (0 if self.size % 2 == 0 else 1))
                y0, y1 = max(0, y-half), min(ny - 1, y +half+ (0 if self.size % 2 == 0 else 1))
                # Only overwrite voxels with paintover_value
                region = self.label_volume[data_index][z, y0:y1, x0:x1].copy()
                if paintover_value != 0:
                    mask = self.label_volume[data_index][z, y0:y1, x0:x1] == paintover_value-1
                    self.label_volume[data_index][z, y0:y1, x0:x1][mask] = int(label_value)
                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                        self.seg_volume[data_index][z, y0:y1, x0:x1][mask] = int(label_value)
                elif paintover_value == 0:
                    self.label_volume[data_index][z, y0:y1, x0:x1] = int(label_value)
                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                        self.seg_volume[data_index][z, y0:y1, x0:x1] = int(label_value)
                else:
                    return

            elif view_name == 'coronal':  # XZ plane, spacing Y ignored
                x0, x1 = max(0, x - half), min(nx - 1, x + half+ (0 if self.size % 2 == 0 else 1))
                z0, z1 = max(0, z - half), min(nz - 1, z + half+ (0 if self.size % 2 == 0 else 1))
                if paintover_value != 0:
                    mask = self.label_volume[data_index][z0:z1, y, x0:x1] == paintover_value-1
                    self.label_volume[data_index][z0:z1, y, x0:x1][mask] = int(label_value)
                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                        self.seg_volume[data_index][z0:z1, y, x0:x1][mask] = int(label_value)
                elif paintover_value == 0:
                    self.label_volume[data_index][z0:z1, y, x0:x1] = int(label_value)
                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                        self.seg_volume[data_index][z0:z1, y, x0:x1] = int(label_value)
                else:
                    return

            elif view_name == 'sagittal':  # YZ plane, spacing X ignored
                y0, y1 = max(0, y - half), min(ny - 1, y + half + (0 if self.size % 2 == 0 else 1))
                z0, z1 = max(0, z - half), min(nz - 1, z + half + (0 if self.size % 2 == 0 else 1))
                if paintover_value != 0:
                    mask = self.label_volume[data_index][z0:z1, y0:y1, x] == paintover_value-1
                    self.label_volume[data_index][z0:z1, y0:y1, x][mask] = int(label_value)
                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                        self.seg_volume[data_index][z0:z1, y0:y1, x][mask] = int(label_value)
                elif paintover_value == 0:
                    self.label_volume[data_index][z0:z1, y0:y1, x] = int(label_value)
                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                        self.seg_volume[data_index][z0:z1, y0:y1, x] = int(label_value)
                else:
                    return

        elif self.brush_type == 'round':
            radius = int(self.size/2)
            radius_vector = []
            radius_vector.append([0,0])
            if self.size%2==0:
                if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d:
                    x_new = x+0.5
                    y_new = y+0.5
                    vol_shape_x = self.label_volume[data_index].shape[2]
                    vol_shape_y = self.label_volume[data_index].shape[1]
                elif view_name == 'coronal':
                    x_new = x+0.5
                    y_new = z+0.5
                    vol_shape_x = self.label_volume[data_index].shape[2]
                    vol_shape_y = self.label_volume[data_index].shape[0]
                elif view_name == 'sagittal':
                    x_new = z+0.5
                    y_new = y+0.5
                    vol_shape_x = self.label_volume[data_index].shape[0]
                    vol_shape_y = self.label_volume[data_index].shape[1]
                for xx in range(int(radius+1)):
                    for yy in range(int(radius+1)):
                        if np.sqrt((xx-0.5)**2+(yy-0.5)**2) < self.size/2*0.98:
                            radius_vector.append([xx-0.5,yy-0.5])
            else:
                if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d:
                    x_new = x
                    y_new = y
                    vol_shape_x = self.label_volume[data_index].shape[2]
                    vol_shape_y = self.label_volume[data_index].shape[1]
                elif view_name == 'coronal':
                    x_new = x
                    y_new = z
                    vol_shape_x = self.label_volume[data_index].shape[2]
                    vol_shape_y = self.label_volume[data_index].shape[0]
                elif view_name == 'sagittal':
                    x_new = z
                    y_new = y
                    vol_shape_x = self.label_volume[data_index].shape[0]
                    vol_shape_y = self.label_volume[data_index].shape[1]
                for xx in range(int(radius+1)):
                    for yy in range(int(radius+1)):
                        if np.sqrt(xx**2+yy**2) < self.size/2*0.93:
                            radius_vector.append([xx,yy])
            region = []
            for sign_x in +1,+1,-1,-1:
                for sign_y in +1,-1,+1,-1:
                    for dx,dy in radius_vector:
                        xi = int(round(x_new + dx*sign_x))
                        yi = int(round(y_new + dy*sign_y))

                        # check bounds
                        if 0 <= xi < vol_shape_x and 0 <= yi < vol_shape_y:
                            if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d:
                                region.append(self.label_volume[data_index][z, yi, xi].copy())
                                if self.label_volume[data_index][z, yi, xi] == paintover_value - 1 or paintover_value == 0:
                                    self.label_volume[data_index][z, yi, xi] = label_value
                                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                                        self.seg_volume[data_index][z, yi, xi] = label_value
                            elif view_name == 'coronal':
                                region.append(self.label_volume[data_index][yi, y, xi].copy())
                                if self.label_volume[data_index][yi, y, xi] == paintover_value - 1 or paintover_value == 0:
                                    self.label_volume[data_index][yi, y, xi] = label_value
                                    if label_value > self.LoadMRI.mrid_tags.num_regions:
                                       self.seg_volume[data_index][yi, y, xi] = label_value
                            elif view_name == 'sagittal':
                                # apply mask
                                region.append(self.label_volume[data_index][xi, yi, x].copy())
                                if 0 <= xi < vol_shape_x:
                                    if self.label_volume[data_index][xi, yi, x] == paintover_value - 1 or paintover_value == 0:
                                        self.label_volume[data_index][xi, yi, x] = label_value
                                        if label_value > self.LoadMRI.mrid_tags.num_regions:
                                           self.seg_volume[data_index][xi, yi, x] = label_value

        # Update the overlay
        self.update_overlay(data_index) #z, y, x)

        if self.histogram_needed:
            self.histogram()

        if self.LoadMRI.heatmap:
            roi_indices = list(np.unique(np.append(np.unique(region), label_value)))
            self.LoadMRI.mrid_tags.update_heatmap(view_name,data_index, roi_indices)


    def get_paint_settings(self,filled:bool,view_name:str,paintbrush_pos:tuple[int, int, int],data_index):
        """
        Create or update a brush actor in a given view.
        """
        LM = self.LoadMRI
        if paintbrush_pos is None:
            return

        z, y, x = map(int, paintbrush_pos)
        nz, ny, nx = self.label_volume[data_index].shape
        # VTK world positions account for fliplr: x axis is flipped in axial/coronal, y axis in sagittal
        cx = (nx - 1 - x) * LM.volumes[data_index].spacing[2]
        cx_even = (nx - 0.5 - x) * LM.volumes[data_index].spacing[2]
        cy_sag = (ny - 1 - y) * LM.volumes[data_index].spacing[1]
        cy_sag_even = (ny - 0.5 - y) * LM.volumes[data_index].spacing[1]

        if self.brush_type == 'square':
            # Create cube
            self.source = vtk.vtkCubeSource()
            self.source.SetZLength(0.1)  # flat in slice plane
            if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d:
                self.source.SetXLength(self.size*LM.volumes[data_index].spacing[2])
                self.source.SetYLength(self.size*LM.volumes[data_index].spacing[1])
                if self.size % 2 == 0:
                    self.source.SetCenter(cx_even, (y - 0.5) * LM.volumes[data_index].spacing[1], 1)
                else:
                    self.source.SetCenter(cx, y * LM.volumes[data_index].spacing[1], 1)
            elif view_name == 'coronal':
                self.source.SetXLength(self.size*LM.volumes[data_index].spacing[2])
                self.source.SetYLength(self.size*LM.volumes[data_index].spacing[0])
                if self.size % 2 == 0:
                    self.source.SetCenter(cx_even, (z - 0.5) * LM.volumes[data_index].spacing[0], 1)
                else:
                    self.source.SetCenter(cx, z * LM.volumes[data_index].spacing[0], 1)
            elif (self.LoadMRI.volumes[0].is_4d and view_name=='sagittal'):
                self.source.SetXLength(self.size*LM.volumes[data_index].spacing[1])
                self.source.SetYLength(self.size*LM.volumes[data_index].spacing[2])
                if self.size % 2 == 0:
                    self.source.SetCenter(cy_sag_even, (x - 0.5) * LM.volumes[data_index].spacing[2], 1)
                else:
                    self.source.SetCenter(cy_sag, x * LM.volumes[data_index].spacing[2], 1)
            elif view_name == 'sagittal':
                self.source.SetXLength(self.size*LM.volumes[data_index].spacing[1])
                self.source.SetYLength(self.size*LM.volumes[data_index].spacing[0])
                if self.size % 2 == 0:
                    self.source.SetCenter(cy_sag_even, (z - 0.5) * LM.volumes[data_index].spacing[0], 1)
                else:
                    self.source.SetCenter(cy_sag, z * LM.volumes[data_index].spacing[0], 1)

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(self.source.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            qcolor = QColor(self.brush_color)
            rgb = (qcolor.redF(), qcolor.greenF(), qcolor.blueF())
            actor.GetProperty().SetColor(rgb)
            actor.GetProperty().SetLineWidth(2.0)
            #actor.GetProperty().SetInterpolationTypeToNearest()

            actor.GetProperty().SetRepresentationToWireframe()
            actor.GetProperty().SetOpacity(1.0)
            for i in range(len(self.LoadMRI.renderers)):
                renderer = self.LoadMRI.renderers[i][view_name] ## FOR ALL IMAGES
                if self.brush_actors.get(view_name) is not None:
                    renderer.RemoveActor(self.brush_actors[view_name])
                renderer.AddActor(actor)
                #self.LoadMRI.vtk_widgets[i][view_name].GetRenderWindow().Render() ## FOR ALL IMAGES
            self.brush_actors[view_name] = None
            self.brush_actors[view_name] = actor
            return actor

        elif self.brush_type == 'round':
            #z, y, x: slides
            radius = int(self.size/2)
            radius_vector = []

            if self.size%2==0:
                if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d:
                    x_new = nx - 0.5 - x
                    y_new = y+0.5
                    spacing_x = LM.volumes[data_index].spacing[2] #x
                    spacing_y = LM.volumes[data_index].spacing[1] #y
                elif view_name == 'coronal':
                    x_new = nx - 0.5 - x
                    y_new = z+ 0.5
                    spacing_x = LM.volumes[data_index].spacing[2]
                    spacing_y = LM.volumes[data_index].spacing[0]
                elif view_name == 'sagittal':
                    x_new = ny - 0.5 - y
                    y_new = z + 0.5
                    spacing_x = LM.volumes[data_index].spacing[1]
                    spacing_y = LM.volumes[data_index].spacing[0]

                for xx in range(int(radius)):
                    xx +=1
                    for yy in range(int(radius)):
                        yy +=1
                        if np.sqrt((xx-0.5)**2+(yy-0.5)**2) > self.size/2*0.98:
                            radius_vector.append([xx-0.5,yy-0.5])
                            break
            else:
                if view_name == 'axial' or self.LoadMRI.volumes[0].is_4d:
                    x_new = nx - 1 - x
                    y_new = y
                    spacing_x = LM.volumes[data_index].spacing[2]
                    spacing_y = LM.volumes[data_index].spacing[1]
                elif view_name == 'coronal':
                    x_new = nx - 1 - x
                    y_new = z
                    spacing_x = LM.volumes[data_index].spacing[2]
                    spacing_y = LM.volumes[data_index].spacing[0]
                elif view_name == 'sagittal':
                    x_new = ny - 1 - y
                    y_new = z
                    spacing_x = LM.volumes[data_index].spacing[1]
                    spacing_y = LM.volumes[data_index].spacing[0]
                for xx in range(int(radius)):
                    xx += 1
                    for yy in range(int(radius)):
                        yy += 1
                        if np.sqrt(xx**2+yy**2) > self.size/2*0.93:
                            radius_vector.append([xx,yy])
                            break

            length = len(radius_vector)
            points = vtkPoints()
            num = 0
            if length > 0:
                #rechts oben
                for ii in range(length):
                    points.InsertNextPoint((x_new + radius_vector[ii][0] - 0.5)* spacing_x, (y_new + radius_vector[ii][1] + 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new + radius_vector[ii][0] - 0.5)* spacing_x, (y_new + radius_vector[ii][1] - 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new + radius_vector[ii][0] + 0.5)* spacing_x, (y_new + radius_vector[ii][1] - 0.5)* spacing_y,1.1)
                    num += 3

                #rechts unten
                for ii in range(length):
                    ii = length-ii-1
                    points.InsertNextPoint((x_new + radius_vector[ii][0] + 0.5)* spacing_x, (y_new - radius_vector[ii][1] + 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new + radius_vector[ii][0] - 0.5)* spacing_x, (y_new - radius_vector[ii][1] + 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new + radius_vector[ii][0] - 0.5)* spacing_x, (y_new - radius_vector[ii][1] - 0.5)* spacing_y,1.1)
                    num += 3

                #links unten
                for ii in range(length):
                    points.InsertNextPoint((x_new - radius_vector[ii][0] + 0.5)* spacing_x, (y_new - radius_vector[ii][1] - 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new - radius_vector[ii][0] + 0.5)* spacing_x, (y_new - radius_vector[ii][1] + 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new - radius_vector[ii][0] - 0.5)* spacing_x, (y_new - radius_vector[ii][1] + 0.5)* spacing_y,1.1)
                    num += 3

                #links oben
                for ii in range(length):
                    ii = length-ii-1
                    points.InsertNextPoint((x_new - radius_vector[ii][0] - 0.5)* spacing_x, (y_new + radius_vector[ii][1] - 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new - radius_vector[ii][0] + 0.5)* spacing_x, (y_new + radius_vector[ii][1] - 0.5)* spacing_y,1.1)
                    points.InsertNextPoint((x_new - radius_vector[ii][0] + 0.5)* spacing_x, (y_new + radius_vector[ii][1] + 0.5)* spacing_y,1.1)
                    num += 3

                #remove duplicated points
                #Extract all VTK points to a NumPy array
                n_points = points.GetNumberOfPoints()
                arr = np.array([points.GetPoint(i) for i in range(n_points)])

                # Convert to (x, y) only, since z is constant
                xy = arr[:, :2]

                # Find first and last occurrence of each unique (x, y)
                unique_xy, first_idx = np.unique(xy, axis=0, return_index=True)
                _, last_idx = np.unique(xy[::-1], axis=0, return_index=True)
                last_idx = len(xy) - 1 - last_idx  # flip back

                # Start with all True → keep all
                keep = np.ones(len(xy), dtype=bool)

                # Remove any points *between* first and last duplicates
                for f, l in zip(first_idx, last_idx):
                    if l > f + 1:  # means there are points between
                        keep[f + 1:l] = False

                # Apply mask
                arr_filtered = arr[keep]

                #close the loop
                if not np.allclose(arr_filtered[0], arr_filtered[-1]):
                    arr_filtered = np.vstack([arr_filtered, arr_filtered[0]])

                # Replace VTK points
                points.Reset()
                num = 0
                for p in arr_filtered:
                    points.InsertNextPoint(*p)
                    num += 1
            else: #radius 1 or 2_new
                points.InsertNextPoint((x_new + 0.5*self.size)* spacing_x, (y_new + 0.5*self.size)* spacing_y,1.1)
                points.InsertNextPoint((x_new + 0.5*self.size)* spacing_x, (y_new - 0.5*self.size)* spacing_y,1.1)
                points.InsertNextPoint((x_new - 0.5*self.size)* spacing_x, (y_new - 0.5*self.size)* spacing_y,1.1)
                points.InsertNextPoint((x_new - 0.5*self.size)* spacing_x, (y_new + 0.5*self.size)* spacing_y,1.1)
                num = 4

            self.source = vtk.vtkPolygon()
            self.source.GetPointIds().SetNumberOfIds(num)
            for i in range(num):
                self.source.GetPointIds().SetId(i,i)

            # Mapper and actor
            # Add the polygon to a list of polygons
            polygons = vtkCellArray()
            polygons.InsertNextCell(self.source)

            # Create a PolyData
            polygonPolyData = vtkPolyData()
            polygonPolyData.SetPoints(points)
            polygonPolyData.SetPolys(polygons)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polygonPolyData)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            qcolor = QColor(self.brush_color)
            rgb = (qcolor.redF(), qcolor.greenF(), qcolor.blueF())
            actor.GetProperty().SetColor(rgb)
            actor.GetProperty().SetLineWidth(2.0)

            actor.GetProperty().SetRepresentationToWireframe()
            actor.GetProperty().SetOpacity(1.0)
            #actor.GetProperty().SetInterpolationTypeToNearest()

            actor.GetProperty().SetRepresentationToWireframe()
            actor.GetProperty().SetOpacity(1.0)
            for i in range(len(self.LoadMRI.renderers)):
                renderer = self.LoadMRI.renderers[i][view_name] # FOR ALL IMAGES
                if self.brush_actors.get(view_name) is not None:
                    renderer.RemoveActor(self.brush_actors[view_name])
                renderer.AddActor(actor)
                #self.LoadMRI.vtk_widgets[i][view_name].GetRenderWindow().Render() # FOR ALL IMAGES
            self.brush_actors[view_name] = None
            self.brush_actors[view_name] = actor

            return actor


    def update_overlay(self,data_index):
        """
        Update the VTK overlay actors for all views based on the label volume.
        """
        z, y, x = self.LoadMRI.slice_indices[data_index]
        layer = self.LoadMRI.MW.Layers[data_index][self.layer_index[data_index]]
        layer.update_vtk(self.LoadMRI.slice_indices[data_index])

        self.LoadMRI.render()



    def setup_lut(self):
        number_colors = len(self.RGB_table)
        lookup = vtk.vtkLookupTable()
        lookup.SetNumberOfTableValues(number_colors)
        lookup.SetRange(0, number_colors-1)
        lookup.Build()
        colors = self.RGB_table
        for i, (r, g, b, a) in enumerate(colors):
            lookup.SetTableValue(i, r, g, b, a)

        return lookup


    def histogram(self):
        """
        Update the histogram for the current label selection in the GUI.
        """
        # assume `image_data` is your MRI slice and `labels` is label array

        # Clear previous plot
        self.widget_histogram.clear()

        if self.histogram_color == 'all anat':
            histog_label=0
        else:
            histog_label = self.color_combobox.index(self.histogram_color)

        if self.LoadMRI.volumes[0].is_4d:
            if histog_label==0:
                mask = np.zeros_like(self.label_volume[self.label_volume_index], dtype=bool)
                for i in range(1, self.LoadMRI.mrid_tags.num_regions+1):
                    mask = self.label_volume[self.label_volume_index] == i
                    intensities = self.LoadMRI.volumes[0].slices[0][mask]
                    # Compute histogram
                    counts, bin_edges = np.histogram(intensities, bins=50)

                    brush = QColor(self.color_combobox[i])
                    brush.setAlpha(100)

                    # Plot directly in your GUI widget
                    self.widget_histogram.plot(
                        bin_edges,counts, stepMode=True, fillLevel=0, brush=brush
                    )
                return
            else:
                mask = self.label_volume[self.label_volume_index] == histog_label
        else:
            mask = self.label_volume[self.label_volume_index] == histog_label
        intensities = self.LoadMRI.volumes[0].slices[0][mask] ## FOR ALL IMAGES


        if intensities.size == 0:
            return

        # Compute histogram
        counts, bin_edges = np.histogram(intensities, bins=50)

        brush = QColor(self.color_combobox[histog_label])
        brush.setAlpha(150)

        # Plot directly in your GUI widget
        self.widget_histogram.plot(
            bin_edges,counts, stepMode=True, fillLevel=0, brush=brush
        )

    def set_label_occupancy(self,var:float):
        """
        Set the opacity of the label overlay and update GUI sliders.
        """
        if var > 1:
            var /= 100
        self.label_occ = var
        self.LoadMRI.brush['label_occ_slider'].blockSignals(True)
        self.LoadMRI.brush['label_occ'].blockSignals(True)
        self.LoadMRI.brush['label_occ'].setValue(self.label_occ)
        self.LoadMRI.brush['label_occ_slider'].setValue(self.label_occ*100)
        self.LoadMRI.brush['label_occ'].blockSignals(False)
        self.LoadMRI.brush['label_occ_slider'].blockSignals(False)

        for idx, layer_index in self.layer_index.items():
            layer = self.LoadMRI.MW.Layers[idx][layer_index]
            layer.set_opacity(self.label_occ*100)
            for widget in self.LoadMRI.vtk_widgets[idx].values():
                widget.GetRenderWindow().Render()

