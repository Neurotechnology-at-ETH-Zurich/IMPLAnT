# This Python file uses the following encoding: utf-8
"""MRI-space override of Rendering (trajectory_planning/rendering.py).

Most of Rendering's drawing code (draw_point, _atlas_point_display_xy,
_draw_dotted_line, _draw_atlas_marker, _draw_atlas_point_label,
check_points_in_slice, _atlas_plane_segment_in_view,
update_atlas_plane_line, update_coronal_plane_line,
_update_shank_angle_display_view, visualize_regionname, show_brainregion)
is already space-agnostic -- it only ever reads whichever volume is
CURRENTLY displayed (self.LoadMRI.volumes[0]), which is the MRI throughout
this whole workflow now, or it delegates (via plain self.method() calls,
resolved dynamically through the subclass's MRO) into the handful of
methods that genuinely need overriding here:

- Bregma/lambda reference points: draw_atlas_reference_points now stores
  MRI-space values (self.movingidx_bregma/movingidx_lambda) into the SAME
  attribute names (self.atlas_bregma_coords/atlas_lambda_coords) the
  inherited code already reads -- so update_atlas_plane_line,
  _atlas_plane_segment_in_view, and the atlas-bregma/lambda-driven parts of
  compute_shank_reference_angle work correctly without their own override,
  once the two functions below that read spacing/shape are fixed.
- Every direct self.fixedImg.GetSpacing()/.GetSize() reference (the ATLAS
  image) needs to become self.movingImg_resampled's (the MRI actually being
  displayed): _atlas_plane_normal_and_point, _atlas_plane_segment,
  compute_shank_reference_angle, _update_shank_angle_display_view (one
  line), draw_electrode_line.
- create_edge_mask: source mask comes from mri_label_vol != 0 (the atlas-
  region-label overlay already scattered onto the MRI's own grid) instead
  of the atlas' own brain-mask file -- the atlas has no skull to show
  anyway.
- reload_atlas_view: switching atlases now only re-scatters the label
  overlay (build_mri_label_overlay) in place -- no restart_gui, no base
  image swap.

See /home/neurox/.claude/plans/wise-popping-nest.md for the full rationale.
"""

import os
import numpy as np
import vtk
from vtk.util import numpy_support
from scipy import ndimage
from PySide6.QtCore import QTimer
import nibabel as nib

from paths_config import _paths
from mrid_utils import atlas_switch
from mrid_utils.atlas_registry import get_active_atlas_id
from trajectory_planning.rendering import Rendering
from trajectory_planning.visualisation3D_mri import VisualisationMri
from core.image_layer import ImageLayer
from core.interactor_style import ObliqueInteractorStyle


class RenderingMri(Rendering):
    def refresh_atlas_bregma_lambda_from_user_points(self):
        """MRI-space override: atlas_bregma_coords/atlas_lambda_coords must
        stay in the MRI's own voxel-index grid here, not the atlas's --
        every consumer in this file (_atlas_point_display_xy via
        self.LoadMRI.volumes[0], _atlas_plane_normal_and_point via
        self.movingImg_resampled) reads them as MRI-grid indices.
        The base CoordTransform version instead runs coords_bregma/
        coords_lambda through mri_to_atlas_via_lookup, converting them to
        ATLAS-grid indices -- correct for the atlas-mode Rendering class
        (whose displayed volume/spacing IS the atlas), but wrong here: it
        made the B/L markers, the dotted line, and the roll/pitch
        reference plane all get scaled by the MRI's spacing/shape while
        holding atlas-grid index values, landing them nowhere near the
        actual clicked points."""
        self.atlas_bregma_coords = list(self.coords_bregma)
        self.atlas_lambda_coords = list(self.coords_lambda)

    def draw_atlas_reference_points(self):
        """Same markers/legend/reference-lines as Rendering's version, but
        anchored at the user's own clicked bregma/lambda (self.coords_
        bregma/coords_lambda, carried over as-is via this class's own
        refresh_atlas_bregma_lambda_from_user_points override above) --
        stored under the SAME attribute names (atlas_bregma_coords/
        atlas_lambda_coords) the inherited plane/angle code already reads,
        so that code keeps working unmodified. No corpus-callosum marker
        here -- _atlas_plane_normal_and_point (the coronal reference plane
        compute_shank_reference_angle/_atlas_plane_segment_in_view use) is
        already driven by the misalignment-dial frame, not CC."""
        # coords_bregma/coords_lambda are always already set by the time
        # this runs (bregma/lambda selection is a mandatory earlier wizard
        # step, gating advancement to this page) -- the atlas's own fixed
        # bregma/lambda (movingidx_bregma/movingidx_lambda) has no role
        # here, only the user's own clicked points do. Self-contained
        # (calls the refresh itself) rather than relying on every caller to
        # have already done so first -- this used to be skipped, since
        # get_shank_line's own refresh_atlas_bregma_lambda_from_user_points()
        # call, immediately before do_get_shank_line -> this method, was
        # silently overwritten right back to the atlas's fixed values below.
        self.refresh_atlas_bregma_lambda_from_user_points()

        self.atlas_ref_actor = {}
        self.atlas_ref_actor['bregma'] = {
            vn: self._draw_atlas_marker(vn, self.atlas_bregma_coords, (1, 1, 0))
            for vn in ('sagittal', 'coronal')
        }
        self.atlas_ref_actor['lambda'] = {
            vn: self._draw_atlas_marker(vn, self.atlas_lambda_coords, (1, 1, 0))
            for vn in ('sagittal', 'coronal')
        }
        self.atlas_ref_label = {
            'bregma': {
                vn: self._draw_atlas_point_label(vn, self.atlas_bregma_coords, "B", (1, 1, 0))
                for vn in ('sagittal', 'coronal')
            },
            'lambda': {
                vn: self._draw_atlas_point_label(vn, self.atlas_lambda_coords, "L", (1, 1, 0))
                for vn in ('sagittal', 'coronal')
            },
        }
        for vn in ('sagittal', 'coronal'):
            self._draw_legend_text(vn, "— Atlas Bregma-Lambda", (1, 1, 0), 0.95)

        self.atlas_bl_line_actor = self._draw_dotted_line(
            'sagittal',
            self._atlas_point_display_xy(self.atlas_bregma_coords, 'sagittal'),
            self._atlas_point_display_xy(self.atlas_lambda_coords, 'sagittal'),
            color=(1, 1, 0))

        self.atlas_plane_actors = {}
        self.update_coronal_plane_line()

        self.render()

    def reload_atlas_view(self, atlas_id):
        """Switches to atlas_id and re-colors the already-displayed MRI's
        label overlay in place -- no restart_gui, since the base/displayed
        volume never stops being the MRI. Returns False (leaving the
        previous atlas showing) if the user cancels the fetch or it fails."""
        if not atlas_switch.switch_active_atlas(atlas_id, self.MW):
            return False

        # re-anchor the atlas<->MRI coordinate machinery against the new
        # atlas (same call trajectory_planning.py's __init__ made
        # initially -- both atlases share one registration-space voxel
        # grid, per mri_label_overlay.py's own correspondence-caching note,
        # so the dense lookup/correspondence tables below are the only
        # things that go stale, not the correspondence itself).
        self.movingidx_bregma, self.movingidx_lambda, _ = self.get_atlas_coords(
            self.LoadMRI.volumes[0], self.transform_path)
        for stale_attr in ('_bl_lookup_atlas', '_bl_lookup_mri', '_bl_lookup_tree',
                           '_bl_lookup_stride', '_bl_lookup_grid_shape',
                           '_bl_lookup_mri_grid', '_bl_lookup_interpolator',
                           '_mri_not_background_mask', '_mri_not_background_mask_key'):
            if hasattr(self, stale_attr):
                delattr(self, stale_attr)

        # re-scatter the newly selected atlas' labels onto the (unchanged)
        # MRI grid, in place -- see build_mri_label_overlay's own note on
        # why this mutates the existing overlay layer/LUT rather than
        # rebuilding them.
        self.build_mri_label_overlay()

        self.LoadMRI.tp_imgvtk = {}
        self.LoadMRI.tp_actor = {}
        self.LoadMRI.tp_renderer = {}
        self.create_edge_mask()

        self.Vis3D = VisualisationMri(self.MW)

        if hasattr(self, 'dwi'):
            del self.dwi
        if _paths.get('atlas_dwi'):
            dwi_path = os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
            nii_dwi = nib.load(dwi_path)
            dwi = np.asanyarray(nii_dwi.dataobj)
            self.dwi = dwi[:, :, :, 0]

        self.draw_atlas_reference_points()
        self._sync_atlas_selector_widget()
        QTimer.singleShot(0, self.render)
        return True

    def _atlas_plane_normal_and_point(self):
        """Normal (unit vector, = RL axis) and a point (both in physical
        mm, MRI space) of the plane through bregma/lambda that roll is
        measured against (CoordTransform.compute_shank_roll_pitch_mri) --
        driven by the user's manually-dialed coronal misalignment angle
        (ap_rl_si_frame_from_misalignment) now, not the raw corpus-
        callosum-centroid cross-product this used to compute directly, so
        the coronal view's yellow reference line and the reported roll
        angle can't disagree."""
        spacing = np.array(self.movingImg_resampled.GetSpacing())
        b = np.array(self.atlas_bregma_coords) * spacing
        l = np.array(self.atlas_lambda_coords) * spacing
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)
        frame = self.ap_rl_si_frame_from_misalignment(b, l, misalignment_deg)
        if frame is None:
            return None, None
        _ap_axis, rl_axis, _si_axis = frame
        return rl_axis, b

    def _atlas_plane_segment(self, normal, plane_point, fixed_idx, fixed_voxel,
                              free_a_idx, free_b_idx, extent_a, extent_b):
        """Same line-vs-rectangle clipping as Rendering._atlas_plane_segment,
        against the MRI's own spacing instead of the atlas'."""
        spacing = np.array(self.movingImg_resampled.GetSpacing())  # xyz
        d = np.dot(normal, plane_point)
        k = d - normal[fixed_idx] * (fixed_voxel * spacing[fixed_idx])
        coef_a = normal[free_a_idx] * spacing[free_a_idx]
        coef_b = normal[free_b_idx] * spacing[free_b_idx]
        if max(abs(coef_a), abs(coef_b)) < 1e-9:
            return None

        max_a, max_b = extent_a - 1, extent_b - 1
        eps = 1e-6
        candidates = []
        if abs(coef_b) > 1e-9:
            for a in (0.0, max_a):
                b = (k - coef_a * a) / coef_b
                if -eps <= b <= max_b + eps:
                    candidates.append((a, min(max(b, 0.0), max_b)))
        if abs(coef_a) > 1e-9:
            for b in (0.0, max_b):
                a = (k - coef_b * b) / coef_a
                if -eps <= a <= max_a + eps:
                    candidates.append((min(max(a, 0.0), max_a), b))

        uniq = []
        for pt in candidates:
            if not any(abs(pt[0] - u[0]) < eps and abs(pt[1] - u[1]) < eps for u in uniq):
                uniq.append(pt)
        if len(uniq) < 2:
            return None

        best_pair, best_dist = None, -1
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                dist = np.hypot(uniq[i][0] - uniq[j][0], uniq[i][1] - uniq[j][1])
                if dist > best_dist:
                    best_dist, best_pair = dist, (uniq[i], uniq[j])

        endpoints = []
        for a, b in best_pair:
            p = [0.0, 0.0, 0.0]
            p[fixed_idx], p[free_a_idx], p[free_b_idx] = fixed_voxel, a, b
            endpoints.append(tuple(p))
        return endpoints

    def compute_shank_reference_angle(self, view_name, shank_number=None):
        """Same as Rendering.compute_shank_reference_angle, against the
        MRI's own spacing instead of the atlas'. atlas_bregma_coords/
        atlas_lambda_coords are already MRI-space here (see
        draw_atlas_reference_points), so the rest of this logic is
        otherwise identical."""
        if shank_number is None:
            shank_number = self.shank_number
        insert = self.coords_insert_point.get(shank_number)
        deep = self.coords_deepest_point.get(shank_number)
        if insert is None or deep is None or getattr(self, 'atlas_bregma_coords', None) is None:
            return None

        spacing = np.array(self.movingImg_resampled.GetSpacing())
        proj = (1, 2) if view_name == 'sagittal' else (0, 2)
        deep_vox = np.array(deep, dtype=float)

        insert_vox = np.array(insert, dtype=float)
        channel_points = self.channel_points.get(shank_number)
        if channel_points is not None and len(channel_points) > 0:
            first_electrode_vox = np.array(channel_points[0], dtype=float)
            if np.allclose(first_electrode_vox, deep_vox):
                insert_vox = np.array(channel_points[-1], dtype=float)
        bl_vec = (np.array(self.atlas_lambda_coords) - np.array(self.atlas_bregma_coords)) * spacing
        shank_vec = (insert_vox - deep_vox) * spacing
        shank_2d = shank_vec[list(proj)]

        if view_name == 'sagittal':
            ref_2d = bl_vec[list(proj)]
            ref_point_vox = np.array(self.atlas_bregma_coords, dtype=float)
        else:
            ref_2d = None
            ref_point_vox = None
            # _atlas_plane_normal_and_point is already misalignment-frame-
            # driven (ap_rl_si_frame_from_misalignment), not corpus-
            # callosum-derived -- no CC gate needed here; it returns
            # (None, None) on its own if bregma/lambda can't form a frame.
            normal, plane_point = self._atlas_plane_normal_and_point()
            if normal is not None:
                segment = self._atlas_plane_segment_in_view(view_name, normal, plane_point)
                if segment is not None:
                    seg_vec = (np.array(segment[1]) - np.array(segment[0])) * spacing
                    ref_2d = seg_vec[list(proj)]
                    ref_point_vox = np.array(segment[0], dtype=float)
                    bl_2d = bl_vec[list(proj)]
                    if np.linalg.norm(bl_2d) > 1e-9 and np.dot(ref_2d, bl_2d) < 0:
                        ref_2d = -ref_2d
            if ref_2d is None:
                return None

        denom = np.linalg.norm(ref_2d) * np.linalg.norm(shank_2d)
        if denom == 0:
            return None
        cos_theta = np.clip(np.dot(ref_2d, shank_2d) / denom, -1, 1)
        angle = np.degrees(np.arccos(cos_theta))
        if view_name == 'sagittal':
            angle = 180 - angle

        # The angle actually DISPLAYED is still the MRI-space roll/pitch
        # (compute_shank_roll_pitch_mri) -- unchanged from Rendering's own
        # version. Under this workflow ref_2d/shank_2d/deep_vox/insert_vox/
        # ref_point_vox are ALREADY MRI-voxel terms (unlike Rendering's
        # atlas-voxel terms), so unlike there, this geometric angle and the
        # displayed MRI-space one are now measuring the same real physical
        # geometry -- they need not (and generally won't, since this is
        # still a different projection/reference-line construction) be
        # numerically identical, but neither is a nonlinearly-distorted
        # picture of the other anymore.
        roll_pitch = self.compute_shank_roll_pitch_mri(shank_number)
        if roll_pitch is not None:
            angle = roll_pitch[1] if view_name == 'sagittal' else roll_pitch[0]

        return {
            'angle': angle, 'proj': proj, 'spacing': spacing,
            'ref_2d': ref_2d, 'shank_2d': shank_2d,
            'deep_vox': deep_vox, 'insert_vox': insert_vox,
            'ref_point_vox': ref_point_vox,
        }

    def _update_shank_angle_display_view(self, view_name):
        """Same as Rendering._update_shank_angle_display_view, against the
        MRI's own size instead of the atlas'."""
        if not hasattr(self, 'LoadMRI') or view_name not in self.LoadMRI.renderers.get(0, {}):
            return
        renderer = self.LoadMRI.renderers[0][view_name]
        if not hasattr(self, 'shank_angle_text_actors'):
            self.shank_angle_text_actors = {}
        if not hasattr(self, 'shank_angle_arc_actors'):
            self.shank_angle_arc_actors = {}
        old_actor = self.shank_angle_text_actors.get(view_name)
        if old_actor is not None:
            renderer.RemoveActor(old_actor)
            self.shank_angle_text_actors[view_name] = None
        old_arc = self.shank_angle_arc_actors.get(view_name)
        if old_arc is not None:
            renderer.RemoveActor(old_arc)
            self.shank_angle_arc_actors[view_name] = None

        result = self.compute_shank_reference_angle(view_name)
        if result is None:
            self.render()
            return
        angle, proj, spacing = result['angle'], result['proj'], result['spacing']
        ref_2d, shank_2d = result['ref_2d'], result['shank_2d']
        deep_vox, insert_vox = result['deep_vox'], result['insert_vox']
        ref_point_vox = result['ref_point_vox']
        flip_axis = proj[0]

        shape = np.array(self.movingImg_resampled.GetSize())  # xyz
        a, b = deep_vox.copy(), insert_vox.copy()
        a[flip_axis] = shape[flip_axis] - 1 - a[flip_axis]
        b[flip_axis] = shape[flip_axis] - 1 - b[flip_axis]
        anchor = a + 0.5 * (b - a)
        pos = (anchor * spacing)[list(proj)]
        deep_disp = (a * spacing)[list(proj)]
        insert_disp = (b * spacing)[list(proj)]

        flip = np.array([-1.0, 1.0])
        shank_dir, ref_dir = shank_2d * flip, ref_2d * flip
        shank_norm, ref_norm = np.linalg.norm(shank_dir), np.linalg.norm(ref_dir)
        if shank_norm > 1e-9 and ref_norm > 1e-9 and ref_point_vox is not None:
            shank_dir, ref_dir = shank_dir / shank_norm, ref_dir / ref_norm
            if view_name == 'sagittal':
                ref_dir = -ref_dir

            ref_point = ref_point_vox.copy()
            ref_point[flip_axis] = shape[flip_axis] - 1 - ref_point[flip_axis]
            ref_point_disp = (ref_point * spacing)[list(proj)]

            arc_center = self._line_intersection_2d(deep_disp, shank_dir, ref_point_disp, ref_dir)
            if arc_center is None:
                arc_center = deep_disp

            i_vec = insert_disp - arc_center
            d_vec = deep_disp - arc_center
            p1_vec = i_vec - (i_vec - d_vec) / 2
            radius = max(np.linalg.norm(p1_vec), 1e-6)
            point1_dir = p1_vec / radius

            point2_dir = ref_dir
            view_angle = float(np.degrees(np.arccos(np.clip(np.dot(point1_dir, ref_dir), -1.0, 1.0))))
            if view_angle > 90.0:
                point2_dir = -point2_dir

            arc = vtk.vtkArcSource()
            arc.SetCenter(arc_center[0], arc_center[1], 1.13)
            arc.SetPoint1(arc_center[0] + point1_dir[0] * radius, arc_center[1] + point1_dir[1] * radius, 1.13)
            arc.SetPoint2(arc_center[0] + point2_dir[0] * radius, arc_center[1] + point2_dir[1] * radius, 1.13)
            arc.SetResolution(20)
            arc_mapper = vtk.vtkPolyDataMapper()
            arc_mapper.SetInputConnection(arc.GetOutputPort())
            arc_actor = vtk.vtkActor()
            arc_actor.SetMapper(arc_mapper)
            arc_actor.GetProperty().SetColor(1, 1, 1)
            arc_actor.GetProperty().SetLineWidth(2)
            renderer.AddActor(arc_actor)
            self.shank_angle_arc_actors[view_name] = arc_actor

            bisector_vec = point1_dir + point2_dir
            bisector_norm = np.linalg.norm(bisector_vec)
            if bisector_norm > 1e-9:
                bisector_dir = bisector_vec / bisector_norm
            else:
                bisector_dir = np.array([-point1_dir[1], point1_dir[0]])
            pos = arc_center + bisector_dir * radius

        caption_text = f"{angle:.1f}°"
        caption = vtk.vtkCaptionActor2D()
        caption.SetCaption(caption_text)
        caption.SetAttachmentPoint(pos[0], pos[1], 1.15)
        caption.BorderOff()
        caption.LeaderOff()
        caption.GetCaptionTextProperty().SetColor(1, 1, 1)
        caption.GetCaptionTextProperty().SetFontSize(40)
        caption.GetCaptionTextProperty().SetBold(True)
        caption.GetCaptionTextProperty().ShadowOff()
        caption.GetCaptionTextProperty().BoldOff()
        caption.SetPosition(3, 3)
        caption.SetWidth(0.16)
        caption.SetHeight(0.045)
        renderer.AddActor(caption)
        self.shank_angle_text_actors[view_name] = caption

        self.render()

    def draw_electrode_line(self, view_name, point_a, point_b, color=(1, 1, 1), height=1.1):
        """Same as Rendering.draw_electrode_line, against the MRI's own
        spacing/size instead of the atlas'."""
        spacing = np.array(self.movingImg_resampled.GetSpacing())  # x,y,z
        shape = np.array(self.movingImg_resampled.GetSize())
        a = np.array(point_a, dtype=float)  # XYZ voxels
        b = np.array(point_b, dtype=float)
        if view_name == "axial" or view_name == "coronal":
            a[0] = shape[0] - 1 - a[0]
            b[0] = shape[0] - 1 - b[0]
        elif view_name == "sagittal":
            a[1] = shape[1] - 1 - a[1]
            b[1] = shape[1] - 1 - b[1]

        perp = {'coronal': (1, 1), 'sagittal': (0, 2), 'axial': (2, 0)}
        axis, slice_dim = perp[view_name]
        slice_idx = self.LoadMRI.slice_indices[0][slice_dim]
        proj = {'coronal': (0, 2), 'sagittal': (1, 2), 'axial': (0, 1)}
        xi, yi = proj[view_name]

        pa = a * spacing
        pb = b * spacing
        mid = (pa + pb) / 2

        # dim_line's endpoints are clamped to the volume's own voxel box --
        # point_b is often atlas_shank_end (electrode_mri.py's
        # create_channel_list), an extrapolation (num_channels-1)*separation
        # past the deepest point, or a loaded probe design's own farthest
        # channel, neither of which is checked against the MRI's FOV. Left
        # unclamped, this line's real vtkActor bounds can land far outside
        # the visible slice, which Zoom.fit_to_window's renderer.
        # ComputeVisiblePropBounds() then has to zoom out to include --
        # shrinking the actual slice to a tiny image in an otherwise-black
        # frame (same class of bug already fixed for the oblique renderer's
        # crosshair/canvas, see _draw_oblique_crosshair/_oblique_output_
        # geometry). The crossing-detection math below (t_min/t_max) still
        # uses the true, unclamped a/b -- only this faint full-length
        # indicator line's drawn geometry is clamped.
        a_dim = np.clip(a, 0, shape - 1)
        b_dim = np.clip(b, 0, shape - 1)
        pa_dim = a_dim * spacing
        pb_dim = b_dim * spacing

        dim_line = vtk.vtkLineSource()
        dim_line.SetPoint1(pa_dim[xi], pa_dim[yi], height - 0.1)
        dim_line.SetPoint2(pb_dim[xi], pb_dim[yi], height - 0.1)
        dim_mapper = vtk.vtkPolyDataMapper()
        dim_mapper.SetInputConnection(dim_line.GetOutputPort())
        dim_actor = vtk.vtkActor()
        dim_actor.SetMapper(dim_mapper)
        dim_actor.GetProperty().SetColor(*color)
        dim_actor.GetProperty().SetOpacity(0.4)
        dim_actor.GetProperty().SetLineWidth(3)
        actors = [dim_actor]

        denom = b[axis] - a[axis]
        if abs(denom) < 1e-6:
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

    def create_edge_mask(self):
        """Same as Rendering.create_edge_mask, sourced from mri_label_vol
        (the atlas-region-label overlay already scattered onto the MRI's
        own grid, one voxel at a time, by build_mri_label_overlay -- see
        registration_mri.py) instead of the atlas' own brain-mask file,
        since the atlas has no skull to show anyway and the mask needs to
        sit on the MRI's own grid now. NOT mri_grid_not_background_mask
        (coord_transform.py) -- that one is a coarser, strided nearest-
        neighbour approximation built for a different consumer (the PDF
        report's masked MRI render, file_input_output.py), whereas
        mri_label_vol is already the exact, full-resolution per-voxel
        scatter and is guaranteed built by this point (do_get_shank_line
        calls build_mri_label_overlay before this)."""
        fg = self.mri_label_vol != 0
        fg_filled = ndimage.binary_fill_holes(fg)
        struct = np.ones((3, 3, 3), dtype=bool)
        eroded = ndimage.binary_erosion(fg_filled, structure=struct)
        border = fg_filled & ~eroded
        edge_mask = border.astype(np.uint8)
        self.edge_mask = edge_mask

        # See build_mri_label_overlay's identical note (registration_mri.py)
        # -- shared with every other overlay-adding call site instead of
        # len(Layers[0]), which can collide with/overwrite this slot.
        self.MW.FileLoader.layer_index += 1
        layer_index = self.MW.FileLoader.layer_index
        lut_vtk = vtk.vtkLookupTable()
        lut_vtk.SetNumberOfTableValues(2)
        lut_vtk.SetTableRange(0, 1)
        lut_vtk.SetTableValue(0, 0, 0, 0, 0.4)
        lut_vtk.SetTableValue(1, 1, 1, 1, 1.0)
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
            lut=lut_vtk,
        )
        self.LoadMRI.setup_layer('coronal', 0, layer_index, visibility_at_start=False)
        self.LoadMRI.MW.Layers[0][layer_index].visibility_btn = self.LoadMRI.intensity_table[0].update_table(
            "Brain Edge", edge_mask, 0, layer_index, visibility_enabled=False)

    def setup_misalignment_controls(self):
        """One-time setup for dial_missalignment/doubleSpinBox_missalignment
        (page_5, groupBox_80 'Misalignment of Coronal Slice') -- both were
        pure Qt-default placeholders (0-99 int/float, unwired) with no
        connection to anything. doubleSpinBox_missalignment is the
        authoritative degree value; the dial is a coarse, synced view onto
        the same number (same blockSignals-based linking idiom as
        core/image_layer.py's opacity slider/spinbox pair)."""
        self.coronal_misalignment_deg = 0.0
        self.misalignment_line_center = None  # set on first draw (_misalignment_center_default); draggable after
        self.ui.dial_missalignment.setRange(-45, 45)
        self.ui.dial_missalignment.setValue(0)
        self.ui.dial_missalignment.setNotchesVisible(True)
        self.ui.doubleSpinBox_missalignment.setRange(-45.0, 45.0)
        self.ui.doubleSpinBox_missalignment.setDecimals(2)
        self.ui.doubleSpinBox_missalignment.setSingleStep(0.1)
        self.ui.doubleSpinBox_missalignment.setValue(0.0)
        self.ui.dial_missalignment.valueChanged.connect(lambda _checked: self.sync_misalignment('dial'))
        self.ui.doubleSpinBox_missalignment.valueChanged.connect(lambda _checked: self.sync_misalignment('spinbox'))
        self.update_misalignment_guide_line()

        # checkBox_constraint_90deg/_coronal live on this same page_5 area
        # (groupBox_80's neighboring checkboxes) -- wired here, not in
        # do_get_shank_line (registration_mri.py), since that method only
        # runs after bregma/lambda + forbidden-area painting are done, and
        # these need to work immediately, before that page is ever reached.
        self.ui.checkBox_constraint_90deg.toggled.connect(self.enforce_constraint_90deg)
        self.ui.checkBox_constraint_90deg_coronal.toggled.connect(self.enforce_constraint_90deg_coronal)

    def sync_misalignment(self, source):
        """Shared handler for dial_missalignment/doubleSpinBox_missalignment,
        tagged by whichever widget the user just touched, so the other one
        follows without re-triggering itself."""
        if source == 'dial':
            value = float(self.ui.dial_missalignment.value())
            self.ui.doubleSpinBox_missalignment.blockSignals(True)
            self.ui.doubleSpinBox_missalignment.setValue(value)
            self.ui.doubleSpinBox_missalignment.blockSignals(False)
        else:
            value = self.ui.doubleSpinBox_missalignment.value()
            self.ui.dial_missalignment.blockSignals(True)
            self.ui.dial_missalignment.setValue(int(round(value)))
            self.ui.dial_missalignment.blockSignals(False)

        self.coronal_misalignment_deg = value
        self.update_misalignment_guide_line()
        if hasattr(self, 'atlas_bregma_coords'):
            self.update_shank_angle_display()
        if self.ui.checkBox_constraint_90deg.isChecked():
            self.update_oblique_coronal_view()
            self.update_oblique_coronal_crossing_line()
        if self.ui.checkBox_constraint_90deg_coronal.isChecked():
            self.update_oblique_sagittal_view()
            self.update_oblique_sagittal_crossing_line()

    def _misalignment_geometry(self):
        """(half_w, half_h): RL/SI half-extents of the coronal slice, in
        the same display-world units update_misalignment_guide_line and
        draw_point use. Shared by the default center, the drag-mode
        classifier, and the line length."""
        spacing = self.LoadMRI.volumes[0].spacing  # zyx, same convention as draw_point
        shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx
        half_w = (shape[2] - 1) / 2.0 * spacing[2]  # RL half-extent (coronal display-x)
        half_h = (shape[0] - 1) / 2.0 * spacing[0]  # SI half-extent (coronal display-y)
        return half_w, half_h

    def _misalignment_center_default(self):
        return self._misalignment_geometry()

    def _misalignment_half_len(self):
        half_w, half_h = self._misalignment_geometry()
        return max(half_w, half_h) * 1.5

    def is_near_misalignment_line(self, world_pos, tolerance_voxels=4):
        """Treat a click as hitting the misalignment line if it lands
        within `tolerance_voxels` physical voxels of it (perpendicular
        distance to the infinite line through misalignment_line_center at
        the current angle) -- the rendered line is only ~1px wide, far too
        thin to reliably click on directly, so this gives it a generous
        margin instead of requiring vtkPropPicker to hit the exact
        geometry. The line only translates (see update_misalignment_line_
        translate) -- its angle is set by dial_missalignment/
        doubleSpinBox_missalignment, not by dragging."""
        cx, cy = self.misalignment_line_center or self._misalignment_center_default()
        theta = np.radians(self.coronal_misalignment_deg)
        dx, dy = np.sin(theta), np.cos(theta)  # unit direction of the line
        px, py = world_pos[0] - cx, world_pos[1] - cy
        perp_dist = abs(px * dy - py * dx)  # 2D cross product magnitude = perpendicular distance
        spacing = self.LoadMRI.volumes[0].spacing  # zyx
        voxel_size = max(spacing[0], spacing[2])  # SI/RL voxel sizes, display-space
        return perp_dist <= tolerance_voxels * voxel_size

    def start_misalignment_line_translate(self, world_pos):
        """CustomInteractorStyle.on_left_button_down, when a drag on the
        misalignment line starts nearer its middle than its ends: remember
        where the drag started so update_misalignment_line_translate can
        move the line by the same delta the mouse has moved since."""
        self._misalignment_drag_start_pos = world_pos
        self._misalignment_drag_start_center = self.misalignment_line_center or self._misalignment_center_default()

    def update_misalignment_line_translate(self, world_pos):
        """CustomInteractorStyle.on_mouse_move, while translate-dragging:
        slide the whole line (keeping its current angle) so it can be
        overlaid exactly onto a landmark that doesn't happen to pass
        through the image's geometric center."""
        start_pos = getattr(self, '_misalignment_drag_start_pos', None)
        start_center = getattr(self, '_misalignment_drag_start_center', None)
        if start_pos is None or start_center is None:
            return
        self.misalignment_line_center = (
            start_center[0] + (world_pos[0] - start_pos[0]),
            start_center[1] + (world_pos[1] - start_pos[1]),
        )
        self.update_misalignment_guide_line()

    def hide_misalignment_guide_line(self):
        """Remove the misalignment guide line -- called once bregma/lambda
        picking (page_5, stackedWidget_trajectoryplanning index 0) is
        done, since the line has no meaning past that step and would
        otherwise linger in the coronal view alongside update_atlas_plane_
        line's yellow reference line on later pages."""
        old = getattr(self, 'misalignment_line_actor', None)
        if old is not None:
            self.LoadMRI.renderers[0]['coronal'].RemoveActor(old)
            self.misalignment_line_actor = None
            self.render()

    def update_misalignment_guide_line(self):
        """dial_missalignment/doubleSpinBox_missalignment: draw a dashed
        guide line through misalignment_line_center (the coronal slice's
        geometric center by default, but draggable -- see
        update_misalignment_line_translate), rotated by the current manual
        misalignment angle away from vertical (0 deg = straight up/down --
        the assumed default with no head tilt). The angle itself is set
        via the dial/spin box; dragging the line only slides it (see
        is_near_misalignment_line/update_misalignment_line_translate) so
        it can be positioned exactly over the interhemispheric fissure (or
        another known-vertical/symmetric landmark) while you dial in the
        angle by eye. Purely a display aid, independent of bregma/lambda
        (which don't need to be set yet) -- redrawn whenever the dial,
        spin box, or line position changes.

        dial_missalignment/doubleSpinBox_missalignment stay live (their
        value still feeds ap_rl_si_frame_from_misalignment on later pages,
        e.g. for the constraint views) well past the bregma/lambda page,
        so sync_misalignment keeps calling this long after hide_
        misalignment_guide_line already removed the line -- without this
        page check, any later nudge of the dial/spin box (e.g. fine-tuning
        misalignment while placing shanks) would silently resurrect a
        guide line that page_5's own docstring says "has no meaning past
        that step".
        """
        view_name = 'coronal'
        old = getattr(self, 'misalignment_line_actor', None)
        if old is not None:
            self.LoadMRI.renderers[0][view_name].RemoveActor(old)
            self.misalignment_line_actor = None

        if self.ui.stackedWidget_trajectoryplanning.currentIndex() != 0:
            self.render()
            return

        if self.misalignment_line_center is None:
            self.misalignment_line_center = self._misalignment_center_default()
        cx, cy = self.misalignment_line_center
        half_len = self._misalignment_half_len()

        theta = np.radians(self.coronal_misalignment_deg)
        dx, dy = np.sin(theta), np.cos(theta)
        p1 = (cx - half_len * dx, cy - half_len * dy)
        p2 = (cx + half_len * dx, cy + half_len * dy)
        self.misalignment_line_actor = self._draw_dotted_line(view_name, p1, p2, color=(0, 1, 1))
        self.render()

    def oblique_click_to_voxel(self, kind, world_pos):
        """core/interactor_style.py's ObliqueInteractorStyle: convert a
        picked point on the oblique actor (world_pos, in the reslice
        OUTPUT's own flat coordinate system -- since the actor displays
        reslice.GetOutput() directly, a vtkPropPicker hit against it comes
        back already in that space, not the original volume's) into a
        voxel index in the original volume, using whatever axes/anchor
        update_oblique_coronal_view/update_oblique_sagittal_view last set
        the reslice to. This is the exact inverse of how those functions
        built the reslice: physical_input = anchor + x_out*x_axis +
        y_out*y_axis (the reslice's own X/Y reslice-axes direction
        cosines; the output's Z is always ~0 since OutputDimensionality
        is 2). Returns a voxel [x, y, z] array, or None if the relevant
        oblique view hasn't been oriented yet (no bregma/lambda/click has
        happened)."""
        if kind == 'coronal':
            axes = getattr(self, '_oblique_click_axes', None)
            anchor_mm = getattr(self, '_oblique_click_anchor_mm', None)
        else:
            axes = getattr(self, '_oblique_sagittal_click_axes', None)
            anchor_mm = getattr(self, '_oblique_sagittal_click_anchor_mm', None)
        if axes is None or anchor_mm is None:
            return None
        x_axis, y_axis, _normal_axis = axes

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        physical = anchor_mm + world_pos[0] * x_axis + world_pos[1] * y_axis
        voxel = physical / mri_spacing
        return voxel

    def set_oblique_cursor(self, kind, x_out, y_out):
        """ObliqueInteractorStyle.on_left_button_down: remember where the
        user just clicked (in the reslice output's own flat coordinate
        system) and redraw this oblique view's markers so the click is
        visibly acknowledged -- same idea as the crosshair cursor the 3
        real 2D views draw on click, just for this independent pipeline."""
        if kind == 'coronal':
            self._oblique_cursor_xy = (x_out, y_out)
        else:
            self._oblique_sagittal_cursor_xy = (x_out, y_out)
        self.refresh_oblique_markers(kind)

    def _oblique_project(self, kind, point_mm):
        """Orthogonal projection of a 3D physical-mm point onto the given
        oblique view's CURRENT cutting plane, in the reslice output's own
        flat (x_out, y_out) coordinate system -- exact inverse of
        oblique_click_to_voxel's forward mapping, since x_axis/y_axis are
        unit and mutually orthogonal. Returns None if that view hasn't
        been oriented yet."""
        if kind == 'coronal':
            axes = getattr(self, '_oblique_click_axes', None)
            anchor_mm = getattr(self, '_oblique_click_anchor_mm', None)
        else:
            axes = getattr(self, '_oblique_sagittal_click_axes', None)
            anchor_mm = getattr(self, '_oblique_sagittal_click_anchor_mm', None)
        if axes is None or anchor_mm is None:
            return None
        x_axis, y_axis, _normal_axis = axes
        diff = np.asarray(point_mm, dtype=float) - anchor_mm
        return float(np.dot(diff, x_axis)), float(np.dot(diff, y_axis))

    def _draw_oblique_line(self, kind, xy1, xy2, color, line_width=3):
        """Straight line between two (x_out, y_out) points on the given
        oblique view -- used to draw the shank itself (refresh_oblique_
        markers), in this pipeline's own flat output coordinates."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        line = vtk.vtkLineSource()
        line.SetPoint1(xy1[0], xy1[1], 1.08)
        line.SetPoint2(xy2[0], xy2[1], 1.08)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetLineWidth(line_width)
        renderer.AddActor(actor)
        return actor

    def _draw_oblique_marker(self, kind, xy, color, radius=0.1):
        """Small filled circle at (x_out, y_out) on the given oblique
        view -- same vtkRegularPolygonSource recipe (and same default
        radius) as Rendering.draw_point, just in this pipeline's own flat
        output coordinates instead of the mirrored per-view convention
        draw_point uses. Was defaulting to radius=1.0 -- 10x draw_point's
        own default -- making the insert/deep dots look enormous next to
        the real 2D views' markers."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        polygon_source = vtk.vtkRegularPolygonSource()
        polygon_source.GeneratePolygonOn()
        polygon_source.SetNumberOfSides(30)
        polygon_source.SetRadius(radius)
        polygon_source.SetCenter(xy[0], xy[1], 1.1)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(polygon_source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetOpacity(0.9)
        renderer.AddActor(actor)
        return actor

    def _draw_oblique_crosshair(self, kind, xy):
        """Blue crosshair (2 line actors spanning the full output image)
        at (x_out, y_out) on the given oblique view -- same role AND
        color as the real 2D views' own crosshair (core/cursor.py's
        SetColor(0, 0, 1)). Sized to this view's own image canvas
        (_oblique_output_geometry) -- previously used a fixed, much
        larger extent (the volume's full 3D diagonal, independent of
        `kind`), so the crosshair's own actor bounds were bigger than the
        actual image's. Since oblique_renderer.ResetCamera() fits every
        actor in the renderer, that oversized crosshair forced the camera
        to zoom out far past the image every time it was on screen,
        making the correctly-sized brain slice look tiny in a mostly
        black frame -- the "cursor is huge / slice isn't fully visible"
        bug."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        sx, sy, n_px_x, n_px_y = self._oblique_output_geometry(kind)
        half_w = (n_px_x - 1) * sx / 2.0
        half_h = (n_px_y - 1) * sy / 2.0

        actors = []
        for p1, p2 in (
            ((-half_w, xy[1], 1.05), (half_w, xy[1], 1.05)),
            ((xy[0], -half_h, 1.05), (xy[0], half_h, 1.05)),
        ):
            line = vtk.vtkLineSource()
            line.SetPoint1(*p1)
            line.SetPoint2(*p2)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(line.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0, 0, 1)
            actor.GetProperty().SetLineWidth(1)
            renderer.AddActor(actor)
            actors.append(actor)
        return actors

    def _oblique_shank_angle_actors(self, kind, mri_spacing):
        """Angle arc + caption for the currently selected shank on the
        oblique view -- same visual style (vtkArcSource + vtkCaptionActor2D)
        as _update_shank_angle_display_view's own arc/caption for the real
        axis-aligned views, but far simpler to compute: this view's own
        local (x_out, y_out) axes from _oblique_project ARE the roll/pitch
        reference frame (ap_rl_si_frame_from_misalignment) by construction,
        so the reference direction is just a fixed local axis -- local +Y
        (SI) for roll (oblique coronal), local +X (AP) for pitch (oblique
        sagittal) -- instead of a projected/clipped reference line. The
        angle NUMBER is still compute_shank_roll_pitch_mri, the same single
        source of truth as the real 2D views' captions and the PDF report,
        so it can't disagree with them.

        Anchored on coords_deepest_point/atlas_shank_end -- the SAME two
        points refresh_oblique_markers projects for the shank line itself
        (NOT mri_insert/mri_deep, which can sit visibly short of the drawn
        line's own far end -- see create_channel_list's own note on
        atlas_shank_end sitting further out than the marked insertion
        point) -- so the arc always lands centered exactly on the visible
        green line instead of floating off near wherever the marked
        insertion point happens to be. Returns [] (nothing to draw) if the
        current shank has no deep point/geometry yet."""
        deep_point = getattr(self, 'coords_deepest_point', {}).get(self.shank_number)
        shank_end = getattr(self, 'atlas_shank_end', {}).get(self.shank_number)
        if deep_point is None or shank_end is None:
            return []
        roll_pitch = self.compute_shank_roll_pitch_mri(self.shank_number)
        if roll_pitch is None:
            return []
        angle = roll_pitch[0] if kind == 'coronal' else roll_pitch[1]

        deep_xy = self._oblique_project(kind, np.array(deep_point, dtype=float) * mri_spacing)
        end_xy = self._oblique_project(kind, np.array(shank_end, dtype=float) * mri_spacing)
        if deep_xy is None or end_xy is None:
            return []
        shank_dir = np.array(end_xy) - np.array(deep_xy)
        shank_norm = np.linalg.norm(shank_dir)
        if shank_norm < 1e-9:
            return []
        shank_dir = shank_dir / shank_norm
        ref_dir = np.array([0.0, 1.0]) if kind == 'coronal' else np.array([1.0, 0.0])

        # the reference is a line, not a directed ray -- draw the acute
        # wedge (matching compute_shank_roll_pitch_mri's own arctan2(abs,
        # abs), which is always in [0, 90] deg) instead of whichever of the
        # two supplementary angles the arbitrary axis sign happened to pick.
        if np.dot(shank_dir, ref_dir) < 0:
            ref_dir = -ref_dir

        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        center = np.array(deep_xy)
        radius = 3.0  # mm -- fixed so the indicator stays a consistent, readable size regardless of shank length

        arc = vtk.vtkArcSource()
        arc.SetCenter(center[0], center[1], 1.13)
        arc.SetPoint1(center[0] + shank_dir[0] * radius, center[1] + shank_dir[1] * radius, 1.13)
        arc.SetPoint2(center[0] + ref_dir[0] * radius, center[1] + ref_dir[1] * radius, 1.13)
        arc.SetResolution(20)
        arc_mapper = vtk.vtkPolyDataMapper()
        arc_mapper.SetInputConnection(arc.GetOutputPort())
        arc_actor = vtk.vtkActor()
        arc_actor.SetMapper(arc_mapper)
        arc_actor.GetProperty().SetColor(1, 1, 1)
        arc_actor.GetProperty().SetLineWidth(2)
        renderer.AddActor(arc_actor)

        bisector = shank_dir + ref_dir
        bisector_norm = np.linalg.norm(bisector)
        bisector_dir = bisector / bisector_norm if bisector_norm > 1e-9 else np.array([-shank_dir[1], shank_dir[0]])
        pos = center + bisector_dir * (radius + 1.0)

        label = "Roll" if kind == 'coronal' else "Pitch"
        caption = vtk.vtkCaptionActor2D()
        caption.SetCaption(f"{label}: {angle:.1f}°")
        caption.SetAttachmentPoint(pos[0], pos[1], 1.15)
        caption.BorderOff()
        caption.LeaderOff()
        caption.GetCaptionTextProperty().SetColor(1, 1, 1)
        caption.GetCaptionTextProperty().SetFontSize(36)
        caption.GetCaptionTextProperty().SetBold(True)
        caption.GetCaptionTextProperty().ShadowOff()
        caption.GetCaptionTextProperty().BoldOff()
        caption.SetPosition(3, 3)
        caption.SetWidth(0.22)
        caption.SetHeight(0.05)
        renderer.AddActor(caption)

        return [arc_actor, caption]

    def _register_zoom_camera(self, camera):
        """Adds camera to the cross-view zoom-link group -- a ModifiedEvent
        observer that copies this camera's parallel scale onto every other
        REGISTERED camera whenever it changes, so zooming/panning any one
        of axial, the real coronal/sagittal views, or their oblique
        constraint-view counterparts keeps every other one in step
        ("connect them altogether", not just a real<->its own oblique
        handoff). Purely additive -- a new observer layered on top of each
        renderer's own existing camera -- so it doesn't touch the shared
        Zoom/Cursor machinery used everywhere else in the app; nothing
        outside this trajectory-planning screen is affected, and it only
        starts applying once a constraint checkbox is used for the first
        time (see _ensure_all_views_zoom_linked, the only caller)."""
        if not hasattr(self, '_zoom_linked_cameras'):
            self._zoom_linked_cameras = []
            self._zoom_sync_in_progress = False
        if any(c is camera for c in self._zoom_linked_cameras):
            return
        self._zoom_linked_cameras.append(camera)

        def on_modified(caller, event):
            if self._zoom_sync_in_progress:
                return
            self._zoom_sync_in_progress = True
            try:
                scale = caller.GetParallelScale()
                for cam in self._zoom_linked_cameras:
                    if cam is not caller and cam.GetParallelScale() != scale:
                        cam.SetParallelScale(scale)
                self.render()
                for r in (getattr(self, 'oblique_renderer', None), getattr(self, 'oblique_sagittal_renderer', None)):
                    if r is not None:
                        r.GetRenderWindow().Render()
            finally:
                self._zoom_sync_in_progress = False

        camera.AddObserver('ModifiedEvent', on_modified)

    def _ensure_all_views_zoom_linked(self):
        """Registers whichever of axial/coronal/sagittal/oblique-coronal/
        oblique-sagittal cameras currently exist into the zoom-link group
        (_register_zoom_camera already no-ops on a camera registered
        twice) -- called from both setup_oblique_coronal_view and setup_
        oblique_sagittal_view so the group ends up complete regardless of
        which constraint checkbox the user tries first."""
        for vn in ('axial', 'coronal', 'sagittal'):
            renderer = self.LoadMRI.renderers.get(0, {}).get(vn)
            if renderer is not None:
                self._register_zoom_camera(renderer.GetActiveCamera())
        if getattr(self, 'oblique_renderer', None) is not None:
            self._register_zoom_camera(self.oblique_renderer.GetActiveCamera())
        if getattr(self, 'oblique_sagittal_renderer', None) is not None:
            self._register_zoom_camera(self.oblique_sagittal_renderer.GetActiveCamera())

    def force_oblique_repaint(self, kind):
        """Extra deferred repaint once the oblique page has just become the
        VISIBLE stackedWidget page (checkBox_constraint_90deg/_coronal's
        toggle handlers, called right after their own setCurrentIndex(1))
        -- VTK doesn't always paint a freshly (re)shown render window until
        something forces it after Qt finishes the page-swap layout, same
        class of bug already documented/worked around elsewhere in this
        codebase (registration.py's do_get_shank_line, update_oblique_
        coronal_view's own trailing QTimer.singleShot) -- the symptom here
        being the oblique view showing a stale/wrong-looking cut until the
        user's first click on it forces a repaint. Unlike those one-time
        page arrivals, this page is entered/left repeatedly by toggling the
        same checkbox, so it needs its own nudge on every entry rather than
        only once at initial setup."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        if renderer is None:
            return
        QTimer.singleShot(0, renderer.GetRenderWindow().Render)

    def refresh_oblique_markers(self, kind):
        """Redraw the insert/deep point markers (red/green, matching the
        real 2D views' own draw_point colors) and the shank line itself
        for the currently selected shank, plus the last-clicked cursor
        crosshair if any click has happened yet, all projected onto
        whatever plane this oblique view is currently cut along
        (_oblique_project). Called whenever that plane moves
        (update_oblique_coronal_view/update_oblique_sagittal_view) or a
        click updates the cursor (set_oblique_cursor)."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        if renderer is None:
            return
        old_actors = getattr(self, '_oblique_marker_actors' if kind == 'coronal' else '_oblique_sagittal_marker_actors', [])
        for a in old_actors:
            renderer.RemoveActor(a)
        new_actors = []

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        mri_insert = getattr(self, 'mri_insert', {}).get(self.shank_number)
        mri_deep = getattr(self, 'mri_deep', {}).get(self.shank_number)

        # The shank line itself -- same endpoints (deepest point ->
        # atlas_shank_end, the electrode's far end past the last channel;
        # see ElecGeometryMri.create_channel_list) and per-shank color as
        # the real 2D views' own draw_electrode_line. Whenever the AP=0/
        # RL=0 constraint is active, the WHOLE shank is exactly coplanar
        # with this oblique cut by construction, so unlike
        # draw_electrode_line there's no separate dim/bright split needed
        # -- the projection alone already places it correctly.
        shank_end = getattr(self, 'atlas_shank_end', {}).get(self.shank_number)
        deep_point = getattr(self, 'coords_deepest_point', {}).get(self.shank_number)
        if shank_end is not None and deep_point is not None:
            xy1 = self._oblique_project(kind, np.array(deep_point, dtype=float) * mri_spacing)
            xy2 = self._oblique_project(kind, np.array(shank_end, dtype=float) * mri_spacing)
            if xy1 is not None and xy2 is not None:
                new_actors.append(self._draw_oblique_line(kind, xy1, xy2, self.get_shank_vtk_color(self.shank_number)))

        if mri_insert is not None:
            xy = self._oblique_project(kind, np.array(mri_insert, dtype=float) * mri_spacing)
            if xy is not None:
                new_actors.append(self._draw_oblique_marker(kind, xy, (1, 0, 0)))
        if mri_deep is not None:
            xy = self._oblique_project(kind, np.array(mri_deep, dtype=float) * mri_spacing)
            if xy is not None:
                new_actors.append(self._draw_oblique_marker(kind, xy, (0, 1, 0)))

        cursor_xy = getattr(self, '_oblique_cursor_xy' if kind == 'coronal' else '_oblique_sagittal_cursor_xy', None)
        if cursor_xy is not None:
            new_actors.extend(self._draw_oblique_crosshair(kind, cursor_xy))

        new_actors.extend(self._oblique_shank_angle_actors(kind, mri_spacing))

        if kind == 'coronal':
            self._oblique_marker_actors = new_actors
        else:
            self._oblique_sagittal_marker_actors = new_actors
        widget = self.ui.vtkWidget_data_coronal_3 if kind == 'coronal' else self.ui.vtkWidget_data_sagittal_3
        widget.GetRenderWindow().Render()

    def _oblique_plane_origin(self, anchor_mm, normal_axis):
        """A point on the same cutting plane as anchor_mm (i.e. with the
        same position along normal_axis) but re-centered on the volume's
        own physical middle in the plane's other two directions -- used
        as ResliceAxesOrigin instead of anchor_mm itself.

        anchor_mm (the current shank's insert point, or bregma) only
        needs to pick WHICH plane gets cut -- its coordinate along
        normal_axis. Using it as-is for ResliceAxesOrigin also centered
        the in-plane (x,y) window on it, so an output canvas sized to
        the volume's own full cross-section (_oblique_output_geometry)
        ran past the volume's true bounds on one side while cutting off
        real anatomy on the other, any time the insert point wasn't near
        the volume's own geometric center -- the "half the slice is
        missing" bug. The real axis-aligned views are never re-centered
        like this; they always show the volume's own natural framing,
        which is what this restores."""
        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        nz, ny, nx = self.LoadMRI.volumes[0].slices[0].shape
        volume_center_mm = np.array([(nx - 1) / 2.0, (ny - 1) / 2.0, (nz - 1) / 2.0]) * mri_spacing
        return volume_center_mm - np.dot(volume_center_mm - anchor_mm, normal_axis) * normal_axis

    def _oblique_output_geometry(self, kind):
        """(spacing_x, spacing_y, n_px_x, n_px_y) for an oblique view's
        output canvas -- exactly the width/height/spacing convention
        ImageLayer.setup_vtk (core/image_layer.py) uses for the real
        axis-aligned 'coronal'/'sagittal' view, instead of an isotropic
        square padded to the volume's largest extent regardless of cut
        orientation. That padding was the "spacing is off" bug: the
        brain rendered small/off-scale next to the real views (ResetCamera
        fits the whole padded canvas, not just the data in it), and every
        reslice recompute (insert-point move, misalignment dial drag) had
        to interpolate a needlessly huge image -- part of why the oblique
        views felt laggy. Used by both setup_oblique_coronal_view/
        setup_oblique_sagittal_view (base MRI) and
        _build_oblique_label_overlay (region-label overlay), so the two
        layers always share the same canvas."""
        spacing_zyx = self.LoadMRI.volumes[0].spacing
        nz, ny, nx = self.LoadMRI.volumes[0].slices[0].shape
        if kind == 'coronal':
            return spacing_zyx[2], spacing_zyx[0], nx, nz
        return spacing_zyx[1], spacing_zyx[0], ny, nz

    def _build_oblique_label_overlay(self, kind):
        """Atlas-region-label overlay (self.mri_label_vol) reslice +
        actor, matching the same output-geometry convention
        (_oblique_output_geometry) setup_oblique_coronal_view/setup_
        oblique_sagittal_view use for the base MRI, for whichever oblique
        view ('coronal' or 'sagittal') this is being built for. Nearest-
        neighbor interpolation (categorical data, unlike the cubic-
        interpolated base MRI). Colored via the same discrete LUT
        (self._mri_label_overlay_lut) and opacity (0.6) as the normal 2D
        views' "Brain Regions" layer (build_mri_label_overlay). Returns
        (reslice, actor), or (None, None) if the overlay hasn't been
        built yet -- self.mri_label_vol only exists once build_mri_label_
        overlay has run, which can be after an oblique view was first set
        up if its constraint checkbox was toggled while still on the
        bregma/lambda page; update_oblique_coronal_view/update_oblique_
        sagittal_view retry this every call until it succeeds."""
        if not hasattr(self, 'mri_label_vol'):
            return None, None
        vol = self.mri_label_vol  # zyx numpy array
        spacing_zyx = self.LoadMRI.volumes[0].spacing
        nz, ny, nx = vol.shape

        vtk_data = numpy_support.numpy_to_vtk(np.ascontiguousarray(vol).ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
        volume_img = vtk.vtkImageData()
        volume_img.SetDimensions(nx, ny, nz)
        volume_img.SetSpacing(spacing_zyx[2], spacing_zyx[1], spacing_zyx[0])
        volume_img.SetOrigin(0.0, 0.0, 0.0)
        volume_img.GetPointData().SetScalars(vtk_data)
        # keep alive -- vtk_data holds no python ref of its own, and a
        # stale/GC'd volume_img would silently blank the overlay
        self._oblique_label_volume_imgs = getattr(self, '_oblique_label_volume_imgs', [])
        self._oblique_label_volume_imgs.append(volume_img)

        sx, sy, n_px_x, n_px_y = self._oblique_output_geometry(kind)

        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(volume_img)
        reslice.SetOutputDimensionality(2)
        reslice.SetInterpolationModeToNearestNeighbor()
        reslice.SetOutputSpacing(sx, sy, 1.0)
        reslice.SetOutputOrigin(-(n_px_x - 1) * sx / 2.0, -(n_px_y - 1) * sy / 2.0, 0.0)
        reslice.SetOutputExtent(0, n_px_x - 1, 0, n_px_y - 1, 0, 0)

        actor = vtk.vtkImageActor()
        actor.GetMapper().SetInputConnection(reslice.GetOutputPort())
        actor.GetProperty().SetInterpolationTypeToNearest()
        actor.GetProperty().SetOpacity(0.6)
        actor.GetProperty().SetLookupTable(self._mri_label_overlay_lut)
        actor.GetProperty().UseLookupTableScalarRangeOn()
        return reslice, actor

    def _wire_oblique_zoom_controls(self, kind):
        """Wire the zoom-in/zoom-out/fit-to-window/pan-arrow buttons form.ui
        already has on this oblique page (form.ui's page_32/page_33 were
        copied from the real coronal/sagittal pages, buttons included) --
        unlike the real 3 axis-aligned views, initialize_zoom_controls
        (gui_utils/buttons_gui_structural.py) never reaches these: it only wires
        button names for idx in range(len(lm.vtk_widgets.items())), and
        the oblique renderers are deliberately never added to lm.
        vtk_widgets/lm.renderers (see setup_oblique_coronal_view's own
        note on why -- several shared per-view loops there aren't safe to
        extend to a 4th/5th view), so these buttons were simply never
        connected to anything. Drives the oblique renderer's own camera
        directly instead of the shared Zoom/Minimap classes, which are
        hard-wired to exactly those 3 real views."""
        suffix = '2_3' if kind == 'coronal' else '1_3'
        zoom_in_btn = getattr(self.ui, f'zoom_in_data3d{suffix}')
        zoom_out_btn = getattr(self.ui, f'zoom_out_data3d{suffix}')
        fit_btn = getattr(self.ui, f'fit_to_zoom_data3d{suffix}')
        go_up_btn = getattr(self.ui, f'go_up_data3d{suffix}')
        go_down_btn = getattr(self.ui, f'go_down_data3d{suffix}')
        go_left_btn = getattr(self.ui, f'go_left_data3d{suffix}')
        go_right_btn = getattr(self.ui, f'go_right_data3d{suffix}')

        zoom_in_btn.clicked.connect(lambda _, k=kind: self._oblique_zoom(k, 1.2))
        zoom_out_btn.clicked.connect(lambda _, k=kind: self._oblique_zoom(k, 0.8))
        fit_btn.clicked.connect(lambda _, k=kind: self._oblique_fit_to_window(k))
        pan_distance = 0.4  # same fraction-of-view step Minimap.pan_arrows uses
        go_up_btn.clicked.connect(lambda _, k=kind: self._oblique_pan(k, 0, pan_distance))
        go_down_btn.clicked.connect(lambda _, k=kind: self._oblique_pan(k, 0, -pan_distance))
        go_right_btn.clicked.connect(lambda _, k=kind: self._oblique_pan(k, pan_distance, 0))
        go_left_btn.clicked.connect(lambda _, k=kind: self._oblique_pan(k, -pan_distance, 0))

    def _oblique_widget(self, kind):
        return self.ui.vtkWidget_data_coronal_3 if kind == 'coronal' else self.ui.vtkWidget_data_sagittal_3

    def _oblique_zoom(self, kind, factor):
        """Relative zoom, same factor/direction convention as Zoom.zoom
        (utils/zoom.py): factor>1 zooms in (smaller parallel scale),
        factor<1 zooms out."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        if renderer is None:
            return
        camera = renderer.GetActiveCamera()
        camera.SetParallelScale(camera.GetParallelScale() / factor)
        self._oblique_widget(kind).GetRenderWindow().Render()

    def _oblique_fit_to_window(self, kind):
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        if renderer is None:
            return
        renderer.ResetCamera()
        self._oblique_widget(kind).GetRenderWindow().Render()

    def _oblique_pan(self, kind, dx_frac, dy_frac):
        """Slide the oblique camera by (dx_frac, dy_frac) times its
        current parallel scale -- same fractional-of-view convention as
        Minimap.pan_arrows, just applied directly to this view's own
        camera instead of going through the shared Minimap class."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        if renderer is None:
            return
        camera = renderer.GetActiveCamera()
        scale = camera.GetParallelScale()
        dx, dy = dx_frac * scale, dy_frac * scale
        fp = camera.GetFocalPoint()
        pos = camera.GetPosition()
        camera.SetFocalPoint(fp[0] + dx, fp[1] + dy, fp[2])
        camera.SetPosition(pos[0] + dx, pos[1] + dy, pos[2])
        self._oblique_widget(kind).GetRenderWindow().Render()

    def setup_oblique_coronal_view(self):
        """One-time setup for the oblique coronal view (vtkWidget_data_
        coronal_3, stackedWidget_coronal page index 2, added directly in
        form.ui) -- a true oblique MPR reslice of the MRI volume
        perpendicular to the actual bregma-lambda (AP) axis, shown instead
        of the normal axis-aligned coronal slice while checkBox_
        constraint_90deg is checked (see ElecGeometryMri.
        enforce_constraint_90deg), since the AP=0-constrained shank
        generally does not lie within any single fixed-y coronal slice.

        Built as a SEPARATE, standalone VTK pipeline (its own renderer,
        its own persistent 3D vtkImageData, its own vtkImageReslice)
        rather than going through the shared ImageLayer/LoadMRI.setup_
        layer machinery every other 2D view uses -- that machinery (and
        Cursor.add_cursor_interaction's per-view crosshair math, and
        Zoom's fit-to-window) is hard-wired for exactly the 3 axis-aligned
        views ('axial','sagittal','coronal') in many places, so bolting a
        4th, differently-oriented view onto it would risk destabilizing
        those already-working views. This stays fully independent:
        nothing about the other 3 views changes.

        Stage 1 (this + update_oblique_coronal_view): gets the picture
        itself geometrically correct -- shows only the base MRI, and
        isn't yet interactive (no bregma/lambda/insert/deep picking on
        it). Click support is a deliberate follow-up once the plane
        geometry has been visually verified against real data.
        """
        if getattr(self, 'oblique_actor', None) is not None:
            return

        renderer = vtk.vtkRenderer()
        self.ui.vtkWidget_data_coronal_3.GetRenderWindow().AddRenderer(renderer)
        # Parallel (orthographic) projection, matching every other 2D view
        # -- Zoom.fit_to_window is what turns this on for axial/sagittal/
        # coronal (utils/zoom.py), but this renderer bypasses that shared
        # mechanism entirely, so without this it stays on VTK's default
        # perspective camera and looks subtly 3D/distorted instead of a
        # flat slice.
        renderer.GetActiveCamera().ParallelProjectionOn()
        self.ui.vtkWidget_data_coronal_3.GetRenderWindow().GetInteractor().SetInteractorStyle(
            ObliqueInteractorStyle(self.LoadMRI, 'coronal'))
        # Deliberately NOT self.LoadMRI.renderers[0]['coronal_oblique'] --
        # several existing generic loops (e.g. core/interactor_style.py's
        # zoom-drag handler, `for vn in self.LoadMRI.renderers.get(0, {})`)
        # iterate that shared dict's keys expecting a matching entry in
        # OTHER per-view dicts too (self.LoadMRI.scale_bar, Zoom.bounds,
        # etc.) that only ever get populated for the 3 real axis-aligned
        # views -- adding a 4th key there crashes those loops with a
        # KeyError the moment you zoom/pan. Kept as its own attribute
        # instead so nothing that iterates the shared registry ever sees it.
        self.oblique_renderer = renderer

        vol = self.LoadMRI.volumes[0].slices[0]  # zyx numpy array
        spacing_zyx = self.LoadMRI.volumes[0].spacing
        nz, ny, nx = vol.shape

        vtk_data = numpy_support.numpy_to_vtk(np.ascontiguousarray(vol).ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        volume_img = vtk.vtkImageData()
        volume_img.SetDimensions(nx, ny, nz)
        volume_img.SetSpacing(spacing_zyx[2], spacing_zyx[1], spacing_zyx[0])
        volume_img.SetOrigin(0.0, 0.0, 0.0)
        volume_img.GetPointData().SetScalars(vtk_data)
        self._oblique_volume_img = volume_img  # keep alive -- vtk_data holds no python ref of its own

        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(volume_img)
        reslice.SetOutputDimensionality(2)
        reslice.SetInterpolationModeToCubic()

        # Output canvas centered on the reslice origin (set per-call in
        # update_oblique_coronal_view), with exactly the real coronal
        # view's own width/height/spacing (_oblique_output_geometry) --
        # not an isotropic square padded to the volume's largest extent.
        sx, sy, n_px_x, n_px_y = self._oblique_output_geometry('coronal')
        reslice.SetOutputSpacing(sx, sy, 1.0)
        reslice.SetOutputOrigin(-(n_px_x - 1) * sx / 2.0, -(n_px_y - 1) * sy / 2.0, 0.0)
        reslice.SetOutputExtent(0, n_px_x - 1, 0, n_px_y - 1, 0, 0)
        self._oblique_reslice = reslice

        actor = vtk.vtkImageActor()
        actor.GetMapper().SetInputConnection(reslice.GetOutputPort())
        actor.GetProperty().SetInterpolationTypeToCubic()
        self._link_oblique_actor_to_contrast(actor)
        renderer.AddActor(actor)
        self.oblique_actor = actor

        label_reslice, label_actor = self._build_oblique_label_overlay('coronal')
        self._oblique_label_reslice = label_reslice
        self.oblique_label_actor = label_actor
        if label_actor is not None:
            renderer.AddActor(label_actor)

        self._wire_oblique_zoom_controls('coronal')
        self.update_oblique_coronal_view()
        self._draw_oblique_reference_line('coronal')
        self._setup_oblique_scale_bar('coronal')
        self._ensure_all_views_zoom_linked()

    def _link_oblique_actor_to_contrast(self, actor):
        """Share the base MRI's own live vtkLookupTable (utils/contrast.py's
        Contrast, data_index 0/image_index 0 -- the same LUT core/image_
        layer.py's ImageLayer attaches to the 3 real axis-aligned views)
        with an oblique-view image actor, same technique/object, so
        dragging the contrast/brightness sliders or hitting Auto/Reset
        repaints this view too instead of it staying stuck at VTK's plain
        default window/level forever. Contrast.update_lut_window_level
        mutates this same table object in place (SetTableRange/Build) and
        then separately triggers the actual repaint -- see its own
        oblique_renderer/oblique_sagittal_renderer render calls, which is
        what this sharing is paired with. No-op (falls back to VTK's
        default grayscale mapping) if Contrast hasn't been set up yet for
        this dataset."""
        contrast = getattr(self.LoadMRI, 'contrast', {}).get(0)
        lut = getattr(contrast, 'lut_vtk', {}).get(0) if contrast is not None else None
        if lut is None:
            return
        actor.GetProperty().SetLookupTable(lut)
        actor.GetProperty().UseLookupTableScalarRangeOn()

    def _draw_oblique_reference_line(self, kind):
        """Yellow line marking the true SI axis within the oblique view's
        own local coordinate frame -- since the reslice's own X axis IS
        the RL axis (coronal) or AP axis (sagittal) and Y axis IS the SI
        axis (see update_oblique_coronal_view/update_oblique_sagittal_
        view's own SetResliceAxesDirectionCosines calls), this is just a
        vertical line through local x=0, unlike the real axis-aligned
        coronal view's update_atlas_plane_line (which needs actual
        plane-vs-slice clipping math since its own display axes aren't
        the reslice's own axes). Drawn once at setup time since the output
        canvas geometry (_oblique_output_geometry) -- and so this line's
        own position within it -- never changes after that; only the
        reslice's CONTENT moves as the anchor/misalignment change."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        _sx, sy, _n_px_x, n_px_y = self._oblique_output_geometry(kind)
        half_h = (n_px_y - 1) * sy / 2.0

        line = vtk.vtkLineSource()
        line.SetPoint1(0, -half_h, 1.06)
        line.SetPoint2(0, half_h, 1.06)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 0)
        actor.GetProperty().SetLineWidth(1)
        actor.GetProperty().SetLineStipplePattern(0xF0F0)  # dashed, same pattern as core/measurement.py
        actor.GetProperty().SetLineStippleRepeatFactor(10)
        renderer.AddActor(actor)
        return actor

    def _setup_oblique_scale_bar(self, kind):
        """Self-contained scale bar for the oblique view -- deliberately
        NOT utils/scale_bar.py's shared Scale class, which re-fetches its
        target renderer via self.LoadMRI.renderers[image_index][view_name]
        internally regardless of the renderer passed in, so it would
        silently draw onto the wrong (real axis-aligned) renderer here --
        see setup_oblique_coronal_view's own note on why this view's
        renderer is deliberately kept out of that shared registry. Redraws
        on every camera change (zoom/pan/reset) via a ModifiedEvent
        observer, same live-updating behaviour as the real views' own
        scale bar, without touching any of that shared machinery."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        if not hasattr(self, '_oblique_scale_bar_actors'):
            self._oblique_scale_bar_actors = {}
        camera = renderer.GetActiveCamera()
        camera.AddObserver('ModifiedEvent', lambda *_: self._update_oblique_scale_bar(kind))
        self._update_oblique_scale_bar(kind)

    def _update_oblique_scale_bar(self, kind, length_cm=1.0, color=(0, 1, 0)):
        """(Re)draws the oblique view's scale bar to match its current
        zoom level -- same bounds-to-display-fraction technique as utils/
        scale_bar.py's Scale.create_bar/update_bar, just against this
        view's own renderer directly instead of a shared per-view-name
        registry lookup."""
        renderer = self.oblique_renderer if kind == 'coronal' else self.oblique_sagittal_renderer
        xmin, xmax, ymin, ymax, zmin, zmax = renderer.ComputeVisiblePropBounds()
        window_width, _ = renderer.GetSize()
        if not window_width or xmax == xmin:
            return

        renderer.SetWorldPoint(xmin, ymin, zmin, 1.0)
        renderer.WorldToDisplay()
        x_nmin = renderer.GetDisplayPoint()[0] / window_width
        renderer.SetWorldPoint(xmax, ymax, zmax, 1.0)
        renderer.WorldToDisplay()
        x_nmax = renderer.GetDisplayPoint()[0] / window_width

        length_mm = length_cm * 10
        length_x = (x_nmax - x_nmin) / (xmax - xmin) * length_mm
        use_mm = length_x > 0.45
        if use_mm:
            length_x /= 10

        old = self._oblique_scale_bar_actors.get(kind)
        if old is not None:
            renderer.RemoveActor2D(old['line'])
            renderer.RemoveActor(old['text'])

        line = vtk.vtkLineSource()
        line.SetPoint1(0, 0, 0)
        line.SetPoint2(length_x * window_width, 0, 0)
        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(line.GetOutputPort())
        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetLineWidth(3)
        actor.SetPositionCoordinate(vtk.vtkCoordinate())
        actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
        offset = (0.95 - length_x, 0.05)
        actor.GetPositionCoordinate().SetValue(*offset)

        text = vtk.vtkTextActor()
        text.SetInput(f"{length_cm} mm" if use_mm else f"{length_cm} cm")
        text.GetPositionCoordinate().SetValue(0.83, offset[1] + 0.03)
        text.GetTextProperty().SetColor(*color)
        text.GetTextProperty().SetFontSize(14)
        text.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()

        renderer.AddActor2D(actor)
        renderer.AddActor(text)
        self._oblique_scale_bar_actors[kind] = {'line': actor, 'text': text}

    def update_oblique_coronal_view(self):
        """Recompute the oblique reslice's cutting plane: origin at the
        currently selected shank's insert point if one exists (most
        relevant to whatever you're currently placing), else bregma;
        axes = (rl_axis, si_axis, ap_axis-as-normal) from ap_rl_si_frame_
        from_misalignment, the exact same frame compute_shank_roll_pitch_
        mri uses, so this view is always cut exactly perpendicular to the
        same true AP axis the angle numbers are measured against. No-op
        if the view hasn't been set up yet or bregma/lambda aren't set."""
        if getattr(self, 'oblique_actor', None) is None:
            return
        if self.coords_bregma is None or self.coords_lambda is None:
            return

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)
        frame = self.ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg)
        if frame is None:
            return
        ap_axis, rl_axis, si_axis = frame

        mri_insert = getattr(self, 'mri_insert', {}).get(self.shank_number)
        anchor_mm = np.array(mri_insert, dtype=float) * mri_spacing if mri_insert is not None else bregma_mm
        plane_origin_mm = self._oblique_plane_origin(anchor_mm, ap_axis)

        # Cached for ObliqueInteractorStyle's click-to-voxel conversion --
        # a picked point on the reslice output (x_out, y_out) maps back to
        # a volume physical point via plane_origin_mm + x_out*x_axis +
        # y_out*y_axis (the reslice's own X/Y direction cosines), and
        # x_axis/y_axis/origin need to be exactly whatever this call just
        # set, not recomputed independently at click time.
        self._oblique_click_axes = (rl_axis, si_axis, ap_axis)
        self._oblique_click_anchor_mm = plane_origin_mm

        reslice = self._oblique_reslice
        reslice.SetResliceAxesDirectionCosines(
            rl_axis[0], rl_axis[1], rl_axis[2],
            si_axis[0], si_axis[1], si_axis[2],
            ap_axis[0], ap_axis[1], ap_axis[2],
        )
        reslice.SetResliceAxesOrigin(plane_origin_mm[0], plane_origin_mm[1], plane_origin_mm[2])
        reslice.Update()

        if getattr(self, 'oblique_label_actor', None) is None:
            # wasn't available at setup time (build_mri_label_overlay
            # hadn't run yet) -- retry now that bregma/lambda are set,
            # which on the real workflow's page order means we're at
            # least as far along as do_get_shank_line.
            label_reslice, label_actor = self._build_oblique_label_overlay('coronal')
            self._oblique_label_reslice = label_reslice
            self.oblique_label_actor = label_actor
            if label_actor is not None:
                self.oblique_renderer.AddActor(label_actor)
        if getattr(self, '_oblique_label_reslice', None) is not None:
            self._oblique_label_reslice.SetResliceAxesDirectionCosines(
                rl_axis[0], rl_axis[1], rl_axis[2],
                si_axis[0], si_axis[1], si_axis[2],
                ap_axis[0], ap_axis[1], ap_axis[2],
            )
            self._oblique_label_reslice.SetResliceAxesOrigin(plane_origin_mm[0], plane_origin_mm[1], plane_origin_mm[2])
            self._oblique_label_reslice.Update()

        self.oblique_renderer.ResetCamera()
        self.refresh_oblique_markers('coronal')
        # self.render() only touches the 3 known axis-aligned widgets (see
        # main_window.py's own render()), so it never repaints vtkWidget_
        # data_coronal_3 -- and per registration_mri.py's own note elsewhere,
        # a freshly (re)shown VTK render window doesn't always get painted
        # until something forces a repaint after Qt finishes laying it out.
        # QTimer.singleShot(0, ...) so this fires after that layout pass,
        # same pattern already used there.
        QTimer.singleShot(0, self.ui.vtkWidget_data_coronal_3.GetRenderWindow().Render)

    def hide_oblique_coronal_crossing_line(self):
        """Remove the white sagittal-view line showing where the oblique
        coronal reslice cuts -- called when checkBox_constraint_90deg is
        unchecked, since that line has no meaning once the coronal panel
        is back to the normal axis-aligned view."""
        old = getattr(self, 'oblique_crossing_line_actor', None)
        if old is not None:
            self.LoadMRI.renderers[0]['sagittal'].RemoveActor(old)
            self.oblique_crossing_line_actor = None
            self.render()

    def update_oblique_coronal_crossing_line(self):
        """White dashed line in the sagittal view showing exactly where
        the oblique coronal reslice (update_oblique_coronal_view) cuts
        through the sagittal slice currently being viewed -- since that
        cut is tilted relative to the raw axes (normal = the true AP
        axis, not raw y), it isn't a fixed vertical/horizontal line the
        way the normal axis-aligned coronal slice's position would be.
        Reuses the same plane-vs-slice crossing math as the yellow roll-
        reference line (update_atlas_plane_line/_atlas_plane_segment_in_
        view) -- same kind of plane (ap_axis-normal), just anchored at
        the oblique view's own reslice origin instead of bregma, and
        drawn in the sagittal view instead of coronal."""
        view_name = 'sagittal'
        old = getattr(self, 'oblique_crossing_line_actor', None)
        if old is not None:
            self.LoadMRI.renderers[0][view_name].RemoveActor(old)
            self.oblique_crossing_line_actor = None

        if getattr(self, 'oblique_actor', None) is None:
            return
        if self.coords_bregma is None or self.coords_lambda is None:
            return


        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())

        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)
        frame = self.ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg)
        if frame is None:
            return
        ap_axis, _rl_axis, _si_axis = frame

        mri_insert = getattr(self, 'mri_insert', {}).get(self.shank_number)
        anchor_mm = np.array(mri_insert, dtype=float) * mri_spacing if mri_insert is not None else bregma_mm

        segment = self._atlas_plane_segment_in_view(view_name, ap_axis, anchor_mm)
        if segment is None:
            return
        p1_xy = self._atlas_point_display_xy(segment[0], view_name)
        p2_xy = self._atlas_point_display_xy(segment[1], view_name)
        self.oblique_crossing_line_actor = self._draw_dotted_line(view_name, p1_xy, p2_xy, color=(1, 1, 1))
        self.render()

    def setup_oblique_sagittal_view(self):
        """Coronal-angle analogue of setup_oblique_coronal_view: one-time
        setup for the oblique sagittal view (vtkWidget_data_sagittal_3,
        stackedWidget_sagittal page index 1, added directly in form.ui) --
        a true oblique MPR reslice of the MRI volume perpendicular to the
        true RL axis, shown instead of the normal axis-aligned sagittal
        slice while checkBox_constraint_90deg_coronal is checked (see
        ElecGeometryMri.enforce_constraint_90deg_coronal), since the
        RL=0-constrained shank generally does not lie within any single
        fixed-x sagittal slice.

        Same fully-separate, standalone VTK pipeline as the coronal
        version, for the same reason (existing per-view generic loops --
        e.g. core/interactor_style.py's zoom-drag handler -- are hard-
        wired for exactly the 3 axis-aligned views and crash if a 4th key
        is added to their shared registries)."""
        if getattr(self, 'oblique_sagittal_actor', None) is not None:
            return

        renderer = vtk.vtkRenderer()
        self.ui.vtkWidget_data_sagittal_3.GetRenderWindow().AddRenderer(renderer)
        renderer.GetActiveCamera().ParallelProjectionOn()  # see setup_oblique_coronal_view's note
        self.ui.vtkWidget_data_sagittal_3.GetRenderWindow().GetInteractor().SetInteractorStyle(
            ObliqueInteractorStyle(self.LoadMRI, 'sagittal'))
        self.oblique_sagittal_renderer = renderer  # NOT self.LoadMRI.renderers -- see setup_oblique_coronal_view's note

        vol = self.LoadMRI.volumes[0].slices[0]  # zyx numpy array
        spacing_zyx = self.LoadMRI.volumes[0].spacing
        nz, ny, nx = vol.shape

        vtk_data = numpy_support.numpy_to_vtk(np.ascontiguousarray(vol).ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        volume_img = vtk.vtkImageData()
        volume_img.SetDimensions(nx, ny, nz)
        volume_img.SetSpacing(spacing_zyx[2], spacing_zyx[1], spacing_zyx[0])
        volume_img.SetOrigin(0.0, 0.0, 0.0)
        volume_img.GetPointData().SetScalars(vtk_data)
        self._oblique_sagittal_volume_img = volume_img  # keep alive -- vtk_data holds no python ref of its own

        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(volume_img)
        reslice.SetOutputDimensionality(2)
        reslice.SetInterpolationModeToCubic()

        # See setup_oblique_coronal_view's identical note -- output canvas
        # matches the real sagittal view's own width/height/spacing.
        sx, sy, n_px_x, n_px_y = self._oblique_output_geometry('sagittal')
        reslice.SetOutputSpacing(sx, sy, 1.0)
        reslice.SetOutputOrigin(-(n_px_x - 1) * sx / 2.0, -(n_px_y - 1) * sy / 2.0, 0.0)
        reslice.SetOutputExtent(0, n_px_x - 1, 0, n_px_y - 1, 0, 0)
        self._oblique_sagittal_reslice = reslice

        actor = vtk.vtkImageActor()
        actor.GetMapper().SetInputConnection(reslice.GetOutputPort())
        actor.GetProperty().SetInterpolationTypeToCubic()
        self._link_oblique_actor_to_contrast(actor)
        renderer.AddActor(actor)
        self.oblique_sagittal_actor = actor

        label_reslice, label_actor = self._build_oblique_label_overlay('sagittal')
        self._oblique_sagittal_label_reslice = label_reslice
        self.oblique_sagittal_label_actor = label_actor
        if label_actor is not None:
            renderer.AddActor(label_actor)

        self._wire_oblique_zoom_controls('sagittal')
        self.update_oblique_sagittal_view()
        self._draw_oblique_reference_line('sagittal')
        self._setup_oblique_scale_bar('sagittal')
        self._ensure_all_views_zoom_linked()

    def update_oblique_sagittal_view(self):
        """Recompute the oblique sagittal reslice's cutting plane: origin
        at the currently selected shank's insert point if one exists,
        else bregma; axes = (ap_axis, si_axis, rl_axis-as-normal) from
        ap_rl_si_frame_from_misalignment -- same frame compute_shank_
        roll_pitch_mri uses, so this view is always cut exactly
        perpendicular to the same true RL axis the roll angle is
        measured against. No-op if the view hasn't been set up yet or
        bregma/lambda aren't set."""
        if getattr(self, 'oblique_sagittal_actor', None) is None:
            return
        if self.coords_bregma is None or self.coords_lambda is None:
            return

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)
        frame = self.ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg)
        if frame is None:
            return
        ap_axis, rl_axis, si_axis = frame

        mri_insert = getattr(self, 'mri_insert', {}).get(self.shank_number)
        anchor_mm = np.array(mri_insert, dtype=float) * mri_spacing if mri_insert is not None else bregma_mm
        plane_origin_mm = self._oblique_plane_origin(anchor_mm, rl_axis)

        # See update_oblique_coronal_view's identical note.
        self._oblique_sagittal_click_axes = (ap_axis, si_axis, rl_axis)
        self._oblique_sagittal_click_anchor_mm = plane_origin_mm

        reslice = self._oblique_sagittal_reslice
        reslice.SetResliceAxesDirectionCosines(
            ap_axis[0], ap_axis[1], ap_axis[2],
            si_axis[0], si_axis[1], si_axis[2],
            rl_axis[0], rl_axis[1], rl_axis[2],
        )
        reslice.SetResliceAxesOrigin(plane_origin_mm[0], plane_origin_mm[1], plane_origin_mm[2])
        reslice.Update()

        if getattr(self, 'oblique_sagittal_label_actor', None) is None:
            label_reslice, label_actor = self._build_oblique_label_overlay('sagittal')
            self._oblique_sagittal_label_reslice = label_reslice
            self.oblique_sagittal_label_actor = label_actor
            if label_actor is not None:
                self.oblique_sagittal_renderer.AddActor(label_actor)
        if getattr(self, '_oblique_sagittal_label_reslice', None) is not None:
            self._oblique_sagittal_label_reslice.SetResliceAxesDirectionCosines(
                ap_axis[0], ap_axis[1], ap_axis[2],
                si_axis[0], si_axis[1], si_axis[2],
                rl_axis[0], rl_axis[1], rl_axis[2],
            )
            self._oblique_sagittal_label_reslice.SetResliceAxesOrigin(plane_origin_mm[0], plane_origin_mm[1], plane_origin_mm[2])
            self._oblique_sagittal_label_reslice.Update()

        self.oblique_sagittal_renderer.ResetCamera()
        self.refresh_oblique_markers('sagittal')
        QTimer.singleShot(0, self.ui.vtkWidget_data_sagittal_3.GetRenderWindow().Render)

    def hide_oblique_sagittal_crossing_line(self):
        """Remove the white coronal-view line showing where the oblique
        sagittal reslice cuts -- called when checkBox_constraint_90deg_
        coronal is unchecked, since that line has no meaning once the
        sagittal panel is back to the normal axis-aligned view."""
        old = getattr(self, 'oblique_sagittal_crossing_line_actor', None)
        if old is not None:
            self.LoadMRI.renderers[0]['coronal'].RemoveActor(old)
            self.oblique_sagittal_crossing_line_actor = None
            self.render()

    def update_oblique_sagittal_crossing_line(self):
        """White dashed line in the coronal view showing exactly where
        the oblique sagittal reslice (update_oblique_sagittal_view) cuts
        through the coronal slice currently being viewed -- coronal-angle
        analogue of update_oblique_coronal_crossing_line, same plane-vs-
        slice crossing math, just for the RL-normal plane and drawn in
        the coronal view instead of sagittal."""
        view_name = 'coronal'
        old = getattr(self, 'oblique_sagittal_crossing_line_actor', None)
        if old is not None:
            self.LoadMRI.renderers[0][view_name].RemoveActor(old)
            self.oblique_sagittal_crossing_line_actor = None

        if getattr(self, 'oblique_sagittal_actor', None) is None:
            return
        if self.coords_bregma is None or self.coords_lambda is None:
            return

        mri_spacing = np.array(self.movingImg_resampled.GetSpacing())
        bregma_mm = np.array(self.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(self.coords_lambda, dtype=float) * mri_spacing
        misalignment_deg = getattr(self, 'coronal_misalignment_deg', 0.0)
        frame = self.ap_rl_si_frame_from_misalignment(bregma_mm, lambda_mm, misalignment_deg)
        if frame is None:
            return
        _ap_axis, rl_axis, _si_axis = frame

        mri_insert = getattr(self, 'mri_insert', {}).get(self.shank_number)
        anchor_mm = np.array(mri_insert, dtype=float) * mri_spacing if mri_insert is not None else bregma_mm

        segment = self._atlas_plane_segment_in_view(view_name, rl_axis, anchor_mm)
        if segment is None:
            return
        p1_xy = self._atlas_point_display_xy(segment[0], view_name)
        p2_xy = self._atlas_point_display_xy(segment[1], view_name)
        self.oblique_sagittal_crossing_line_actor = self._draw_dotted_line(view_name, p1_xy, p2_xy, color=(1, 1, 1))
        self.render()
