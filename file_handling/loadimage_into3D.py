# This Python file uses the following encoding: utf-8

import SimpleITK as sitk
import numpy as np
import vtk
from vtk.util import numpy_support

class LoadImage3D:
    def __init__(self,MainWindow, filename):
        """
        Initializes class to add another layer to 3D data.
        """
        self.MW = MainWindow
        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.actors_non_mainimage = {}
        self.img_vtks = {}
        self.vol = {}
        self.LoadMRI.non_mainindex = 0
        self.label_file_imported = False


    def open_file(self,filename):
        """
        Open File, save the data and render
        """
        self.LoadMRI.actors_non_mainimage[self.LoadMRI.non_mainindex] = {}
        self.img_vtks[self.LoadMRI.non_mainindex]  = {}
        self.vol[self.LoadMRI.non_mainindex], self.spacing = self.resample_tofit(filename) #self.resample_tofit(filename)

        # Set-up first slide
        z, y, x = self.LoadMRI.slice_indices[0]
        self.setup_vtkdata(np.fliplr(self.vol[self.LoadMRI.non_mainindex][z, :, :]), self.LoadMRI.vtk_widgets[0]["axial"], "axial",0,)
        self.setup_vtkdata(np.fliplr(self.vol[self.LoadMRI.non_mainindex][:, y, :]), self.LoadMRI.vtk_widgets[0]["coronal"], "coronal",0)
        self.setup_vtkdata(np.fliplr(self.vol[self.LoadMRI.non_mainindex][:, :, x]), self.LoadMRI.vtk_widgets[0]["sagittal"], "sagittal",0)

        #render
        for _,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                widget.GetRenderWindow().Render()

        return self.vol[self.LoadMRI.non_mainindex]



    def setup_vtkdata(self,slice_img:np.array,vtk_widget, view_name:str,image_index:int):
        """
        Create or update the VTK pipeline for a given view (axial, coronal  , sagittal).
        Handles reslice, actor creation, and LUT setup.
        """
        vtk_data = numpy_support.numpy_to_vtk(slice_img.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        img_vtk = vtk.vtkImageData()
        h, w = slice_img.shape
        img_vtk.SetDimensions(w, h, 1)  # VTK expects width x height x depth

        # Correct spacing per view
        if view_name == "axial":      # z fixed -> (y,x)
            spacing = (self.spacing[2], self.spacing[1], 1)
        elif view_name == "coronal": # y fixed -> (z,x)
            spacing = (self.spacing[2], self.spacing[0], 1)
        elif view_name == "sagittal":# x fixed -> (y,z)
            spacing = (self.spacing[1], self.spacing[0], 1)

        img_vtk.SetSpacing(spacing)
        img_vtk.GetPointData().SetScalars(vtk_data)

        # reuse renderer if exists, otherwise create one
        renderer = self.LoadMRI.renderers[0][view_name]

        # High-quality smoothing for better visual clarity
        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(img_vtk)
        #reslice.SetInterpolationModeToNearestNeighbor() #Cubic()  # Options: Nearest, Linear, Cubic
        reslice.SetInterpolationModeToCubic()
        reslice.Update()

        # Add image to actor to then be added to renderer
        actor = vtk.vtkImageActor()
        actor.SetInputData(reslice.GetOutput())
        actor.Modified()
        #actor.GetProperty().SetInterpolationTypeToNearest() #Linear()
        actor.GetProperty().SetInterpolationTypeToCubic()
        actor.GetProperty().SetOpacity(0.6)

        # Attach LUT for contrast and brightness
        vminmax_perc = [0, 1] #reset
        vmin, vmax = np.percentile(self.vol[self.LoadMRI.non_mainindex], [vminmax_perc[0]*100, vminmax_perc[1]*100])
        lut_vtk = vtk.vtkLookupTable()
        lut_vtk.SetTableRange(vmin, vmax)
        lut_vtk.SetValueRange(0.0, 1.0)
        lut_vtk.SetSaturationRange(0.0, 0.0)
        lut_vtk.Build()

        prop = actor.GetProperty()
        prop.SetLookupTable(lut_vtk)
        prop.UseLookupTableScalarRangeOn()  # force LUT range

        # Save actor, renderer, img_vtks to later be used again
        self.LoadMRI.actors_non_mainimage[self.LoadMRI.non_mainindex][view_name] = actor
        self.img_vtks[self.LoadMRI.non_mainindex][view_name] = img_vtk

        print('bin ich hier?',flush=True)

        renderer.AddActor(actor)

        #Update renderer
        vtk_widget.GetRenderWindow().Render()


    def resample_tofit(self,filename):
        """
        Resample the new data to fit to the main image (spacing and size).
        """
        #load new image
        img = sitk.ReadImage(filename)
        #img = sitk.DICOMOrient(img, self.LoadMRI.volumes[0].DICOMOrient)
        if len(img.GetSize())==4:
            img = self.get3Dimage(img)
        img = sitk.Cast(img, sitk.sitkFloat32)

        ref_img = sitk.ReadImage(self.LoadMRI.volumes[0].file_path)
        ref_img = sitk.DICOMOrient(ref_img, self.LoadMRI.volumes[0].DICOMOrient)

        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(ref_img)
        resampler.SetInterpolator(sitk.sitkBSpline) #sitkNearestNeighbor #sitkLinear
        resampler.SetDefaultPixelValue(0)

        # Resample
        resampled = resampler.Execute(img)
        vol = sitk.GetArrayFromImage(resampled)
        spacing = resampled.GetSpacing()[::-1]

        return vol, spacing


    def resample_tofit_bregma(self,filename):
        """
        Resample the new data to fit to the main image (spacing and size).
        """
        #load new image
        img = sitk.ReadImage(filename)
        img = sitk.DICOMOrient(img, self.LoadMRI.volumes[0].DICOMOrient)
        ref_img = sitk.ReadImage(self.LoadMRI.volumes[0].file_path)
        ref_img = sitk.DICOMOrient(ref_img, self.LoadMRI.volumes[0].DICOMOrient)

        # Per-axis minimum spacing across both inputs (or just pick isotropic 0.1)
        target_spacing = tuple(min(a, b) for a, b in zip(img.GetSpacing(), ref_img.GetSpacing()))
        # target_spacing = (0.1, 0.1, 0.1)  # alternative: fully isotropic

        # Build grid size to cover ref_img's physical extent at the new spacing
        ref_extent_mm = [sz * sp for sz, sp in zip(ref_img.GetSize(), ref_img.GetSpacing())]
        new_size = [int(round(extent / sp)) for extent, sp in zip(ref_extent_mm, target_spacing)]

        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputSpacing(target_spacing)
        resampler.SetSize(new_size)
        resampler.SetOutputOrigin(ref_img.GetOrigin())
        resampler.SetOutputDirection(ref_img.GetDirection())
        resampler.SetInterpolator(sitk.sitkBSpline)
        resampler.SetDefaultPixelValue(0)

        resampled = resampler.Execute(img)
        vol = sitk.GetArrayFromImage(resampled)
        spacing = resampled.GetSpacing()[::-1]
        return vol, spacing

    def get3Dimage(self,img):
        """
        Extract first timestamp incase new data is 4D.
        """
        t_index = 0
        size = list(img.GetSize())
        img3d = sitk.Extract(img, size[:3] + [0], [0, 0, 0, t_index])

        return img3d


    def only_display_slide(self, slice_img:np.array, view_name:str,index:int):
        """
        Update an existing vtkImageData with new scalar data for a given slice.
        """
        img_vtk = self.img_vtks[index][view_name]
        vtk_data = numpy_support.numpy_to_vtk(slice_img.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        img_vtk.GetPointData().SetScalars(vtk_data)
        img_vtk.Modified()
        self.LoadMRI.actors_non_mainimage[self.LoadMRI.non_mainindex][view_name].GetMapper().SetInputData(img_vtk)


