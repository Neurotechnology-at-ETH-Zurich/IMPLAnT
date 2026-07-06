# This Python file uses the following encoding: utf-8
from vtk.util import numpy_support
import vtk
import numpy as np
import os
from PySide6.QtGui import QIcon
import SimpleITK as sitk

class ImageLayer:
    def __init__(self, volume,spacing,view_names,slice_indices,is_4d,render_fct,contrast_class=None, vtk_dtype=vtk.VTK_FLOAT,interpolation='cubic', opacity=1.0,lut=None,visibility_at_start=True, flip=True):
        self.volume = volume
        self.spacing = spacing
        self.is_4d = is_4d
        self.view_names = view_names
        self.opacity = opacity
        self.vtk_dtype = vtk_dtype
        self.interpolation = interpolation
        self.render_fct = render_fct
        self.visibility_at_start = visibility_at_start
        self.flip = flip

        if np.all(np.isin(self.volume,[0,1])):
            self.is_binary = True
        else:
            self.is_binary = False

        self.visible = True
        self.actors = {vn: {} for vn in self.view_names}
        self.img_vtks = {vn: {} for vn in self.view_names}
        self.lut_vtk = contrast_class.lut_vtk if contrast_class else lut

        for image_index, vol in self.volume.items():
            for view_name in self.view_names:
                self.setup_vtk(slice_indices,image_index,vol,view_name)


    def setup_vtk(self,slice_indices,image_index,vol,view_name):
        """
        Create or update the VTK pipeline for a given view (axial, coronal  , sagittal).
        Handles reslice, actor creation, and LUT setup.
        """
        z,y,x = slice_indices

        # Correct spacing per view
        if not self.is_4d:
            if view_name == "axial":      # z fixed -> (y,x)
                slice_img = np.fliplr(vol[z, :, :]) if self.flip else vol[z, :, :]
                spacing = (self.spacing[2], self.spacing[1], 1)
            elif view_name == "coronal": # y fixed -> (z,x)
                slice_img = np.fliplr(vol[:, y, :]) if self.flip else vol[:, y, :]
                spacing = (self.spacing[2], self.spacing[0], 1)
            elif view_name == "sagittal":# x fixed -> (y,z)
                slice_img = np.fliplr(vol[:, :, x]) if self.flip else vol[:, :, x]
                spacing = (self.spacing[1], self.spacing[0], 1)
        else:
            #if view_name == "axial" or view_name == "coronal":
            slice_img = np.fliplr(vol[z, :, :])
            spacing = (self.spacing[2], self.spacing[1], 1)

        vtk_data = numpy_support.numpy_to_vtk(slice_img.ravel(), deep=True, array_type=self.vtk_dtype)
        img_vtk = vtk.vtkImageData()
        h, w = slice_img.shape
        img_vtk.SetDimensions(w, h, 1)  # VTK expects width x height x depth

        img_vtk.SetSpacing(spacing)
        img_vtk.GetPointData().SetScalars(vtk_data)

        # High-quality smoothing for better visual clarity
        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(img_vtk)
        if self.interpolation=='nearest':
            reslice.SetInterpolationModeToNearestNeighbor()
        else:
            reslice.SetInterpolationModeToCubic()
        reslice.Update()

        # Add image to actor to then be added to renderer
        actor = vtk.vtkImageActor()
        actor.SetInputData(reslice.GetOutput())
        #if self.interpolation=='nearest':
        #    actor.GetProperty().SetInterpolationTypeToNearest()
        if self.interpolation=='cubic':
            actor.GetProperty().SetInterpolationTypeToCubic()
        actor.GetProperty().SetOpacity(self.opacity)

        # Attach LUT for contrast and brightness
        if isinstance(self.lut_vtk, dict): # and image_index in self.lut_vtk:
            prop = actor.GetProperty()
            prop.SetLookupTable(self.lut_vtk[image_index])
            prop.UseLookupTableScalarRangeOn()  # force LUT range
        else:
            prop = actor.GetProperty()
            prop.SetLookupTable(self.lut_vtk)
            prop.UseLookupTableScalarRangeOn()

        # Save actor, renderer, img_vtks to later be used again
        self.actors[view_name][image_index] = actor
        self.img_vtks[view_name][image_index] = img_vtk


    def update_vtk(self,slice_indices):
        z,y,x = slice_indices
        for image_index, vol in self.volume.items():
            flip = np.fliplr if self.flip else (lambda a: a)
            if not self.is_4d:
                self.update_slide_img(flip(vol[:, y, :]), "coronal",image_index)
                self.update_slide_img(flip(vol[:, :, x]), "sagittal",image_index)
                self.update_slide_img(flip(vol[z, :, :]), "axial",image_index)
            else:
                self.update_slide_img(flip(vol[z, :, :]), self.view_names[0],image_index)


    def update_slide_img(self, slice_img:np.array, view_name:str,image_index:int):
        """
        Update an existing vtkImageData with new scalar data for a given slice.
        """
        img_vtk = self.img_vtks[view_name][image_index]
        actor = self.actors[view_name][image_index]
        vtk_data = numpy_support.numpy_to_vtk(slice_img.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        img_vtk.GetPointData().SetScalars(vtk_data)
        img_vtk.Modified()
        actor.GetMapper().SetInputData(img_vtk)


    def update_lut(self, index, vmin, vmax):
        """Update the display range of overlay index's LUT in all views and re-render."""
        if isinstance(self.lut_vtk, dict):
            for lut in self.lut_vtk.values():
                lut.SetTableRange(vmin, vmax)
                lut.Build()
        else:
            self.lut_vtk.SetTableRange(vmin, vmax)
            self.lut_vtk.Build()
        self.render_fct()

    def set_opacity(self, value,slider=None,box=None):
        #for layer_index, layer in self.LoadMRI.MW.Layers[self.data_index].items():
        for vn, actors_by_index in self.actors.items():
            for idx, actor in actors_by_index.items():
                #for actor in self.actors.values():
                actor.GetProperty().SetOpacity(value/100)

        if slider is not None:
            slider.blockSignals(True)
            box.blockSignals(True)
            slider.setValue(value)
            box.setValue(value)
            slider.blockSignals(False)
            box.blockSignals(False)

        self.render_fct()


    def toggle_visibility(self, checked,btn):
        """
        Toggle visibility of a selected layer in all three orthogonal views.
        """
        if not hasattr(self,'icon_visible'):
            icon_dir = os.path.join(os.path.dirname(os.path.dirname((__file__))), "Icons/mri")
            self.icon_visible = QIcon(os.path.join(icon_dir, "eye_open.png"))
            self.icon_hidden = QIcon(os.path.join(icon_dir, "eye_closed.png"))

        #if not self.is_4d:
            #for layer_index, layer in self.LoadMRI.MW.Layers[self.data_index].items():
        for vn, actors_by_index in self.actors.items():
            for idx, actor in actors_by_index.items():
                actor.SetVisibility(checked)

        if btn is not None:
            if checked:
                btn.setIcon(self.icon_visible)
            else:
                btn.setIcon(self.icon_hidden)

        self.render_fct()


    def timestamp4D_changed(self,index: int,image_index,array_4d):
        """
        Update the current timestamp (4D volume selection).
        """
        self.volume[image_index] = array_4d[index, :, :, :].copy()

        #return vol



    def save_layer(self,file_name,save_path):
        """
        Save the layer volume as a NIfTI (.nii.gz) file.
        Prompts the user for location and name. Copies image metadata from the original MRI.
        Emits:
            fileSaved(str): The path to the saved file.
        """
        # Convert your NumPy label array back to a SimpleITK image
        image = sitk.GetImageFromArray(self.volume)
        ref_image = sitk.ReadImage(self.LoadMRI.volumes[data_index].file_path)
        image.CopyInformation(ref_image)

        sitk.WriteImage(image, file_name)
        self.fileSaved.emit(save_path)  # emit the signal



    #  9. Binary LUT not handled — if is_binary, the LUT should be red/black (2 values), not the grayscale from Contrast. Add a _build_binary_lut() helper and use it when is_binary and no contrast_class.


    #    def set_lut_range(self, vmin, vmax):
    #        self.lut.SetTableRange(vmin, vmax)
    #        self.lut.Build()
  #
    #Then LoadMRI (or MW) just keeps a list:
    #self.layers: list[ImageLayer] = []
    ## main image
    #self.layers.append(ImageLayer.from_file(file_path, ...))
    ## overlay
    #self.layers.append(ImageLayer.from_file(file_path, resample_to=self.layers[0], ...))
    #self.layers[0].actors["axial"]   # main image
    #self.layers[3].actors["axial"]   # overlay index 2

