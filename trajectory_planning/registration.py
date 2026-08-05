# This Python file uses the following encoding: utf-8
import os
import re
import sys
import json as _json
import numpy as np
import SimpleITK as sitk
import ants
import nibabel as nib
from PySide6.QtWidgets import QDockWidget
from gui_utils.busy_overlay import BusyOverlay
from trajectory_planning.visualisation3D import Visualisation3D
from core.registration import Registration

_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)

class TpRegistration:
    def register_to_main_img(self,filename):
        self.ui.comboBox_movingimg.addItem(os.path.basename(filename))
        self.LoadMRI.movingimg_filename.append(filename)
        self.LoadMRI.coarsest_index = 1 #comboBox_coarsest
        self.LoadMRI.finest_index = 0 #comboBox_finest

        Registration(self.LoadMRI,self.MW.ButtonsGUI_3D,0)
        m = re.search(r"ind_(\d+)", self.main_file)
        fixed_ind = int(m.group(1))

        moving_ind = int(filename.split("ind_")[1].split(".")[0])
        transform_filename = f"transformation-ind_{moving_ind}-to-ind_{fixed_ind}.txt"
        transform_file_path = os.path.join(self.LoadMRI.session_path, "anat", transform_filename)

        transform = sitk.ReadTransform(transform_file_path)
        transform = transform.GetInverse()

        fixed = ants.image_read(self.main_file)
        moving = ants.image_read(filename)

        img_aligned = ants.apply_transforms(
            fixed=fixed,
            moving=moving,
            transformlist=transform_file_path,
            interpolator="lanczosWindowedSinc", #bSpline",
        )

        new_name = filename[:-7]+f"-aligned_to_ind_{fixed_ind}.nii.gz"
        ants.image_write(img_aligned, new_name)

        self.MW.FileLoader.layer_index += 1
        self.MW.FileLoader.initialize_file(new_name,self.MW.FileLoader.layer_index,'coronal',0)
        #add to registration combobox
        self.MW.ui.comboBox_movingimg.addItem(os.path.basename(new_name))
        self.LoadMRI.movingimg_filename.append(new_name)
        self.LoadMRI.combo_Regimgname = self.MW.ui.comboBox_movingimg

        original_path = f"{'_'.join(self.LoadMRI.volumes[0].file_path.split('_')[:-1])}.nii.gz"
        mask_path = original_path[:-7] + "-mask.nii.gz"
        if os.path.exists(mask_path):
            self.MW.FileLoader.layer_index += 1
            self.MW.FileLoader.initialize_file(mask_path,self.MW.FileLoader.layer_index,'coronal',0)
            #add to registration combobox
            self.MW.ui.comboBox_movingimg.addItem(os.path.basename(mask_path))
            self.LoadMRI.movingimg_filename.append(mask_path)
            self.mask_idx = self.MW.FileLoader.layer_index

        return new_name


    def get_shank_line(self,transformPath=None):
        self.MW.overlay = BusyOverlay(self.MW, message="Loading data for next step, please wait…")
        if transformPath is not None:
            self.MW.overlay.run(self.warp_red_areas, transformPath)
        else:
            self.MW.overlay.run(self.do_get_shank_line)

    def do_get_shank_line(self):
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(1)

        region_to_avoid_img = None
        if hasattr(self,'region_to_avoid_img'):
            region_to_avoid_img = self.region_to_avoid_img

        #load atlas file for further trajectory planning
        path_main = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        self.MW.restart_gui(path_main, full_restart=False,label_file=True,data_view='coronal')

        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.TrajPlanning = self
        self.LoadMRI.show_edge_mask = False

        if not hasattr(self.LoadMRI,'tg_edge_mask'):
            self.LoadMRI.tp_imgvtk = {}
            self.LoadMRI.tp_actor = {}
            self.LoadMRI.tp_renderer = {}
            self.create_edge_mask()

        self.ui.pushButton_tp_deep.clicked.connect(self.get_deepest_point)
        self.ui.pushButton_tp_insert.clicked.connect(self.get_insert_point)
        self.ui.pushButton_edgemask.clicked.connect(self.show_edge_mask) #checkable
        self.ui.spinBox_tp_channels.valueChanged.connect(self.change_shank_parameters)
        self.ui.spinBox_tp_separation.valueChanged.connect(self.change_shank_parameters)
        self.show_label = True #is checked
        self.ui.checkBox_brain_region.toggled.connect(lambda checked: self.show_brainregion(checked))

        if region_to_avoid_img is not None:
            self.MW.FileLoader.layer_index += 1
            self.MW.FileLoader.initialize_file(region_to_avoid_img,self.MW.FileLoader.layer_index,'coronal',0)
            self.region_to_avoid = sitk.GetArrayFromImage(region_to_avoid_img)

        # load atlas for 3d visualisation
        self.Vis3D = Visualisation3D(self.MW)
        # load dwi atlas
        if not hasattr(self,'dwi'):
            dwi_path=os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
            nii_dwi=nib.load(dwi_path)
            dwi=np.asanyarray(nii_dwi.dataobj)
            self.dwi=dwi[:,:,:,0]

    def paint_red_areas(self):
        self.ui.stackedWidget_3d.setVisible(False)
        layout = self.ui.page_3D.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)

        if self.mask_idx is not None:
            layer = self.LoadMRI.MW.Layers[0][self.mask_idx]
            layer.toggle_visibility(False,self.LoadMRI.MW.Layers[0][self.mask_idx].visibility_btn)

        self.MW.ButtonsGUI_3D.initialize_paintbrush(red_only=True)
        #increase maximum due to resampling
        self.LoadMRI.brush['size'].setRange(1,30)
        self.LoadMRI.brush['size_slider'].setRange(1,30)

        self.ui.pushButton_paint_done.setVisible(True)


    def warp_red_areas(self, transform_path):
        label_vol = self.MW.Layers[0][self.MW.Paintbrush.layer_index[0]].volume[0]
        label_img = sitk.GetImageFromArray(label_vol)
        label_img.CopyInformation(self.LoadMRI.volumes[0].oriented_ref_image)
        label_img_rawOrientation = sitk.DICOMOrient(label_img, self.LoadMRI.volumes[0].raw_DICOMOrient)
        #resample to atlas
        label_img_raw_np = sitk.GetArrayFromImage(label_img_rawOrientation)

        raw_ref = self.LoadMRI.volumes[0].raw_ref_image
        label_ants = ants.from_numpy(
            label_img_raw_np.T.astype(np.float32),
            origin=list(raw_ref.GetOrigin()),
            spacing=list(raw_ref.GetSpacing()),
            direction=np.array(raw_ref.GetDirection()).reshape(3, 3),
        )
        #register to atlas
        raw_fixed = ants.image_read(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        label_aligned = ants.apply_transforms(
            fixed=raw_fixed,
            moving=label_ants,
            transformlist=transform_path,
            interpolator="nearestNeighbor",
        )

        atlas_img = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        self.region_to_avoid_img = sitk.GetImageFromArray(label_aligned.numpy().T)
        self.region_to_avoid_img.CopyInformation(atlas_img) #(self.LoadMRI.volumes[0].raw_ref_image)
        self.ui.stackedWidget_3d.setVisible(True)
        dock = self.MW.findChild(QDockWidget, "dock_paintbrush")
        dock.close()
        self.do_get_shank_line()
