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

The only thing that genuinely still needs the atlas' OWN grid is the
background/region SHAPE itself (a reliable, ready-made brain outline with
real atlas region indices as its 'NIFTI' cell data, which render_clipped/
pick_label/_bg_colors_for_shank all key off unmodified) -- load_atlas below
builds that shape from the atlas volume exactly as before, then reprojects
every vertex into true MRI physical-mm space via atlas_points_to_mri_
indices (same technique trajectory_planning_3d/window.py's own
_build_background_mesh/_build_mask_mesh already use successfully),
leaving the NIFTI cell data itself untouched -- repositioning a mesh's
points does not change which cell each point belongs to.
"""

import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pyvista as pv
import nibabel as nib
from matplotlib.colors import ListedColormap

from paths_config import _paths
from mrid_utils import handlers
from trajectory_planning.visualisation3D import Visualisation3D


class VisualisationMri(Visualisation3D):
    def load_atlas(self):
        def load_background_mesh(scale):
            background_path = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
            img = nib.load(background_path)
            data = img.get_fdata().astype(int)[::scale, ::scale, ::scale]
            zooms = img.header.get_zooms()[:3]
            mesh = pv.ImageData()
            mesh.dimensions = np.array(data.shape) + 1
            mesh.spacing = tuple(s * scale for s in zooms)
            mesh.origin = tuple(-s for s in zooms)
            mesh.cell_data['NIFTI'] = data.flatten(order='F')
            return mesh

        def load_labels():
            labels_path = os.path.join(_paths['atlas_folder'], _paths['atlas_labels'])
            return handlers.read_itk_snap_labels(labels_path)

        def load_background_full_numpy():
            background_path = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
            img = nib.load(background_path)
            return np.array(img.header.get_zooms()[:3])

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_small = executor.submit(load_background_mesh, 3)
            future_full = executor.submit(load_background_full_numpy)
            future_labels = executor.submit(load_labels)

            self.atlaslabelsdf = future_labels.result()
            self.background_small = future_small.result().threshold(value=0.5)
            self.brain_surface_small = self.background_small.extract_surface(algorithm='dataset_surface')
            self.brain_surface_small = self.brain_surface_small.smooth_taubin(n_iter=50, pass_band=0.1)
            self.background_full_zooms = future_full.result()

        # Reproject vertex positions only -- NIFTI cell data (atlas region
        # indices) stays exactly as built, so render_clipped/pick_label/
        # _bg_colors_for_shank need no changes of their own.
        tp = self.MW.LoadMRI.TrajPlanning
        mri_spacing = np.array(tp.movingImg_resampled.GetSpacing())
        self.background_small.points = tp.atlas_points_to_mri_indices(self.background_small.points) * mri_spacing
        self.brain_surface_small.points = tp.atlas_points_to_mri_indices(self.brain_surface_small.points) * mri_spacing

        max_idx = int(self.atlaslabelsdf['IDX'].max())
        self.rgba = np.zeros((max_idx + 1, 4))
        rgba_background = np.zeros((max_idx + 1, 4))

        for _, row in self.atlaslabelsdf.iterrows():
            r, g, b = row['R'] / 255, row['G'] / 255, row['B'] / 255
            rgba_background[int(row['IDX'])] = [r, g, b, 0.1]

        self.cmap = ListedColormap(self.rgba)
        self.cmap_background = ListedColormap(rgba_background)

        self.plotter_co.add_axes()
        self.plotter_sa.add_axes()
        self.plotter_ax.add_axes()
