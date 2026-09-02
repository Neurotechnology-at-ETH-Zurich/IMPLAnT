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



    def get_atlas_coords(self,vol,transformPath,bregma_coords=None,lamdba_coords=None):
        # Per-atlas voxel coordinates -- defaults fall back to WHS's own
        # values when the active atlas doesn't override them (see
        # mrid_utils/atlas_registry.py).
        if bregma_coords is None:
            bregma_coords = _paths.get('atlas_bregma_coords', [245, 652, 439])
        if lamdba_coords is None:
            lamdba_coords = _paths.get('atlas_lambda_coords', [243, 441, 463])
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


    def atlas_points_to_mri_indices(self, atlas_points_mm):
        """
        Vectorized, approximate atlas-physical-mm point(s) -> MRI/working-
        volume voxel-index conversion, for repositioning whole meshes (e.g.
        the 3D view's background shell/region surfaces) into true MRI space
        without a per-vertex atlas_to_mri_coordinates call each (which is a
        real SimpleITK transform lookup, too slow for thousands of
        vertices). Trilinearly interpolates the dense correspondence grid
        _build_bregma_lambda_lookup already builds. NOT sub-voxel-exact --
        for a single precise point (e.g. a clicked landmark), use
        atlas_to_mri_coordinates instead.

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
    def ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg):
        """
        Orthonormal (AP, RL, SI) frame from bregma/lambda alone plus the
        user's manually-dialed-in coronal misalignment angle
        (dial_missalignment/doubleSpinBox_missalignment on the bregma/
        lambda page) -- RL/SI no longer come from a corpus-callosum-centroid
        -derived axis, which depended on a single, potentially noisy
        interior landmark instead of something the user can verify by eye.

        AP is exactly the bregma->lambda direction.
        RL/SI are fixed by taking the raw image's own SI axis (0,0,1),
        projecting it perpendicular to AP (the "no coronal rotation"
        baseline), then rotating that baseline (and its matching RL
        baseline) around AP by -misalignment_deg.

        The minus sign corrects for how that angle is actually measured:
        update_misalignment_guide_line draws a line on the coronal view
        that the user rotates onscreen until it matches the interhemispheric
        fissure, and that view's RL/display-x axis is mirrored (radiological
        convention -- see rendering.py's _atlas_point_display_xy). A line
        drawn rotating by +theta on screen therefore corresponds to a
        physical rotation of -theta around AP in raw voxel/mm space. Keep
        this in sync with that function if either one changes.

        Returns (ap_axis, rl_axis, si_axis), or None if bregma == lambda.
        """
        bl_vec = np.asarray(lambda_mm, dtype=float) - np.asarray(bregma_mm, dtype=float)
        bl_dist = float(np.linalg.norm(bl_vec))
        if bl_dist <= 1e-9:
            return None
        ap_axis = bl_vec / bl_dist

        raw_si = np.array([0.0, 0.0, 1.0])
        si_ref = raw_si - np.dot(raw_si, ap_axis) * ap_axis
        si_ref_norm = float(np.linalg.norm(si_ref))
        if si_ref_norm <= 1e-6:
            # ap_axis is (near-)parallel to the raw SI axis -- fall back to
            # the raw RL axis as the perpendicular reference instead.
            raw_rl = np.array([1.0, 0.0, 0.0])
            si_ref = raw_rl - np.dot(raw_rl, ap_axis) * ap_axis
            si_ref_norm = float(np.linalg.norm(si_ref))
            if si_ref_norm <= 1e-9:
                return None
        si_ref = si_ref / si_ref_norm
        rl_ref = np.cross(ap_axis, si_ref)

        theta = np.radians(-misalignment_deg)
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        si_axis = si_ref * cos_t + np.cross(ap_axis, si_ref) * sin_t
        rl_axis = rl_ref * cos_t + np.cross(ap_axis, rl_ref) * sin_t

        return ap_axis, rl_axis, si_axis


    def refresh_atlas_bregma_lambda_from_user_points(self):
        """
        Point draw_atlas_reference_points' atlas_bregma_coords/
        atlas_lambda_coords (previously the atlas's hardcoded defaults) at
        the user's own clicked bregma/lambda instead, converted directly to
        atlas space -- no correction of any kind, the user's own click is
        trusted as-is. Called from get_shank_line's proceed() (registration.
        py), alongside warp_red_areas -- already wrapped in a BusyOverlay
        there, so this runs synchronously rather than showing its own.
        """
        if self.coords_bregma is not None:
            self.atlas_bregma_coords = list(self.mri_to_atlas_via_lookup(self.coords_bregma))
        if self.coords_lambda is not None:
            self.atlas_lambda_coords = list(self.mri_to_atlas_via_lookup(self.coords_lambda))


    def compute_shank_roll_pitch_mri(self, shank_number):
        """
        Shank angle to two bregma/lambda-anchored planes, in MRI/working-
        volume space -- the physically meaningful space, since insertion
        actually happens into the real animal, not the atlas (a nonlinear
        SyN warp connects the two and does not preserve angles, so
        computing this in atlas space instead would not give the same
        number for the same physical trajectory). Single source of truth
        for this math, used by both the 2D/3D view angle indicators
        (rendering.py's compute_shank_reference_angle) and the PDF report
        (file_input_output.py's compute()) -- previously duplicated with
        the 3D view computed in atlas space instead, which is why the two
        used to disagree.

        These are 2D angles to a reference LINE within the relevant plane,
        each dropping (discarding, not folding in) whichever axis isn't
        that plane's reference direction -- NOT true 3D line-to-plane
        angles (theta = arcsin(|shank_dir . plane_normal|)), which was
        this function's previous definition. That line-to-plane version
        coupled roll and pitch together in a way that didn't match how a
        real stereotaxic frame's independent ML/AP tilt dials behave (e.g.
        it made checkBox_constraint_90deg's exact-AP=0 correction show
        LESS than 90 degrees in the sagittal view whenever there was also
        coronal tilt, since that formula folded the coronal/RL component's
        magnitude back into the reported angle instead of ignoring it).

        RL/SI axes come from ap_rl_si_frame_from_misalignment: AP is the
        bregma-lambda direction, and RL/SI are fixed by the user's own
        manually-dialed-in coronal misalignment angle (dial_missalignment/
        doubleSpinBox_missalignment on the bregma/lambda page), NOT the
        corpus-callosum centroid this used to derive RL from -- a single
        interior landmark's centroid was a noisier way to pin down the
        rotation around the AP axis than having the user align a guide
        line to the interhemispheric fissure by eye.

        Roll = angle from vertical (SI), within the RL-SI plane, dropping
        the AP component entirely -- how far the shank leans toward RL,
        ignoring any AP tilt. Shown in the coronal view.
        Pitch = angle from the AP line, within the AP-SI plane, dropping
        the RL component entirely -- how far the shank tilts off the AP
        line, ignoring any coronal/RL tilt. Shown in the sagittal view.
        Since each angle now discards a DIFFERENT component instead of
        both reading off the same one remaining degree of freedom, roll
        and pitch are no longer forced to sum to 90 degrees the way the
        old line-to-plane formula was whenever AP happened to be zero.

        Returns (roll_deg, pitch_deg), or None if bregma/lambda or this
        shank's MRI-space insert/deepest points aren't set yet, or bregma
        == lambda (degenerate, no well-defined AP axis).
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
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)

        frame = self.ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg)
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
        ap_comp = abs(float(np.dot(shank_dir, ap_axis)))
        rl_comp = abs(float(np.dot(shank_dir, rl_axis)))
        si_comp = abs(float(np.dot(shank_dir, si_axis)))
        roll_deg = float(np.degrees(np.arctan2(rl_comp, si_comp)))
        pitch_deg = float(np.degrees(np.arctan2(si_comp, ap_comp)))

        return roll_deg, pitch_deg


    def _deep_point_in_bounds(self, deep_mm, mri_spacing):
        """True if the given MRI-space physical-mm point converts to a
        voxel index still inside the working volume's own grid (with half
        a voxel of slack for rounding) -- the one non-negotiable bound
        constrain_shank_ap_to_zero must respect, since a deep point
        outside the volume isn't a point at all."""
        voxel = deep_mm / mri_spacing
        shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx
        max_xyz = (shape[2] - 1, shape[1] - 1, shape[0] - 1)
        return all(-0.5 <= voxel[i] <= max_xyz[i] + 0.5 for i in range(3))

    def _max_feasible_axis_correction(self, insert_mm, raw_dir, corrected_dir, depth, mri_spacing):
        """Largest t in [0, 1] for which insert_mm - depth * direction(t)
        stays within the volume, where direction(t) blends from raw_dir
        (t=0, the shank's original direction -- always feasible, since
        that's where the deep point already was) to corrected_dir (t=1,
        fully perpendicular to whichever axis is being zeroed -- AP for
        constrain_shank_ap_to_zero, RL for constrain_shank_rl_to_zero).
        t=1 is used whenever it's already feasible (the common case);
        otherwise this is the "as close to 90 degrees as the volume
        bounds allow" fallback -- binary search, assuming feasibility
        flips at most once along this blend (true in practice: t=0 is a
        small nudge away from the shank's existing, already-valid
        direction, and the blend sweeps smoothly and monotonically
        toward corrected_dir with no reason to re-enter the volume after
        leaving it for a typical correction-sized angle)."""
        def direction_at(t):
            if t <= 0.0:
                return raw_dir
            if t >= 1.0:
                return corrected_dir
            blended = (1 - t) * raw_dir + t * corrected_dir
            norm = np.linalg.norm(blended)
            return blended / norm if norm > 1e-9 else corrected_dir

        def feasible(t):
            return self._deep_point_in_bounds(insert_mm - depth * direction_at(t), mri_spacing)

        if feasible(1.0):
            return 1.0
        lo, hi = 0.0, 1.0  # feasible(0.0) assumed True -- raw_dir is the shank's existing, already-valid direction
        for _ in range(20):
            mid = (lo + hi) / 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid
        return lo

    def constrain_shank_ap_to_zero(self, shank_number):
        """
        checkBox_constraint_90deg: zero out the bregma-lambda (AP) axis
        component of this shank's deep->insert direction, so the shank is
        exactly perpendicular to the bregma-lambda line -- while leaving
        whatever coronal/RL tilt already existed untouched (renormalized
        to fill the remaining unit-direction budget). Insert is always the
        anchor and never moves here; mri_deep/coords_deepest_point are
        overwritten with the corrected point, preserving the existing
        insert-to-deep depth.

        If going fully to 90 degrees would push the deep point outside the
        MRI volume's own grid (insert is anchored at the skull surface, so
        a long, steep shank can run out of volume before reaching true
        perpendicular), this doesn't silently produce an invalid point --
        _max_feasible_axis_correction finds the largest angle actually
        achievable while keeping the deep point inside the volume,
        blending back toward the shank's original (already-valid)
        direction just enough to stay in bounds.

        Only needs bregma/lambda (unlike compute_shank_roll_pitch_mri, which
        also needs the coronal misalignment angle to build the full RL/SI
        frame) -- removing a single axis component from a vector doesn't
        require the rest of an orthonormal frame.

        No-op if bregma/lambda or this shank's insert/deep aren't set yet,
        or if bregma==lambda.
        """
        if self.coords_bregma is None or self.coords_lambda is None:
            return
        mri_insert = getattr(self, 'mri_insert', {}).get(shank_number)
        mri_deep = getattr(self, 'mri_deep', {}).get(shank_number)
        if mri_insert is None or mri_deep is None:
            return

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        bl_vec = lambda_mm - bregma_mm
        bl_dist = float(np.linalg.norm(bl_vec))
        if bl_dist <= 1e-9:
            return
        ap_axis = bl_vec / bl_dist

        insert_mm = np.array(mri_insert, dtype=float) * mri_spacing
        deep_mm = np.array(mri_deep, dtype=float) * mri_spacing
        vec = insert_mm - deep_mm  # deep->insert direction, same convention as compute_shank_roll_pitch_mri
        depth = float(np.linalg.norm(vec))
        if depth <= 1e-9:
            return
        raw_dir = vec / depth

        ap_comp = float(np.dot(vec, ap_axis))
        remaining = vec - ap_comp * ap_axis
        remaining_norm = float(np.linalg.norm(remaining))
        if remaining_norm <= 1e-9:
            # Shank was purely along AP -- no coronal/vertical component to
            # preserve; fall back to straight up in image space.
            remaining = np.array([0.0, 0.0, 1.0])
            remaining_norm = 1.0

        corrected_dir = remaining / remaining_norm
        t = self._max_feasible_axis_correction(insert_mm, raw_dir, corrected_dir, depth, mri_spacing)
        if t <= 0.0:
            final_dir = raw_dir
        elif t >= 1.0:
            final_dir = corrected_dir
        else:
            blended = (1 - t) * raw_dir + t * corrected_dir
            final_dir = blended / np.linalg.norm(blended)
        new_deep_mm = insert_mm - depth * final_dir
        new_deep_voxel = new_deep_mm / mri_spacing

        self.mri_deep[shank_number] = [int(round(c)) for c in new_deep_voxel]
        self.coords_deepest_point[shank_number] = list(self.mri_deep[shank_number])

    def constrain_shank_rl_to_zero(self, shank_number):
        """
        checkBox_constraint_90deg_coronal: the coronal-angle analogue of
        constrain_shank_ap_to_zero -- zero out the RL (mediolateral) axis
        component of this shank's deep->insert direction instead of the
        AP component, so the shank is exactly perpendicular to the RL
        axis (runs entirely within the true AP-SI/sagittal plane), while
        leaving whatever AP tilt already existed untouched (renormalized
        to fill the remaining unit-direction budget). Insert is always
        the anchor and never moves here; mri_deep/coords_deepest_point
        are overwritten with the corrected point, preserving the
        existing insert-to-deep depth. Same in-bounds fallback as the AP
        version (_max_feasible_axis_correction) if going fully to zero RL
        would push the deep point outside the MRI volume's own grid.

        Needs the full (AP, RL, SI) frame (ap_rl_si_frame_from_
        misalignment), unlike constrain_shank_ap_to_zero which only
        needs the bregma-lambda vector directly -- RL isn't derivable
        from bregma/lambda alone, it also depends on the user's manually-
        dialed-in coronal misalignment angle.

        No-op if bregma/lambda or this shank's insert/deep aren't set
        yet, or if bregma==lambda.
        """
        if self.coords_bregma is None or self.coords_lambda is None:
            return
        mri_insert = getattr(self, 'mri_insert', {}).get(shank_number)
        mri_deep = getattr(self, 'mri_deep', {}).get(shank_number)
        if mri_insert is None or mri_deep is None:
            return

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)
        frame = self.ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg)
        if frame is None:
            return
        _ap_axis, rl_axis, _si_axis = frame

        insert_mm = np.array(mri_insert, dtype=float) * mri_spacing
        deep_mm = np.array(mri_deep, dtype=float) * mri_spacing
        vec = insert_mm - deep_mm  # deep->insert direction, same convention as compute_shank_roll_pitch_mri
        depth = float(np.linalg.norm(vec))
        if depth <= 1e-9:
            return
        raw_dir = vec / depth

        rl_comp = float(np.dot(vec, rl_axis))
        remaining = vec - rl_comp * rl_axis
        remaining_norm = float(np.linalg.norm(remaining))
        if remaining_norm <= 1e-9:
            # Shank was purely along RL -- no AP/vertical component to
            # preserve; fall back to straight up in image space.
            remaining = np.array([0.0, 0.0, 1.0])
            remaining_norm = 1.0

        corrected_dir = remaining / remaining_norm
        t = self._max_feasible_axis_correction(insert_mm, raw_dir, corrected_dir, depth, mri_spacing)
        if t <= 0.0:
            final_dir = raw_dir
        elif t >= 1.0:
            final_dir = corrected_dir
        else:
            blended = (1 - t) * raw_dir + t * corrected_dir
            final_dir = blended / np.linalg.norm(blended)
        new_deep_mm = insert_mm - depth * final_dir
        new_deep_voxel = new_deep_mm / mri_spacing

        self.mri_deep[shank_number] = [int(round(c)) for c in new_deep_voxel]
        self.coords_deepest_point[shank_number] = list(self.mri_deep[shank_number])


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
            if view_name in ('sagittal', 'coronal'):
                # row = Z (dorsal-ventral) here -- insertion is always
                # through the dorsal (top) skull surface, never the
                # ventral/skull-base side, so always take the highest-Z
                # crossing. Picking whichever crossing merely happened to
                # be nearest the clicked pixel could just as easily land
                # on the wrong (bottom) side of a multi-crossing shell.
                crossing = max(crossings, key=lambda c: c.max())
            else:
                # axial: row = Y (AP) -- no anatomical "always this side"
                # rule for anterior vs. posterior, so nearest-the-click
                # is still the right tiebreak here.
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