# This Python file uses the following encoding: utf-8
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor,vtkPolyDataMapper
import numpy as np
from scipy import ndimage
import vtk
import SimpleITK as sitk
from PySide6 import QtWidgets
import os
import json as _json
from PySide6.QtWidgets import QWidget,QVBoxLayout, QMessageBox
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'paths_config.json')) as _f:
    _paths = _json.load(_f)
import ants
from PySide6.QtWidgets import QTableWidgetItem
from trajectory_planning.visualisation3D import Visualisation3D
from core.registration import Registration
import re
from core.image_layer import ImageLayer
from mrid_utils.channel_mapper import plot_dwi_1D_cross_section
import nibabel as nib
from PySide6.QtWidgets import QDockWidget
from gui_utils.busy_overlay import BusyOverlay
from itertools import groupby
from trajectory_planning.file_input_output import FileOutput

## EVERYTHING IS WRITTEN WRT XYZ (not zyx)

class TrajectoryPlanning:
    def __init__(self,MW,ui,file_names,transformPath):
        self.MW = MW
        self.ui = ui
        self.LoadMRI = MW.LoadMRI
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(0)

        self.main_file = file_names[0]
        self.second_file = file_names[1]
        self.mask_idx = None
        self.shank_number = 0
        self.line_actor = {}
        self.line_actor[self.shank_number] = {}
        self.label_actor = {}
        self.label_actor[self.shank_number] = {}

        if self.second_file:
            self.second_file = self.register_to_main_img(self.second_file)

        self.ui.pushButton_tp_bregma.clicked.connect(self.get_bregma)
        self.ui.pushButton_tp_lambda.clicked.connect(self.get_lambda)
        self.ui.pushButton_coronalView.clicked.connect(lambda checked: self.change_view_coronal(checked))
        self.ui.pushButton_sagittalView.clicked.connect(lambda checked: self.change_view_sagittal(checked))
        self.ui.pushButton_axialView.clicked.connect(lambda checked: self.change_view_axial(checked))


        self.selecting_point = False
        self.show_label = False
        self.point_actor_bregma = {}
        self.point_actor_lambda = {}
        self.point_actor_deep = {}
        self.point_actor_insert = {}
        self.point_actor_deep[self.shank_number] = {}
        self.point_actor_insert[self.shank_number] = {}
        self.text_actor = {}
        self.clicked_viewname = "axial"

        self.coords_bregma = None
        self.coords_lambda = None
        # [shank] -> array
        self.coords_deepest_point = {}
        self.coords_insert_point= {}
        self.mri_deep = {}
        self.mri_insert = {}
        self.direction_atlas = {}
        self.channel_points = {}
        self.coords_deepest_point[self.shank_number] = None
        self.coords_insert_point[self.shank_number] = None
        self.mri_deep[self.shank_number] = None
        self.mri_insert[self.shank_number] = None
        self.direction_atlas[self.shank_number] = None
        self.channel_points[self.shank_number] = []
        self.atlas_shank_end = {}
        self.atlas_shank_end[self.shank_number] = None


        self.LoadMRI.tp_imgvtk = {}
        self.LoadMRI.show_edge_mask = False

        self.movingidx_bregma, self.movingidx_lambda, atlas_distance = self.get_atlas_coords(self.LoadMRI.volumes[0],transformPath)
        self.ui.spinBox_atlas_bregma_x.setValue(self.movingidx_bregma[0]+1)
        self.ui.spinBox_atlas_bregma_y.setValue(self.movingidx_bregma[1]+1)
        self.ui.spinBox_atlas_bregma_z.setValue(self.movingidx_bregma[2]+1)
        self.ui.spinBox_atlas_lambda_x.setValue(self.movingidx_lambda[0]+1)
        self.ui.spinBox_atlas_lambda_y.setValue(self.movingidx_lambda[1]+1)
        self.ui.spinBox_atlas_lambda_z.setValue(self.movingidx_lambda[2]+1)
        self.ui.doubleSpinBox_distanceAtlas.setValue(atlas_distance)
        self.ui.spinBox_tp_bregma_x.valueChanged.connect(self.change_bregma)
        self.ui.spinBox_tp_bregma_y.valueChanged.connect(self.change_bregma)
        self.ui.spinBox_tp_bregma_z.valueChanged.connect(self.change_bregma)
        self.ui.spinBox_tp_lambda_x.valueChanged.connect(self.change_lambda)
        self.ui.spinBox_tp_lambda_y.valueChanged.connect(self.change_lambda)
        self.ui.spinBox_tp_lambda_z.valueChanged.connect(self.change_lambda)

        self.ui.pushButton_tp_next0.clicked.connect(lambda _: self.get_shank_line(None))
        self.ui.pushButton_redAreas.clicked.connect(self.paint_red_areas)
        self.ui.pushButton_paint_done.clicked.connect(lambda _: self.get_shank_line(transformPath))
        #spinBox.setKeyboardTracking(False)
        self.ui.spinBox_tp_insert_x.setKeyboardTracking(False)
        self.ui.spinBox_tp_insert_y.setKeyboardTracking(False)
        self.ui.spinBox_tp_insert_z.setKeyboardTracking(False)
        self.ui.spinBox_tp_deep_x.setKeyboardTracking(False)
        self.ui.spinBox_tp_deep_y.setKeyboardTracking(False)
        self.ui.spinBox_tp_deep_z.setKeyboardTracking(False)
        self.ui.spinBox_tp_insert_x.valueChanged.connect(self.change_insert_point)
        self.ui.spinBox_tp_insert_y.valueChanged.connect(self.change_insert_point)
        self.ui.spinBox_tp_insert_z.valueChanged.connect(self.change_insert_point)
        self.ui.spinBox_tp_deep_x.valueChanged.connect(self.change_deepest_point)
        self.ui.spinBox_tp_deep_y.valueChanged.connect(self.change_deepest_point)
        self.ui.spinBox_tp_deep_z.valueChanged.connect(self.change_deepest_point)

        self.ui.spinBox_tp_bregma_x.setMaximum(self.LoadMRI.volumes[0].slices[0].shape[2])
        self.ui.spinBox_tp_bregma_y.setMaximum(self.LoadMRI.volumes[0].slices[0].shape[1])
        self.ui.spinBox_tp_bregma_z.setMaximum(self.LoadMRI.volumes[0].slices[0].shape[0])
        self.ui.spinBox_tp_lambda_x.setMaximum(self.LoadMRI.volumes[0].slices[0].shape[2])
        self.ui.spinBox_tp_lambda_y.setMaximum(self.LoadMRI.volumes[0].slices[0].shape[1])
        self.ui.spinBox_tp_lambda_z.setMaximum(self.LoadMRI.volumes[0].slices[0].shape[0])

        #pyl detection using dwi
        self.ui.pushButton_PyLdetection.clicked.connect(self.show_canvas)

        self.ui.comboBox_Shanks.addItem("Shank 1")
        self.ui.pushButton_addShank.clicked.connect(self.add_shank)
        self.ui.comboBox_Shanks.currentIndexChanged.connect(self.select_shank)
        self.ui.pushButton_removeShank.clicked.connect(self.remove_shank)
        self.ui.pushButton_SaveTraj.clicked.connect(lambda _: FileOutput(self.MW, self.MW.data_pre_resampled,parent=self.MW).exec())


    def get_bregma(self):
        self.selecting_point = True
        self.coords_bregma = self.LoadMRI.slice_indices[0][::-1].copy()
        self.set_value(self.coords_bregma.copy(),self.ui.spinBox_tp_bregma_x,self.ui.spinBox_tp_bregma_y,self.ui.spinBox_tp_bregma_z)
        #draw bregma red
        self.draw_point(self.coords_bregma,(1,0,0),'bregma')
        self.render()
        d = self.calculate_distance(self.coords_bregma,self.movingidx_bregma,return_distance=True)
        self.set_value(d,self.ui.doubleSpinBox_d_bregmax,self.ui.doubleSpinBox_d_bregmay,self.ui.doubleSpinBox_d_bregmaz,distance=True)
        if self.coords_lambda is not None:
            self.calculate_distance(self.coords_bregma,self.coords_lambda)
            self.ui.pushButton_tp_next0.setEnabled(True)
            self.ui.pushButton_redAreas.setEnabled(True)
        self.selecting_point = False


    def get_lambda(self):
        self.coords_lambda = self.LoadMRI.slice_indices[0][::-1].copy()
        self.set_value(self.coords_lambda.copy(),self.ui.spinBox_tp_lambda_x,self.ui.spinBox_tp_lambda_y,self.ui.spinBox_tp_lambda_z)

        #draw lambda green
        self.draw_point(self.coords_lambda,(0,1,0),'lambda')
        self.render()
        d = self.calculate_distance(self.coords_lambda,self.movingidx_lambda,return_distance=True)
        self.set_value(d,self.ui.doubleSpinBox_d_lambdax,self.ui.doubleSpinBox_d_lambday,self.ui.doubleSpinBox_d_lambdaz,distance=True)
        if self.coords_bregma is not None:
            self.calculate_distance(self.coords_bregma,self.coords_lambda)
            self.ui.pushButton_tp_next0.setEnabled(True)
            self.ui.pushButton_redAreas.setEnabled(True)
        self.selecting_point = False

    def get_deepest_point(self):
        self.selecting_point = True
        self.coords_deepest_point[self.shank_number] = self.LoadMRI.slice_indices[0][::-1].copy()
        self.set_value(self.coords_deepest_point[self.shank_number].copy(),self.ui.spinBox_tp_deep_x,self.ui.spinBox_tp_deep_y,self.ui.spinBox_tp_deep_z)

        #draw deep green
        self.draw_point(self.coords_deepest_point[self.shank_number],(0,1,0),'deep')

        self.mri_deep[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_deepest_point[self.shank_number])) #xyz
        if self.mri_insert[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.selecting_point = False
        self.render()

    def change_shank_parameters(self):
        if self.coords_deepest_point[self.shank_number] is not None and self.coords_insert_point[self.shank_number] is not None:
            self.create_channel_list()

        self.render()

    def get_insert_point(self,view_name):
        self.selecting_point = True
        self.coords_insert_point[self.shank_number] = self.get_point_at_edge()

        self.set_value(self.coords_insert_point[self.shank_number].copy(),self.ui.spinBox_tp_insert_x,self.ui.spinBox_tp_insert_y,self.ui.spinBox_tp_insert_z)

        #draw insert red
        self.draw_point(self.coords_insert_point[self.shank_number],(1,0,0),'insert')
        self.mri_insert[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_insert_point[self.shank_number])) #xyz
        if self.mri_deep[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.selecting_point = False
        self.render()

    def set_value(self,point,spinbox_x,spinbox_y,spinbox_z,distance=False):
        if not distance:
            point[2] = point[2]+1
            point[1] = point[1]+1
            point[0] = point[0]+1
        #else:
        #    point = point[::-1]

        spinbox_x.blockSignals(True)
        spinbox_y.blockSignals(True)
        spinbox_z.blockSignals(True)
        spinbox_x.setValue(np.abs(point[0]))
        spinbox_y.setValue(np.abs(point[1]))
        spinbox_z.setValue(np.abs(point[2]))
        spinbox_x.blockSignals(False)
        spinbox_y.blockSignals(False)
        spinbox_z.blockSignals(False)



    def change_bregma(self):
        self.coords_bregma = [self.ui.spinBox_tp_bregma_x.value()-1,self.ui.spinBox_tp_bregma_y.value()-1,self.ui.spinBox_tp_bregma_z.value()-1]
        self.draw_point(self.coords_bregma,(1,0,0),'bregma')
        d = self.calculate_distance(self.coords_bregma,self.movingidx_bregma,return_distance=True)
        self.set_value(d,self.ui.doubleSpinBox_d_bregmax,self.ui.doubleSpinBox_d_bregmay,self.ui.doubleSpinBox_d_bregmaz,distance=True)
        if self.coords_lambda is not None:
            self.calculate_distance(self.coords_bregma,self.coords_lambda)
        self.render()

    def change_lambda(self):
        self.coords_lambda = [self.ui.spinBox_tp_lambda_x.value()-1,self.ui.spinBox_tp_lambda_y.value()-1,self.ui.spinBox_tp_lambda_z.value()-1]
        self.draw_point(self.coords_lambda,(0,1,0),'lambda')
        d = self.calculate_distance(self.coords_lambda,self.movingidx_lambda,return_distance=True)
        self.set_value(d,self.ui.doubleSpinBox_d_lambdax,self.ui.doubleSpinBox_d_lambday,self.ui.doubleSpinBox_d_lambdaz,distance=True)
        if self.coords_bregma is not None:
            self.calculate_distance(self.coords_bregma,self.coords_lambda)
        self.render()

    def change_insert_point(self):
        self.coords_insert_point[self.shank_number] = [self.ui.spinBox_tp_insert_x.value()-1,self.ui.spinBox_tp_insert_y.value()-1,self.ui.spinBox_tp_insert_z.value()-1]
        self.draw_point(self.coords_insert_point[self.shank_number],(0,1,0),'insert')
        self.mri_insert[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_insert_point[self.shank_number]))
        if self.mri_deep[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.render()

    def change_deepest_point(self):
        self.coords_deepest_point[self.shank_number] = [self.ui.spinBox_tp_deep_x.value()-1,self.ui.spinBox_tp_deep_y.value()-1,self.ui.spinBox_tp_deep_z.value()-1]
        self.draw_point(self.coords_deepest_point[self.shank_number],(0,1,0),'deep')
        self.mri_deep[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_deepest_point[self.shank_number]))
        if self.mri_insert[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

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
                self.line_actor[self.shank_number][view_name], self.label_actor[self.shank_number][view_name] = self.draw_electrode_line(view_name, self.coords_deepest_point[self.shank_number], self.atlas_shank_end[self.shank_number])
                for a in self.line_actor[self.shank_number][view_name]:
                    self.LoadMRI.renderers[0][view_name].AddActor(a)
                self.LoadMRI.renderers[0][view_name].AddActor(self.label_actor[self.shank_number][view_name])


    def render(self):
        for _,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                widget.GetRenderWindow().Render()

    def register_to_main_img(self,filename):
        self.ui.comboBox_movingimg.addItem(os.path.basename(filename))
        self.LoadMRI.movingimg_filename.append(filename)
        self.LoadMRI.coarsest_index = 1 #comboBox_coarsest
        self.LoadMRI.finest_index = 0 #comboBox_finest

        Registration(self.LoadMRI,self.MW.ButtonsGUI_3D,0)
        m = re.search(r"ind_(\d+)", self.main_file)
        fixed_ind = int(m.group(1))

        moving_ind = int(filename.split("ind_")[1].split(".")[0])
        transform_filename = f"transformation_ind_{moving_ind}-to-ind_{fixed_ind}.txt"
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


    def get_atlas_coords(self,vol,transformPath,bregma_coords = [246-1,653-1,440-1],lamdba_coords = [244-1,442-1,464-1]):
        #load transformation dataf
        self.fixedImg = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        self.atlas_vol = sitk.GetArrayFromImage(self.fixedImg)
        self.movingImg = sitk.ReadImage(self.MW.data_pre_resampled) #vol.raw_ref_image
        self.movingImg_resampled = self.LoadMRI.volumes[0].oriented_ref_image
        self.transform_moving2fixed = sitk.ReadTransform(transformPath)
        movingidx_bregma = self.atlas_to_mri_coordinates(bregma_coords)
        movingidx_lambda = self.atlas_to_mri_coordinates(lamdba_coords)
        spacing = np.array(self.movingImg_resampled.GetSpacing())
        distance = np.linalg.norm((np.array(bregma_coords) - np.array(lamdba_coords)) * spacing)

        return movingidx_bregma,movingidx_lambda,distance


    def atlas_to_mri_coordinates(self,atlas_coord,raw=False):
        fixedpnt_atlas = self.fixedImg.TransformIndexToPhysicalPoint(atlas_coord) #mm
        movingpnt = self.transform_moving2fixed.TransformPoint(fixedpnt_atlas) #mri
        raw_mri_idx = self.movingImg.TransformPhysicalPointToIndex(movingpnt) #px
        if raw:
            return raw_mri_idx
        phys = self.movingImg.TransformIndexToPhysicalPoint(raw_mri_idx)
        mri_idx = self.movingImg_resampled.TransformPhysicalPointToIndex(phys)
        return mri_idx



    def calculate_distance(self,start,end,return_distance=False):
        # spacing of the resampled displayed image (xyz) — NOT movingImg which is pre-resampled
        self.mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        if return_distance:
            distance = (np.array(end) - np.array(start)) * self.mri_spacing
            return distance
        if self.ui.stackedWidget_trajectoryplanning.currentIndex()==0:
            distance = np.linalg.norm((np.array(end) - np.array(start)) * self.mri_spacing)
            self.ui.doubleSpinBox_distance.setValue(distance)
            self.ui.doubleSpinBox_tp_ratio.setValue(distance/self.ui.doubleSpinBox_distanceAtlas.value())
        else:
            distance = np.linalg.norm((np.array(end) - np.array(start)) * self.mri_spacing)
            self.ui.doubleSpinBox_distance_shank.setValue(distance)
            self.ui.doubleSpinBox_distance_shank.setEnabled(True)
            self.ui.textEdit_distance_shank.setEnabled(True)


    def get_shank_line(self,transformPath=None):
        self.MW.overlay = BusyOverlay(self.MW, message="Processing, please wait…")
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



    def get_point_at_edge(self):
        clicked_x,clicked_y,clicked_z = self.LoadMRI.slice_indices[0][::-1].copy() #zyx
        view_name = self.clicked_viewname
        if view_name=='sagittal':
            mask2d = self.edge_mask[:,:,clicked_x]
            indices2d = [clicked_z,clicked_y] #self.LoadMRI.volumes[0].slices[0].shape[1]-1-
        elif view_name=='coronal':
            mask2d = self.edge_mask[:,clicked_y,:]
            indices2d = [clicked_z,clicked_x]
        elif view_name=='axial':
            mask2d = self.edge_mask[clicked_z,:,:]
            indices2d = [clicked_y,clicked_x]

        pts = np.argwhere(mask2d > 0)
        same_x = pts[pts[:, 1] == indices2d[1]]
        if len(same_x) > 0:
            dists_y = np.abs(same_x[:, 0] - indices2d[0])
            indices_edge2d = same_x[np.argmin(dists_y)]
        else:
            indices_edge2d = indices2d

        indices_edge = [clicked_z,clicked_y,clicked_x]

        if view_name=='sagittal':
            indices_edge[0] = indices_edge2d[0]
        elif view_name=='coronal':
            indices_edge[0] = indices_edge2d[0]
        elif view_name=='axial':
            indices_edge[1] = indices_edge2d[0]

        return indices_edge[::-1]


    def create_channel_list(self):
        self.ui.groupBox_shank.setEnabled(True)
        self.ui.pushButton_coronalView.setEnabled(True)
        self.ui.pushButton_sagittalView.setEnabled(True)
        self.ui.pushButton_axialView.setEnabled(True)

        num_channels = self.ui.spinBox_tp_channels.value()
        self.direction_atlas[self.shank_number] = (np.array(self.coords_insert_point[self.shank_number]) - np.array(self.coords_deepest_point[self.shank_number]))
        self.direction_atlas[self.shank_number] = self.direction_atlas[self.shank_number] / np.linalg.norm(self.direction_atlas[self.shank_number])
        physical_per_atlas_voxel = np.linalg.norm(self.direction_atlas[self.shank_number] * np.array(self.fixedImg.GetSpacing()))
        d_separation_atlas = (self.ui.spinBox_tp_separation.value() / 1000) / physical_per_atlas_voxel
        self.atlas_shank_end[self.shank_number] = self.coords_deepest_point[self.shank_number] + (num_channels-1)*d_separation_atlas*self.direction_atlas[self.shank_number]

        self.channel_points[self.shank_number] = np.array([self.coords_deepest_point[self.shank_number] + i * d_separation_atlas * self.direction_atlas[self.shank_number] for i in range(num_channels)])

        atlas_values = [self.atlas_vol[tuple(np.round(p[::-1]).astype(int))] for p in self.channel_points[self.shank_number]]
        atlas_values_sorted = [(val, sum(1 for _ in group)) for val, group in groupby(atlas_values)]
        region_name = [self.LoadMRI.tp_labels[val][4] for val,_ in atlas_values_sorted]

        table = self.ui.tableWidget_shank_info
        table.setRowCount(len(atlas_values_sorted))
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        for i, (val, count) in enumerate(atlas_values_sorted):
            layer_item = QTableWidgetItem(f"{count}")
            table.setItem(len(atlas_values_sorted)-1-i , 0, layer_item)
            layer_item = QTableWidgetItem(f"{region_name[i]}")
            table.setItem(len(atlas_values_sorted)-1-i , 1, layer_item)

        #line
        for view_name in 'axial','sagittal','coronal':
            if view_name in self.line_actor[self.shank_number]:
                for a in self.line_actor[self.shank_number][view_name]:
                    self.LoadMRI.renderers[0][view_name].RemoveActor(a)
                self.LoadMRI.renderers[0][view_name].RemoveActor(self.label_actor[self.shank_number][view_name])
            self.line_actor[self.shank_number][view_name], self.label_actor[self.shank_number][view_name] = self.draw_electrode_line(view_name, self.coords_deepest_point[self.shank_number], self.atlas_shank_end[self.shank_number])
            for a in self.line_actor[self.shank_number][view_name]:
                self.LoadMRI.renderers[0][view_name].AddActor(a)
            self.LoadMRI.renderers[0][view_name].AddActor(self.label_actor[self.shank_number][view_name])
        self.render()

        if self.ui.stackedWidget_coronal.currentIndex() == 1: #coronal
            self.change_view_coronal(checked=False)
        if self.ui.stackedWidget_sagittal.currentIndex() == 1: #coronal
            self.change_view_sagittal(checked=False)

        atlas_values = [self.atlas_vol[tuple(np.round(p[::-1]).astype(int))] for p in self.channel_points[self.shank_number]]
        region_name = [self.LoadMRI.tp_labels[val][4] for val in atlas_values]
        self.check_CA1_or_2(region_name,self.channel_points[self.shank_number],num_channels)

        self.check_region_to_avoid()

    def check_region_to_avoid(self):
        if not hasattr(self, 'region_to_avoid_img') or self.region_to_avoid_img is None:
            return
        #shape = self.region_to_avoid.shape
        hit = False
        deep = np.array(self.coords_deepest_point[self.shank_number])
        insert = np.array(self.coords_insert_point[self.shank_number])
        n_steps = int(np.max(np.abs(insert - deep))) + 1 #check every voxel
        samples = np.linspace(deep, insert, n_steps)
        for p in samples:
            idx = tuple(np.round(p[::-1]).astype(int))
            if self.region_to_avoid[idx] > 0:
                hit = True
                break
        if hit:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText(f"Shank {self.shank_number} passes through a region which should be avoided!")
            msg_box.addButton("OK", QMessageBox.ActionRole)
            msg_box.exec()



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



    def check_CA1_or_2(self,regionNames,points,num_channels):
        if "Cornu ammonis 1" in regionNames:
            self.ui.pushButton_PyLdetection.setEnabled(True)
            if not hasattr(self,'dwi'):
                dwi_path=os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
                nii_dwi=nib.load(dwi_path)
                dwi=np.asanyarray(nii_dwi.dataobj)
                self.dwi=dwi[:,:,:,0]
            minPixVal = 2e16
            pyrChIdx = 0
            dwi1Dsignal = np.zeros((num_channels,))

            #interpolated = []
            #points = [self.coords_deepest_point[self.shank_number]] + list(self.channel_points)
            #for i, n in enumerate(points_in_region):
            #    if i + 1 >= len(points):
            #        break
            #    pts = np.linspace(points[i], points[i + 1], n, endpoint=False)
            #    interpolated.extend(pts)
            #interpolated = np.array(interpolated)

            for idx, point in enumerate(points):
                z, y, x = [int(c) for c in point]
                currPixVal = self.dwi[x, y, z]
                dwi1Dsignal[idx] = currPixVal

            #regionNames = np.repeat(region_name[:len(points_in_region)], points_in_region).tolist()

            for i, name in enumerate(regionNames):
                if name == "Cornu ammonis 1":
                    if currPixVal < minPixVal:
                        minPixVal = currPixVal
                        pyrChIdx = i

            #canvas?
            plot_dwi_1D_cross_section(dwi1Dsignal,regionNames,pyrChIdx,num_channels,mplwidget=self.ui.tp_dwi1D_widget)
        else:
            self.ui.pushButton_PyLdetection.setEnabled(False)

    def show_canvas(self):
        if not hasattr(self, 'dwi_window'):
            self.dwi_window = QWidget()
            self.dwi_window.setWindowTitle("DWI 1D Cross Section")
            layout = QVBoxLayout(self.dwi_window)
            layout.addWidget(self.ui.tp_dwi1D_frame)

        self.dwi_window.show()
        self.dwi_window.raise_()



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

            if not hasattr(self,'Vis3D'):
                self.Vis3D = Visualisation3D(self.MW)
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
            if not hasattr(self,'Vis3D'):
                self.Vis3D = Visualisation3D(self.MW)
            self.Vis3D.render_clipped(normal,'sagittal',self.shank_number)

    def change_view_axial(self,checked):
        if checked:
            # axial view
            self.ui.stackedWidget_axial.setCurrentIndex(0) #axial
        else:
            self.ui.stackedWidget_axial.setCurrentIndex(1) ##CHANGE TO 1
            #axis_x = (0,0,1)
            #direction = self.direction_atlas[self.shank_number]
            normal = np.array([0,0,1]) #normal = np.array(axis_x) - np.dot(axis_x, direction) * direction
            #normal /= np.linalg.norm(normal)
            #if normal[2]>0:
            #    normal *= -1
            atlas_z = self.fixedImg.GetSize()[2]
            if not hasattr(self, 'axial_slider_connected'):
                self.ui.horizontalSlider_axial3D.setRange(0, atlas_z - 1)
                self.ui.horizontalSlider_axial3D.setValue(self.coords_deepest_point[self.ui.comboBox_Shanks.currentIndex()][2])
                self.ui.horizontalSlider_axial3D.valueChanged.connect(self.update_axial_depth)
                self.axial_slider_connect = True
            depth = self.ui.horizontalSlider_axial3D.value()
            if not hasattr(self,'Vis3D'):
                self.Vis3D = Visualisation3D(self.MW)
            self.Vis3D.render_clipped(normal,'axial',self.shank_number,depth=depth)


    def update_axial_depth(self, depth):
        normal = np.array([0,0,1]) #normal = np.array(axis_x) - np.dot(axis_x, direction) * direction
        self.Vis3D.render_clipped(normal,'axial',self.shank_number,depth=depth)


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



    def _reset_shank_gui(self):
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(True)
            sb.setValue(0)
            sb.blockSignals(False)
        self.ui.doubleSpinBox_distance_shank.setValue(0.0)
        self.ui.tableWidget_shank_info.setRowCount(0)

    def add_shank(self):
        n = self.ui.comboBox_Shanks.count()
        self.shank_number = n
        self.line_actor[n] = {}
        self.label_actor[n] = {}
        self.channel_points[n] = []
        self.ui.comboBox_Shanks.addItem(f"Shank {n+1}")
        self.ui.comboBox_Shanks.setCurrentIndex(n)  # triggers select_shank
        self.point_actor_deep[n] = {}
        self.point_actor_insert[n] = {}
        self.mri_deep[n] = None
        self.mri_insert[n] = None
        self.coords_deepest_point[n] = None
        self.coords_insert_point[n] = None
        self.direction_atlas[n] = None
        self.atlas_shank_end[n] = None
        self._reset_shank_gui()

    def remove_shank(self):
        if self.ui.comboBox_Shanks.count() <= 1:
            return  # always keep at least one
        shank_idx = self.shank_number
        for view_name in ('axial', 'sagittal', 'coronal'):
            if view_name in self.line_actor.get(shank_idx, {}):
                for a in self.line_actor[shank_idx][view_name]:
                    self.LoadMRI.renderers[0][view_name].RemoveActor(a)
                self.LoadMRI.renderers[0][view_name].RemoveActor(self.label_actor[shank_idx][view_name])
                self.LoadMRI.vtk_widgets[0][view_name].GetRenderWindow().Render()
        del self.line_actor[shank_idx]
        del self.label_actor[shank_idx]
        del self.channel_points[shank_idx]
        # block signal to avoid select_shank firing mid-cleanup
        self.ui.comboBox_Shanks.blockSignals(True)
        self.ui.comboBox_Shanks.removeItem(self.ui.comboBox_Shanks.currentIndex())
        self.ui.comboBox_Shanks.blockSignals(False)
        self.shank_number = self.ui.comboBox_Shanks.currentIndex()
        self.select_shank(self.shank_number)



    def select_shank(self, index):
        self.shank_number = index
        for shank_idx in self.line_actor:
            is_active = (shank_idx == index)
            color = (1, 1, 1) if is_active else (0.35, 0.35, 0.35)
            opacity = 1.0 if is_active else 0.4
            for view_name, actors in self.line_actor[shank_idx].items():
                for a in actors:
                    a.GetProperty().SetColor(*color)
                    a.GetProperty().SetOpacity(opacity * a.GetProperty().GetOpacity())
                self.label_actor[shank_idx][view_name].GetCaptionTextProperty().SetColor(*color)
                self.LoadMRI.vtk_widgets[0][view_name].GetRenderWindow().Render()

        # update spinboxes
        insert = self.coords_insert_point.get(index)
        deep   = self.coords_deepest_point.get(index)
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(True)
        if insert is not None:
            self.set_value(list(insert), self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z)
        else:
            self.ui.spinBox_tp_insert_x.setValue(0)
            self.ui.spinBox_tp_insert_y.setValue(0)
            self.ui.spinBox_tp_insert_z.setValue(0)
        if deep is not None:
            self.set_value(list(deep), self.ui.spinBox_tp_deep_x, self.ui.spinBox_tp_deep_y, self.ui.spinBox_tp_deep_z)
        else:
            self.ui.spinBox_tp_deep_x.setValue(0)
            self.ui.spinBox_tp_deep_y.setValue(0)
            self.ui.spinBox_tp_deep_z.setValue(0)
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(False)

        # update distance spinbox
        dist = 0.0
        if insert is not None and deep is not None:
            spacing = np.array(self.fixedImg.GetSpacing())
            dist = float(np.linalg.norm((np.array(insert) - np.array(deep)) * spacing))
        self.ui.doubleSpinBox_distance_shank.setValue(dist)

        # repopulate table from stored channel_points
        table = self.ui.tableWidget_shank_info
        pts = self.channel_points.get(index)
        if pts is not None and len(pts) > 0:
            atlas_values = [self.atlas_vol[tuple(np.round(p[::-1]).astype(int))] for p in pts]
            atlas_values_sorted = [(val, sum(1 for _ in group)) for val, group in groupby(atlas_values)]
            region_name = [self.LoadMRI.tp_labels[val][4] for val, _ in atlas_values_sorted]
            table.setRowCount(len(atlas_values_sorted))
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for i, (val, count) in enumerate(atlas_values_sorted):
                table.setItem(len(atlas_values_sorted) - 1 - i, 0, QTableWidgetItem(f"{count}"))
                table.setItem(len(atlas_values_sorted) - 1 - i, 1, QTableWidgetItem(f"{region_name[i]}"))
        else:
            table.setRowCount(0)



