# This Python file uses the following encoding: utf-8
import os
import SimpleITK as sitk
import numpy as np
from PySide6.QtWidgets import QFileDialog
import sys
from paths_config import _paths
from core.mrid_tags import MRID_tags
from collections import Counter
from core.load_MRI_file import LoadMRI
from PySide6.QtWidgets import QMessageBox
from file_handling.mri_volume import MRIVolume
from file_handling.metadata import Metadata
from core.image_layer import ImageLayer
from gui_utils.intensity_table import IntensityTable
from gui_utils.buttons_gui3D import ButtonsGUI_3D
from gui_utils.buttons_gui4D import ButtonsGUI_4D
from core.cursor import Cursor
import vtk

class FileLoader:
    def __init__(self,MainWindow):
        """
        Initializes class to add file.
        """
        self.MW = MainWindow
        self.label_file_imported = False
        self.layer_index = 0 #for Image layer later#
        self.MW.Layers = {}
        self.MW.Layers[0] = {}

    ##
    #LoadImage4D is still imported and instantiated in two places:
    #- gui_utils/buttons_gui4D.py lines 437, 523
    #- utils/mrid_inputdialog.py line 146



    def choose_file(self,path=None,add_another_file=False,skip_dialog=False):
        """
        Let the user pick a NIfTI file and confirm the choice.
        Returns the file path, or None if the user cancelled.
        skip_dialog=True returns `path` (an exact file, not a directory)
        immediately, with no picker/confirmation -- for silently restoring a
        previously-used file via load_previous_session().
        """
        if skip_dialog:
            return path
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open NIfTI File",
            _paths['raw_base'] if path is None else path,
            "NIfTI files (*.nii.gz)"
        )
        #User cancelled
        if not file_name:
            return None

        msg_box = QMessageBox()
        if not add_another_file:
            msg_box.setWindowTitle("Open Main File")
            msg_box.setText(f"Do you want to open the file \n {file_name}?")
        else:
            msg_box.setWindowTitle("Add another File")
            msg_box.setText(f"Do you want to add the file \n {file_name}?")
        msg_box.addButton("Yes", QMessageBox.ActionRole)
        btn_no = msg_box.addButton("No, other File", QMessageBox.ActionRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.ActionRole)
        msg_box.exec()
        if msg_box.clickedButton()==btn_cancel:
            return None
        elif msg_box.clickedButton()==btn_no:
            return self.choose_file(path=path,add_another_file=add_another_file)

        return file_name

    def open_user_dialog(self,layer_index=0,add_another_file=False,path=None,skip_dialog=False):
        """
        Open the initial User Dialog when the application starts.
        """
        file_name = self.choose_file(path=path,add_another_file=layer_index!=0,skip_dialog=skip_dialog)
        if file_name is None:
            return None, None

        #pop up asking for the view if 4D data used
        image = sitk.ReadImage(file_name)
        volume = sitk.GetArrayFromImage(image)
        if volume.ndim==4:
            self.is_4d = True
            data_view = self.get_data_view(file_name)
            if data_view is None:
                return None, None
        else:
            self.is_4d = False
            data_view = 'coronal'

        if not hasattr(self.MW,'LoadMRI') or add_another_file:
            self.initialize_file(file_name,layer_index,data_view,0)
        else:
            if not self.MW._confirm_replace_session('mri'):
                return None, None
            self.MW.snapshot_view_state()
            self.MW.restart_gui(file_name,data_view=data_view)
            self.MW.reapply_view_state(file_name)
        #self.MW.refresh_mri_cache_combo()

        return file_name,data_view

    def restore_file(self,file_name):
        """
        Load a previously-used file directly (no picker/confirmation dialog),
        for restoring a saved session. Returns (file_name, data_view), or
        (None, None) if the file can't be read or the user cancels the
        4D-view prompt.
        """
        image = sitk.ReadImage(file_name)
        volume = sitk.GetArrayFromImage(image)
        if volume.ndim==4:
            self.is_4d = True
            data_view = self.get_data_view(file_name)
            if data_view is None:
                return None, None
        else:
            self.is_4d = False
            data_view = 'coronal'

        if not hasattr(self.MW,'LoadMRI'):
            self.initialize_file(file_name,0,data_view,0)
        else:
            # a LoadMRI/Cursor already exists from an earlier file this session --
            # go through the same teardown-and-rebuild restart_gui() uses for a
            # second file, instead of layering a second set of scrollbar/spinbox
            # signal connections on top of the first (which ping-pongs into
            # infinite recursion the next time a scrollbar is moved).
            if not self.MW._confirm_replace_session('mri'):
                return None, None
            self.MW.snapshot_view_state()
            self.MW.restart_gui(file_name,data_view=data_view)
            self.MW.reapply_view_state(file_name)
        #self.MW.refresh_mri_cache_combo()

        return file_name,data_view

    def get_data_view(self,file_name):
        print(file_name,flush=True)
        if 'coronal' in file_name or 'Coronal' in file_name:
            data_view = "coronal"
        elif 'sagittal' in file_name or 'Sagittal' in file_name:
            data_view = "sagittal"
        elif 'axial' in file_name or 'Axial' in file_name:
            data_view = "axial"
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Data view")
            msg_box.setText(f"Could not automatically detect the data view. \n Please select the anatomical view of your 4D data called \n {file_name}")
            btn_axial = msg_box.addButton("Axial", QMessageBox.ActionRole)
            btn_coronal = msg_box.addButton("Coronal", QMessageBox.ActionRole)
            btn_sagittal = msg_box.addButton("Sagittal", QMessageBox.ActionRole)
            btn_cancel = msg_box.addButton("Cancel", QMessageBox.ActionRole)
            msg_box.exec()
            if msg_box.clickedButton()==btn_cancel:
                return None
            data_view = {btn_axial: "axial", btn_coronal: "coronal", btn_sagittal: "sagittal"}.get(msg_box.clickedButton())
        return data_view

    def init_gui(self, data_view, data_index,label_file):
        #TODO: test if img_flipped = sitk.DICOMOrient(image, 'LSA') is better!
        vol = self.MW.LoadMRI.volumes[data_index]
        #Initiate GUI and connect buttons
        if data_index==0:
            self.MW.LoadMRI.session_path = os.path.dirname(os.path.dirname(vol.file_path))
            if not vol.is_4d:
                self.MW.ButtonsGUI_3D = ButtonsGUI_3D(self.MW,data_index,label_file)
            else:
                self.MW.ButtonsGUI_4D = ButtonsGUI_4D(self.MW,data_index,data_view)
        else:
            self.MW.ButtonsGUI_4D.initialize_contrast(data_index,data_view)
            self.MW.ButtonsGUI_4D.initialize_timestamps(data_index,data_view)

    def init_vtk(self, data_view, data_index,layer_index):
        vol = self.MW.LoadMRI.volumes[data_index]
        self.MW.LoadMRI.setup_layer(data_view,data_index,layer_index)
        #Set table for images and intensities
        if layer_index == 0:
            if not vol.is_4d:
                self.MW.LoadMRI.intensity_table[data_index] = IntensityTable(self.MW,data_index,self.MW.ui.tableintensity_data3d,vol.slices[0])
            else:
                table = getattr(self.MW.ui, f"tableintensity_data{data_index}")
                self.MW.LoadMRI.intensity_table[data_index] = IntensityTable(self.MW,data_index,table,vol.slices[0])
            if data_index==0:
                self.MW.Cursor = Cursor(self.MW, self.MW.LoadMRI.cursor_ui,data_index,data_view)
            else:
                #keep the existing cursor, only hook up the widgets of the new data view
                self.MW.Cursor.init_widgets(data_index,data_view)

        self.MW.Cursor.start_cursor(True,data_index,data_view)

    def initialize_file(self,file_name,layer_index,data_view,data_index,full_restart=True,label_file=False,binary_color=None,layer_label=None,visibility_enabled=None):
        if layer_index==0: #not hasattr(self.MW,'LoadMRI'):
            # Create loader
            self.MW.LoadMRI = LoadMRI(self.MW)
            self.prepare_mainvolume(data_index, file_name,data_view)
            self.init_gui(data_view, data_index,label_file)
            #create first Layer
            if not self.is_4d:
                vol = self.MW.LoadMRI.volumes[data_index]
                ##how to do 4d with image_index
                self.MW.Layers[data_index][layer_index] = ImageLayer(
                    vol.slices,vol.spacing,
                    vol.view_names,
                    self.MW.LoadMRI.slice_indices[data_index],
                    self.is_4d,
                    self.MW.LoadMRI.render,
                    contrast_class=self.MW.LoadMRI.contrast[data_index],
                )
                self.init_vtk(data_view, data_index,layer_index)
                self.Metadata = Metadata(self.MW)
            else:
                for image_index in range(len(self.MW.LoadMRI.vtk_widgets)):  # 0, 1, 2
                    self.MW.LoadMRI.renderers[image_index] = {}
                vol = self.MW.LoadMRI.volumes[data_index]
                self.MW.Layers[data_index][layer_index] = ImageLayer(
                    vol.slices,vol.spacing,
                    vol.view_names,
                    self.MW.LoadMRI.slice_indices[data_index],
                    self.is_4d,
                    self.MW.LoadMRI.render,
                    contrast_class=self.MW.LoadMRI.contrast[data_index],
                )
                self.init_vtk(data_view, data_index,layer_index)
                self.Metadata = Metadata(self.MW)
                #self.LoadMRI.setup_layer(data_view, data_index, layer_index)

        else:
            # add another file
            if not self.MW.LoadMRI.volumes[0].is_4d:
                vol, spacing, binary = self.resample_tofit(file_name)
                layer_index = len(self.MW.Layers[data_index])
                if binary:
                    lut = vtk.vtkLookupTable()
                    lut.SetNumberOfTableValues(2)
                    lut.SetTableRange(0, 1)
                    lut.SetTableValue(0, 0,0,0, 0.0)
                    if binary_color is not None:
                        lut.SetTableValue(1, *binary_color, 1.0)
                    elif hasattr(self.MW.LoadMRI,'TrajPlanning') and hasattr(self.MW.LoadMRI.TrajPlanning,'region_to_avoid_img'):
                        lut.SetTableValue(1, 0.12,0.12,0.12, 1.0) #super dark grey
                    else:
                        lut.SetTableValue(1, 1,0,0, 1.0) #red
                    lut.Build()
                else:
                    vminmax_perc = [0, 1] #reset
                    vmin, vmax = np.percentile(vol, [vminmax_perc[0]*100, vminmax_perc[1]*100])
                    lut = vtk.vtkLookupTable()
                    lut.SetTableRange(vmin, vmax)
                    lut.SetValueRange(0.0, 1.0)
                    lut.SetSaturationRange(0.0, 0.0)
                    lut.Build()
                is_forbidden = isinstance(file_name, sitk.Image)
                if layer_label is not None:
                    intensity_filename = layer_label
                else:
                    # every sitk.Image passed in here used to be assumed to be
                    # the forbidden-regions overlay -- callers with their own
                    # sitk.Image overlay now pass an explicit layer_label
                    # instead of being mislabeled by this.
                    intensity_filename = 'Forbidden Regions' if is_forbidden else os.path.basename(file_name)
                if visibility_enabled is None:
                    visibility_enabled = not is_forbidden
                self.MW.Layers[data_index][layer_index] = ImageLayer({0: vol},self.MW.Layers[data_index][0].spacing,self.MW.Layers[data_index][0].view_names,self.MW.LoadMRI.slice_indices[data_index],False,self.MW.LoadMRI.render,lut=lut,opacity=0.6)
                self.MW.Layers[data_index][layer_index].visibility_btn = self.MW.LoadMRI.intensity_table[0].update_table(intensity_filename, vol,0,layer_index,visibility_enabled=visibility_enabled)
                self.init_vtk(data_view, data_index,layer_index)

            else:
                if data_view is not None:
                    keys = list(self.MW.LoadMRI.vtk_widgets[0].keys())
                    idx = keys.index(data_view)
                if "-segmentation" in file_name:
                    self.load_segmentation(file_name,data_view,idx)
                elif "-anat" in file_name:
                    self.load_anat(file_name,data_view,idx)
                elif file_name.endswith(".txt"):
                    tag_data,num_regions,regions = self.get_label_names(file_name)
                    return tag_data,num_regions,regions
                else:
                    print('not yet implemented')


    def add_data_view(self,file_name,data_view,data_index):
        """
        4D only: load another 4D acquisition of the same brain as its own data set
        (own group box, own timestamps and contrast), not as an overlay layer.

        The VTK widgets of `data_index` have to be registered in LoadMRI.vtk_widgets
        before this is called (see ButtonsGUI_4D.add_view_widgets).
        """
        self.MW.Layers[data_index] = {}

        #data
        self.prepare_mainvolume(data_index, file_name, data_view)
        #contrast and timestamp controls of the new group box
        self.init_gui(data_view, data_index, False)
        #vtk
        vol = self.MW.LoadMRI.volumes[data_index]
        self.MW.Layers[data_index][0] = ImageLayer(
            vol.slices,vol.spacing,
            vol.view_names,
            self.MW.LoadMRI.slice_indices[data_index],
            True,
            self.MW.LoadMRI.render,
            contrast_class=self.MW.LoadMRI.contrast[data_index],
        )
        self.init_vtk(data_view, data_index, 0)


    def prepare_mainvolume(self, data_index, file_name,data_view):
        """Pure data preparation — no Qt, no VTK widgets."""
        self.MW.LoadMRI.volumes[data_index] = MRIVolume.from_file(file_name,view_name=data_view)

        if data_index==0:
            self.MW.LoadMRI.opacity = {}
        self.MW.LoadMRI.opacity[data_index] = 100

        # Load file
        self.MW.LoadMRI.slice_indices[data_index] = [
            int(self.MW.LoadMRI.volumes[data_index].slices[0].shape[0]/2),
            int(self.MW.LoadMRI.volumes[data_index].slices[0].shape[1]/2),
            int(self.MW.LoadMRI.volumes[data_index].slices[0].shape[2]/2)
        ]


    def resample_tofit(self,filename):
        """
        Resample the new data to fit to the main image (spacing and size).
        """
        #load new image
        if isinstance(filename, sitk.Image):
            img = filename
        else:
            img = sitk.ReadImage(filename)

        if img.GetNumberOfComponentsPerPixel() > 1:
            img = sitk.VectorIndexSelectionCast(img, 0, sitk.sitkFloat32)

        vol = sitk.GetArrayFromImage(img)
        if vol.ndim == 4:
            vol = vol[0, :, :, :].copy()

        if np.all(np.isin(vol,[0,1])):
            binary = True
        else:
            binary = False

        if len(img.GetSize())==4:
            img = self.get3Dimage(img)
        img = sitk.Cast(img, sitk.sitkFloat32)

        ref_img = sitk.ReadImage(self.MW.LoadMRI.volumes[0].file_path)
        ref_img = sitk.DICOMOrient(ref_img, self.MW.LoadMRI.volumes[0].DICOMOrient)

        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(ref_img)
        resampler.SetInterpolator(sitk.sitkBSpline) #sitkNearestNeighbor #sitkLinear
        resampler.SetDefaultPixelValue(0)

        # Resample
        resampled = resampler.Execute(img)
        vol = sitk.GetArrayFromImage(resampled)
        spacing = resampled.GetSpacing()[::-1]

        return vol, spacing, binary

    def get3Dimage(self,img):
        """
        Extract first timestamp incase new data is 4D.
        """
        t_index = 0
        size = list(img.GetSize())
        img3d = sitk.Extract(img, size[:3] + [0], [0, 0, 0, t_index])

        return img3d


    def label_array_on_grid(self, filename, data_index):
        """
        A label/mask file as an array on data set `data_index`'s voxel grid, or
        None if it cannot be put there.

        label_volume is indexed with that data set's cursor by the paintbrush and
        the intensity table, so a mask arriving in a different orientation or
        resolution is not merely misaligned — it raises IndexError. Note the
        reference is volumes[data_index], not volumes[0]: each 4D view has its
        own orientation code (RSA for coronal/axial, ASR for sagittal), so
        orienting another view's mask like the first one permutes its axes.

        Vector and 4D inputs are reduced to a single 3D scalar component first,
        and the resampling is nearest neighbour so label values survive it.
        """
        volume = self.MW.LoadMRI.volumes[data_index]
        img = sitk.ReadImage(filename)
        if img.GetNumberOfComponentsPerPixel() > 1:
            img = sitk.VectorIndexSelectionCast(img, 0)
        if len(img.GetSize()) == 4:
            img = self.get3Dimage(img)
        if len(img.GetSize()) != 3:
            QMessageBox.warning(
                None, "Cannot load mask",
                f"{os.path.basename(filename)} is {len(img.GetSize())}D; a label "
                "mask has to be a 3D (or 4D) image to be placed on the data grid.")
            return None

        img = sitk.DICOMOrient(img, volume.DICOMOrient)
        ref = volume.oriented_ref_image
        if (img.GetSize() != ref.GetSize() or img.GetSpacing() != ref.GetSpacing()
                or img.GetDirection() != ref.GetDirection()
                or img.GetOrigin() != ref.GetOrigin()):
            resampler = sitk.ResampleImageFilter()
            resampler.SetReferenceImage(ref)
            resampler.SetInterpolator(sitk.sitkNearestNeighbor)
            resampler.SetDefaultPixelValue(0)
            img = resampler.Execute(img)
        return sitk.GetArrayFromImage(img)

    def load_anat(self,filename,data_view,idx):
        """
        Loads files including "-anat" in filename as anatomical region label mask.
        """
        # Create the actor
        vol = self.label_array_on_grid(filename, idx)
        if vol is None:
            return

        self.MW.Paintbrush.label_volume[idx] = vol

        self.MW.LoadMRI.update_slices(idx,data_view)
        self.MW.Paintbrush.histogram()


    def load_segmentation(self,filename,data_view,idx):
        """
        Loads files including "-segmentation" in filename as segmentation label mask.
        """
        vol = self.label_array_on_grid(filename, idx)
        if vol is None:
            return

        self.MW.Paintbrush.label_volume[idx] = np.maximum(self.MW.Paintbrush.label_volume[idx], vol)
        self.MW.Layers[idx][self.MW.Paintbrush.layer_index[idx]].volume[0] = self.MW.Paintbrush.label_volume[idx]
        self.MW.Layers[idx][self.MW.Paintbrush.layer_index[idx]].volume[1] = self.MW.Paintbrush.label_volume[idx]
        self.MW.Layers[idx][self.MW.Paintbrush.layer_index[idx]].volume[2] = self.MW.Paintbrush.label_volume[idx]

        self.MW.LoadMRI.intensity_table[idx].intensity_volumes[self.MW.Paintbrush.layer_index[idx]] = self.MW.Paintbrush.label_volume[idx]

        # Refresh all
        self.MW.LoadMRI.update_slices(idx,data_view)

        # Recompute heatmap for any custom ROIs in the loaded segmentation
        if hasattr(self.MW.LoadMRI, 'mrid_tags'):
            roi_indices = np.unique(self.MW.Paintbrush.label_volume[idx])
            roi_indices = roi_indices[roi_indices > self.MW.LoadMRI.mrid_tags.num_regions]
            if len(roi_indices):
                self.MW.LoadMRI.mrid_tags.update_heatmap(data_view, idx, roi_indices)

    def get_label_names(self,filename):
        """
        Loads label names in case text file in uploaded.
        """
        labels = []
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue
                # Split by tab or spaces
                parts = line.split()
                # The last column is the quoted label name
                if len(parts) >= 8:
                    label = parts[-1].strip('"')
                    labels.append(label)
        labels.pop(0)
        num_regions = 0
        regions = []
        tag_data = []
        pure_labels = [l.rstrip("0123456789") for l in labels]
        counts = Counter(pure_labels)
        counts_dict = dict(counts)

        tag_labels = False

        for i, label in enumerate(labels):
            if label.endswith("1"):
                tag_data.append((pure_labels[i],counts_dict[pure_labels[i]]))
                tag_labels = True
            elif not tag_labels:
                num_regions +=1
                regions.append([label,1])

        if not hasattr(self.MW.LoadMRI, "mrid_tags"):
            self.MW.LoadMRI.mrid_tags = MRID_tags(self.MW, tag_data,num_regions,regions)
        else:
            self.MW.LoadMRI.mrid_tags.tag_data = tag_data
            self.MW.LoadMRI.mrid_tags.num_regions = num_regions
            self.MW.LoadMRI.mrid_tags.region_data = regions


        return tag_data,num_regions,regions



