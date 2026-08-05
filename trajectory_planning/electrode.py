# This Python file uses the following encoding: utf-8
import numpy as np
from itertools import groupby
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QMessageBox
from mrid_utils.channel_mapper import plot_dwi_1D_cross_section

class ElecGeometry:
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



    def get_insert_point(self):
        self.selecting_point = True
        self.coords_insert_point[self.shank_number] = self.get_point_at_edge(self.edge_mask, self.clicked_viewname)

        self.set_value(self.coords_insert_point[self.shank_number].copy(),self.ui.spinBox_tp_insert_x,self.ui.spinBox_tp_insert_y,self.ui.spinBox_tp_insert_z)

        #draw insert red
        self.draw_point(self.coords_insert_point[self.shank_number],(1,0,0),'insert')
        self.mri_insert[self.shank_number] = self.atlas_to_mri_coordinates(tuple(int(x) for x in self.coords_insert_point[self.shank_number])) #xyz
        if self.mri_deep[self.shank_number] is not None:
            self.calculate_distance(self.mri_deep[self.shank_number],self.mri_insert[self.shank_number])
            self.create_channel_list()

        self.selecting_point = False
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

    def change_shank_parameters(self):
        if self.coords_deepest_point[self.shank_number] is not None and self.coords_insert_point[self.shank_number] is not None:
            self.create_channel_list()

        self.render()


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
        vtk_color = self.get_shank_vtk_color(self.shank_number)
        for view_name in 'axial','sagittal','coronal':
            if view_name in self.line_actor[self.shank_number]:
                for a in self.line_actor[self.shank_number][view_name]:
                    self.LoadMRI.renderers[0][view_name].RemoveActor(a)
                self.LoadMRI.renderers[0][view_name].RemoveActor(self.label_actor[self.shank_number][view_name])
            self.line_actor[self.shank_number][view_name], self.label_actor[self.shank_number][view_name] = self.draw_electrode_line(view_name, self.coords_deepest_point[self.shank_number], self.atlas_shank_end[self.shank_number], color=vtk_color)
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


    def check_CA1_or_2(self,regionNames,points,num_channels):
        if "Cornu ammonis 1" in regionNames:
            self.ui.pushButton_PyLdetection.setEnabled(True)

            minPixVal = 2e16
            pyrChIdx = 0
            dwi1Dsignal = np.zeros((num_channels,))

            for idx, point in enumerate(points):
                z, y, x = [int(c) for c in point]
                currPixVal = self.dwi[x, y, z]
                dwi1Dsignal[idx] = currPixVal

            for i, name in enumerate(regionNames):
                if name == "Cornu ammonis 1":
                    if currPixVal < minPixVal:
                        minPixVal = currPixVal
                        pyrChIdx = i

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
