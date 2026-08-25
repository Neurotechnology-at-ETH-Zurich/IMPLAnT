# This Python file uses the following encoding: utf-8
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import vtkActor,vtkPolyDataMapper
import numpy as np
from scipy import ndimage
import vtk
import SimpleITK as sitk
from PySide6 import QtWidgets
import os
from PySide6.QtWidgets import QWidget,QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
import sys
from paths_config import _paths
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
from trajectory_planning.coord_transform import CoordTransform
from trajectory_planning.rendering import Rendering
from trajectory_planning.registration import TpRegistration
from trajectory_planning.electrode import ElecGeometry
from trajectory_planning.shank import ShankRendering, NEON_COLORS, _make_color_icon
from trajectory_planning.dfx_geometry import DfxGeometry
from trajectory_planning.shank_sidebar import ShankSidebarWidget
from trajectory_planning_3d.window import TrajectoryPlanning3DWindow

## EVERYTHING IS WRITTEN WRT XYZ (not zyx)

class TrajectoryPlanning(CoordTransform, Rendering, TpRegistration, ElecGeometry, ShankRendering, DfxGeometry):
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

        self.tp3d_window = None
        self.ui.pushButton_tp_3d.clicked.connect(self.open_3d_window)

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

        self.transform_path = transformPath
        self.skull_mask_native_path = None

        # insertion-point refinement page (page_31, stackedWidget_
        # trajectoryplanning index 2) state -- see electrode.py.
        # self.LoadMRI.volumes[0] is still the resampled MRI working volume
        # here (get_atlas_coords below builds movingImg_resampled from this
        # exact same volume) -- captured now, before do_get_shank_line's
        # atlas swap, since MW.data_pre_resampled is a DIFFERENT file (the
        # original, non-resampled scan, only ever used elsewhere for
        # filename display) and loading that instead would silently put
        # mri_insert/mri_deep on the wrong voxel grid.
        self._mri_working_volume_path = self.LoadMRI.volumes[0].file_path
        self._insertion_confirmed = set()
        self._insertion_guide_actor = {}
        self._insertion_guide_t_max = {}
        self._insertion_direction_mri = {}
        self._mri_marker_actor = {'deep': {}, 'insert': {}}
        self._overlay_layers_reloaded = False
        self.LoadMRI.picking_insertion_point = False

        self.LoadMRI.tp_imgvtk = {}

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

        self.ui.pushButton_tp_next0.clicked.connect(lambda _: self.ask_paint_forbidden_areas())
        self.ui.pushButton_paint_done.clicked.connect(lambda _: self.get_shank_line(transformPath))
        self.ui.pushButton_paint_done.setToolTip(
            "Finish marking forbidden regions and continue to shank geometry")
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

        self.update_voxel_spinbox_ranges()

        #pyl detection using dwi
        self.ui.pushButton_PyLdetection.clicked.connect(self.show_canvas)

        self.shank_colors = {0: 0}  # shank_idx → NEON_COLORS index, default neon green
        self.shank_geometry_mode = "uniform"  # matches ShankSetupDialog.get_values()'s {'uniform', 'custom'}
        self._insertion_popup_shown = False
        self._geometry_popup_shown = False

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
        self.ui.pushButton_SaveTraj.clicked.connect(lambda _: self.enter_insertion_refinement_page())

        # page_31 (insertion-point refinement) setup -- comboBox_insertion_shank
        # mirrors comboBox_Shanks/comboBox_geometry_shanks, but drives shank
        # switching itself (_switch_insertion_shank_mri) rather than
        # select_shank, since this page displays the MRI, not the atlas.
        # spinBox_insertion_* are read-only displays kept in sync by
        # pick_insertion_point_from_click/_switch_insertion_shank_mri.
        self.ui.comboBox_insertion_shank.clear()
        self.ui.comboBox_insertion_shank.addItem("Shank 1")
        self.ui.comboBox_insertion_shank.setItemData(0, 0)
        self.ui.comboBox_insertion_shank.setItemIcon(0, _make_color_icon(0))
        self.ui.comboBox_insertion_shank.currentIndexChanged.connect(self._switch_insertion_shank_mri)
        # spinBox_insertion_x/y/z always display native-MRI-space voxel
        # indices (see electrode.py's insertion-refinement page), unlike the
        # atlas-ranged spinBox_tp_insert_* -- self.LoadMRI.volumes[0] is
        # still the subject's own MRI at this point in __init__, before the
        # atlas swap below, so its shape is the right one to range against.
        mri_shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx
        for sb, maximum in ((self.ui.spinBox_insertion_x, mri_shape[2]),
                             (self.ui.spinBox_insertion_y, mri_shape[1]),
                             (self.ui.spinBox_insertion_z, mri_shape[0])):
            sb.setMaximum(maximum)
            sb.setReadOnly(True)
            sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ui.textEdit_5.setPlainText(
            "Click directly in the 2D views to set each shank's insertion "
            "point -- it will snap onto that shank's own trajectory line. "
            "Use NEXT (or the dropdown above) to move to the next shank.")
        self.ui.pushButton_nextShank.clicked.connect(self.on_next_shank_clicked)

        # widget_tp_sidebar is an empty placeholder in the .ui (native
        # QWidget, no layout) -- populate it the same way widget_dfx is
        # populated in init_dfx_geometry.
        self.shank_sidebar = ShankSidebarWidget(self)
        sidebar_layout = QVBoxLayout(self.ui.widget_tp_sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(self.shank_sidebar)
        self.shank_sidebar.refresh()

        self.init_dfx_geometry()

        # comboBox_Shanks.currentIndexChanged is only connected above, after
        # "Shank 1" was already added -- Qt doesn't re-fire the signal for
        # that, so select_shank(0) has to be called explicitly to actually
        # apply shank 1's state (spinboxes, table, sidebar, colour combo).
        self.select_shank(0)

        self._popup_bregma_lambda()

    def update_voxel_spinbox_ranges(self):
        """Keep the bregma/lambda/insert/deepest-point voxel spinboxes'
        limits in sync with whichever volume is currently active -- the
        subject's own MRI here at setup, the atlas once
        Registration.do_get_shank_line swaps self.LoadMRI.volumes[0] to
        it. Without a refresh there, they keep the MRI's (usually
        smaller) shape as their max forever: any atlas voxel coordinate
        beyond that gets silently clamped by Qt when set. insert/deep
        never had their max set at all before this, silently relying on
        whatever default the .ui file's spinboxes happened to have."""
        shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx
        max_x, max_y, max_z = shape[2], shape[1], shape[0]
        for sb in (self.ui.spinBox_tp_bregma_x, self.ui.spinBox_tp_lambda_x,
                   self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_deep_x):
            sb.setMaximum(max_x)
        for sb in (self.ui.spinBox_tp_bregma_y, self.ui.spinBox_tp_lambda_y,
                   self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_deep_y):
            sb.setMaximum(max_y)
        for sb in (self.ui.spinBox_tp_bregma_z, self.ui.spinBox_tp_lambda_z,
                   self.ui.spinBox_tp_insert_z, self.ui.spinBox_tp_deep_z):
            sb.setMaximum(max_z)

    def open_3d_window(self):
        """Opens (or resurfaces) the standalone 3D atlas/shank view -- kept as a
        single persistent instance so its region/shank visibility stays put
        between opens. It's a QDockWidget added to MW once, appended into
        MW's own dock area (not floating) the first time, so it starts
        docked alongside the main window rather than as a separate floating
        window -- the user can still drag it out to float it afterwards."""
        if self.tp3d_window is None:
            self.tp3d_window = TrajectoryPlanning3DWindow(self.MW)
            self.MW.addDockWidget(Qt.RightDockWidgetArea, self.tp3d_window)
            # addDockWidget alone can leave it docked but squeezed to near
            # nothing if MW's central widget claims all the space -- give it
            # a sane starting width instead of just hoping there's room.
            self.MW.resizeDocks([self.tp3d_window], [500], Qt.Horizontal)
        self.tp3d_window.show()
        self.tp3d_window.raise_()
        self.tp3d_window.activateWindow()

    def show_step_popup(self, title, steps):
        msg_box = QMessageBox(self.MW)
        msg_box.setWindowTitle(title)
        msg_box.setText("\n".join(f"{i+1}. {s}" for i, s in enumerate(steps)))
        msg_box.addButton("OK", QMessageBox.ActionRole)
        msg_box.exec()

    def show_current_step_popup(self):
        """pushButton_questionmark: show whichever step's instructions are
        actually relevant right now, based on live state -- NOT whatever
        popup happened to fire last (that goes stale the moment the user
        moves to a different step/shank than when it was shown)."""
        seg_dock = self.MW.findChild(QDockWidget, "dock_segmentation")
        if seg_dock is not None and seg_dock.isVisible():
            # skull segmentation is its own sub-workflow (threshold/bubbles
            # or paint/evolution), tracked by stackedWidget_segmentation /
            # stackedWidget_initialization -- NOT stackedWidget_trajectoryplanning,
            # which is still sitting at index 0 the whole time this dock is
            # open, so it has to be checked before anything below.
            self._popup_segment_skull()
            return
        if self.ui.stackedWidget_trajectoryplanning.currentIndex() == 0:
            if self.ui.pushButton_paint_done.isVisible():
                self._popup_red_areas()
            else:
                self._popup_bregma_lambda()
        elif (self.shank_geometry_mode == "custom"
                and self.ui.stackedWidget_dfx.currentIndex() == 1):
            self._popup_geometry()
        else:
            self._popup_insertion()

    def _popup_bregma_lambda(self):
        self.show_step_popup(
            "Step 1: Bregma and Lambda",
            ["Move the cursor onto Bregma in the MRI views, then click "
             "'Save Cursor Position as Bregma'.",
             "Move the cursor onto Lambda in the MRI views, then click "
             "'Save Cursor Position as Lambda'.",
             "Then click 'Next' to continue."])

    def _popup_red_areas(self):
        self.show_step_popup(
            "Mark Regions to Avoid",
            ["Use the paintbrush to mark, in red, any regions the shank(s) must avoid.",
             "Click 'Continue with Trajectory Planning' when done."])

    def _popup_segment_skull(self):
        self.show_step_popup(
            "Segment the Skull",
            ["Enable 'Threshold' and set the intensity threshold (skull is "
             "dark) and the search radius around the existing brain mask.",
             "The brain mask shows red, the computed skull mask stays "
             "transparent (so you can check it's actually bone), and "
             "everything the radius/threshold rule out is purple -- all "
             "updating live as you adjust the controls.",
             "Click 'Finish Skull Segmentation' when you're happy with it."])

    def _popup_geometry(self):
        self.show_step_popup(
            "Step 2: Define Shank Geometry",
            ["Click 'Please load dxf File' to select this shank's DXF drawing.",
             "Click 'Run bending model' to bend it into the probe geometry.",
             "Click 'Add current run as shank' to commit it to this shank.",
             "Repeat for every shank (switch shanks with the dropdown above)."])

    def _popup_insertion(self):
        self.show_step_popup(
            "Step 2: Insertion and Deepest Point",
            ["Move the cursor to where the shank enters the brain, then click "
             "'Save Edge Point vertically above Cursor Position as Insert-Point'.",
             "Move the cursor to the shank's deepest point, then click "
             "'Save Cursor Position as Deepest-Point'."])

    def show_geometry_step_popup(self):
        """Auto-triggered once, right when the custom (DXF) geometry panel
        first opens -- the insertion/deepest-point popup is deliberately
        held back until this is done for every shank (see
        show_insertion_step_popup). Adding a shank later re-arms this so a
        shank added after the initial batch still gets a reminder."""
        if self._geometry_popup_shown:
            return
        self._geometry_popup_shown = True
        self._popup_geometry()

    def show_insertion_step_popup(self):
        """Auto-triggered: for 'predefined' geometry this is shown as soon
        as the insertion/deepest-point page appears. For 'custom' (DXF)
        geometry it's held back until every shank has geometry plotted --
        placing insertion/deepest points before that is premature, since
        the user still has to load/bend the DXF geometry for each shank
        first. Adding a shank later re-arms this (see add_shank)."""
        if self._insertion_popup_shown:
            return
        self._insertion_popup_shown = True
        self._popup_insertion()
