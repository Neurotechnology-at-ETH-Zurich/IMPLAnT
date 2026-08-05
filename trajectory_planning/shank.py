# This Python file uses the following encoding: utf-8
import numpy as np
from itertools import groupby
from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap, QIcon, QColor
from PySide6.QtWidgets import QTableWidgetItem

NEON_COLORS = [
    ("Neon Green",  (0,   255,  28), (0.0,        1.0,  28/255)),
    ("Neon Pink",   (255,  20, 147), (1.0,   20/255, 147/255)),
    ("Neon Blue",   (0,   191, 255), (0.0,  191/255,     1.0)),
    ("Neon Yellow", (255, 255,   0), (1.0,        1.0,     0.0)),
    ("White",       (255, 255, 255), (1.0,        1.0,     1.0)),
]

def _make_color_icon(color_idx, size=14):
    r, g, b = NEON_COLORS[color_idx][1]
    px = QPixmap(size, size)
    px.fill(QColor(r, g, b))
    return QIcon(px)


class ShankRendering:
    def add_shank(self):
        n = self.ui.comboBox_Shanks.count()
        self.shank_number = n
        self.shank_colors[n] = 0  # default neon green
        self.line_actor[n] = {}
        self.label_actor[n] = {}
        self.channel_points[n] = []
        self.ui.comboBox_Shanks.addItem(f"Shank {n+1}")
        self.ui.comboBox_Shanks.setItemData(n, n)
        self.ui.comboBox_Shanks.setItemIcon(n, _make_color_icon(0))
        self.ui.comboBox_Shanks.setCurrentIndex(n)  # triggers select_shank
        self.point_actor_deep[n] = {}
        self.point_actor_insert[n] = {}
        self.mri_deep[n] = None
        self.mri_insert[n] = None
        self.coords_deepest_point[n] = None
        self.coords_insert_point[n] = None
        self.direction_atlas[n] = None
        self.atlas_shank_end[n] = None
        self.reset_shank_gui()

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
        self.ui.comboBox_tpColor.blockSignals(True)
        self.ui.comboBox_tpColor.setCurrentIndex(self.shank_colors.get(index, 0))
        self.ui.comboBox_tpColor.blockSignals(False)
        for shank_idx in self.line_actor:
            is_active = (shank_idx == index)
            color = self.get_shank_vtk_color(shank_idx) if is_active else (0.35, 0.35, 0.35)
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

    def get_shank_vtk_color(self, shank_idx):
        return NEON_COLORS[self.shank_colors.get(shank_idx, 0)][2]

    def update_shank_icon(self, shank_number):
        icon = _make_color_icon(self.shank_colors.get(shank_number, 0))
        for i in range(self.ui.comboBox_Shanks.count()):
            if self.ui.comboBox_Shanks.itemData(i) == shank_number:
                self.ui.comboBox_Shanks.setItemIcon(i, icon)
                break

    def change_shank_color(self, color_idx):
        self.shank_colors[self.shank_number] = color_idx
        vtk_color = NEON_COLORS[color_idx][2]
        for view_name, actors in self.line_actor[self.shank_number].items():
            for a in actors:
                a.GetProperty().SetColor(*vtk_color)
            self.label_actor[self.shank_number][view_name].GetCaptionTextProperty().SetColor(*vtk_color)
        self.update_shank_icon(self.shank_number)
        self.render()
        if hasattr(self, 'Vis3D'):
            self.Vis3D.refresh_clipped_views(self.shank_number)

    def reset_shank_gui(self):
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(True)
            sb.setValue(0)
            sb.blockSignals(False)
        self.ui.doubleSpinBox_distance_shank.setValue(0.0)
        self.ui.tableWidget_shank_info.setRowCount(0)
