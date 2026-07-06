# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject
import vtk
from vtk.util import numpy_support
import numpy as np
from utils.zoom import Zoom
from utils.scale_bar import Scale
from file_handling.mri_volume import MRIVolume
from gui_utils.intensity_table import IntensityTable
from utils.contrast import Contrast

class LoadMRI(QObject):
    """
    Handles loading, managing, and displaying MRI volumes (3D and 4D).
    """
    def __init__(self, MW,parent=None):
        super().__init__(parent)
        # Core volume data
        self.MW = MW
        self.volumes: dict[int, MRIVolume] = {}
        self.slice_indices = {}
        self.slice_indices[0] = [0, 0, 0]  # z y x (for cursor +1)

        # GUI-related
        self.contrast_ui_elements = {}
        self.zoom_tf ={}
        self.zoom_tf['axial']=False
        self.zoom_tf['coronal']=False
        self.zoom_tf['sagittal']=False
        self.scale_bar = {}
        self.threshold_on = False

        # Rendering
        self.renderers = {}
        self.renderers[0] = {}
        self.is_first_slice = True

        self.intensity_table: dict[int, IntensityTable] = {}
        self.contrast: dict[int, Contrast] = {}

        self.Layers = MW.Layers



    def setup_layer(self,data_view,data_index,layer_index,visibility_at_start=True):
        """
        Initialize data structures after data is loaded.
        Emits `fileLoaded` signal once data is loaded.
        """
        if data_index not in self.renderers:
            self.renderers[data_index] = {}
        #for layer_index, layer in layers.items():
        main_layer = self.Layers[data_index][0]
        for view_name in main_layer.view_names:
            if view_name not in self.renderers[data_index]:
                if not self.volumes[0].is_4d:
                    self.setup_renderer(data_index,view_name)
                    self.setup_extras(data_index,view_name,data_view)
                else:
                    for img_idx in range(len(self.vtk_widgets)):
                        self.setup_renderer(img_idx,view_name)
                        self.setup_extras(data_index,view_name,data_view,img_idx=img_idx)

            #3d
            layer = self.Layers[data_index][layer_index]
            if not self.volumes[0].is_4d:
                self.renderers[data_index][view_name].AddActor(layer.actors[view_name][0])
                if not visibility_at_start:
                    layer.actors[view_name][0].SetVisibility(visibility_at_start)
                #Update renderer
                if self.is_first_slice:
                    self.renderers[data_index][view_name].ResetCamera()
                    self.zoom_tf[view_name]=False
            #4d
            else:
                for img_idx in range(len(self.vtk_widgets)):
                    self.renderers[img_idx][view_name].AddActor(layer.actors[view_name][img_idx])
                    if not visibility_at_start:
                        layer.actors[view_name][img_idx].SetVisibility(visibility_at_start)
                    #Update renderer
                    if self.is_first_slice:
                        self.renderers[img_idx][view_name].ResetCamera()
                        self.zoom_tf[view_name]=False

        if self.is_first_slice:
            #fit to window to make it look nice
            if self.volumes[0].is_4d:
                Zoom.fit_to_window(self.vtk_widgets[0][data_view], self.vtk_widgets.values(), self.scale_bar, self.vtk_widgets, data_index)
            else: #3d
                Zoom.fit_to_window(self.vtk_widgets[0]["coronal"], self.vtk_widgets.values(), self.scale_bar, self.vtk_widgets, data_index)
            self.is_first_slice = False

        self.render()


    def setup_renderer(self,data_index,view_name):
        vtk_widget = self.vtk_widgets[data_index][view_name]
        renderer = vtk.vtkRenderer()
        vtk_widget.GetRenderWindow().AddRenderer(renderer)
        vtk_widget.GetRenderWindow().SetMultiSamples(16)
        self.renderers[data_index][view_name] = renderer

        camera = renderer.GetActiveCamera()
        cx, cy, cz = camera.GetFocalPoint()
        pos = camera.GetPosition()
        camera.SetPosition(cx, cy, pos[2])
        ##TEST
        #transform = vtk.vtkTransform()
        #transform.Scale(-1, 1, 1)
        #camera.SetUserTransform(transform)
        ##TEST
        half_height = camera.GetParallelScale()
        width_px, height_px = renderer.GetSize()
        if height_px == 0:
            return
        half_width = half_height * width_px / height_px
        Zoom.bounds[view_name] = [cx - half_width, cx + half_width, cy - half_height, cy + half_height]


    def setup_extras(self,data_index,view_name,data_view,img_idx=None):
        if not self.volumes[0].is_4d:
            img_idx = data_index
            img_vtk = self.Layers[data_index][0].img_vtks[view_name][0]
        else:
            img_vtk = self.Layers[data_index][0].img_vtks[view_name][img_idx]
        renderer = self.renderers[img_idx][view_name]
        vtk_widget = self.vtk_widgets[img_idx][view_name]

        #Add axes to each widget
        self.add_axes(renderer, img_vtk, view_name)
        self.minimap.add_minimap(view_name,img_vtk,img_idx,vtk_widget,data_index)

        # Add scale_bar and minimap
        if self.volumes[0].is_4d and data_view!=view_name:
            pass #continue
        else:
            if not self.volumes[0].is_4d or img_idx == len(self.vtk_widgets) - 1:
                renderer = self.renderers[data_index][view_name]
                if view_name not in self.scale_bar:
                    self.scale_bar[view_name] = Scale(self)
                self.scale_bar[view_name].create_bar(renderer,view_name,length_cm=1.0)



    def update_slices(self,image_index:int,data_index,data_view):
        """
        Refresh all slice views (axial, coronal, sagittal) based on current slice indices.
        Handles threshold overlays and distance measurement visibility.
        """
        z, y, x = self.slice_indices[data_index].copy() if hasattr(self, 'slice_indices') else [0, 0, 0]

        if self.threshold_on == True:
            layer = self.Layers[0][self.SegmentationGUI.layer_index]
            layer.update_vtk([z,y,x])
        else:
            for data_index, layers in self.Layers.items():
                for layer_index, layer in layers.items():
                    layer.update_vtk([z,y,x])

        #measurement
        if hasattr(self.MW,'Measurement'):
            self.MW.Measurement.update_measurement_visibility([z,y,x])

        #Trajectory Planning
        if hasattr(self,'TrajPlanning'):
            self.TrajPlanning.check_points_in_slice()

        #Segmentation
        if hasattr(self,'segmentation_mask'):
            self.SegEvolution.update_evolution_initializtion()
        elif hasattr(self,'SegInitialization'):
            self.SegInitialization.update_bubbles_visible()

        self.render()

        ##
        return


        if not self.volumes[0].is_4d:
            self.only_display_slide(np.fliplr(self.volumes[data_index].slices[image_index][:, y, :]), "coronal",0)
            self.only_display_slide(np.fliplr(self.volumes[data_index].slices[image_index][:, :, x]), "sagittal",0)
            self.only_display_slide(np.fliplr(self.volumes[data_index].slices[image_index][z, :, :]), "axial",0)
        else:
            if data_view=='sagittal':
                self.only_display_slide(self.volumes[data_index].slices[image_index][z, :, :].T, data_view,image_index)
            else:
                self.only_display_slide(self.volumes[data_index].slices[image_index][z, :, :], data_view,image_index)


        if hasattr(self,'mrid_tags') and hasattr(self.mrid_tags,'actor_heatmap'):
            if data_view=='sagittal':
                slice_img = np.flip(self.mrid_tags.heatmap_slice[data_index][:, :, z],axis=0)
            else:
                slice_img = np.flip(self.mrid_tags.heatmap_slice[data_index][:, :, z].T)
            # Always flatten in Fortran order for VTK
            vtk_data = numpy_support.numpy_to_vtk(slice_img.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
            h, w = slice_img.shape
            spacing = (self.volumes[data_index].spacing[2], self.volumes[data_index].spacing[1], 1)
            img_vtk = vtk.vtkImageData()
            img_vtk.SetDimensions(w, h, 1)  # VTK expects width x height x depth
            img_vtk.SetSpacing(spacing)
            img_vtk.GetPointData().SetScalars(vtk_data)

            self.mrid_tags.actor_heatmap[data_index].SetInputData(img_vtk)
            self.mrid_tags.actor_heatmap[data_index].Modified()
            #self.vtk_widgets_heatmap['axial'].GetRenderWindow().Render()
            self.mrid_tags.add_legend(slice_img,False,data_index)



    def add_axes(self, renderer: vtk.vtkRenderer, img_vtk: vtk.vtkImageData, view_name:str):
        """
        Add L/R/A/P/S/I axes to the given view for orientation.
        """
        center = 0.5
        up = 0.9
        if view_name == "coronal":      # slice in XY plane
            texts = [("L", 0.95, center),
                     ("R", 0.05, center),
                     ("S", center, up),
                     ("I", center, 0.05)]

        elif view_name == "axial":  # slice in XZ plane
            texts = [("L", 0.95, center),
                     ("R", 0.05, center),
                     ("A", center, up),
                     ("P", center, 0.05)]

        elif view_name == "sagittal": # slice in YZ plane
            texts = [("P", 0.95, center),
                     ("A", 0.05, center),
                     ("S", center, up),
                     ("I", center, 0.05)]

        for text, x, y in texts:
            actor = vtk.vtkTextActor()
            actor.SetInput(text)
            prop = actor.GetTextProperty()
            if self.volumes[0].is_4d and view_name != 'axial':
                prop.SetFontSize(10)
            else:
                prop.SetFontSize(16)
            prop.SetColor(1, 1, 0)  # red text
            prop.BoldOn()
            actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
            actor.SetPosition(x, y)

            renderer.AddActor2D(actor)


    def render(self):
        for _,vtk_widget_image in self.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                widget.GetRenderWindow().Render()