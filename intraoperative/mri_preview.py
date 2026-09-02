# This Python file uses the following encoding: utf-8
"""
Standalone 3D reference view for the Surgery tab: renders the ORIGINAL
planned shank trajectories over the subject's own MRI scan, in MRI space.

Deliberately independent of TrajectoryPlanning/registration/atlas -- this
is a static reference only. The intraoperative bregma/lambda correction
(intraoperative/reprojection.py) lives in the manipulator's own physical
frame, which has no defined mapping back into image space (no fiducial or
calibration ties "the null point" to a location in this scan), so the
correction can't be reflected here -- this view always shows the pre-op
plan as originally saved, for visual orientation/sanity-check only.
"""
import os
import sys
import glob
import numpy as np
from scipy import ndimage
from skimage.filters import threshold_otsu
import SimpleITK as sitk
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer
from mrid_utils.handlers import find_ind_data
from paths_config import _paths

# Same palette as trajectory_planning/shank.py's NEON_COLORS (vtk-color
# tuples only, not reusing that module directly to avoid pulling in its
# Qt-icon-building helpers for a single color list).
_SHANK_COLORS = [
    (0.0, 1.0, 28 / 255), (1.0, 20 / 255, 147 / 255), (0.0, 191 / 255, 1.0),
    (1.0, 1.0, 0.0), (138 / 255, 0.0, 196 / 255), (1.0, 92 / 255, 0.0), (1.0, 1.0, 1.0),
]


class SurgeryMRIPreview:
    """Owns one QtInteractor embedded in a plain placeholder QWidget (same
    pattern as Visualisation3D.__init__, trajectory_planning/
    visualisation3D.py). ui is kept only for toggle_perspective's icon
    swap (resetCamera_vis3D_2/change_perspective_vis3D_2, wired in
    main_window.py's add_actions, mirror the docked pre-op 3D view's own
    resetCamera_vis3D/change_perspective_vis3D -- see TrajectoryPlanning3D
    Window._toggle_perspective, trajectory_planning_3d/window.py)."""

    def __init__(self, container_widget, ui):
        self.ui = ui
        self.parallel_projection = True
        self.last_missing_reason = None
        self._render_generation = 0
        pv.global_theme.background = 'black'
        layout = QVBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(container_widget)
        # Same MSAA-off + desired-update-rate perf settings as the docked
        # pre-op 3D view (TrajectoryPlanning3DWindow.__init__/
        # Visualisation3D.__init__, trajectory_planning_3d/window.py:79-81)
        # -- this view previously never set either, which is the actual
        # cause of it feeling laggy on interaction.
        self.plotter.render_window.SetMultiSamples(0)
        self.plotter.render_window.GetInteractor().SetDesiredUpdateRate(30)
        layout.addWidget(self.plotter)

    def toggle_perspective(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.parallel_projection:
            self.plotter.disable_parallel_projection()
            self.ui.change_perspective_vis3D_2.setIcon(
                QIcon(os.path.join(base_dir, "Icons", "ephys", "projection_prespective.png")))
            self.parallel_projection = False
        else:
            self.plotter.enable_parallel_projection()
            self.ui.change_perspective_vis3D_2.setIcon(
                QIcon(os.path.join(base_dir, "Icons", "ephys", "projection_parallel.png")))
            self.parallel_projection = True

    def locate_resampled_mri(self, pdf_path, individual_id, mri_spacing_mm):
        """Reconstructs the same resampled-filename convention finish_
        trajectory_work uses (main_window.py:1065-1085) without any of that
        function's registration/TrajectoryPlanning setup. Returns None
        (rather than regenerating a missing file) if it isn't already on
        disk -- this is a read-only reference view, not a data pipeline.

        Tries the exact name finish_trajectory_work would use for this
        plan's recorded spacing first -- branching on the 25um case exactly
        like it does, since at that one spacing the file on disk is samri_
        main.py's own registration output (ResampleData.resampling25um's
        fixed "_resampled.nii.gz" name, no spacing suffix), not the generic
        "_resampled{spacing}um.nii.gz" resampling50um_trajectoryPlanning
        produces at every other spacing -- but that exact name is a guess
        that's frequently wrong: mri_spacing_mm (this plan's recorded
        value) is tp.movingImg_resampled.GetSpacing(), the REAL spacing
        read back off the resampled file's own header
        (file_input_output.py:982), whereas the FILENAME finish_
        trajectory_work writes is built from data[2], the spacing the user
        REQUESTED (main_window.py:1085) -- and resampling50um_
        trajectoryPlanning rounds the voxel count to an integer
        (file_handling/resample_data.py:295-303), so the true final
        spacing it ends up writing essentially never equals the clean
        requested number in the filename (e.g. plan records
        0.0499798879mm, actual file on disk is "..._resampled50um.nii.gz").

        So when the exact name doesn't exist, every "_resampled*.nii.gz"
        file actually sitting next to the raw scan is opened just far
        enough to read its header spacing, and whichever one is closest to
        mri_spacing_mm[0] (within 20%, to reject an unrelated file rather
        than silently picking the nearest of several genuinely different
        resamplings -- e.g. 25/50/100um candidates are all >2x apart, well
        outside that band) is returned. This replaces trusting there being
        exactly one "_resampled*" candidate, which breaks the moment a
        subject has been resampled at more than one spacing (common: 25um
        for atlas registration, 50/100um for trajectory planning).

        self.last_missing_reason is set to a human-readable explanation
        (naming the exact path(s)/candidates checked) whenever this
        returns None, and left untouched on success --
        surgery_controller.load_plan surfaces it in the "Loaded:" label
        (persistent, unlike a status-bar message) so a black 3D view
        always has a visible, on-screen cause."""
        if not individual_id:
            self.last_missing_reason = "no individual_id in the loaded plan"
            print(f"[SurgeryMRIPreview] {self.last_missing_reason} -- can't look for an MRI.", flush=True)
            return None
        folder = os.path.dirname(os.path.abspath(pdf_path))
        matches = find_ind_data(individual_id, folder)
        if len(matches) != 1:
            self.last_missing_reason = (
                f"expected exactly one raw scan matching '*-{individual_id}.nii.gz' "
                f"in {folder}, found {len(matches)}")
            print(f"[SurgeryMRIPreview] {self.last_missing_reason}: {matches}", flush=True)
            return None
        raw_path = os.path.join(folder, matches[0])
        stem = raw_path[:-7]
        if abs(mri_spacing_mm[0] - 0.025) < 1e-9:
            expected_path = f"{stem}_resampled.nii.gz"
        else:
            spacing_um = mri_spacing_mm[0] * 1000
            expected_path = f"{stem}_resampled{spacing_um:.10g}um.nii.gz"
        if os.path.exists(expected_path):
            return expected_path

        candidates = glob.glob(f"{stem}_resampled*.nii.gz")
        if not candidates:
            self.last_missing_reason = (
                f"no '_resampled*.nii.gz' file next to the raw scan (checked "
                f"exact name {expected_path}, and glob '{stem}_resampled*.nii.gz')")
            print(f"[SurgeryMRIPreview] {self.last_missing_reason}", flush=True)
            return None

        best_path, best_diff = None, None
        spacings = {}
        for candidate in candidates:
            try:
                reader = sitk.ImageFileReader()
                reader.SetFileName(candidate)
                reader.ReadImageInformation()
                candidate_spacing = reader.GetSpacing()[0]
            except Exception as exc:
                spacings[candidate] = f"<unreadable: {exc!r}>"
                continue
            spacings[candidate] = candidate_spacing
            diff = abs(candidate_spacing - mri_spacing_mm[0])
            if best_diff is None or diff < best_diff:
                best_path, best_diff = candidate, diff

        if best_path is not None and best_diff <= 0.2 * mri_spacing_mm[0]:
            return best_path

        self.last_missing_reason = (
            f"none of the {len(candidates)} '_resampled*.nii.gz' candidate(s) next to the raw scan "
            f"have a spacing close to this plan's recorded {mri_spacing_mm[0] * 1000:.10g}um "
            f"(candidates and their actual spacings: "
            f"{ {os.path.basename(k): v for k, v in spacings.items()} })")
        print(f"[SurgeryMRIPreview] {self.last_missing_reason}", flush=True)
        return None

    def _locate_registration_transform(self, mri_path):
        """registration/output_Composite.h5 -- the actual SimpleITK
        rigid+affine+SyN transform saved by the offline registration run
        (samri/samri_main.py:257-276) -- sits as a SIBLING of the anat-style
        folder mri_path lives in (confirmed against real session layouts:
        .../<session>/anat/<...>.nii.gz next to .../<session>/registration/
        output_Composite.h5), same convention core/electrode_localization.py
        already relies on via LoadMRI.session_path. Returns None (rather
        than trying to regenerate it) if it isn't there -- this is a
        read-only reference view, not a data pipeline (see module
        docstring)."""
        registration_dir = os.path.join(os.path.dirname(os.path.dirname(mri_path)), 'registration')
        transform_path = os.path.join(registration_dir, 'output_Composite.h5')
        return transform_path if os.path.exists(transform_path) else None

    def _build_atlas_warped_shell(self, mri_img_ras, transform_path, downsample):
        """Exactly TrajectoryPlanning3DWindow._build_background_mesh's own
        MRI-mode construction (trajectory_planning_3d/window.py:791-865):
        the shell's SHAPE always comes from the atlas volume's own
        threshold(0.5) mask -- a clean, hand-curated brain outline -- never
        from this subject's own (noisy) raw MRI intensities. Every vertex
        is then warped into this subject's true MRI space through the real
        registration transform, the same math as CoordTransform.
        atlas_to_mri_coordinates (trajectory_planning/coord_transform.py)
        applies per landmark point -- just run here directly, since this
        tab has no live TrajectoryPlanning instance to call it on. Only the
        shell's COLOR then comes from this subject's real MRI intensity,
        sampled at those already atlas-shaped, already correctly
        positioned vertices.

        Returns None (triggering the raw-MRI Otsu fallback below) if the
        atlas or transform can't be loaded, or the transform doesn't apply
        to this atlas -- e.g. an older/differently-atlas'd registration."""
        try:
            fixed_img = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
            atlas_vol = sitk.GetArrayFromImage(fixed_img)
            transform = sitk.ReadTransform(transform_path)
        except Exception:
            return None

        data_zyx = atlas_vol[::downsample, ::downsample, ::downsample]
        data_xyz = np.transpose(data_zyx, (2, 1, 0))
        vol = pv.ImageData()
        vol.dimensions = np.array(data_xyz.shape) + 1
        vol.spacing = tuple(s * downsample for s in fixed_img.GetSpacing())
        vol.origin = (0.0, 0.0, 0.0)
        vol.cell_data['NIFTI'] = data_xyz.flatten(order='F')

        background = vol.threshold(value=0.5)
        background = background.extract_surface(algorithm='dataset_surface')
        background = background.clean().triangulate()
        background = background.fill_holes(hole_size=1e10)
        background = background.clean().triangulate()
        background = background.decimate(0.75)
        smoothed = background.smooth_taubin(n_iter=50, pass_band=0.1)

        # smoothed.points sit on vol's own (origin=0, spacing=atlas_spacing
        # *downsample) grid, so dividing back out by the ATLAS's true
        # (non-downsampled) spacing recovers each vertex's continuous
        # native-resolution atlas voxel index -- exactly the "atlas voxel
        # index" atlas_to_mri_coordinates's own TransformIndexToPhysical
        # Point takes, just continuous (post-decimate/smooth vertices don't
        # land exactly on integer voxels) rather than integer, via
        # TransformContinuousIndexToPhysicalPoint. mri_img_ras is already
        # this subject's own resampled scan reoriented to canonical RAS --
        # the exact same object TrajectoryPlanning calls movingImg_resampled
        # -- so a single TransformPhysicalPointToContinuousIndex on it here
        # already lands in the right grid, with no separate round-trip
        # through a raw, un-resampled moving image needed.
        atlas_spacing = np.array(fixed_img.GetSpacing())
        mri_idx = np.empty_like(smoothed.points)
        for i, pt in enumerate(smoothed.points):
            fixed_pt = fixed_img.TransformContinuousIndexToPhysicalPoint((pt / atlas_spacing).tolist())
            moving_pt = transform.TransformPoint(fixed_pt)
            mri_idx[i] = mri_img_ras.TransformPhysicalPointToContinuousIndex(moving_pt)

        mri_spacing = np.array(mri_img_ras.GetSpacing())
        mri_arr = sitk.GetArrayFromImage(mri_img_ras).astype(np.float32)  # zyx, full resolution
        # Trilinear sample (see the Otsu-path fallback's own comment on
        # why), zero outside the volume's own bounds -- same as
        # _build_background_mesh's explicit in_bounds check.
        coords_zyx = mri_idx[:, ::-1].T
        intensity = ndimage.map_coordinates(mri_arr, coords_zyx, order=1, mode='constant', cval=0.0)

        smoothed.points = mri_idx * mri_spacing
        smoothed.point_data['MRI'] = intensity
        return smoothed

    def _build_otsu_shell(self, arr_zyx_full, spacing, downsample):
        """Raw-MRI-intensity fallback for subjects with no registration/
        output_Composite.h5 on disk (see _locate_registration_transform) --
        the same Otsu + largest-connected-component segmentation this
        method used exclusively before the atlas-warp path above existed.
        Less faithful to TP-3D's own MRI-mode shell (that one never
        segments the raw MRI at all), but the best available without a
        real registration to warp the atlas mask through."""
        arr_zyx = arr_zyx_full[::downsample, ::downsample, ::downsample]
        arr_xyz = np.transpose(arr_zyx, (2, 1, 0))

        # A voxel with no actual value (NaN -- genuinely missing/undefined
        # data, not just a real reading of zero) gets filled in from its
        # neighbors; every real zero (background, air, or otherwise) stays
        # zero and is excluded outright below -- no "is this zero actually
        # background or noise" guessing.
        missing_mask = np.isnan(arr_xyz)
        if missing_mask.any():
            valid_mask = ~missing_mask
            neighbor_sum = ndimage.uniform_filter(np.where(valid_mask, arr_xyz, 0.0), size=3) * 27
            neighbor_count = ndimage.uniform_filter(valid_mask.astype(np.float32), size=3) * 27
            with np.errstate(invalid='ignore', divide='ignore'):
                local_mean = np.where(neighbor_count > 0, neighbor_sum / neighbor_count, 0.0)
            arr_xyz = np.where(missing_mask, local_mean, arr_xyz)

        # This tab has no atlas/registration to reproject a "not background"
        # mask from (see module docstring). A raw, unstripped MRI's
        # background isn't exact zero --
        # scanner noise floor, skull, scalp -- so a bare 1e-6 threshold lets
        # nearly the whole volume through, producing a noisy, not-brain-
        # shaped shell instead of a recognizable head. Otsu's method finds
        # the intensity cutoff that best separates that noise floor from
        # real tissue; binary_fill_holes closes any internal gaps the cutoff
        # leaves in solid tissue, and keeping only the largest connected
        # component drops stray noise blobs that survive thresholding but
        # aren't attached to the head at all.
        otsu = threshold_otsu(arr_xyz[arr_xyz > 0])
        mask = arr_xyz > otsu
        mask = ndimage.binary_fill_holes(mask)
        labeled, num_components = ndimage.label(mask)
        if num_components > 0:
            sizes = ndimage.sum(mask, labeled, range(1, num_components + 1))
            mask = labeled == (1 + np.argmax(sizes))
        # Zero out everything outside the mask in arr_xyz itself (not just
        # a separate copy used for the shell's shape) -- the later
        # intensity resampling below reads from this same array, so
        # skull/scalp/noise voxels just outside the mask boundary would
        # otherwise still bleed into the shell's own coloring.
        arr_xyz = np.where(mask, arr_xyz, 0.0)

        vol = pv.ImageData()
        vol.dimensions = np.array(arr_xyz.shape) + 1
        vol.spacing = spacing
        vol.origin = (0.0, 0.0, 0.0)
        vol.cell_data['MRI'] = arr_xyz.flatten(order='F')

        # Shell = threshold (drop everything outside the Otsu+largest-
        # component mask above) -> extract the outer surface -> clean/fill/
        # re-triangulate -> decimate (BEFORE smoothing, so the final
        # triangle count is capped rather than scaling with input
        # resolution) -> Taubin-smooth to hide the facets decimation
        # introduces. Exact same steps, same order, as
        # _build_background_mesh (trajectory_planning_3d/window.py:812-823).
        mesh = vol.threshold(value=1e-6, scalars='MRI')
        mesh = mesh.extract_surface(algorithm='dataset_surface')
        mesh = mesh.clean().triangulate()
        mesh = mesh.fill_holes(hole_size=1e10)
        mesh = mesh.clean().triangulate()
        mesh = mesh.decimate(0.75)
        smoothed = mesh.smooth_taubin(n_iter=50, pass_band=0.1)

        # Re-sample MRI intensity at the smoothed shell's own vertex
        # positions -- trilinear interpolation (map_coordinates, order=1),
        # NOT nearest-voxel rounding: the shell's surface sits exactly on
        # the boundary between nonzero and background cells, so rounding
        # to the nearest voxel lands on the zero side roughly half the
        # time there (verified against a synthetic test volume), speckling
        # the shell with false-black facets. Trilinear sampling blends
        # smoothly across that boundary instead.
        voxel_coords = smoothed.points / spacing  # continuous (x, y, z) indices
        intensity = ndimage.map_coordinates(arr_xyz, voxel_coords.T, order=1, mode='nearest')
        smoothed.point_data['MRI'] = intensity
        return smoothed

    def render(self, mri_path, data, downsample=3):
        """data: the parsed plan JSON (FileOutput.compute()'s output,
        trajectory_planning/file_input_output.py). Renders the scan as a
        static translucent surface shell, shaped and positioned the exact
        same way TrajectoryPlanning3DWindow._build_background_mesh's own
        MRI-mode shell is (see _build_atlas_warped_shell) whenever this
        subject's registration outputs are available on disk, falling back
        to a plain raw-MRI segmentation (_build_otsu_shell) otherwise --
        plus each shank's original mri_insert/mri_deep line segment (the
        exact voxel indices the saved plan already carries, so no atlas/
        registration lookup is needed for those).

        downsample=3, matching _build_background_mesh's own factor: the
        decimate(0.75) step inside each shell builder caps the final
        triangle count regardless of input resolution.

        Returns True on success, False if any step failed -- in which case
        the scene is left cleared (see clear()) rather than half-built, and
        the exception is printed so a black view has a visible cause
        instead of failing silently."""
        try:
            self._render(mri_path, data, downsample)
            return True
        except Exception as exc:
            import traceback
            self.last_missing_reason = f"render of {mri_path} failed: {exc!r}"
            print(f"[SurgeryMRIPreview] 3D preview render failed for {mri_path!r}:", flush=True)
            traceback.print_exc()
            sys.stderr.flush()
            self.clear()
            return False

    def _render(self, mri_path, data, downsample):
        self._render_generation += 1
        generation = self._render_generation
        self.plotter.clear()
        img = sitk.ReadImage(mri_path)
        # mri_insert/mri_deep are voxel indices into movingImg_resampled,
        # which is the RAW resampled file reoriented to canonical RAS
        # (LoadMRI.volumes[0].oriented_ref_image, set via file_handling/
        # mri_volume.py:56's sitk.DICOMOrient(image_raw, "RAS")) -- NOT the
        # raw file's own on-disk orientation, which resample_data.py never
        # canonicalizes. Applying the same reorientation here is required
        # for those voxel indices (and axis0/1/2 = axial/coronal/sagittal,
        # relied on by axial_view.py) to mean the same thing they do
        # everywhere else in the app.
        img = sitk.DICOMOrient(img, "RAS")
        # mri_insert/mri_deep (below) are voxel indices into the FULL-
        # resolution resampled grid -- keep the true spacing for converting
        # those to physical mm, separate from the volume's own (downsampled)
        # grid spacing, or shanks/landmarks would be placed ~downsample-fold
        # too far out.
        orig_spacing = np.array(img.GetSpacing())

        transform_path = self._locate_registration_transform(mri_path)
        smoothed = None
        if transform_path is not None:
            smoothed = self._build_atlas_warped_shell(img, transform_path, downsample)
        if smoothed is None:
            arr_zyx_full = sitk.GetArrayFromImage(img).astype(np.float32)
            smoothed = self._build_otsu_shell(arr_zyx_full, orig_spacing * downsample, downsample)

        intensity = smoothed.point_data['MRI']
        # Stretch contrast to the real tissue range, same 1st/99th
        # percentile-of-nonzero convention as _build_background_mesh's own
        # MRI-mode clim.
        nonzero = intensity[intensity > 0]
        clim = [float(p) for p in np.percentile(nonzero, [1, 99])] if nonzero.size else None
        print(f"[SurgeryMRIPreview] sampled shell intensity: min={intensity.min():.3g} "
              f"max={intensity.max():.3g} mean={intensity.mean():.3g} "
              f"nonzero_frac={nonzero.size / max(intensity.size, 1):.3f} clim={clim}", flush=True)
        # Background (intensity<=0, e.g. a sampling/registration mismatch
        # putting shell vertices outside real tissue) must be fully
        # transparent, not just cmap='gray' opaque-black at 0.5 opacity --
        # a shell that's uniformly (or mostly) background would otherwise
        # look identical to the plain black pv.global_theme.background,
        # with no visual signal that anything is wrong.
        point_opacity = np.where(intensity > 0, 0.5, 0.0)

        self.plotter.add_mesh(smoothed, scalars='MRI', cmap='gray', clim=clim, show_scalar_bar=False,
                              opacity=point_opacity, style='surface', culling='front', pickable=False,
                              name='surgery_mri_volume', reset_camera=False, render=False)

        shank_keys = sorted(data["shanks"], key=lambda k: int(k.split("_")[1]))
        for i, key in enumerate(shank_keys):
            raw = data["shanks"][key]["raw"]
            insert_mm = np.array(raw["mri_insert"], dtype=float) * orig_spacing
            deep_mm = np.array(raw["mri_deep"], dtype=float) * orig_spacing
            color = _SHANK_COLORS[i % len(_SHANK_COLORS)]
            self.plotter.add_mesh(pv.Line(deep_mm, insert_mm), color=color,
                                   line_width=4, name=f'surgery_shank_line_{i}')
            # Small floating label at the insertion point -- same
            # add_point_labels call convention as the docked pre-op 3D
            # view's own per-shank labels (Visualisation3D.render_shanks,
            # trajectory_planning/visualisation3D.py:809-824), just at a
            # smaller font size since this is a compact reference view, not
            # the main working canvas.
            self.plotter.add_point_labels(
                pv.PolyData(insert_mm.reshape(1, 3)), [f"Shank {i + 1}"],
                text_color=color, font_size=10, shape=None, bold=True,
                shadow=False, show_points=False, always_visible=True,
                name=f'surgery_shank_label_{i}', render=False, reset_camera=False)

        # Same red/green convention as everywhere else bregma/lambda are
        # drawn (CoordTransform.get_bregma/get_lambda, trajectory_planning/
        # coord_transform.py). bregma_mm/lambda_mm are already physical mm
        # (FileOutput.compute()'s raw block), same space as insert_mm/
        # deep_mm above -- no further spacing multiply needed. lighting=
        # False renders them as flat, fully-saturated color regardless of
        # viewing angle -- shaded phong spheres (the previous default)
        # go dark/brown on their unlit side and read as dull, not colorful.
        # Colors MUST be floats (1.0, not 1) -- pv.Color treats an all-int
        # tuple as literal 0-255 8-bit values, not normalized 0-1, so
        # color=(1, 0, 0) silently became near-black #010000 instead of red.
        bregma_mm = np.array(data["raw"]["bregma_mm"], dtype=float)
        lambda_mm = np.array(data["raw"]["lambda_mm"], dtype=float)
        self.plotter.add_mesh(pv.Sphere(radius=0.4, center=bregma_mm), color=(1.0, 0.0, 0.0),
                               lighting=False, pickable=False, name='surgery_bregma')
        self.plotter.add_mesh(pv.Sphere(radius=0.4, center=lambda_mm), color=(0.0, 0.0, 1.0),
                               lighting=False, pickable=False, name='surgery_lambda')
        # Label text stays plain white (readable against both the dark
        # background and the gray MRI shell) rather than matching each
        # sphere's own color -- add_point_labels only takes one text_color
        # per call anyway, so bregma/lambda still need their own calls.
        for point_mm, text in ((bregma_mm, "Bregma"), (lambda_mm, "Lambda")):
            self.plotter.add_point_labels(
                pv.PolyData(point_mm.reshape(1, 3)), [text],
                text_color='white', font_size=10, shape=None, bold=True,
                shadow=False, show_points=False, always_visible=True,
                name=f'surgery_{text.lower()}_label', render=False, reset_camera=False)

        # Orientation widget, same call as the docked pre-op 3D view
        # (trajectory_planning_3d/window.py:147).
        self.plotter.add_axes()

        self.plotter.reset_camera()
        self.plotter.render()
        print(f"[SurgeryMRIPreview] render() done for {mri_path!r}: "
              f"{smoothed.n_points} shell points, bounds={smoothed.bounds}, "
              f"n_actors={len(self.plotter.renderer.actors)}, "
              f"widget size={self.plotter.width()}x{self.plotter.height()}, "
              f"widget visible={self.plotter.isVisible()}, "
              f"camera pos={self.plotter.camera_position}", flush=True)
        # reset_camera() right after add_mesh can land on a degenerate
        # camera if the container widget hasn't been given a real size yet
        # (e.g. first-ever visit to the Surgery tab, still mid-layout) --
        # same failure mode trajectory_planning_3d/window.py's own
        # _maybe_reset_camera works around, just via retries here instead
        # of showEvent/resizeEvent (this class isn't a QWidget to override
        # those on). `generation` no-ops a retry if a newer render() (or
        # clear()) has already superseded this one.
        for delay_ms in (50, 200, 500):
            QTimer.singleShot(delay_ms, lambda g=generation: self._maybe_redo_camera(g))

    def _maybe_redo_camera(self, generation):
        if generation != self._render_generation:
            return
        if self.plotter.width() <= 10 or self.plotter.height() <= 10:
            return
        self.plotter.reset_camera()
        self.plotter.render()

    def clear(self):
        self._render_generation += 1
        self.plotter.clear()
        self.plotter.render()
