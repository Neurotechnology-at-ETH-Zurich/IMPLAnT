# This Python file uses the following encoding: utf-8
"""MRI-space override of Visualisation3D (trajectory_planning/
visualisation3D.py) -- the embedded 3-pane clipped 3D view on page_30.

Only load_atlas needs overriding. Everything else in Visualisation3D
(pick_label, _bg_colors_for_shank, render_clipped, draw_electrode_lines,
_atlas_sagittal_plane_normal_and_point, _draw_atlas_reference_plane,
_draw_shank_angle_indicator, pick_shank, refresh_clipped_views, reset_*)
already works correctly once:
- self.spacing (set in __init__, inherited unchanged) is read from
  self.MW.LoadMRI.volumes[0].file_path, which is now the MRI itself (never
  swapped away) instead of the atlas, so it's already MRI spacing;
- tp.coords_deepest_point/coords_insert_point/channel_points/mri_deep/
  mri_insert are already MRI-voxel-native everywhere (see
  ElecGeometryMri's overrides in electrode_mri.py);
- tp.atlas_bregma_coords/atlas_lambda_coords already hold MRI-space values
  under the SAME attribute names (see RenderingMri.draw_atlas_reference_
  points in rendering_mri.py), which _atlas_sagittal_plane_normal_and_point
  (defined locally here) and tp._atlas_plane_normal_and_point() (resolved
  dynamically to RenderingMri's MRI-space, misalignment-frame-driven
  override) both already read directly.

The only thing that genuinely still needs a ready-made brain-outline shape
is the background/region SHAPE itself (real atlas region indices as its
'NIFTI' cell data, which render_clipped/pick_label/_bg_colors_for_shank all
key off unmodified) -- load_atlas below builds that shape directly from
tp.mri_label_vol (registration_mri.py's build_mri_label_overlay), which is
already the WHS atlas' region labels warped onto the MRI's own grid. This
used to instead re-read the atlas volume file from scratch and reproject
every vertex into MRI space via atlas_points_to_mri_indices, so that the
mesh could track whichever atlas was currently active independent of the
WHS-pinned overlay -- but that atlas-switch feature was removed (see
registration_mri.py's _WHS_ATLAS_FILES comment; atlas_points_to_mri_indices,
coord_transform.py, now has no other caller), so tp.mri_label_vol IS this
mesh's atlas now, already on the right grid, and no second disk read or
reprojection is needed.
"""

import os

import numpy as np
import pyvista as pv
from matplotlib.colors import ListedColormap

from paths_config import _paths
from mrid_utils import handlers
from trajectory_planning.visualisation3D import Visualisation3D
from gui_utils.busy_worker import run_off_thread


class VisualisationMri(Visualisation3D):
    def load_atlas(self):
        # The pure numpy/pyvista computation below (no Qt/VTK scene object
        # touched -- these meshes/colormaps aren't attached to
        # self.plotter_co/sa/ax yet) runs off the GUI thread via
        # run_off_thread instead; only the final add_axes() calls stay here.
        (self.atlaslabelsdf, self.background_small, self.brain_surface_small,
         self.background_full_zooms, self.rgba, self.cmap,
         self.cmap_background) = run_off_thread(self._load_atlas_compute)

        self.plotter_co.add_axes()
        self.plotter_sa.add_axes()
        self.plotter_ax.add_axes()

    def _load_atlas_compute(self):
        """Pure numpy/pyvista half of load_atlas -- no Qt/VTK scene object
        touched -- safe to run off the GUI thread (see run_off_thread in
        load_atlas above). Returns (atlaslabelsdf, background_small,
        brain_surface_small, background_full_zooms (actually MRI spacing,
        kept under this name since visualisation3D.py's render_clipped
        already reads it against MRI-space mesh points), rgba, cmap,
        cmap_background)."""
        tp = self.MW.LoadMRI.TrajPlanning
        mri_spacing = np.array(tp.movingImg_resampled.GetSpacing())

        def load_background_mesh(scale):
            # tp.mri_label_vol is zyx (numpy convention); pv.ImageData with
            # flatten(order='F') needs xyz-ordered array axes to match
            # mesh.dimensions/spacing below.
            data = np.transpose(tp.mri_label_vol, (2, 1, 0))[::scale, ::scale, ::scale].astype(int)
            mesh = pv.ImageData()
            mesh.dimensions = np.array(data.shape) + 1
            mesh.spacing = tuple(s * scale for s in mri_spacing)
            mesh.origin = tuple(-s for s in mri_spacing)
            mesh.cell_data['NIFTI'] = data.flatten(order='F')
            return mesh

        def load_labels():
            labels_path = os.path.join(_paths['atlas_folder'], _paths['atlas_labels'])
            return handlers.read_itk_snap_labels(labels_path)

        atlaslabelsdf = load_labels()
        background_small = load_background_mesh(3).threshold(value=0.5)
        brain_surface_small = background_small.extract_surface(algorithm='dataset_surface')
        brain_surface_small = brain_surface_small.smooth_taubin(n_iter=50, pass_band=0.1)

        max_idx = int(atlaslabelsdf['IDX'].max())
        rgba = np.zeros((max_idx + 1, 4))
        rgba_background = np.zeros((max_idx + 1, 4))

        for _, row in atlaslabelsdf.iterrows():
            r, g, b = row['R'] / 255, row['G'] / 255, row['B'] / 255
            rgba_background[int(row['IDX'])] = [r, g, b, 0.1]

        cmap = ListedColormap(rgba)
        cmap_background = ListedColormap(rgba_background)

        return (atlaslabelsdf, background_small, brain_surface_small,
                mri_spacing, rgba, cmap, cmap_background)
