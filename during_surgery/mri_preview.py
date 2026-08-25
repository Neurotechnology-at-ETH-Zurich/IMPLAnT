# This Python file uses the following encoding: utf-8
"""
Standalone 3D reference view for the Surgery tab: renders the ORIGINAL
planned shank trajectories over the subject's own MRI scan, in MRI space.

Deliberately independent of TrajectoryPlanning/registration/atlas -- this
is a static reference only. The intraoperative bregma/lambda correction
(during_surgery/reprojection.py) lives in the manipulator's own physical
frame, which has no defined mapping back into image space (no fiducial or
calibration ties "the null point" to a location in this scan), so the
correction can't be reflected here -- this view always shows the pre-op
plan as originally saved, for visual orientation/sanity-check only.
"""
import os
import numpy as np
from scipy import ndimage
import SimpleITK as sitk
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QIcon
from mrid_utils.handlers import find_ind_data

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
        pv.global_theme.background = 'black'
        layout = QVBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(container_widget)
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
        trajectory_work uses (main_window.py) without any of that
        function's registration/TrajectoryPlanning setup. Returns None
        (rather than regenerating a missing file) if it isn't already on
        disk -- this is a read-only reference view, not a data pipeline."""
        if not individual_id:
            return None
        folder = os.path.dirname(os.path.abspath(pdf_path))
        matches = find_ind_data(individual_id, folder)
        if len(matches) != 1:
            return None
        raw_path = os.path.join(folder, matches[0])
        spacing_um = mri_spacing_mm[0] * 1000
        resampled_path = f"{raw_path[:-7]}_resampled{spacing_um:.10g}um.nii.gz"
        return resampled_path if os.path.exists(resampled_path) else None

    def render(self, mri_path, data, downsample=5):
        """data: the parsed plan JSON (FileOutput.compute()'s output,
        trajectory_planning/file_input_output.py). Renders the WHOLE scan
        as a real volumetric render (add_volume -- GPU/software ray
        casting, not a hollow outer-surface shell) so internal structure
        stays visible with depth, plus each shank's original mri_insert/
        mri_deep line segment (the exact voxel indices the saved plan
        already carries, so no atlas/registration lookup is needed).

        downsample=5: at full resampled-MRI resolution, the percentile/
        cell_data_to_point_data/threshold/add_volume steps below are slow
        enough (tens of seconds, not the "does this look right" reference
        this view is meant to be) to need downsampling at all -- same
        reasoning the docked pre-op 3D view's own background mesh
        (TrajectoryPlanning3DWindow._build_background_mesh, trajectory_
        planning_3d/window.py) uses for the same kind of data, just with a
        higher factor here since this view's data is denser and speed
        matters more than detail for a static reference."""
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
        spacing = orig_spacing * downsample
        arr_zyx = sitk.GetArrayFromImage(img).astype(np.float32)[::downsample, ::downsample, ::downsample]
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

        vol = pv.ImageData()
        vol.dimensions = np.array(arr_xyz.shape) + 1
        vol.spacing = spacing
        vol.origin = (0.0, 0.0, 0.0)
        vol.cell_data['MRI'] = arr_xyz.flatten(order='F')
        # add_volume ray-casts point data; cell data (what a plain
        # pv.ImageData carries here) renders blocky/voxelated instead of
        # a smooth volume.
        vol = vol.cell_data_to_point_data()

        nonzero = arr_xyz[arr_xyz > 0]
        clim = [float(p) for p in np.percentile(nonzero, [2, 98])] if nonzero.size else None

        # Remove real background/air cells (still ~zero after the outlier
        # fill above) from the geometry -- same threshold() pattern as
        # file_input_output.py's _get_mri_masked_volume and the docked
        # view's own background mesh -- rather than relying on opacity to
        # fade them out (a preset string opacity only ramps smoothly from
        # its low end, so background still clamps to a small nonzero
        # opacity there, and ray-casting accumulates that over the whole
        # background depth into a solid-looking box). A tiny epsilon, not
        # the clim midpoint -- this should only cut real background, not
        # dim real tissue.
        vol = vol.threshold(value=1e-6, scalars='MRI')
        self.plotter.add_volume(vol, scalars='MRI', cmap='gray', clim=clim,
                                 opacity='linear', shade=True, show_scalar_bar=False,
                                 name='surgery_mri_volume')

        shank_keys = sorted(data["shanks"], key=lambda k: int(k.split("_")[1]))
        for i, key in enumerate(shank_keys):
            raw = data["shanks"][key]["raw"]
            insert_mm = np.array(raw["mri_insert"], dtype=float) * orig_spacing
            deep_mm = np.array(raw["mri_deep"], dtype=float) * orig_spacing
            color = _SHANK_COLORS[i % len(_SHANK_COLORS)]
            self.plotter.add_mesh(pv.Line(deep_mm, insert_mm), color=color,
                                   line_width=4, name=f'surgery_shank_line_{i}')

        # Same red/green convention as everywhere else bregma/lambda are
        # drawn (CoordTransform.get_bregma/get_lambda, trajectory_planning/
        # coord_transform.py). bregma_mm/lambda_mm are already physical mm
        # (FileOutput.compute()'s raw block), same space as insert_mm/
        # deep_mm above -- no further spacing multiply needed.
        bregma_mm = np.array(data["raw"]["bregma_mm"], dtype=float)
        lambda_mm = np.array(data["raw"]["lambda_mm"], dtype=float)
        self.plotter.add_mesh(pv.Sphere(radius=0.4, center=bregma_mm), color=(1, 0, 0),
                               pickable=False, name='surgery_bregma')
        self.plotter.add_mesh(pv.Sphere(radius=0.4, center=lambda_mm), color=(0, 1, 0),
                               pickable=False, name='surgery_lambda')

        # Reminder this is the static pre-op plan, not the intraoperative
        # correction (see this module's docstring) -- easy to forget once
        # it's sitting next to the "measured" bregma/lambda fields.
        self.plotter.add_text("Original Positions", position='upper_left',
                               font_size=10, color='white', name='surgery_original_positions_label')

        # Orientation widget, same call as the docked pre-op 3D view
        # (trajectory_planning_3d/window.py:147).
        self.plotter.add_axes()

        # Scale bar: a real 3D ruler over a fixed 5mm span, anchored to the
        # volume's own geometry -- unlike show_bounds (data-relative tick
        # labels that read badly once zoomed far in/out, since the box
        # itself is what's being labeled rather than a fixed reference),
        # a ruler is a real object in the scene whose on-screen size scales
        # naturally with zoom, the same as everything else here.
        x0, _x1, y0, _y1, z0, _z1 = vol.bounds
        self.plotter.add_ruler(
            (x0, y0, z0), (x0 + 5.0, y0, z0), title="5 mm",
            font_size_factor=0.5, label_size_factor=0.5)

        self.plotter.reset_camera()
        self.plotter.render()

    def clear(self):
        self.plotter.clear()
        self.plotter.render()
