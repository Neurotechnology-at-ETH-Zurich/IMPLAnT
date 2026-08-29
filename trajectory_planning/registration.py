# This Python file uses the following encoding: utf-8
import os
import re
import sys
import numpy as np
import SimpleITK as sitk
import ants
import nibabel as nib
from PySide6.QtWidgets import QDockWidget, QDialog, QMessageBox
from PySide6.QtCore import QTimer
from gui_utils.busy_overlay import BusyOverlay
from trajectory_planning.visualisation3D import Visualisation3D
from trajectory_planning.shank_setup_dialog import ShankSetupDialog
from core.registration import Registration
from paths_config import _paths

class TpRegistration:
    def register_to_main_img(self,filename):
        self.ui.comboBox_movingimg.addItem(os.path.basename(filename))
        self.LoadMRI.movingimg_filename.append(filename)
        self.LoadMRI.coarsest_index = 1 #comboBox_coarsest
        self.LoadMRI.finest_index = 0 #comboBox_finest

        m = re.search(r"ind_(\d+)", self.main_file)
        fixed_ind = int(m.group(1))
        moving_ind = int(filename.split("ind_")[1].split(".")[0])
        transform_filename = f"transformation-ind_{moving_ind}-to-ind_{fixed_ind}.txt"
        transform_file_path = os.path.join(self.LoadMRI.session_path, "anat", transform_filename)
        new_name = filename[:-7]+f"-aligned_to_ind_{fixed_ind}.nii.gz"

        # Registration() runs a real (slow) rigid registration and
        # apply_transforms/image_write re-warps the full volume -- both are
        # deterministic for a given fixed/moving pair, so skip whichever
        # part already has its output on disk from a previous run.
        if not os.path.exists(new_name):
            if not os.path.exists(transform_file_path):
                Registration(self.LoadMRI,self.MW.ButtonsGUI_3D,0)

            fixed = ants.image_read(self.main_file)
            moving = ants.image_read(filename)

            img_aligned = ants.apply_transforms(
                fixed=fixed,
                moving=moving,
                transformlist=transform_file_path,
                interpolator="lanczosWindowedSinc", #bSpline",
            )

            ants.image_write(img_aligned, new_name)

        # initialize_file's "add another file" branch (loader.py) actually
        # keys self.MW.Layers[0] by len(self.MW.Layers[0]) at call time, not
        # by the layer_index passed in below -- capture that same key here
        # so paint_red_areas can find this layer again afterwards.
        self.second_file_layer_index = len(self.MW.Layers[0])
        self.MW.FileLoader.layer_index += 1
        self.MW.FileLoader.initialize_file(new_name,self.MW.FileLoader.layer_index,'coronal',0)
        #add to registration combobox
        self.MW.ui.comboBox_movingimg.addItem(os.path.basename(new_name))
        self.LoadMRI.movingimg_filename.append(new_name)
        self.LoadMRI.combo_Regimgname = self.MW.ui.comboBox_movingimg

        #original_path = f"{'_'.join(self.LoadMRI.volumes[0].file_path.split('_')[:-1])}.nii.gz"
        #mask_path = original_path[:-7] + "-mask.nii.gz"
        #if os.path.exists(mask_path):
        #    self.MW.FileLoader.layer_index += 1
        #    self.MW.FileLoader.initialize_file(mask_path,self.MW.FileLoader.layer_index,'coronal',0)
        #    #add to registration combobox
        #    self.MW.ui.comboBox_movingimg.addItem(os.path.basename(mask_path))
        #    self.LoadMRI.movingimg_filename.append(mask_path)
        #    self.mask_idx = self.MW.FileLoader.layer_index

        return new_name


    def get_shank_line(self,transformPath=None):
        dlg = ShankSetupDialog(self.MW)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        n_shanks, mode, xml_path, xml_groups, xml_nchannels = dlg.get_values()
        self.shank_geometry_mode = mode
        # stackedWidget_geometry: page_25 (index 0) holds the user-defined /
        # "Shank Geometry" entry point, page_26 (index 1) the pre-defined
        # equal-spacing channel/separation inputs.
        self.ui.stackedWidget_geometry.setCurrentIndex(0 if mode == "custom" else 1)

        # Carry a Neuroscope XML loaded in the setup dialog straight into
        # the same state browse_dfx_xml (dfx_geometry.py) would have set,
        # so every shank's channel numbers are already there once its DXF
        # bending is run (see refresh_dfx_channel_display) -- no need to
        # load the same file a second time from inside the Shank Geometry
        # panel. init_dfx_geometry (TrajectoryPlanning.__init__) has always
        # already run by this point, so these attributes exist.
        if xml_path is not None:
            self.dfx_xml_file = xml_path
            self.dfx_xml_groups = xml_groups
            self.dfx_xml_nchannels = xml_nchannels
            self.ui.pushButton_xml.setText(os.path.basename(xml_path))
            self.ui.pushButton_xml.setToolTip(xml_path)
        while self.ui.comboBox_Shanks.count() < n_shanks:
            self.add_shank()
        self.ui.comboBox_Shanks.setCurrentIndex(0)
        self.select_shank(0)  # setCurrentIndex above is a no-op (no signal fires) when it's already 0

        def proceed():
            self.refresh_atlas_bregma_lambda_from_user_points()
            if transformPath is not None:
                self.warp_red_areas(transformPath)
            else:
                self.do_get_shank_line()
            if mode == "custom":
                # Same as clicking "Shank Geometry": drop the user straight
                # into the DXF bending panel for the first shank.
                self.show_dfx_panel()
                self.show_geometry_step_popup()
                self.ui.stackedWidget_3d.setVisible(False)
                # collapse its column so the remaining views re-flow to fill
                # the freed space (same pattern as paint_red_areas)
                layout = self.ui.page_3D.layout()
                layout.setColumnStretch(0, 1)
                layout.setColumnStretch(1, 1)
                layout.setColumnStretch(2, 1)
                layout.setColumnStretch(3, 0)

        self.MW.overlay = BusyOverlay(self.MW, message="Loading data for next step, please wait…")
        self.MW.overlay.run(proceed)

    def do_get_shank_line(self):
        self.ui.stackedWidget_trajectoryplanning.setCurrentIndex(1)

        # Custom (DXF) geometry needs each shank's geometry defined first --
        # that popup is deferred to add_dfx_shank() instead, once every
        # shank has geometry plotted.
        if self.shank_geometry_mode != "custom":
            self.show_insertion_step_popup()

        region_to_avoid_img = None
        if hasattr(self,'region_to_avoid_img'):
            region_to_avoid_img = self.region_to_avoid_img

        self.ui.stackedWidget_3d_tp.setCurrentIndex(1)
        self.ui.stackedWidget_3d.setCurrentIndex(0)
        self._ensure_atlas_selector_widget()
        #load atlas file for further trajectory planning
        path_main = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        self.MW.restart_gui(path_main, full_restart=False,label_file=True,data_view='coronal')

        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.TrajPlanning = self
        # tp_labels (the atlas region-label lookup, built by Contrast.
        # build_label_lut when label_file=True) lives on LoadMRI, which gets
        # replaced wholesale on every restart_gui call -- cache it here, on
        # self (which survives those swaps), since the insertion-refinement
        # page's own restart_gui round-trip (electrode.py) briefly displays
        # the subject's own MRI (no atlas labels at all) in between.
        self.tp_labels = self.LoadMRI.tp_labels
        # bregma/lambda/insert/deepest-point spinboxes were last ranged
        # against the subject's own MRI (see TrajectoryPlanning.__init__)
        # -- re-range them against the atlas now that it's the active
        # volume, or any atlas voxel coordinate beyond the MRI's shape
        # gets silently clamped.
        self.update_voxel_spinbox_ranges()

        if not hasattr(self.LoadMRI,'tg_edge_mask'):
            self.LoadMRI.tp_imgvtk = {}
            self.LoadMRI.tp_actor = {}
            self.LoadMRI.tp_renderer = {}
            self.create_edge_mask()

        self.draw_atlas_reference_points()

        # VTK sometimes doesn't actually paint a freshly (re)shown render
        # window until something forces a repaint after Qt has finished
        # laying it out -- symptom: the other two views stay black through
        # the very first interaction after switching into this step (e.g. a
        # right-drag zoom), then recover on any subsequent action. Force one
        # extra render once the event loop settles instead of waiting on that.
        QTimer.singleShot(0, self.render)

        self.ui.pushButton_tp_deep.clicked.connect(self.get_deepest_point)
        self.ui.pushButton_tp_insert.clicked.connect(self.get_insert_point)
        self.ui.spinBox_tp_channels.valueChanged.connect(self.change_shank_parameters)
        self.ui.spinBox_tp_separation.valueChanged.connect(self.change_shank_parameters)
        self.show_label = True #is checked
        self.ui.checkBox_brain_region.toggled.connect(lambda checked: self.show_brainregion(checked))

        if region_to_avoid_img is not None:
            self.MW.FileLoader.layer_index += 1
            self.MW.FileLoader.initialize_file(region_to_avoid_img,self.MW.FileLoader.layer_index,'coronal',0)
            self.region_to_avoid = sitk.GetArrayFromImage(region_to_avoid_img)

        # load atlas for 3d visualisation
        self.Vis3D = Visualisation3D(self.MW)
        # load dwi atlas -- not every atlas has one (see ATLASES[...]['has_dwi'])
        if not hasattr(self,'dwi') and _paths.get('atlas_dwi'):
            dwi_path=os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
            nii_dwi=nib.load(dwi_path)
            dwi=np.asanyarray(nii_dwi.dataobj)
            self.dwi=dwi[:,:,:,0]

        self.init_page30_mirror()

    def init_page30_mirror(self):
        """page_30 (stackedWidget_3d_tp index 1) used to have its own dead
        copies of the Cursor Position / Intensity under cursor widgets
        (spinBox_*_data3d_2, tableintensity_data3d_2), poll-synced from the
        real *_data3d widgets every 200ms -- but the copies were never
        actually interactive (a static icon item, a read-only text item),
        so the eye-icon toggle did nothing there and the opacity cell only
        looked editable.

        page_29 (which holds the real spinBox_*_data3d/tableintensity_data3d)
        and page_30 are two pages of the same stackedWidget_3d_tp, so they're
        never visible at the same time -- reparent the real, already fully
        wired widgets into page_30's layout instead of maintaining a second
        copy. Removing a widget that isn't currently in a given layout (or
        re-adding one that's already in it) is a harmless no-op, so this can
        run again later (e.g. after an insertion-refinement round trip)
        without needing to guard against repeats.
        """
        ui = self.ui

        for axis, dst_row, dst_col in (('x', 1, 1), ('y', 1, 2), ('z', 1, 3)):
            mirror = getattr(ui, f"spinBox_{axis}_data3d_2")
            ui.gridLayout_212.removeWidget(mirror)
            mirror.setParent(None)
            mirror.hide()

            real = getattr(ui, f"spinBox_{axis}_data3d")
            ui.gridLayout_157.removeWidget(real)
            ui.gridLayout_212.addWidget(real, dst_row, dst_col)

        mirror_table = ui.tableintensity_data3d_2
        ui.gridLayout_213.removeWidget(mirror_table)
        mirror_table.setParent(None)
        mirror_table.hide()

        table = ui.tableintensity_data3d
        ui.gridLayout_156.removeWidget(table)
        ui.gridLayout_213.addWidget(table, 1, 0)

    def ask_paint_forbidden_areas(self):
        """pushButton_tp_next0 ('Next'): ask whether to mark forbidden
        regions before moving on to shank geometry, replacing the separate
        'Paint Areas To Avoid' button with a Yes/No prompt."""
        msg_box = QMessageBox(self.MW)
        msg_box.setWindowTitle("Mark Forbidden Areas?")
        msg_box.setText("Do you want to paint any regions the shank(s) must "
                         "avoid before continuing to shank geometry?")
        btn_yes = msg_box.addButton("Yes, paint forbidden areas", QMessageBox.ActionRole)
        msg_box.addButton("No, continue", QMessageBox.ActionRole)
        msg_box.exec()
        if msg_box.clickedButton() == btn_yes:
            self.paint_red_areas()
        else:
            self.get_shank_line(None)


    def paint_red_areas(self):
        self._popup_red_areas()

        # Step 1's bregma/lambda markers are just clutter once the user is
        # focused on painting forbidden areas.
        self._set_bregma_lambda_visible(False)
        # Same for the misalignment guide line (RenderingMri-only -- see
        # hide_misalignment_guide_line) -- do_get_shank_line hides it too,
        # but that only runs once painting is DONE (warp_red_areas ->
        # do_get_shank_line); without this, it stayed visible for the
        # entire painting step itself.
        if hasattr(self, 'hide_misalignment_guide_line'):
            self.hide_misalignment_guide_line()

        self.ui.stackedWidget_3d.setVisible(False)
        layout = self.ui.page_3D.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)

        if self.mask_idx is not None:
            layer = self.LoadMRI.MW.Layers[0][self.mask_idx]
            layer.toggle_visibility(False,self.LoadMRI.MW.Layers[0][self.mask_idx].visibility_btn)

        if self.second_file and self.second_file_layer_index is not None:
            # Hidden, not disabled -- the eye toggle stays clickable so the
            # user can still bring the registered second file back while
            # painting, same as every other layer's toggle. toggle_visibility
            # only swaps the icon/actor visibility, not the button's own
            # checked state -- set that too, or the next real click (which
            # flips checked from its still-True state) would toggle it the
            # wrong way and it'd stay hidden.
            layer = self.LoadMRI.MW.Layers[0][self.second_file_layer_index]
            layer.visibility_btn.setChecked(False)
            layer.toggle_visibility(False, layer.visibility_btn)

        self.MW.ButtonsGUI_3D.initialize_paintbrush(red_only=True)
        #increase maximum due to resampling
        self.LoadMRI.brush['size'].setRange(1,30)
        self.LoadMRI.brush['size_slider'].setRange(1,30)

        self.ui.pushButton_paint_done.setVisible(True)


    # warp_red_areas removed -- dead code. Only TrajectoryPlanningMri is
    # ever instantiated (see main_window.py), and TpRegistrationMri.
    # warp_red_areas (registration_mri.py) is a complete standalone
    # replacement (including its own copy of the stackedWidget_3d/dock/
    # do_get_shank_line tail), never calling super().
