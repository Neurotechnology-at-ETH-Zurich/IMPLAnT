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
import sys
_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)
import ants
from PySide6.QtWidgets import QTableWidgetItem
from trajectory_planning.visualisation3D import Visualisation3D
from core.registration import Registration
import re

from mrid_utils.channel_mapper import plot_dwi_1D_cross_section
import nibabel as nib
from PySide6.QtWidgets import QDockWidget
from PySide6.QtGui import QPixmap, QIcon, QColor
from gui_utils.busy_overlay import BusyOverlay
from itertools import groupby
from trajectory_planning.file_input_output import FileOutput
from trajectory_planning.coord_transform import CoordTransform
from trajectory_planning.rendering import Rendering
from trajectory_planning.registration import TpRegistration
from trajectory_planning.electrode import ElecGeometry
from trajectory_planning.shank import ShankRendering, NEON_COLORS, _make_color_icon

## EVERYTHING IS WRITTEN WRT XYZ (not zyx)

class TrajectoryPlanning(CoordTransform, Rendering, TpRegistration, ElecGeometry, ShankRendering):
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

        self.shank_colors = {0: 0}  # shank_idx → NEON_COLORS index, default neon green

        # ShankRendering UI setup
        self.ui.comboBox_Shanks.addItem("Shank 1")
        self.ui.comboBox_Shanks.setItemData(0, 0)
        self.ui.comboBox_Shanks.setItemIcon(0, _make_color_icon(0))
        self.ui.comboBox_tpColor.blockSignals(True)
        for i, (name, _, _) in enumerate(NEON_COLORS):
            self.ui.comboBox_tpColor.addItem(_make_color_icon(i), name)
        self.ui.comboBox_tpColor.setCurrentIndex(0)
        self.ui.comboBox_tpColor.blockSignals(False)
        self.ui.comboBox_tpColor.currentIndexChanged.connect(self.change_shank_color)

        self.ui.pushButton_addShank.clicked.connect(self.add_shank)
        self.ui.comboBox_Shanks.currentIndexChanged.connect(self.select_shank)
        self.ui.pushButton_removeShank.clicked.connect(self.remove_shank)
        self.ui.pushButton_SaveTraj.clicked.connect(lambda _: FileOutput(self.MW, self.MW.data_pre_resampled,parent=self.MW).exec())
