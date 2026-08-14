# This Python file uses the following encoding: utf-8
import os
from segmentation.segmentation_utils import Segmentation, SegmentationInitialization
from segmentation.evolution import SegmentationEvolution
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QDockWidget, QMessageBox, QApplication
from utils.zoom import zoom_notifier
from core.image_layer import ImageLayer
from scipy import ndimage as ndi
import SimpleITK as sitk
import vtk
import numpy as np

class SegmentationGUI:
    """
    The SegmentationGUI class connects the segmentation workflow (thresholding, bubble initialization,
    and level-set evolution) to the application's Qt UI.

    The segmentation is not yet finished.

    Parameters
    ----------
    MW : object
        The main window instance containing the Qt UI and MRI data management (LoadMRI).
    """
    def __init__(self,MW,samri=False,mode=None,on_finish=None):
        """Initialize the segmentation GUI and connect UI elements to corresponding handlers.

        mode/on_finish let a caller other than SAMRI (e.g. the trajectory
        planning wizard's skull-segmentation step) reuse this same
        threshold/bubble/level-set workflow: mode picks the output mask's
        filename suffix (see mask_suffix below) so it doesn't collide with
        an existing SAMRI moving mask for the same image, and on_finish is
        invoked once segmentation is done instead of the SAMRI-specific
        finish behaviour.
        """
        self.LoadMRI = MW.LoadMRI
        self.MW = MW
        self.ui = MW.ui
        self.initialization_first_time = True
        self.ui.checkBox_threshold.stateChanged.connect(self.on_threshold_changed)

        self.ui.groupBox_skull_radius.setVisible(mode == "skull")
        if mode == "skull":
            # skull is thin and often the same dark intensity as interior
            # structures (ventricles, CSF) -- rather than seed bubbles + a
            # level-set evolution that can leak into those, the mask is
            # built directly as a thresholded shell around the existing
            # brain mask (see _compute_skull_th_vol) and previewed right on
            # the threshold page itself (red mask / purple excluded), live
            # as the upper-bound and radius controls move. There is no
            # bubble/evolution step at all for skull mode -- Next1 just
            # finishes, since the mask is already saved continuously.
            self.ui.pushButton_Next1.clicked.connect(self.seg_finish)
            self.ui.pushButton_Next1.setText("Finish \n Skull Segmentation")
            self.ui.doubleSpinBox_skull_radius.setValue(3.0)
            self.ui.ScrollBar_skull_radius.setValue(3000)
            self.ui.doubleSpinBox_skull_radius.valueChanged.connect(self.on_spin_changed_skull_radius)
            self.ui.ScrollBar_skull_radius.valueChanged.connect(self.on_scroll_changed_skull_radius)
            self.ui.toolButton_runEvo.setEnabled(False)
            self.ui.toolButton_forwardEvo.setEnabled(False)
            self.ui.toolButton_backwardEvo.setEnabled(False)
        else:
            self.ui.pushButton_Next1.clicked.connect(self.active_bubbles)
            self.ui.pushButton_Next1.setText("Next")
            self.ui.toolButton_runEvo.setEnabled(True)
            self.ui.toolButton_forwardEvo.setEnabled(True)
            self.ui.toolButton_backwardEvo.setEnabled(True)
        self.ui.pushButton_Back2.clicked.connect(self.threshold_seg)
        self.ui.pushButton_Next2.clicked.connect(self.evolution)
        self.ui.pushButton_Back3.clicked.connect(self.active_bubbles)
        self.ui.pushButton_Finish.clicked.connect(self.seg_finish)
        # skull segmentation is mandatory when this page is reached in
        # skull mode -- unlike other modes/SAMRI, there is no "leave
        # without a mask" path, so Back1 stays disabled there.
        if samri or (mode is not None and mode != "skull"):
            self.ui.pushButton_Back1.setEnabled(True)
        self.ui.pushButton_Back1.setText("Back")
        self.ui.pushButton_Back1.clicked.connect(self.seg_finish)
        self.samri = samri
        self.mode = mode
        self.on_finish = on_finish
        self.mask_suffix = "-skullmask.nii.gz" if mode == "skull" else "-mask.nii.gz"
        self.evolution_first_time = True
        self.ui.stackedWidget_segmentation.setCurrentIndex(0)


    def on_threshold_changed(self, checked:bool):
        """
            Toggle thresholding on/off and update UI and data accordingly.
            When enabled, threshold segmentation is initialized and its parameters (upper/lower bounds)
            are linked to spinboxes and scrollbars in the UI.
        """
        #Segmentation
        if not hasattr(self.LoadMRI, 'Segmentation'):
            self.LoadMRI.Segmentation = Segmentation(self.LoadMRI)
            if self.mode == "skull":
                # the skull shows up as a thin bright shell -- upper-bounded
                # thresholding with a low default cutoff isolates it far
                # better than the generic bounded 10-50 default.
                self.LoadMRI.Segmentation.threshold_mode = 'upper'
                self.LoadMRI.Segmentation.upper = 15
                self.ui.radioButton_upper.setChecked(True)
            #threshold limits
            self.ui.doubleSpinBox_lower.setValue(self.LoadMRI.Segmentation.lower)
            self.ui.ScrollBar_lower.setValue(self.LoadMRI.Segmentation.lower)
            self.ui.doubleSpinBox_upper.setValue(self.LoadMRI.Segmentation.upper)
            self.ui.ScrollBar_upper.setValue(self.LoadMRI.Segmentation.upper)
            self.ui.doubleSpinBox_lower.setRange(0,int(self.LoadMRI.volumes[0].slices[0].max())+1)
            self.ui.ScrollBar_lower.setRange(0,int(self.LoadMRI.volumes[0].slices[0].max())+1)
            self.ui.doubleSpinBox_upper.setRange(0,int(self.LoadMRI.volumes[0].slices[0].max())+1)
            self.ui.ScrollBar_upper.setRange(0,int(self.LoadMRI.volumes[0].slices[0].max())+1)
            self.ui.doubleSpinBox_lower.editingFinished.connect(self.on_spin_changed_lower)
            self.ui.ScrollBar_lower.valueChanged.connect(self.on_scroll_changed_lower)
            self.ui.doubleSpinBox_upper.editingFinished.connect(self.on_spin_changed_upper)
            self.ui.ScrollBar_upper.valueChanged.connect(self.on_scroll_changed_upper)

            #threshold buttons
            self.ui.radioButton_bounded.toggled.connect(
                lambda checked: (setattr(self.LoadMRI.Segmentation, 'threshold_mode', 'bounded'), self.update_threshold_display()) if checked else None
            )
            self.ui.radioButton_lower.toggled.connect(
                lambda checked: (setattr(self.LoadMRI.Segmentation, 'threshold_mode', 'lower'), self.update_threshold_display()) if checked else None
            )
            self.ui.radioButton_upper.toggled.connect(
                lambda checked: (setattr(self.LoadMRI.Segmentation, 'threshold_mode', 'upper'), self.update_threshold_display()) if checked else None
            )
            self.update_threshold_display()
        if checked:  # If true, original images not needed
            self.LoadMRI.threshold_on = True
            self.ui.checkBox_threshold.setText("Threshold ON")
        else:  # If false, original images needed and loaded incase indexes have changed
            self.LoadMRI.threshold_on = False
            self.ui.checkBox_threshold.setText("Threshold OFF")
        # in skull mode the very first update_threshold_display() above can
        # bail out (and never create the layer) if the required brain mask
        # is missing -- shouldn't happen given segment_skull()'s precondition,
        # but don't crash the checkbox toggle over it.
        if hasattr(self, 'layer_index'):
            layer = self.LoadMRI.MW.Layers[0][self.layer_index]
            layer.toggle_visibility(checked,None)


    def threshold_seg(self):
        """Display the threshold adjustment page."""
        self.ui.stackedWidget_segmentation.setCurrentIndex(0)
        self.update_threshold_display()


    def update_threshold_display(self):
        """Refresh the thresholded image display according to current mode and bounds."""
        if self.mode == "skull":
            # brain mask red / skull mask transparent (so the raw MRI
            # shows through) / everything else purple -- see
            # _compute_skull_th_vol. Recomputed (and re-saved) on every
            # call, so the upper-bound controls AND the radius control
            # (which also calls this) both drive the live preview from
            # right here on the threshold page.
            th_vol = self._compute_skull_th_vol()
            self.ui.ScrollBar_lower.setEnabled(False)
            self.ui.doubleSpinBox_lower.setEnabled(False)
            self.ui.ScrollBar_upper.setEnabled(True)
            self.ui.doubleSpinBox_upper.setEnabled(True)
            if th_vol is None:
                return
        elif self.LoadMRI.Segmentation.threshold_mode == 'bounded':
            th_vol = self.LoadMRI.Segmentation.smooth_binary_threshold(self.LoadMRI.volumes[0].slices[0], lower=self.LoadMRI.Segmentation.lower, upper=self.LoadMRI.Segmentation.upper)
            self.ui.ScrollBar_lower.setEnabled(True)
            self.ui.doubleSpinBox_lower.setEnabled(True)
            self.ui.ScrollBar_upper.setEnabled(True)
            self.ui.doubleSpinBox_upper.setEnabled(True)
        elif self.LoadMRI.Segmentation.threshold_mode == 'lower':
            th_vol = self.LoadMRI.Segmentation.smooth_binary_threshold(self.LoadMRI.volumes[0].slices[0], lower=self.LoadMRI.Segmentation.lower, upper=None)
            self.ui.ScrollBar_lower.setEnabled(True)
            self.ui.doubleSpinBox_lower.setEnabled(True)
            self.ui.ScrollBar_upper.setEnabled(False)
            self.ui.doubleSpinBox_upper.setEnabled(False)
        elif self.LoadMRI.Segmentation.threshold_mode == 'upper':
            th_vol = self.LoadMRI.Segmentation.smooth_binary_threshold(self.LoadMRI.volumes[0].slices[0], lower=None, upper=self.LoadMRI.Segmentation.upper)
            self.ui.ScrollBar_lower.setEnabled(False)
            self.ui.doubleSpinBox_lower.setEnabled(False)
            self.ui.ScrollBar_upper.setEnabled(True)
            self.ui.doubleSpinBox_upper.setEnabled(True)

        idx = 0
        if not hasattr(self,'layer_index'):
            layer_index = len(self.LoadMRI.MW.Layers[idx])
            lut = self.setup_skull_lut() if self.mode == "skull" else self.setup_lut(th_vol)
            self.LoadMRI.MW.Layers[idx][layer_index] = ImageLayer(
                volume={0: th_vol},  # same array reference — mutations are picked up automatically
                spacing=self.LoadMRI.volumes[0].spacing,
                view_names=['axial', 'coronal', 'sagittal'],
                slice_indices=self.LoadMRI.slice_indices[0],
                is_4d=False,
                render_fct=self.LoadMRI.render,
                #vtk_dtype=vtk.VTK_UNSIGNED_CHAR,
                interpolation='nearest',
                opacity=1,
                lut = lut
            )
            self.layer_index = layer_index
            self.LoadMRI.setup_layer('coronal',idx,layer_index) ##data_view
        else:
            layer = self.LoadMRI.MW.Layers[idx][self.layer_index]
            layer.volume = {0: th_vol}
            layer.update_vtk(self.LoadMRI.slice_indices[0])
            # the LUT built at layer creation (above) isn't rebuilt here --
            # for skull mode that's fine since setup_skull_lut's range is
            # fixed regardless of th_vol; for the generic setup_lut it means
            # the grayscale/blue mapping stays pinned to the first call's
            # th_vol.min()/max() as the threshold sliders move afterward.
            # ImageLayer.update_vtk() alone never triggers a repaint (unlike
            # update_lut/toggle_visibility/set_opacity, which do it
            # themselves), so trigger it directly.
            self.LoadMRI.render()

        #create table entry or update with new volume
        indices = [i for i, val in enumerate(self.LoadMRI.intensity_table[0].file_name) if val == 'Threshold Image']
        if not indices:
            self.LoadMRI.intensity_table[0].update_table('Threshold Image',th_vol/ 32767.0, 0,layer_index,visibility_enabled=False)
        else:
            index = indices[0]
            self.LoadMRI.intensity_table[0].intensity_volumes[index] = th_vol/ 32767.0
            #update table
            self.LoadMRI.intensity_table[0].update_intensity_values(0)

    # --- Synchronize UI values for lower/upper threshold bounds ---
    def on_spin_changed_lower(self):
        val = self.ui.doubleSpinBox_lower.value()
        self.LoadMRI.Segmentation.lower = val
        self.ui.ScrollBar_lower.blockSignals(True)
        self.ui.ScrollBar_lower.setValue(self.LoadMRI.Segmentation.lower)
        self.ui.ScrollBar_lower.blockSignals(False)
        self.check_rangeLow()
        self.update_threshold_display()
        return

    def on_spin_changed_upper(self):
        val = self.ui.doubleSpinBox_upper.value()
        self.LoadMRI.Segmentation.upper = val
        self.ui.ScrollBar_upper.blockSignals(True)
        self.ui.ScrollBar_upper.setValue(self.LoadMRI.Segmentation.upper)
        self.ui.ScrollBar_upper.blockSignals(False)
        self.check_rangeUp()
        self.update_threshold_display()

    def on_scroll_changed_lower(self,val):
        self.LoadMRI.Segmentation.lower = val
        self.ui.doubleSpinBox_lower.blockSignals(True)
        self.ui.doubleSpinBox_lower.setValue(self.LoadMRI.Segmentation.lower)
        self.ui.doubleSpinBox_lower.blockSignals(False)
        self.check_rangeLow()
        self.update_threshold_display()

    def on_scroll_changed_upper(self,val):
        self.LoadMRI.Segmentation.upper = val
        self.ui.doubleSpinBox_upper.blockSignals(True)
        self.ui.doubleSpinBox_upper.setValue(self.LoadMRI.Segmentation.upper)
        self.ui.doubleSpinBox_upper.blockSignals(False)
        self.check_rangeUp()
        self.update_threshold_display()

    def check_rangeUp(self):
        """Ensure upper bound >= lower bound."""
        if self.LoadMRI.Segmentation.upper < self.LoadMRI.Segmentation.lower:
            self.LoadMRI.Segmentation.lower = self.LoadMRI.Segmentation.upper
            self.ui.doubleSpinBox_lower.blockSignals(True)
            self.ui.ScrollBar_lower.blockSignals(True)
            self.ui.doubleSpinBox_lower.setValue(self.LoadMRI.Segmentation.lower)
            self.ui.ScrollBar_lower.setValue(self.LoadMRI.Segmentation.lower)
            self.ui.doubleSpinBox_lower.blockSignals(False)
            self.ui.ScrollBar_lower.blockSignals(False)

    def check_rangeLow(self):
        """Ensure upper bound >= lower bound."""
        if self.LoadMRI.Segmentation.lower > self.LoadMRI.Segmentation.upper:
            self.LoadMRI.Segmentation.upper = self.LoadMRI.Segmentation.lower
            self.ui.doubleSpinBox_upper.blockSignals(True)
            self.ui.ScrollBar_upper.blockSignals(True)
            self.ui.doubleSpinBox_upper.setValue(self.LoadMRI.Segmentation.upper)
            self.ui.ScrollBar_upper.setValue(self.LoadMRI.Segmentation.upper)
            self.ui.doubleSpinBox_upper.blockSignals(False)
            self.ui.ScrollBar_upper.blockSignals(False)

    # --- Synchronize UI values for the skull-shell search radius (mm) ---
    # ScrollBar_skull_radius is an int slider scaled x1000 against the
    # 3-decimal doubleSpinBox_skull_radius (0-10mm), same scaling scheme
    # get_bubble_radius uses (x100) for the 2-decimal bubble radius.
    def on_spin_changed_skull_radius(self, val):
        self.ui.ScrollBar_skull_radius.blockSignals(True)
        self.ui.ScrollBar_skull_radius.setValue(int(round(val * 1000)))
        self.ui.ScrollBar_skull_radius.blockSignals(False)
        if hasattr(self.LoadMRI, 'Segmentation'):
            self.update_threshold_display()

    def on_scroll_changed_skull_radius(self, val):
        self.ui.doubleSpinBox_skull_radius.blockSignals(True)
        self.ui.doubleSpinBox_skull_radius.setValue(val / 1000)
        self.ui.doubleSpinBox_skull_radius.blockSignals(False)
        if hasattr(self.LoadMRI, 'Segmentation'):
            self.update_threshold_display()

    def _load_skull_inputs(self):
        """Load the original scan + existing brain mask the skull shell is
        computed against, once, and cache them on self -- so dragging the
        radius/upper-bound controls re-triggers only the (cheap) dilation
        + threshold below, not a disk read on every tick."""
        if getattr(self, '_skull_orig_img', None) is not None:
            return True
        # masks are named off, and computed against, the original
        # (pre-resample) file -- not the working "_resampledXXum" volume
        # actually loaded for planning -- so the mask and the intensity
        # data being thresholded are always on the same native grid,
        # with no resampling of the (binary) mask needed.
        brain_mask_path = self.MW.data_pre_resampled[:-7] + "-mask.nii.gz"
        if not os.path.exists(brain_mask_path):
            QMessageBox.warning(
                self.MW, "Brain Mask Required",
                "No brain mask found for this scan -- segment the brain first, then retry.")
            return False

        orig_img = sitk.ReadImage(self.MW.data_pre_resampled)
        mask_img = sitk.ReadImage(brain_mask_path)
        orig_intensity = sitk.GetArrayFromImage(orig_img)
        brain_mask = sitk.GetArrayFromImage(mask_img).astype(bool)

        if orig_intensity.shape != brain_mask.shape:
            QMessageBox.warning(
                self.MW, "Brain Mask Mismatch",
                "The existing brain mask doesn't match the original scan's "
                "dimensions -- resegment the brain, then retry.")
            return False

        self._skull_orig_img = orig_img
        self._skull_orig_intensity = orig_intensity
        self._skull_brain_mask = brain_mask
        return True

    def _compute_skull_th_vol(self):
        """Compute the skull mask for the current radius/upper-bound
        settings, save it to disk, and return a display volume encoding
        three categories the same way setup_lut's generic threshold
        volumes do (scaled to roughly +-32767, via setup_skull_lut), so it
        slots straight into the SAME ImageLayer/intensity-table pipeline
        the threshold page already uses for other modes:

        - the existing brain mask (+32767) -> red, just for orientation.
        - the computed skull mask (0) -> fully transparent, so the raw MRI
          underneath is visible and you can check it's actually bone.
        - everything else (-32767) -> purple: excluded either by the
          radius shell or by the intensity threshold.

        Called from update_threshold_display on every relevant change, so
        the saved mask file is never stale relative to what's on screen."""
        if not self._load_skull_inputs():
            return None

        orig_img = self._skull_orig_img
        orig_intensity = self._skull_orig_intensity
        brain_mask = self._skull_brain_mask

        radius_mm = self.ui.doubleSpinBox_skull_radius.value()
        mean_spacing = float(np.mean(orig_img.GetSpacing()))
        iterations = max(1, int(round(radius_mm / mean_spacing)))

        shell = ndi.binary_dilation(brain_mask, iterations=iterations) & ~brain_mask
        dark = orig_intensity < self.LoadMRI.Segmentation.upper
        skull_mask = shell & dark

        img = sitk.GetImageFromArray(skull_mask.astype(np.uint8))
        img.CopyInformation(orig_img)
        mask_path = self.MW.data_pre_resampled[:-7] + self.mask_suffix
        sitk.WriteImage(img, mask_path)

        # resample (nearest-neighbor, display only) onto the working
        # volume's grid so it lines up with the slice widgets reusing the
        # generic threshold ImageLayer.
        skull_mask_display = self._resample_bool_to_display(skull_mask, orig_img)
        brain_mask_display = self._resample_bool_to_display(brain_mask, orig_img)

        return np.where(
            brain_mask_display, 32767.0,
            np.where(skull_mask_display, 0.0, -32767.0)
        ).astype(np.float32)

    def _resample_bool_to_display(self, mask, mask_ref_img):
        """Nearest-neighbor resample a bool mask from the original scan
        grid onto the working (resampled) volume's grid -- display only,
        the file saved by _compute_skull_th_vol stays on the native grid."""
        img = sitk.GetImageFromArray(mask.astype(np.uint8))
        img.CopyInformation(mask_ref_img)
        img = sitk.Resample(
            img, self.LoadMRI.volumes[0].oriented_ref_image,
            sitk.Transform(), sitk.sitkNearestNeighbor, 0)
        return sitk.GetArrayFromImage(img).astype(bool)

    def active_bubbles(self):
        """
            Switch to the bubble initialization page.
            Creates a table for bubble management and connects UI elements
            for radius control and bubble addition/removal.
        """
        self.ui.stackedWidget_segmentation.setCurrentIndex(1)
        if self.initialization_first_time:
            #Get radius
            self.LoadMRI.SegInitialization = SegmentationInitialization(self.LoadMRI)
            table = self.ui.tableView_activeBub
            self.LoadMRI.SegInitialization.create_table(table)
            self.LoadMRI.SegInitialization.radius = 2
            self.ui.doubleSpinBox_Bubradius.setValue(self.LoadMRI.SegInitialization.radius)
            self.ui.horizontalSlider_Bubradius.setValue(self.LoadMRI.SegInitialization.radius*100)
            self.ui.doubleSpinBox_Bubradius.setRange(0.01,6)
            self.ui.horizontalSlider_Bubradius.setRange(1,6*100)
            self.ui.doubleSpinBox_Bubradius.valueChanged.connect(lambda val: self.get_bubble_radius('SpinBox',val=val))
            self.ui.horizontalSlider_Bubradius.valueChanged.connect(lambda val: self.get_bubble_radius('Slider',val=val))
            self.ui.pushButton_addBubbles.clicked.connect(lambda val: self.LoadMRI.SegInitialization.draw_bubble(self.ui.pushButton_Next2))
            #info if row in table is selected
            self.ui.tableView_activeBub.selectionModel().selectionChanged.connect(self.row_selected)
            #delete bubble
            self.ui.pushButton_delete.clicked.connect(self.delete_bubble)

            self.initialization_first_time = False
        else:
            self.ui.stackedWidget_3d.setVisible(False)
            box = self.ui.page_3D
            layout = box.layout()
            layout.setColumnStretch(0, 1)
            layout.setColumnStretch(1, 1)
            layout.setColumnStretch(2, 1)
            layout.setColumnStretch(3, 0)
            if getattr(self.LoadMRI, "SegEvolution", None) is not None:
                self.LoadMRI.SegEvolution.reset()

            self.LoadMRI.SegInitialization.table.show()

    def delete_bubble(self):
        """
            Delete the currently selected bubble from the visualization and table.
            Ensures both the actor and data model are updated consistently.
        """
        for i,[view_name,actor,_,_,_,_] in enumerate(self.LoadMRI.SegInitialization.actor_bubble):
            #remove from renderer
            if int(i/3) == self.LoadMRI.SegInitialization.row_index:
                renderer = self.LoadMRI.renderers[0][view_name]
                renderer.RemoveActor(actor)

                actor_entry = self.LoadMRI.SegInitialization.actor_selected[i]
                renderer.RemoveActor(actor_entry[2])

        #remove from list (3 enteries)
        self.LoadMRI.SegInitialization.actor_bubble.pop(self.LoadMRI.SegInitialization.row_index*3+2)
        self.LoadMRI.SegInitialization.actor_bubble.pop(self.LoadMRI.SegInitialization.row_index*3+1)
        self.LoadMRI.SegInitialization.actor_bubble.pop(self.LoadMRI.SegInitialization.row_index*3)
        self.LoadMRI.SegInitialization.actor_selected.pop(self.LoadMRI.SegInitialization.row_index*3+2)
        self.LoadMRI.SegInitialization.actor_selected.pop(self.LoadMRI.SegInitialization.row_index*3+1)
        self.LoadMRI.SegInitialization.actor_selected.pop(self.LoadMRI.SegInitialization.row_index*3)
        self.LoadMRI.SegInitialization.index -= 1

        #remove from table
        self.ui.tableView_activeBub.selectionModel().selectionChanged.disconnect(self.row_selected)
        self.LoadMRI.SegInitialization.model.removeRow(self.LoadMRI.SegInitialization.row_index)
        self.ui.tableView_activeBub.selectionModel().selectionChanged.connect(self.row_selected)

        self.LoadMRI.SegInitialization.row_index = min(self.LoadMRI.SegInitialization.row_index, self.LoadMRI.SegInitialization.model.rowCount()-1)
        self.LoadMRI.SegInitialization.update_bubbles_visible()
        for view_name in 'axial','coronal','sagittal':
            self.LoadMRI.renderers[0][view_name].GetRenderWindow().Render()
        if self.LoadMRI.SegInitialization.model.rowCount() == 0:
            self.ui.pushButton_Next2.setEnabled(False)
        self.LoadMRI.render()

    def row_selected(self,selected,deselected):
        self.LoadMRI.SegInitialization.row_selected(selected,deselected)
        for ix in selected.indexes():
            row_index = ix.row()
            radius = self.LoadMRI.SegInitialization.actor_bubble[row_index * 3][3]
            self.ui.doubleSpinBox_Bubradius.blockSignals(True)
            self.ui.horizontalSlider_Bubradius.blockSignals(True)
            self.ui.doubleSpinBox_Bubradius.setValue(radius)
            self.ui.horizontalSlider_Bubradius.setValue(radius*100)
            self.ui.doubleSpinBox_Bubradius.blockSignals(False)
            self.ui.horizontalSlider_Bubradius.blockSignals(False)

    def get_bubble_radius(self,mode,val):
        """
            Sync bubble radius between spinbox and slider and update visual bubbles.
            Parameters
            ----------
            mode : str
                'SpinBox' or 'Slider'
            val : float
                The new radius value (in mm)
        """
        if mode == 'SpinBox':
            self.LoadMRI.SegInitialization.radius = val
            self.ui.horizontalSlider_Bubradius.setEnabled(False)
            self.ui.horizontalSlider_Bubradius.setValue(int(self.LoadMRI.SegInitialization.radius*100))
            self.ui.horizontalSlider_Bubradius.setEnabled(True)
        elif mode == 'Slider':
            self.LoadMRI.SegInitialization.radius = val /100
            self.ui.doubleSpinBox_Bubradius.setEnabled(False)
            self.ui.doubleSpinBox_Bubradius.setValue(self.LoadMRI.SegInitialization.radius)
            self.ui.doubleSpinBox_Bubradius.setEnabled(True)

        if self.LoadMRI.SegInitialization.selected:
            for i in 0,1,2:
                self.LoadMRI.SegInitialization.actor_bubble[self.LoadMRI.SegInitialization.row_index*3+i][3] = self.LoadMRI.SegInitialization.radius
            self.LoadMRI.SegInitialization.update_bubbles_visible()
            self.LoadMRI.SegInitialization.model.setItem(self.LoadMRI.SegInitialization.row_index,3, QStandardItem(str(self.LoadMRI.SegInitialization.radius)))

        self.LoadMRI.render()

    def evolution(self):
        """
            Switch to the segmentation evolution page and initialize the
            level-set (or bubble evolution) process.
        """
        self.ui.stackedWidget_segmentation.setCurrentIndex(2)

        if self.evolution_first_time:
            spin_iterations = self.ui.doubleSpinBox_Segiter
            btn_resetCamera = self.ui.pushButton_seg3D
            self.LoadMRI.SegEvolution = SegmentationEvolution(self.LoadMRI,self.LoadMRI.SegInitialization,self.LoadMRI.Segmentation,self.ui.toolButton_runEvo,spin_iterations,btn_resetCamera,mask_suffix=self.mask_suffix,status_lineedit=self.ui.lineEdit_evolution_status)

            self.ui.toolButton_runEvo.clicked.connect(self.LoadMRI.SegEvolution.on_play_pause)
            self.ui.doubleSpinBox_SegStep.setValue(self.LoadMRI.SegEvolution.CHUNK)
            self.ui.doubleSpinBox_SegStep.valueChanged.connect(lambda v: setattr(self.LoadMRI.SegEvolution, "CHUNK", int(v)))
            self.evolution_first_time = False
            self.ui.toolButton_forwardEvo.clicked.connect(lambda: self.LoadMRI.SegEvolution.play_oneStep())
            self.ui.toolButton_backwardEvo.clicked.connect(lambda: self.LoadMRI.SegEvolution.reset())

        self.LoadMRI.SegEvolution.vtkwidget_3d = self.ui.vtkWidget_data_seg3D
        self.ui.lineEdit_vis3D.setVisible(True)
        self.ui.frame_vis3D.setVisible(True)
        self.ui.stackedWidget_3d.setVisible(True)
        self.ui.stackedWidget_3d.setCurrentIndex(1)
        box = self.ui.page_3D
        layout = box.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        # the widget only gets its final on-screen size once Qt has processed
        # the visibility/layout changes above -- rendering right away (before
        # that) renders at a stale/undersized geometry, showing pixelated
        # until the next resize/render forces a redraw at the right size.
        QApplication.processEvents()
        self.ui.vtkWidget_data_seg3D.GetRenderWindow().Render()


    def seg_finish(self):
        dock = self.MW.findChild(QDockWidget, "dock_segmentation")
        dock.close()

        if self.samri:
            self.ui.textEdit_SAMRI_reg.setVisible(False)
            self.ui.textEdit_SAMRI_reg.setVisible(False)
            self.ui.tabWidget.setCurrentIndex(5)
            self.MW.Samri_input.update_mov_mask_path()
            #to be able to create another mask
            # Disconnect scroll signals
            self.LoadMRI.cursor_ui["scroll_0"].valueChanged.disconnect()
            self.LoadMRI.cursor_ui["scroll_1"].valueChanged.disconnect()
            self.LoadMRI.cursor_ui["scroll_2"].valueChanged.disconnect()

            if hasattr(self.MW.LoadMRI, "minimap"):
                zoom_notifier.factorChanged.disconnect(self.LoadMRI.minimap.create_small_rectangle)
            ##del self.MW.LoadMRI # = None
        elif self.on_finish is not None:
            self.on_finish()

        return


    def setup_skull_lut(self):
        """Fixed three-color LUT for the skull preview (see
        _compute_skull_th_vol): +32767 (the existing brain mask) red, just
        for orientation; 0 (the computed skull mask) fully transparent, so
        the raw MRI shows through and you can check it's actually bone;
        -32767 (everything else -- excluded by the radius shell or the
        intensity threshold) purple. Unlike setup_lut this table's range
        never needs rescaling, since the encoding is always fixed."""
        lut = vtk.vtkLookupTable()
        lut.SetTableRange(-32767.0, 32767.0)
        lut.SetNumberOfTableValues(256)
        lut.Build()
        for i in range(256):
            val = -32767.0 + 2 * 32767.0 * i / 255.0
            if val > 16383.0:
                lut.SetTableValue(i, 1.0, 0.0, 0.0, 200/255)  # red: brain mask
            elif val < -16383.0:
                lut.SetTableValue(i, 0.5, 0.0, 0.5, 140/255)  # purple: excluded
            else:
                lut.SetTableValue(i, 0.0, 0.0, 0.0, 0.0)      # transparent: skull mask
        return lut

    def setup_lut(self,th_vol):
        #set to blue if outside threshold bounds
        th_vol_float = th_vol.astype(np.float32)
        lut = vtk.vtkLookupTable()
        lut.SetTableRange(th_vol_float.min(), th_vol_float.max())
        lut.SetNumberOfTableValues(256)
        lut.Build()
        for i in range(256):
            val = th_vol_float.min() + (th_vol_float.max() - th_vol_float.min()) * i / 255.0
            if val < 0:
                blue_intensity = -val / abs(th_vol_float.min())  # scale 0 -> min_val to 0->1
                lut.SetTableValue(i, blue_intensity/2, 0, blue_intensity, 1)  # blue
            elif val == 0:
                    lut.SetTableValue(i, 0, 0, 0, 0)
            else:
                gray = val / th_vol_float.max()
                lut.SetTableValue(i, gray, gray, gray, 1)  # grayscal

        return lut