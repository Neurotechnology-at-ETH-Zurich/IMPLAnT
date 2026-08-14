# This Python file uses the following encoding: utf-8
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
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

        self.direction_atlas[self.shank_number] = (np.array(self.coords_insert_point[self.shank_number]) - np.array(self.coords_deepest_point[self.shank_number]))
        self.direction_atlas[self.shank_number] = self.direction_atlas[self.shank_number] / np.linalg.norm(self.direction_atlas[self.shank_number])
        physical_per_atlas_voxel = np.linalg.norm(self.direction_atlas[self.shank_number] * np.array(self.fixedImg.GetSpacing()))

        dfx_shank = self.dfx_shank_data.get(self.shank_number)
        if dfx_shank is not None:
            # Use the DXF-bent contact depths (distance from the deepest/tip
            # contact, in um) directly along the deepest->insert axis; the
            # lateral (X) bundling offset has no defined direction in 3D
            # (the probe's roll around this axis is unknown), so it is
            # collapsed/ignored here.
            depth_um = dfx_shank["geometry"][:, 1]
            offsets_atlas = (depth_um / 1000) / physical_per_atlas_voxel
            self.channel_points[self.shank_number] = (
                self.coords_deepest_point[self.shank_number]
                + offsets_atlas[:, None] * self.direction_atlas[self.shank_number])
            self.atlas_shank_end[self.shank_number] = self.channel_points[self.shank_number][
                np.argmax(depth_um)]
            num_channels = depth_um.shape[0]
        else:
            num_channels = self.ui.spinBox_tp_channels.value()
            d_separation_atlas = (self.ui.spinBox_tp_separation.value() / 1000) / physical_per_atlas_voxel
            self.atlas_shank_end[self.shank_number] = self.coords_deepest_point[self.shank_number] + (num_channels-1)*d_separation_atlas*self.direction_atlas[self.shank_number]
            self.channel_points[self.shank_number] = np.array([self.coords_deepest_point[self.shank_number] + i * d_separation_atlas * self.direction_atlas[self.shank_number] for i in range(num_channels)])

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
        if hasattr(self, 'atlas_bregma_coords'):
            self.update_shank_angle_display()
            self.update_coronal_plane_line()

        if self.ui.stackedWidget_coronal.currentIndex() == 1: #coronal
            self.change_view_coronal(checked=False)
        if self.ui.stackedWidget_sagittal.currentIndex() == 1: #coronal
            self.change_view_sagittal(checked=False)
        atlas_values = [self.atlas_vol[tuple(np.round(p[::-1]).astype(int))] for p in self.channel_points[self.shank_number]]
        region_name = [self.LoadMRI.tp_labels[val][4] for val in atlas_values]
        self.check_CA1_or_2(region_name,self.channel_points[self.shank_number],num_channels)
        self.check_region_to_avoid()
        self.check_shank_intersections()
        if hasattr(self, 'shank_sidebar'):
            self.shank_sidebar.refresh()


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


    def check_shank_intersections(self):
        """Warn if the current shank's deep->insert line crosses (or passes
        implausibly close to) any other shank's line -- two physical
        probes can't occupy the same space, so this is a real planning
        error, not just a soft "too close for comfort" hint. Same trigger
        point/style as check_region_to_avoid."""
        spacing = np.array(self.fixedImg.GetSpacing())
        deep = self.coords_deepest_point.get(self.shank_number)
        insert = self.coords_insert_point.get(self.shank_number)
        if deep is None or insert is None:
            return
        deep_mm = np.array(deep, dtype=float) * spacing
        insert_mm = np.array(insert, dtype=float) * spacing

        # Sub-voxel threshold: below this, the two shank lines are
        # effectively occupying the same physical location.
        TOUCH_DIST_MM = 0.05
        hit_shanks = []
        for other_idx, other_deep in self.coords_deepest_point.items():
            if other_idx == self.shank_number or other_deep is None:
                continue
            other_insert = self.coords_insert_point.get(other_idx)
            if other_insert is None:
                continue
            other_deep_mm = np.array(other_deep, dtype=float) * spacing
            other_insert_mm = np.array(other_insert, dtype=float) * spacing
            dist = self._segment_segment_distance(
                deep_mm, insert_mm, other_deep_mm, other_insert_mm)
            if dist < TOUCH_DIST_MM:
                hit_shanks.append(other_idx)

        if hit_shanks:
            shanks_str = ", ".join(str(i + 1) for i in sorted(hit_shanks))
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText(
                f"Shank {self.shank_number + 1} intersects with shank(s) {shanks_str}!")
            msg_box.addButton("OK", QMessageBox.ActionRole)
            msg_box.exec()

    @staticmethod
    def _segment_segment_distance(p1, p2, p3, p4):
        """Closest distance between 3D line segments p1->p2 and p3->p4
        (standard closest-point-between-segments construction)."""
        d1, d2, r = p2 - p1, p4 - p3, p1 - p3
        a, e, f = np.dot(d1, d1), np.dot(d2, d2), np.dot(d2, r)

        if a <= 1e-12 and e <= 1e-12:
            return float(np.linalg.norm(p1 - p3))
        if a <= 1e-12:
            s, t = 0.0, np.clip(f / e, 0.0, 1.0)
        else:
            c = np.dot(d1, r)
            if e <= 1e-12:
                t, s = 0.0, np.clip(-c / a, 0.0, 1.0)
            else:
                b = np.dot(d1, d2)
                denom = a * e - b * b
                s = np.clip((b * f - c * e) / denom, 0.0, 1.0) if abs(denom) > 1e-12 else 0.0
                t = (b * s + f) / e
                if t < 0.0:
                    t, s = 0.0, np.clip(-c / a, 0.0, 1.0)
                elif t > 1.0:
                    t, s = 1.0, np.clip((b - c) / a, 0.0, 1.0)

        closest1 = p1 + d1 * s
        closest2 = p3 + d2 * t
        return float(np.linalg.norm(closest1 - closest2))

    def check_CA1_or_2(self,regionNames,points,num_channels):
        if "Cornu ammonis 1" in regionNames:
            self.ui.pushButton_PyLdetection.setEnabled(True)

            minPixVal = 2e16
            pyrChIdx = 0
            dwi1Dsignal = np.zeros((num_channels,))

            for idx, point in enumerate(points):
                z, y, x = [int(c) for c in point]
                dwi1Dsignal[idx] = self.dwi[x, y, z]

                if regionNames[idx] == "Cornu ammonis 1":
                    if dwi1Dsignal[idx] < minPixVal:
                        minPixVal = dwi1Dsignal[idx]
                        pyrChIdx = idx
                    print(pyrChIdx,flush=True)

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
