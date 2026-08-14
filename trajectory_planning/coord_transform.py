# This Python file uses the following encoding: utf-8
import numpy as np
import SimpleITK as sitk
import os
import sys
import json as _json
_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)

class CoordTransform:
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
        self.selecting_point = False


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



    def get_atlas_coords(self,vol,transformPath,bregma_coords = [246-1,653-1,440-1],lamdba_coords = [244-1,442-1,464-1]):
        #load transformation dataf
        self.fixedImg = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        self.atlas_vol = sitk.GetArrayFromImage(self.fixedImg)
        # kept (not just local args) so the insertion/deepest-point step can
        # draw the atlas's own fixed bregma/lambda as reference markers
        self.atlas_bregma_coords = bregma_coords
        self.atlas_lambda_coords = lamdba_coords
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


    def get_point_at_edge(self,edge_mask,clicked_viewname):
        clicked_x,clicked_y,clicked_z = self.LoadMRI.slice_indices[0][::-1].copy() #zyx
        view_name = clicked_viewname
        if view_name=='sagittal':
            mask2d = edge_mask[:,:,clicked_x]
            indices2d = [clicked_z,clicked_y] #self.LoadMRI.volumes[0].slices[0].shape[1]-1-
        elif view_name=='coronal':
            mask2d = edge_mask[:,clicked_y,:]
            indices2d = [clicked_z,clicked_x]
        elif view_name=='axial':
            mask2d = edge_mask[clicked_z,:,:]
            indices2d = [clicked_y,clicked_x]

        pts = np.argwhere(mask2d > 0)
        same_x = pts[pts[:, 1] == indices2d[1]]
        if len(same_x) > 0:
            # the skull mask is a real-thickness shell (its search radius,
            # e.g. a few mm) rather than a single-voxel boundary, so this
            # column can cross it more than once (once per side of the
            # head) and, within each crossing, span several rows (its
            # inner surface closest to the brain vs. its outer surface
            # closest to the scalp).
            rows = np.sort(same_x[:, 0])
            splits = np.where(np.diff(rows) > 1)[0] + 1
            crossings = np.split(rows, splits)
            # pick the crossing (side of the head) nearest the click...
            crossing = min(crossings, key=lambda c: np.min(np.abs(c - indices2d[0])))
            # ...then, within that crossing, the row farthest from the
            # mask's own centroid in this slice -- i.e. the OUTER surface,
            # not whichever row of the shell happened to be nearest the
            # exact pixel clicked.
            centroid_row = pts[:, 0].mean()
            row = crossing[np.argmax(np.abs(crossing - centroid_row))]
            indices_edge2d = [row, indices2d[1]]
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