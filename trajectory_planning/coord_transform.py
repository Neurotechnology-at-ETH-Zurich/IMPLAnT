# This Python file uses the following encoding: utf-8
import numpy as np
import SimpleITK as sitk
from scipy.spatial import cKDTree
from scipy.interpolate import RegularGridInterpolator
import os
import sys
from paths_config import _paths

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


    def _build_bregma_lambda_lookup(self, stride=6):
        """
        Dense atlas->MRI correspondence table covering the WHOLE atlas, used
        to approximate the inverse (MRI->atlas) direction via nearest-
        neighbour lookup. The actual registration transform (rigid+affine+
        SyN) has no usable analytic inverse (SimpleITK's GetInverse() fails
        on it). An earlier version restricted this to a box around the
        atlas's own hardcoded bregma/lambda coordinates for speed -- that
        silently broke whenever a real click's true correspondence fell
        outside that box: the nearest-neighbour search had nothing better to
        offer than the box's own edge, for every such point, with no error.
        Confirmed empirically (two very different clicks both returned the
        same clamped Z). Covering the whole atlas costs a few seconds
        (~3.8us/point here) and is correct regardless of where a real click
        falls.
        """
        size = self.fixedImg.GetSize()
        xs = list(range(0, size[0], stride))
        ys = list(range(0, size[1], stride))
        zs = list(range(0, size[2], stride))
        atlas_pts = []
        mri_pts = []
        for x in xs:
            for y in ys:
                for z in zs:
                    atlas_idx = [x, y, z]
                    atlas_pts.append(atlas_idx)
                    mri_pts.append(self.atlas_to_mri_coordinates(atlas_idx))

        self._bl_lookup_atlas = np.array(atlas_pts)
        self._bl_lookup_mri = np.array(mri_pts)
        self._bl_lookup_tree = cKDTree(self._bl_lookup_mri)
        # Same table, reshaped into its natural (x, y, z, 3) grid -- the
        # nested x/y/z loop above fills it in exactly that (C-contiguous)
        # order -- so atlas_points_to_mri_indices can look up an arbitrary
        # (non-grid-aligned) atlas point by trilinear interpolation instead
        # of nearest-neighbour, which matters for mesh vertices (e.g. the
        # smoothed background shell) that don't sit exactly on this grid.
        self._bl_lookup_stride = stride
        self._bl_lookup_grid_shape = (len(xs), len(ys), len(zs))
        self._bl_lookup_mri_grid = self._bl_lookup_mri.reshape(len(xs), len(ys), len(zs), 3).astype(float)
        self._bl_lookup_interpolator = RegularGridInterpolator(
            (np.arange(len(xs)), np.arange(len(ys)), np.arange(len(zs))),
            self._bl_lookup_mri_grid, bounds_error=False, fill_value=None)


    def mri_to_atlas_via_lookup(self, mri_idx):
        if not hasattr(self, '_bl_lookup_tree'):
            self._build_bregma_lambda_lookup()
        _, nearest_i = self._bl_lookup_tree.query(mri_idx)
        return self._bl_lookup_atlas[nearest_i]


    def mri_grid_not_background_mask(self, background_label=0, mask_stride=2):
        """
        Boolean mask, same shape as movingImg_resampled's own array (zyx),
        marking every MRI voxel whose nearest atlas correspondence (via
        the same dense atlas->MRI lookup table _build_bregma_lambda_lookup
        already builds) has a NON-background atlas label -- i.e. "not
        Clear Label" in the atlas's own segmentation, reprojected onto the
        real MRI grid via nearest-neighbour (same technique/accuracy as
        mri_to_atlas_via_lookup, just batched). Used to mask the subject's
        own MRI intensity data down to just the brain, in true MRI space,
        for the PDF report's MRI-space renders -- there's no separate
        warped "subject MRI in atlas space" file to mask in atlas space
        instead, but this direction (which MRI voxels correspond to atlas
        background) only needs this lookup table's already-built KD-tree,
        no new registration.

        Computed on a coarser (mask_stride) grid and nearest-neighbour
        upsampled back to the MRI's native shape -- querying the KD-tree
        for every single native-resolution voxel (can be tens of millions)
        is unnecessary for a background/foreground boundary, which doesn't
        need per-voxel precision; the actual MRI intensity data this mask
        is applied to stays at full native resolution regardless.
        """
        if not hasattr(self, '_bl_lookup_tree'):
            self._build_bregma_lambda_lookup()
        cache_key = (background_label, mask_stride)
        if getattr(self, '_mri_not_background_mask_key', None) != cache_key:
            mri_shape = sitk.GetArrayFromImage(self.movingImg_resampled).shape  # zyx
            zs = np.arange(0, mri_shape[0], mask_stride)
            ys = np.arange(0, mri_shape[1], mask_stride)
            xs = np.arange(0, mri_shape[2], mask_stride)
            zz, yy, xx = np.meshgrid(zs, ys, xs, indexing='ij')
            query_pts = np.stack([xx.ravel(), yy.ravel(), zz.ravel()], axis=1)  # xyz, matches _bl_lookup_mri's convention

            _, nearest_i = self._bl_lookup_tree.query(query_pts)
            atlas_idx = self._bl_lookup_atlas[nearest_i]
            labels = self.atlas_vol[atlas_idx[:, 2], atlas_idx[:, 1], atlas_idx[:, 0]]
            coarse_mask = (labels != background_label).reshape(zz.shape)

            mask = np.repeat(np.repeat(np.repeat(
                coarse_mask, mask_stride, axis=0), mask_stride, axis=1), mask_stride, axis=2)
            self._mri_not_background_mask = mask[:mri_shape[0], :mri_shape[1], :mri_shape[2]]
            self._mri_not_background_mask_key = cache_key
        return self._mri_not_background_mask


    def get_cc_mri_voxel_mean(self, cc_label=67):
        """
        Mean position of the atlas's corpus callosum, in MRI/working-volume
        voxel space (same space/units as coords_bregma/coords_lambda/
        mri_insert/mri_deep) -- the MRI-space counterpart of get_cc_mri_mean
        below, which converts this same mean into atlas space for display.
        Reuses the whole-atlas correspondence table _build_bregma_lambda_
        lookup already computes (atlas points -> their forward-transformed
        MRI points) -- no separate transforming needed: filter those
        already-computed pairs down to the ones labelled corpus callosum
        and average their MRI side.
        """
        if not hasattr(self, '_cc_mean_mri'):
            if not hasattr(self, '_bl_lookup_tree'):
                self._build_bregma_lambda_lookup()
            atlas_xyz = self._bl_lookup_atlas
            labels = self.atlas_vol[atlas_xyz[:, 2], atlas_xyz[:, 1], atlas_xyz[:, 0]]
            self._cc_mean_mri = self._bl_lookup_mri[labels == cc_label].mean(axis=0)
        return self._cc_mean_mri


    def get_cc_mri_mean(self, cc_label=67):
        """
        Mean position of the atlas's corpus callosum, in atlas space --
        see get_cc_mri_voxel_mean for the MRI-space version this is
        derived from.
        """
        if not hasattr(self, '_cc_mean_atlas'):
            cc_mri_mean = self.get_cc_mri_voxel_mean(cc_label)
            self._cc_mean_atlas = self.mri_to_atlas_via_lookup(cc_mri_mean)
        return self._cc_mean_atlas


    def atlas_points_to_mri_indices(self, atlas_points_mm):
        """
        Vectorized, approximate atlas-physical-mm point(s) -> MRI/working-
        volume voxel-index conversion, for repositioning whole meshes (e.g.
        the 3D view's background shell/region surfaces) into true MRI space
        without a per-vertex atlas_to_mri_coordinates call each (which is a
        real SimpleITK transform lookup, too slow for thousands of
        vertices). Trilinearly interpolates the dense correspondence grid
        _build_bregma_lambda_lookup already builds -- same underlying data
        and accuracy as get_cc_mri_voxel_mean's centroid, just sampled at
        arbitrary (non-grid-aligned) points instead of averaged over one
        region's voxels. NOT sub-voxel-exact -- for a single precise point
        (e.g. a clicked landmark), use atlas_to_mri_coordinates instead.

        atlas_points_mm: (N, 3) array in the atlas voxel-index * atlas-
        spacing convention used throughout this file (e.g. mesh.points from
        a pv.ImageData built with fixedImg's spacing).
        Returns: (N, 3) float array of MRI voxel indices (movingImg_
        resampled's own grid) -- multiply by movingImg_resampled's spacing
        to get MRI physical mm, matching mri_insert/mri_deep/coords_bregma/
        coords_lambda's convention.
        """
        if not hasattr(self, '_bl_lookup_interpolator'):
            self._build_bregma_lambda_lookup()
        atlas_spacing = np.array(self.fixedImg.GetSpacing())
        stride = self._bl_lookup_stride
        nx, ny, nz = self._bl_lookup_grid_shape
        grid_idx = np.asarray(atlas_points_mm, dtype=float) / atlas_spacing / stride
        grid_idx = np.clip(grid_idx, [0, 0, 0], [nx - 1, ny - 1, nz - 1])
        return self._bl_lookup_interpolator(grid_idx)


    @staticmethod
    def ap_rl_si_frame(bregma_mm, lambda_mm, cc_mm):
        """
        Orthonormal (AP, RL, SI) frame from bregma, lambda and the corpus-
        callosum centroid, all in the same physical-mm space (MRI or
        atlas -- this is pure vector math, agnostic to which). Shared by
        compute_shank_roll_pitch_mri (MRI space) and the 3D view's
        landmark/plane drawing (either space, depending on what's
        currently displayed) so the two can't drift apart.

        AP = unit bregma->lambda vector.
        RL = unit normal of the plane through bregma, lambda and the CC
        centroid -- automatically exactly perpendicular to AP, since it's
        a cross product built from it, and anchored to real anatomy via
        the CC landmark rather than a raw-image-axis guess. This plane
        (spanned by AP/SI) is "the bregma-lambda-CC plane".
        SI = AP x RL, completing the frame. The plane spanned by AP/RL
        (normal = SI) is "the bregma-lambda plane parallel to RL".

        Returns (ap_axis, rl_axis, si_axis), or None if bregma/lambda/CC
        are degenerate (near-collinear, so no well-defined plane).
        """
        bl_vec = np.asarray(lambda_mm, dtype=float) - np.asarray(bregma_mm, dtype=float)
        bl_dist = float(np.linalg.norm(bl_vec))
        if bl_dist <= 1e-9:
            return None
        ap_axis = bl_vec / bl_dist

        rl_normal = np.cross(bl_vec, np.asarray(cc_mm, dtype=float) - np.asarray(bregma_mm, dtype=float))
        rl_norm = float(np.linalg.norm(rl_normal))
        if rl_norm <= 1e-9:
            return None
        rl_axis = rl_normal / rl_norm

        si_axis = np.cross(ap_axis, rl_axis)
        return ap_axis, rl_axis, si_axis


    def refresh_atlas_bregma_lambda_from_user_points(self):
        """
        Point draw_atlas_reference_points' atlas_bregma_coords/
        atlas_lambda_coords (previously the atlas's hardcoded defaults) at
        the user's own clicked bregma/lambda instead, converted directly to
        atlas space -- no correction of any kind, the user's own click is
        trusted as-is. Called from get_shank_line's proceed() (registration.
        py), alongside warp_skull_mask/warp_red_areas -- already wrapped in
        a BusyOverlay there, so this runs synchronously rather than showing
        its own.
        """
        if self.coords_bregma is not None:
            self.atlas_bregma_coords = list(self.mri_to_atlas_via_lookup(self.coords_bregma))
        if self.coords_lambda is not None:
            self.atlas_lambda_coords = list(self.mri_to_atlas_via_lookup(self.coords_lambda))


    def compute_shank_roll_pitch_mri(self, shank_number):
        """
        Shank angle to two bregma/lambda/corpus-callosum-anchored planes,
        in MRI/working-volume space -- the physically meaningful space,
        since insertion actually happens into the real animal, not the
        atlas (a nonlinear SyN warp connects the two and does not preserve
        angles, so computing this in atlas space instead would not give
        the same number for the same physical trajectory). Single source
        of truth for this math, used by both the 2D/3D view angle
        indicators (rendering.py's compute_shank_reference_angle) and the
        PDF report (file_input_output.py's compute()) -- previously
        duplicated with the 3D view computed in atlas space instead, which
        is why the two used to disagree.

        These are true line-to-plane angles (theta = arcsin(|shank_dir .
        plane_normal|)) using the shank's full 3D deep->insert direction,
        NOT the angle of that direction's projection into a 2D view (which
        is what an ML/DV or AP/DV atan2 decomposition would give, and
        would silently discard whichever component isn't in that view).

        RL axis = unit normal of the plane through bregma, lambda and the
        corpus-callosum centroid (get_cc_mri_voxel_mean) -- automatically
        exactly perpendicular to the bregma-lambda/AP axis, since it's a
        cross product built from it, and anchored to real anatomy via the
        CC landmark rather than a raw-image-axis guess. SI axis = AP x RL,
        the remaining direction completing the (AP, RL, SI) orthonormal
        frame.

        Roll = angle between the shank and the bregma-lambda-CC plane
        itself (spanned by AP/SI, normal = RL) -- how far the shank leans
        out of the true sagittal plane. Shown in the coronal view, where
        that lean is what's visible.
        Pitch = angle between the shank and the bregma-lambda plane
        parallel to RL (spanned by AP/RL, normal = SI) -- how far the
        shank tilts off horizontal. Shown in the sagittal view.

        Returns (roll_deg, pitch_deg), or None if bregma/lambda or this
        shank's MRI-space insert/deepest points aren't set yet, or the
        three landmarks are degenerate (near-collinear, so no well-defined
        plane).
        """
        if self.coords_bregma is None or self.coords_lambda is None:
            return None
        mri_insert = getattr(self, 'mri_insert', {}).get(shank_number)
        mri_deep = getattr(self, 'mri_deep', {}).get(shank_number)
        if mri_insert is None or mri_deep is None:
            return None

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        cc_mm = np.array(self.get_cc_mri_voxel_mean(), dtype=float) * mri_spacing

        frame = self.ap_rl_si_frame(bregma_mm, lambda_mm, cc_mm)
        if frame is None:
            return None
        ap_axis, rl_axis, si_axis = frame

        insert_mm = np.array(mri_insert, dtype=float) * mri_spacing
        deep_mm = np.array(mri_deep, dtype=float) * mri_spacing
        shank_vec = insert_mm - deep_mm
        shank_dist = float(np.linalg.norm(shank_vec))
        if shank_dist <= 1e-9:
            return 0.0, 0.0

        shank_dir = shank_vec / shank_dist
        roll_deg = float(np.degrees(np.arcsin(np.clip(abs(np.dot(shank_dir, rl_axis)), 0.0, 1.0))))
        pitch_deg = float(np.degrees(np.arcsin(np.clip(abs(np.dot(shank_dir, si_axis)), 0.0, 1.0))))

        return roll_deg, pitch_deg


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