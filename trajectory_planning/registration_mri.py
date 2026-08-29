# This Python file uses the following encoding: utf-8
"""MRI-space override of TpRegistration (trajectory_planning/registration.py)
-- keeps the subject's own MRI as the displayed/base volume for the whole
trajectory-planning workflow instead of swapping to the atlas volume, and
shows the atlas' region labels as a colored overlay warped onto the MRI's
own grid (see mri_label_overlay.py). Only the methods that actually depend
on which volume is displayed are overridden here; everything else
(register_to_main_img, get_shank_line, init_page30_mirror,
sync_page30_display, ask_paint_forbidden_areas, paint_red_areas) is
inherited unchanged from TpRegistration.

See /home/neurox/.claude/plans/wise-popping-nest.md for the full rationale.
"""

import os
import numpy as np
import SimpleITK as sitk
import vtk
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDockWidget
import nibabel as nib

from paths_config import _paths
from trajectory_planning.registration import TpRegistration
from trajectory_planning.visualisation3D_mri import VisualisationMri
from trajectory_planning.mri_label_overlay import (
    load_or_build_mri_grid_correspondence,
    scatter_atlas_labels_to_mri_grid,
    parse_itk_snap_label_file,
    build_discrete_label_lut,
)
from core.image_layer import ImageLayer


class TpRegistrationMri(TpRegistration):
    def build_mri_label_overlay(self):
        """Builds (first call) or refreshes (subsequent calls, e.g. an
        atlas switch via reload_atlas_view) the atlas-region-label overlay
        on the MRI's own grid: self.mri_label_vol (the raw zyx label array,
        used everywhere region-index lookups used to read self.atlas_vol)
        and self.tp_labels (the same {index: (r,g,b,a,name)} dict
        build_label_lut used to populate, read unmodified by
        core/interactor_style.py's hover lookup and shank.py's region-name
        display).

        Constructs the overlay directly as an ImageLayer (create_edge_mask's
        pattern), NOT through file_handling/loader.py's initialize_file
        "add another file" branch -- that path resamples with BSpline and
        builds a continuous grayscale LUT, both wrong for this categorical
        label data."""
        session_registration_dir = os.path.dirname(self.transform_path)
        if not hasattr(self, '_mri_grid_fixed_idx'):
            # samri_main.py's start_registration now builds moving_img_resampled25um-
            # indeces.npy against ResampleData.resampling25um's actual output
            # (<data_pre_resampled>_resampled.nii.gz), not self.movingImg's own
            # native/anisotropic grid -- read that same file here so
            # reconcile_raw_to_display_indices interprets the indices correctly.
            movingImg_25um_path = self.MW.data_pre_resampled[:-len('.nii.gz')] + '_resampled.nii.gz'
            # plain read, matching samri_main.py's own plain read of this file --
            # reconcile_raw_to_display_indices's physical-space math already
            # handles the orientation difference against self.movingImg_resampled
            # (which does stay "RAS", since that's what's actually displayed).
            movingImg_25um = sitk.ReadImage(movingImg_25um_path)
            self._mri_grid_fixed_idx, self._mri_grid_mri_idx = load_or_build_mri_grid_correspondence(
                session_registration_dir, movingImg_25um, self.movingImg_resampled)

        atlas_label_volume_path = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        mri_shape = self.LoadMRI.volumes[0].slices[0].shape  # zyx
        self.mri_label_vol = scatter_atlas_labels_to_mri_grid(
            atlas_label_volume_path, self._mri_grid_fixed_idx, self._mri_grid_mri_idx, mri_shape)

        label_file_path = os.path.join(_paths['atlas_folder'], _paths['atlas_labels'])
        self.tp_labels = parse_itk_snap_label_file(label_file_path)

        if not hasattr(self, '_mri_label_overlay_layer_index'):
            lut_vtk = build_discrete_label_lut(self.tp_labels)
            # Shared with every other "add an overlay layer" call site (e.g.
            # this same method's own region_to_avoid_img load below,
            # main_window.py's add_another_file) -- NOT len(Layers[0]),
            # which only reflects layers added via THAT counter and silently
            # collides with (overwrites) whichever Layers[0][layer_index]
            # slot this picks once anything else has used self.MW.
            # FileLoader.layer_index in the meantime. That collision is
            # exactly what left "Brain Regions"'/"Brain Edge"'s intensity-
            # table row toggling some other, unrelated layer instead.
            self.MW.FileLoader.layer_index += 1
            layer_index = self.MW.FileLoader.layer_index
            self._mri_label_overlay_layer_index = layer_index
            self._mri_label_overlay_lut = lut_vtk
            self.LoadMRI.MW.Layers[0][layer_index] = ImageLayer(
                volume={0: self.mri_label_vol},
                spacing=self.LoadMRI.volumes[0].spacing,
                view_names=['axial', 'coronal', 'sagittal'],
                slice_indices=self.LoadMRI.slice_indices[0],
                is_4d=False,
                render_fct=self.LoadMRI.render,
                vtk_dtype=vtk.VTK_UNSIGNED_SHORT,
                interpolation='nearest',
                opacity=0.6,
                lut=lut_vtk,
            )
            self.LoadMRI.setup_layer('coronal', 0, layer_index, visibility_at_start=True)
            self.LoadMRI.MW.Layers[0][layer_index].visibility_btn = self.LoadMRI.intensity_table[0].update_table(
                "Brain Regions", self.mri_label_vol, 0, layer_index, visibility_enabled=True)
        else:
            # Atlas switch: mutate the existing layer's array in place (same
            # "same array reference -- mutations are picked up
            # automatically" trick create_edge_mask's own comment
            # documents) and rebuild its LUT's table values in place, rather
            # than tearing down/recreating the layer -- that would also
            # need re-attaching a new vtkLookupTable to every already-built
            # VTK actor property.
            layer_index = self._mri_label_overlay_layer_index
            layer = self.LoadMRI.MW.Layers[0][layer_index]
            layer.volume[0][...] = self.mri_label_vol
            build_discrete_label_lut(self.tp_labels, lut=self._mri_label_overlay_lut)
            data_view = getattr(self.LoadMRI, 'data_view', 'coronal')
            self.LoadMRI.update_slices(0, data_view)

    def do_get_shank_line(self):
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(1)
        # The misalignment guide line (dial_missalignment) only belongs on
        # page_5 (bregma/lambda picking, index 0) -- otherwise it lingers
        # in the coronal view alongside update_atlas_plane_line's yellow
        # reference line (which only draws on index 1), showing two
        # overlapping/conflicting-looking lines with no way to tell they
        # serve different steps of the workflow.
        self.hide_misalignment_guide_line()

        # Custom (DXF) geometry needs each shank's geometry defined first --
        # that popup is deferred to add_dfx_shank() instead, once every
        # shank has geometry plotted.
        if self.shank_geometry_mode != "custom":
            self.show_insertion_step_popup()

        self.ui.stackedWidget_3d_tp.setCurrentIndex(1)
        self.ui.stackedWidget_3d.setCurrentIndex(0)
        self._ensure_atlas_selector_widget()

        # The registered second file (register_to_main_img) was only ever
        # needed for reference during bregma/lambda picking -- unlike the
        # base (non-Mri) workflow, restart_gui never runs here to clear it
        # out on its own, so it would otherwise sit in the table for the
        # rest of the session. Remove it outright (not just hide it, unlike
        # paint_red_areas' treatment of it) now that shank placement has
        # started.
        if self.second_file_layer_index is not None:
            table = self.LoadMRI.intensity_table[0]
            row = table.opacity_index.index(self.second_file_layer_index)
            table.remove_layer(row, 0)
            self.second_file_layer_index = None

        # MRI stays the displayed/base volume for the whole workflow -- no
        # restart_gui, no atlas swap. Build the atlas-region-label overlay
        # on the MRI's own grid instead of loading the atlas itself as the
        # label_file=True base image.
        self.build_mri_label_overlay()
        self.update_voxel_spinbox_ranges()

        if not hasattr(self.LoadMRI, 'tg_edge_mask'):
            self.LoadMRI.tp_imgvtk = {}
            self.LoadMRI.tp_actor = {}
            self.LoadMRI.tp_renderer = {}
            self.create_edge_mask()

        self.draw_atlas_reference_points()

        # See TpRegistration.do_get_shank_line's own comment: VTK sometimes
        # doesn't paint a freshly (re)shown render window until something
        # forces a repaint after Qt finishes laying it out.
        QTimer.singleShot(0, self.render)

        self.ui.pushButton_tp_deep.clicked.connect(self.get_deepest_point)
        self.ui.pushButton_tp_insert.clicked.connect(self.get_insert_point)
        self.ui.spinBox_tp_channels.valueChanged.connect(self.change_shank_parameters)
        self.ui.spinBox_tp_separation.valueChanged.connect(self.change_shank_parameters)
        self.show_label = True  # is checked
        self.ui.checkBox_brain_region.toggled.connect(lambda checked: self.show_brainregion(checked))
        # checkBox_constraint_90deg/_coronal are wired in setup_misalignment_
        # controls (rendering_mri.py), called from TrajectoryPlanningMri.
        # __init__ -- NOT here, since this method (do_get_shank_line) only
        # runs after bregma/lambda + forbidden-area painting are done, but
        # those checkboxes live on page_5 alongside bregma/lambda and need
        # to work from the very start, not just once this later page is
        # reached. Wiring them here left them completely dead (no
        # connection at all, so clicking did nothing) for anyone who
        # toggled them before advancing past page_5.

        # region_to_avoid_img (if painted in the forbidden-areas step) is
        # already MRI-space now -- warp_red_areas below no longer warps it
        # into atlas space, so it just needs (re)loading as a display
        # overlay here, same as before. Unlike the base (non-Mri) workflow,
        # this method's table/layers never get torn down by a restart_gui
        # call, and get_shank_line can run this method more than once (e.g.
        # reopening the Shank Setup dialog) -- guard with
        # _forbidden_regions_loaded so it's only ever added once instead of
        # piling up a duplicate "Forbidden Regions" row on every re-entry.
        # visibility_enabled=True (initialize_file otherwise defaults
        # visibility off for any sitk.Image overlay) so it's actually shown
        # while placing the shank, not hidden.
        if getattr(self, 'region_to_avoid_img', None) is not None and not getattr(self, '_forbidden_regions_loaded', False):
            self.MW.FileLoader.layer_index += 1
            self.MW.FileLoader.initialize_file(
                self.region_to_avoid_img, self.MW.FileLoader.layer_index, 'coronal', 0,
                visibility_enabled=True)
            # Kept for _set_insertion_refinement_layers_visible
            # (electrode_mri.py) to hide this layer again once the user
            # reaches the final skull-point click, same as
            # _mri_label_overlay_layer_index above.
            self._region_to_avoid_layer_index = self.MW.FileLoader.layer_index
            self.region_to_avoid = sitk.GetArrayFromImage(self.region_to_avoid_img)
            self._forbidden_regions_loaded = True

        # load MRI-space 3d visualisation
        self.Vis3D = VisualisationMri(self.MW)
        # load dwi atlas -- not every atlas has one (see ATLASES[...]['has_dwi']).
        # Kept atlas-native (not scattered onto the MRI grid): only ever
        # sampled at a handful of channel points via the existing
        # mri_to_atlas_via_lookup approximation (see ElecGeometryMri.
        # check_CA1_or_2), not displayed as a full volume.
        if not hasattr(self, 'dwi') and _paths.get('atlas_dwi'):
            dwi_path = os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
            nii_dwi = nib.load(dwi_path)
            dwi = np.asanyarray(nii_dwi.dataobj)
            self.dwi = dwi[:, :, :, 0]

        self.init_page30_mirror()

    def warp_red_areas(self, transform_path):
        """The painted forbidden-region mask is already in MRI space (it
        was painted directly onto the displayed MRI, which never stops
        being MRI in this workflow) -- unlike TpRegistration's original
        (atlas-space) version, there is nothing left to warp; just wrap it
        as region_to_avoid_img on the MRI's own grid. transform_path is
        accepted (and ignored) only to keep the same call signature as the
        base class's version (get_shank_line's proceed() calls it
        positionally)."""
        label_vol = self.MW.Layers[0][self.MW.Paintbrush.layer_index[0]].volume[0]
        label_img = sitk.GetImageFromArray(label_vol)
        label_img.CopyInformation(self.LoadMRI.volumes[0].oriented_ref_image)
        self.region_to_avoid_img = label_img

        # The paintbrush's own live "Forbidden Regions" row/layer (red,
        # opacity 0.5) is superseded by the finalized grey "Forbidden
        # Regions" overlay do_get_shank_line loads below -- remove it
        # outright (same reasoning as do_get_shank_line's own removal of the
        # second_file layer once its job is done), rather than leaving two
        # same-named rows in the table with the old one stuck on its last
        # painted (red) state.
        #
        # NOT using intensity_table.remove_layer's own 'Label'/'Forbidden
        # Regions' branch here -- it iterates layer.actors.items() as if
        # the value were a single actor, but ImageLayer.actors is actually
        # {view_name: {image_index: actor}} (core/image_layer.py), so that
        # branch calls RemoveActor with a dict and raises. Removing the
        # actors and the table row directly instead.
        table = self.LoadMRI.intensity_table[0]
        paint_layer_index = self.MW.Paintbrush.layer_index[0]
        if paint_layer_index in table.opacity_index:
            row = table.opacity_index.index(paint_layer_index)
            paint_layer = self.MW.Layers[0][paint_layer_index]
            for vn, actors_by_index in paint_layer.actors.items():
                renderer = self.LoadMRI.renderers[0][vn]
                for actor in actors_by_index.values():
                    renderer.RemoveActor(actor)
            table.table_delete_row(row)
            self.render()

        self.ui.stackedWidget_3d.setVisible(True)
        dock = self.MW.findChild(QDockWidget, "dock_paintbrush")
        if dock is not None:
            dock.close()
        self.do_get_shank_line()
