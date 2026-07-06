# This Python file uses the following encoding: utf-8
import numpy as np
import vtk
from vtk.util import numpy_support
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor,vtkPolyDataMapper
from PySide6.QtGui import QStandardItemModel,QFont,QStandardItem


class Segmentation:
    def __init__(self,LoadMRI):
        super().__init__()
        # Load original image
        self.LoadMRI = LoadMRI

        # Default thresholds
        self.lower = 10
        self.upper = 50

        #if tab in toolbar is clicked on -> bounded thresholding
        self.threshold_mode = 'bounded'
        self.LoadMRI.threshold_on = True


    def smooth_binary_threshold(self,image, lower=None, upper=None, imin=None, imax=None):
        #update threshold data
        smoothness=3 #set to equal itk snap

        bidir = (lower is not None) and (upper is not None)

        # handle invalid bidirectional threshold -> black image
        if bidir and lower >= upper:
            return np.zeros_like(image, dtype=np.float32)

        factor_lower = 1.0 if lower is not None else 0.0
        factor_upper = 1.0 if upper is not None else 0.0
        shift = 1.0 - (factor_lower + factor_upper)

        if imin is None:
            imin = np.min(image)
        if imax is None:
            imax = np.max(image)

        # scaling factor based on smoothness
        if bidir:
            range_val = upper - lower
        else:
            range_val = (imax - imin) / 3.0  # ITK-SNAP default "arbitrary" choice

        eps = 10 ** (-smoothness)
        scaling_factor = np.log((2 - eps) / eps) / range_val

        # compute smooth threshold
        z = image.astype(np.float32)

        y_lower = factor_lower * np.tanh((z - lower) * scaling_factor) if lower is not None else 0
        y_upper = factor_upper * np.tanh((upper - z) * scaling_factor) if upper is not None else 0

        t = y_lower + y_upper + shift

        return (t * 0x7fff).astype(np.int16)




class SegmentationInitialization:
    def __init__(self,LoadMRI):
        super().__init__()

        self.LoadMRI = LoadMRI
        self.actor_bubble = []
        self.index = 0
        self.selected = False
        self.actor_selected = []

    def get_bubble_center(self,view_name):
        shape = self.LoadMRI.volumes[0].slices[0].shape
        if view_name == "axial":      # z fixed -> (x,y)
            self.center = [
                (shape[2]-self.LoadMRI.slice_indices[0][2])*self.LoadMRI.volumes[0].spacing[2],
                self.LoadMRI.slice_indices[0][1]*self.LoadMRI.volumes[0].spacing[1],
                1.1 #otherwise not visible
            ]
        elif view_name == "coronal": # y fixed -> (z,x)
            self.center = [
                (shape[2]-self.LoadMRI.slice_indices[0][2])*self.LoadMRI.volumes[0].spacing[2],
                self.LoadMRI.slice_indices[0][0]*self.LoadMRI.volumes[0].spacing[0],
                1.1 #otherwise not visible
            ]
        elif view_name == "sagittal":# x fixed -> (y,z)
            self.center = [
                (shape[1]-self.LoadMRI.slice_indices[0][1])*self.LoadMRI.volumes[0].spacing[1],
                self.LoadMRI.slice_indices[0][0]*self.LoadMRI.volumes[0].spacing[0],
                1.1 #otherwise not visible
            ]
        self.center_px = self.LoadMRI.slice_indices[0].copy()


    def row_selected(self,selected,deselected):
        for ix in selected.indexes():
            self.row_index = ix.row()
            self.selected = True
            self.update_bubbles_visible()
            self.LoadMRI.render()
            break

    def draw_bubble(self,push_btn):
        print('start',self.radius,flush=True)
        for view_name in 'axial','sagittal','coronal':
            #Get cursor position
            self.get_bubble_center(view_name)

            polygonSource = vtkRegularPolygonSource()
            polygonSource.GeneratePolygonOn()
            polygonSource.SetNumberOfSides(100)
            polygonSource.SetRadius(self.radius)
            polygonSource.SetCenter(self.center)

            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(polygonSource.GetOutputPort())

            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(1,0,0)
            actor.GetProperty().SetOpacity(0.3)

            renderer = self.LoadMRI.renderers[0][view_name]
            renderer.AddActor(actor)
            self.actor_bubble.append([view_name,actor,self.center,self.radius,self.center_px,polygonSource])

            self.create_circle_around_selected_bubble(view_name,self.radius,self.center)


        self.selected = True
        row = self.model.rowCount()
        self.row_index = row
        self.model.insertRow(row)
        self.model.setItem(row,0, QStandardItem(str(self.center_px[2]+1)))
        self.model.setItem(row,1, QStandardItem(str(self.center_px[1]+1)))
        self.model.setItem(row,2, QStandardItem(str(self.center_px[0]+1)))
        self.model.setItem(row,3, QStandardItem(str(self.radius)))
        self.index += 1
        #select row in table
        self.table.selectRow(row)

        #make new circle selected circle
        for i in 1,2,3:
            actor_entry = self.actor_selected[len(self.actor_bubble)-i]
            actor_entry[2].SetVisibility(1)
            polygonSource = actor_entry[3]
            polygonSource.SetRadius(self.radius)
            polygonSource.Modified()

        for _,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                widget.GetRenderWindow().Render()

        if not push_btn.isEnabled():
            push_btn.setEnabled(True)

        print('end',self.radius,flush=True)

    def create_table(self,table):
        self.table = table
        self.model = QStandardItemModel(0,4)
        self.model.setHorizontalHeaderLabels(["X","Y","Z","Radius"])
        header_font = QFont()
        header_font.setBold(True)

        self.table.setModel(self.model)

        self.table.setColumnWidth(0,35)
        self.table.setColumnWidth(1,35)
        self.table.setColumnWidth(2,35)
        self.table.setColumnWidth(3,60)

        self.table.horizontalHeader().setFont(header_font)
        self.table.verticalHeader().setVisible(False)
        self.table.show()


    def create_circle_around_selected_bubble(self,view_name,radius,center):
        for i,[view_name, actor,center,radius,c_px,_] in enumerate(self.actor_bubble):
            if i < len(self.actor_bubble)-1:
                actor_cirlce = self.actor_selected[i]
                actor_cirlce[2].SetVisibility(0)

        polygonSource = vtkRegularPolygonSource()
        polygonSource.GeneratePolygonOff()
        polygonSource.SetNumberOfSides(100)
        polygonSource.SetRadius(radius)
        polygonSource.SetCenter(center)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(polygonSource.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1,0,0)
        actor.GetProperty().SetOpacity(1)

        renderer = self.LoadMRI.renderers[0][view_name]
        renderer.AddActor(actor)
        self.actor_selected.append([view_name,self.index,actor,polygonSource])



    def update_bubbles_visible(self):
        for i,[view_name, actor,center,radius,c_px,_] in enumerate(self.actor_bubble):
            # Correct spacing per view
            if view_name == "axial":      # z fixed -> (x,y)
                distance = (self.LoadMRI.slice_indices[0][0] - c_px[0])*self.LoadMRI.volumes[0].spacing[0]
            elif view_name == "sagittal":# x fixed -> (z,y)
                distance = (self.LoadMRI.slice_indices[0][2] - c_px[2])*self.LoadMRI.volumes[0].spacing[2]
            elif view_name == "coronal": # y fixed -> (x,z)
                distance = (self.LoadMRI.slice_indices[0][1] - c_px[1])*self.LoadMRI.volumes[0].spacing[1]

            if radius > abs(distance):
                actor.SetVisibility(1)
                radius_new = np.sqrt(radius**2-distance**2)
                self.update_bubble_radius(i, radius_new)
            else:
                #Make invisible: Actor and Outline-Circle
                actor.SetVisibility(0)
                actor_cirlce = self.actor_selected[i]
                actor_cirlce[2].SetVisibility(0)



    def update_bubble_radius(self, index, new_radius):
        actor_entry = self.actor_bubble[index]
        polygonSource = actor_entry[5]
        polygonSource.SetRadius(new_radius)
        polygonSource.Modified()

        #circles of selected bubbles
        if self.row_index == int(index/3) and self.selected:
            actor_entry = self.actor_selected[index]
            actor_entry[2].SetVisibility(1)
            polygonSource = actor_entry[3]
            polygonSource.SetRadius(new_radius)
            polygonSource.Modified()
        else:
            actor_entry = self.actor_selected[index]
            actor_entry[2].SetVisibility(0)

