# This Python file uses the following encoding: utf-8
import os
import re
import sys
import json as _json
import numpy as np
import SimpleITK as sitk
import ants
import nibabel as nib
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDockWidget, QDialog, QAbstractSpinBox, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QTimer, Qt
from gui_utils.busy_overlay import BusyOverlay
from trajectory_planning.visualisation3D import Visualisation3D
from trajectory_planning.shank_setup_dialog import ShankSetupDialog
from core.registration import Registration

_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)

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
        n_shanks, mode = dlg.get_values()
        self.shank_geometry_mode = mode
        # stackedWidget_geometry: page_25 (index 0) holds the user-defined /
        # "Shank Geometry" entry point, page_26 (index 1) the pre-defined
        # equal-spacing channel/separation inputs.
        self.ui.stackedWidget_geometry.setCurrentIndex(0 if mode == "custom" else 1)
        while self.ui.comboBox_Shanks.count() < n_shanks:
            self.add_shank()
        self.ui.comboBox_Shanks.setCurrentIndex(0)
        self.select_shank(0)  # setCurrentIndex above is a no-op (no signal fires) when it's already 0

        def proceed():
            if self.skull_mask_native_path is not None:
                # optional overlay -- a failure here (e.g. a warping bug)
                # must not take the whole next step down with it: without
                # this guard, an exception here means do_get_shank_line()
                # below (spinbox ranging, atlas load, everything else)
                # never runs at all, which looks like unrelated features
                # silently breaking.
                try:
                    self.warp_skull_mask()
                except Exception:
                    import traceback
                    traceback.print_exc()
                    print("[skull_mask] warp_skull_mask failed -- "
                          "continuing without the skull overlay", flush=True)
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

        skull_mask_img = None
        if hasattr(self,'skull_mask_img'):
            skull_mask_img = self.skull_mask_img


        self.ui.stackedWidget_3d_tp.setCurrentIndex(1)
        self.ui.stackedWidget_3d.setCurrentIndex(0)
        #load atlas file for further trajectory planning
        path_main = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        self.MW.restart_gui(path_main, full_restart=False,label_file=True,data_view='coronal')

        self.LoadMRI = self.MW.LoadMRI
        self.LoadMRI.TrajPlanning = self
        self.LoadMRI.show_edge_mask = False
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
        self.ui.pushButton_edgemask.clicked.connect(self.show_edge_mask) #checkable
        self.ui.spinBox_tp_channels.valueChanged.connect(self.change_shank_parameters)
        self.ui.spinBox_tp_separation.valueChanged.connect(self.change_shank_parameters)
        self.show_label = True #is checked
        self.ui.checkBox_brain_region.toggled.connect(lambda checked: self.show_brainregion(checked))

        if region_to_avoid_img is not None:
            self.MW.FileLoader.layer_index += 1
            self.MW.FileLoader.initialize_file(region_to_avoid_img,self.MW.FileLoader.layer_index,'coronal',0)
            self.region_to_avoid = sitk.GetArrayFromImage(region_to_avoid_img)

        if skull_mask_img is not None:
            self.MW.FileLoader.layer_index += 1
            # dark grey, deliberately distinct from the forbidden-region
            # overlay's grey/red and not tied to whether one happens to be
            # loaded too -- initialize_file's default red/grey heuristic
            # picks color based on that unrelated coincidence. Also give it
            # its own label/visibility toggle -- without layer_label it's a
            # sitk.Image just like the forbidden-region overlay, so it would
            # otherwise be mislabeled "Forbidden Regions" in the layer table
            # (and have its own visibility toggle disabled) by that same
            # isinstance-based heuristic.
            self.MW.FileLoader.initialize_file(
                skull_mask_img,self.MW.FileLoader.layer_index,'coronal',0,
                binary_color=(0.3,0.3,0.3),layer_label="Skull Mask",visibility_enabled=True)

        # load atlas for 3d visualisation
        self.Vis3D = Visualisation3D(self.MW)
        # load dwi atlas
        if not hasattr(self,'dwi'):
            dwi_path=os.path.join(_paths['atlas_folder'], _paths['atlas_dwi'])
            nii_dwi=nib.load(dwi_path)
            dwi=np.asanyarray(nii_dwi.dataobj)
            self.dwi=dwi[:,:,:,0]

        self.init_page30_mirror()

    def init_page30_mirror(self):
        """page_30 (stackedWidget_3d_tp index 1) has its own copies of the
        Cursor Position / Intensity under cursor widgets (spinBox_*_data3d_2,
        tableintensity_data3d_2) so that info stays visible during the
        insertion/deepest-point step -- but they aren't wired into the
        shared Cursor/IntensityTable machinery (that only drives the
        original *_data3d widgets), so they were always stuck showing
        nothing. Mirror the real widgets into them here instead of touching
        that shared, app-wide machinery.
        """
        for sb in (self.ui.spinBox_x_data3d_2, self.ui.spinBox_y_data3d_2, self.ui.spinBox_z_data3d_2):
            sb.setReadOnly(True)
            sb.setButtonSymbols(QAbstractSpinBox.NoButtons)

        table = self.ui.tableintensity_data3d_2
        table.setRowCount(1)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.sync_page30_display()

        if hasattr(self.MW, '_page30_mirror_timer') and self.MW._page30_mirror_timer is not None:
            self.MW._page30_mirror_timer.stop()
        timer = QTimer(self.MW)
        timer.timeout.connect(self.sync_page30_display)
        timer.start(200)
        self.MW._page30_mirror_timer = timer

    def sync_page30_display(self):
        for src_name, dst_name in (
            ('spinBox_x_data3d', 'spinBox_x_data3d_2'),
            ('spinBox_y_data3d', 'spinBox_y_data3d_2'),
            ('spinBox_z_data3d', 'spinBox_z_data3d_2'),
        ):
            src = getattr(self.ui, src_name)
            dst = getattr(self.ui, dst_name)
            if dst.value() != src.value():
                dst.setValue(src.value())

        src_table = self.ui.tableintensity_data3d
        dst_table = self.ui.tableintensity_data3d_2

        # mirror every layer row, not just row 0 -- previously any overlay
        # added after the base image (region-to-avoid, skull mask, ...)
        # never appeared here even though it was genuinely in the real
        # table, because this only ever synced row 0 and never grew the
        # mirror table's row count to match.
        if dst_table.rowCount() != src_table.rowCount():
            dst_table.setRowCount(src_table.rowCount())

        for row in range(src_table.rowCount()):
            # columns 1 (Layer) and 2 (Intensity) are plain QTableWidgetItems
            # on the real table -- mirror their text directly.
            for col in (1, 2):
                src_item = src_table.item(row, col)
                text = src_item.text() if src_item is not None else ""
                dst_item = dst_table.item(row, col)
                if dst_item is None:
                    dst_item = QTableWidgetItem()
                    dst_item.setFlags(dst_item.flags() & ~Qt.ItemIsEditable)
                    dst_table.setItem(row, col, dst_item)
                if dst_item.text() != text:
                    dst_item.setText(text)

            # columns 0 (visibility toggle) and 3 (opacity) are cell WIDGETS
            # on the real table (QToolButton / QDoubleSpinBox), not items --
            # there's nothing for item(row, col) to read there, which is why
            # they were missing entirely before. This panel is a passive
            # display, not another interactive control, so mirror both as
            # read-only.
            visible_widget = src_table.cellWidget(row, 0)
            icon_item = dst_table.item(row, 0)
            if icon_item is None:
                icon_item = QTableWidgetItem()
                icon_item.setFlags(icon_item.flags() & ~Qt.ItemIsEditable)
                icon_item.setTextAlignment(Qt.AlignCenter)
                dst_table.setItem(row, 0, icon_item)
            if visible_widget is not None:
                icon_item.setIcon(visible_widget.icon())

            opacity_widget = src_table.cellWidget(row, 3)
            opacity_item = dst_table.item(row, 3)
            if opacity_item is None:
                opacity_item = QTableWidgetItem()
                opacity_item.setFlags(opacity_item.flags() & ~Qt.ItemIsEditable)
                opacity_item.setTextAlignment(Qt.AlignCenter)
                dst_table.setItem(row, 3, opacity_item)
            if opacity_widget is not None:
                text = f"{opacity_widget.value():.1f} %"
                if opacity_item.text() != text:
                    opacity_item.setText(text)

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
            self.segment_skull(None)

    def segment_skull(self, transformPath):
        # segment_skull runs right after Step 1 (bregma/lambda picked on the
        # animal's own MRI), before the atlas is even loaded -- the Step 1
        # markers are still sitting on these same renderers and are just
        # clutter now that the user is focused on the skull, not bregma/lambda.
        self._set_bregma_lambda_visible(False)

        # done painting (or skipped it) -- close the paintbrush dock now,
        # right as we move on to skull segmentation, instead of leaving it
        # open underneath the skull-segmentation dock until warp_red_areas
        # closes it much later (only once the ENTIRE skull step is also
        # finished). A no-op if painting was skipped or already closed.
        paintbrush_dock = self.MW.findChild(QDockWidget, "dock_paintbrush")
        if paintbrush_dock is not None:
            paintbrush_dock.close()
        # closing the dock doesn't turn the brush itself off -- brush_on
        # stays True and the cursor/brush actors stay live on the render
        # views underneath. Un-checking the same checkbox the user would
        # normally uncheck triggers brush_3D(False) properly (clears
        # brush_on, removes the brush actors) instead of duplicating that
        # logic here.
        if hasattr(self.ui, 'checkBox_Brush') and self.ui.checkBox_Brush.isChecked():
            self.ui.checkBox_Brush.setChecked(False)

        # informational only (no Yes/No) -- skull segmentation is mandatory
        # once this step is reached, there is no skip path.
        msg_box = QMessageBox(self.MW)
        msg_box.setWindowTitle("Skull Segmentation")
        msg_box.setText("Continuing with skull segmentation.")
        msg_box.exec()

        self.ui.stackedWidget_3d.setVisible(False)
        layout = self.ui.page_3D.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)

        #make second image invisible and lock its toggle so the user can't
        #click it back on during skull segmentation (data_index=0, layer_index=1)
        if self.LoadMRI.TrajPlanning.second_file:
            layer = self.MW.Layers[0][1]
            layer.toggle_visibility(False, layer.visibility_btn)
            layer.visibility_btn.setEnabled(False)

        #same treatment for the painted forbidden-regions overlay, if the
        #user painted one -- its toggle is already created disabled (see
        #PaintbrushGUI.brush_3D), but nothing had ever actually hidden the
        #layer itself
        if hasattr(self.MW, 'Paintbrush') and 0 in self.MW.Paintbrush.layer_index:
            forbidden_layer = self.MW.Layers[0][self.MW.Paintbrush.layer_index[0]]
            forbidden_layer.toggle_visibility(False, forbidden_layer.visibility_btn)
            forbidden_layer.visibility_btn.setEnabled(False)

        # skull segmentation now derives its search region from the brain
        # mask (a dilated shell around it, see SegmentationGUI._compute_skull_th_vol)
        # -- without one there is nothing to build that shell from, so send
        # the user to segment the brain first and resume here once it's saved.
        # masks are named off the original (pre-resample) file, not the
        # working "_resampledXXum" volume actually loaded for planning.
        brain_mask_path = self.MW.data_pre_resampled[:-7] + "-mask.nii.gz"
        if not os.path.exists(brain_mask_path):
            msg_box = QMessageBox(self.MW)
            msg_box.setWindowTitle("Brain Mask Required")
            msg_box.setText(
                "Skull segmentation needs an existing brain mask to define "
                "its search region, and none was found for this scan.\n\n"
                "Segment the brain now -- skull segmentation will continue "
                "automatically once the brain mask is saved.")
            msg_box.exec()

            def _load_brain():
                self.MW.ButtonsGUI_3D.initialize_segmentation(
                    on_finish=lambda: self.segment_skull(transformPath))

            self.MW.overlay = BusyOverlay(self.MW, message="Loading brain segmentation, please wait…")
            self.MW.overlay.run(_load_brain)
            return

        def _load():
            # initialize_segmentation() builds a thresholded volume + a new
            # image layer for the full 3D image, which is heavy enough to
            # freeze the UI for a moment on a typical scan -- same overlay
            # pattern as get_shank_line's "please wait" while it loads.
            self.MW.ButtonsGUI_3D.initialize_segmentation(
                mode="skull",
                on_finish=lambda: self._skull_segmentation_finished(transformPath))
            # the instructions popup only makes sense once the segmentation
            # dock is actually up -- deferred a tick so it appears after the
            # busy overlay (which closes right as this function returns)
            # has cleared, not stacked underneath it.
            QTimer.singleShot(0, self._popup_segment_skull)

        self.MW.overlay = BusyOverlay(self.MW, message="Loading skull segmentation, please wait…")
        self.MW.overlay.run(_load)

    def _skull_segmentation_finished(self, transformPath):
        self.ui.stackedWidget_3d.setVisible(True)
        self._set_bregma_lambda_visible(True)
        skull_mask_path = self.MW.data_pre_resampled[:-7] + "-skullmask.nii.gz"
        if os.path.exists(skull_mask_path):
            self.skull_mask_native_path = skull_mask_path
        self.get_shank_line(transformPath)

    def warp_skull_mask(self):
        """Warp the manually segmented skull mask (native subject space)
        into atlas space, the same way warp_red_areas does for painted
        forbidden regions, so it can be shown as an overlay once
        trajectory planning switches into atlas space.

        Unlike the paintbrush label (already on the working volume's
        grid), the skull mask on disk was saved against the original
        (pre-resample) scan -- see SegmentationGUI._compute_skull_th_vol --
        a different, finer grid than raw_ref_image (the working volume's
        raw-oriented image). Resample onto raw_ref_image's grid first so
        the spacing/origin/direction pulled from it below actually
        describe the array being warped, instead of mislabeling a
        finer-grid array with the working grid's (coarser) geometry."""
        mask_img_rawOrientation = sitk.ReadImage(self.skull_mask_native_path)

        raw_ref = self.LoadMRI.volumes[0].raw_ref_image
        mask_img_rawOrientation = sitk.Resample(
            mask_img_rawOrientation, raw_ref,
            sitk.Transform(), sitk.sitkNearestNeighbor, 0)
        mask_raw_np = sitk.GetArrayFromImage(mask_img_rawOrientation)

        mask_ants = ants.from_numpy(
            mask_raw_np.T.astype(np.float32),
            origin=list(raw_ref.GetOrigin()),
            spacing=list(raw_ref.GetSpacing()),
            direction=np.array(raw_ref.GetDirection()).reshape(3, 3),
        )
        raw_fixed = ants.image_read(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        mask_aligned = ants.apply_transforms(
            fixed=raw_fixed,
            moving=mask_ants,
            transformlist=self.transform_path,
            interpolator="nearestNeighbor",
        )
        atlas_img = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        self.skull_mask_img = sitk.GetImageFromArray(mask_aligned.numpy().T)
        self.skull_mask_img.CopyInformation(atlas_img)

    def paint_red_areas(self):
        self._popup_red_areas()

        # Step 1's bregma/lambda markers are just clutter once the user is
        # focused on painting forbidden areas -- segment_skull already hides
        # them for the skull-segmentation step right after this one, but
        # painting itself left them on screen until now.
        self._set_bregma_lambda_visible(False)

        self.ui.stackedWidget_3d.setVisible(False)
        layout = self.ui.page_3D.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)

        if self.mask_idx is not None:
            layer = self.LoadMRI.MW.Layers[0][self.mask_idx]
            layer.toggle_visibility(False,self.LoadMRI.MW.Layers[0][self.mask_idx].visibility_btn)

        self.MW.ButtonsGUI_3D.initialize_paintbrush(red_only=True)
        #increase maximum due to resampling
        self.LoadMRI.brush['size'].setRange(1,30)
        self.LoadMRI.brush['size_slider'].setRange(1,30)

        self.ui.pushButton_paint_done.setVisible(True)


    def warp_red_areas(self, transform_path):
        label_vol = self.MW.Layers[0][self.MW.Paintbrush.layer_index[0]].volume[0]
        label_img = sitk.GetImageFromArray(label_vol)
        label_img.CopyInformation(self.LoadMRI.volumes[0].oriented_ref_image)
        label_img_rawOrientation = sitk.DICOMOrient(label_img, self.LoadMRI.volumes[0].raw_DICOMOrient)
        #resample to atlas
        label_img_raw_np = sitk.GetArrayFromImage(label_img_rawOrientation)

        raw_ref = self.LoadMRI.volumes[0].raw_ref_image
        label_ants = ants.from_numpy(
            label_img_raw_np.T.astype(np.float32),
            origin=list(raw_ref.GetOrigin()),
            spacing=list(raw_ref.GetSpacing()),
            direction=np.array(raw_ref.GetDirection()).reshape(3, 3),
        )
        #register to atlas
        raw_fixed = ants.image_read(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        label_aligned = ants.apply_transforms(
            fixed=raw_fixed,
            moving=label_ants,
            transformlist=transform_path,
            interpolator="nearestNeighbor",
        )

        atlas_img = sitk.ReadImage(os.path.join(_paths['atlas_folder'], _paths['atlas_volume']))
        self.region_to_avoid_img = sitk.GetImageFromArray(label_aligned.numpy().T)
        self.region_to_avoid_img.CopyInformation(atlas_img) #(self.LoadMRI.volumes[0].raw_ref_image)
        self.ui.stackedWidget_3d.setVisible(True)
        dock = self.MW.findChild(QDockWidget, "dock_paintbrush")
        dock.close()
        self.do_get_shank_line()
