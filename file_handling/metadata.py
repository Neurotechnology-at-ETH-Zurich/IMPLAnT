# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QDialog, QVBoxLayout
import numpy as np
import SimpleITK as sitk
from file_handling.mri_volume import MRIVolume

class Metadata:
    def __init__(self,MW):
        self.MW = MW
        self.ui = MW.ui
        self.LoadMRI = MW.LoadMRI
        # a new Metadata is built every time a base layer (layer_index==0) is
        # loaded, but pushButton_metadata etc. are single shared widgets - without
        # disconnecting the previous instance's slot first, connections pile up
        # and one click fires show_metadata on every still-connected instance,
        # each stealing frame_metadata into its own popup (see show_metadata)
        self._reconnect(self.ui.pushButton_metadata.clicked, self.show_metadata)
        self._reconnect(self.ui.pushButton_changeSpacing.clicked, self.change_spacing)
        self._reconnect(self.ui.pushButton_SaveSpacing.clicked, self.save_new_spacing)
        self._reconnect(self.ui.pushButton_SaveMetadata.clicked, self.set_metadata)
        self._reconnect(self.ui.pushButton_reorient.clicked, self.reorient_volume)

        self._reconnect(self.ui.doubleSpinBox_spax.valueChanged, lambda val: self.changed_parameters_spacing(val,'x'))
        self._reconnect(self.ui.doubleSpinBox_spay.valueChanged, lambda val: self.changed_parameters_spacing(val,'y'))
        self._reconnect(self.ui.doubleSpinBox_spaz.valueChanged, lambda val: self.changed_parameters_spacing(val,'z'))
        self._reconnect(self.ui.doubleSpinBox_fovx.valueChanged, lambda val: self.changed_parameters_fov(val,'x'))
        self._reconnect(self.ui.doubleSpinBox_fovy.valueChanged, lambda val: self.changed_parameters_fov(val,'y'))
        self._reconnect(self.ui.doubleSpinBox_fovz.valueChanged, lambda val: self.changed_parameters_fov(val,'z'))

    @staticmethod
    def _orientation_axis_permutation(from_code, to_code):
        """
        perm such that [values_in_from_code[perm[i]] for i in range(3)] gives
        values in to_code's axis order -- i.e. axis i of to_code corresponds
        to axis perm[i] of from_code. Needed because DICOMOrient can permute
        axes, not just flip signs (e.g. a raw scan natively in "LSA" order
        has its Y/Z axes swapped relative to "RAS" -- confirmed empirically:
        raw spacing (0.102, 0.100, 0.450) becomes (0.102, 0.450, 0.100) once
        oriented to RAS). Spacing edited in the displayed orientation must be
        permuted back through this before being applied to the raw file.
        """
        pair = {'L': 'LR', 'R': 'LR', 'A': 'AP', 'P': 'AP', 'S': 'SI', 'I': 'SI'}
        from_pairs = [pair[c] for c in from_code]
        to_pairs = [pair[c] for c in to_code]
        return [from_pairs.index(p) for p in to_pairs]

    @staticmethod
    def _reconnect(signal,slot):
        signal.disconnect()
        signal.connect(slot)


    def show_metadata(self):
        if hasattr(self, "popup") and self.popup.isVisible():
            self.popup.raise_()
            self.popup.activateWindow()
            return
        self.popup = PopupDialog(parent=self.MW,ui_widget=self.ui.frame_metadata)
        self.popup.resize(300, 300)
        self.popup.show()
        self.ui.pushButton_cancel_metadata.clicked.connect(self.popup.close)
        self.fill_metadata()

    def change_spacing(self):
        if hasattr(self, "spacing_popup") and self.spacing_popup.isVisible():
            self.popup.raise_()
            self.popup.activateWindow()
            return
        self.spacing_popup = PopupDialog(parent=self.MW,ui_widget=self.ui.frame_spacing)
        self.spacing_popup.resize(300, 300)
        self.spacing_popup.show()
        self.ui.pushButton_cancel_spacing.clicked.connect(self.spacing_popup.close)
        self.fill_spacing_metadata()

    def fill_metadata(self):
        self.volume = self.LoadMRI.volumes[0]
        image = self.LoadMRI.volumes[0].oriented_ref_image
        #dimensions
        self.ui.spinBox_dimx.setValue(self.volume.slices[0].shape[2])
        self.ui.spinBox_dimy.setValue(self.volume.slices[0].shape[1])
        self.ui.spinBox_dimz.setValue(self.volume.slices[0].shape[0])
        #spacing
        self.ui.doubleSpinBox_spacingx.setValue(self.volume.spacing[2])
        self.ui.doubleSpinBox_spacingy.setValue(self.volume.spacing[1])
        self.ui.doubleSpinBox_spacingz.setValue(self.volume.spacing[0])
        #origin
        self.ui.doubleSpinBox_originx.setValue(image.GetOrigin()[2])
        self.ui.doubleSpinBox_originy.setValue(image.GetOrigin()[1])
        self.ui.doubleSpinBox_originz.setValue(image.GetOrigin()[0])
        #orientation
        orient_filter = sitk.DICOMOrientImageFilter()
        current_orient = orient_filter.GetOrientationFromDirectionCosines(image.GetDirection())
        self.ui.lineEdit_DicomOrient.setText(current_orient)

        #affine
        direction = image.GetDirection()
        self.ui.lineEdit_direction.setText(f"{direction}")

        #Intensity Range
        self.ui.doubleSpinBox_maxIntensity.setValue(self.volume.slices[0].max())
        self.ui.doubleSpinBox_minIntensity.setValue(self.volume.slices[0].min())

        self.ui.pushButton_SaveMetadata.setText("OK")



    def save_new_spacing(self):
        self.ui.doubleSpinBox_spacingx.setValue(self.ui.doubleSpinBox_spax.value())
        self.ui.doubleSpinBox_spacingy.setValue(self.ui.doubleSpinBox_spay.value())
        self.ui.doubleSpinBox_spacingz.setValue(self.ui.doubleSpinBox_spaz.value())

        current_spacing = [self.volume.spacing[2], self.volume.spacing[1], self.volume.spacing[0]]
        new_spacing = [self.ui.doubleSpinBox_spacingx.value(), self.ui.doubleSpinBox_spacingy.value(), self.ui.doubleSpinBox_spacingz.value()]
        if all(abs(a - b) < 1e-6 for a, b in zip(new_spacing, current_spacing)):
            self.ui.pushButton_SaveMetadata.setText("OK")
        else:
            self.ui.pushButton_SaveMetadata.setText("Save Metadata")

        self.spacing_popup.close()


    def fill_spacing_metadata(self):
        self.ui.doubleSpinBox_spax.blockSignals(True)
        self.ui.doubleSpinBox_spay.blockSignals(True)
        self.ui.doubleSpinBox_spaz.blockSignals(True)
        self.ui.doubleSpinBox_fovx.blockSignals(True)
        self.ui.doubleSpinBox_fovy.blockSignals(True)
        self.ui.doubleSpinBox_fovz.blockSignals(True)
        #dimensions
        self.ui.spinBox_dimex.setValue(self.volume.slices[0].shape[2])
        self.ui.spinBox_dimey.setValue(self.volume.slices[0].shape[1])
        self.ui.spinBox_dimez.setValue(self.volume.slices[0].shape[0])
        #spacing
        self.ui.doubleSpinBox_spax.setValue(self.volume.spacing[2])
        self.ui.doubleSpinBox_spay.setValue(self.volume.spacing[1])
        self.ui.doubleSpinBox_spaz.setValue(self.volume.spacing[0])
        #field of view
        fov_x = self.volume.slices[0].shape[2] * self.volume.spacing[2]
        fov_y = self.volume.slices[0].shape[1] * self.volume.spacing[1]
        fov_z = self.volume.slices[0].shape[0] * self.volume.spacing[0]
        self.ui.doubleSpinBox_fovx.setValue(fov_x)
        self.ui.doubleSpinBox_fovy.setValue(fov_y)
        self.ui.doubleSpinBox_fovz.setValue(fov_z)
        self.ui.doubleSpinBox_spax.blockSignals(False)
        self.ui.doubleSpinBox_spay.blockSignals(False)
        self.ui.doubleSpinBox_spaz.blockSignals(False)
        self.ui.doubleSpinBox_fovx.blockSignals(False)
        self.ui.doubleSpinBox_fovy.blockSignals(False)
        self.ui.doubleSpinBox_fovz.blockSignals(False)

    def changed_parameters_fov(self,val,axis):
        self.ui.doubleSpinBox_spax.blockSignals(True)
        self.ui.doubleSpinBox_spay.blockSignals(True)
        self.ui.doubleSpinBox_spaz.blockSignals(True)

        if axis=='x':
            spa_x = val / self.volume.slices[0].shape[2]
            self.ui.doubleSpinBox_spax.setValue(spa_x)
        elif axis=='y':
            spa_y = val / self.volume.slices[0].shape[1]
            self.ui.doubleSpinBox_spay.setValue(spa_y)
        elif axis=='z':
            spa_z = val / self.volume.slices[0].shape[0]
            self.ui.doubleSpinBox_spaz.setValue(spa_z)
        self.ui.doubleSpinBox_spax.blockSignals(False)
        self.ui.doubleSpinBox_spay.blockSignals(False)
        self.ui.doubleSpinBox_spaz.blockSignals(False)

    def changed_parameters_spacing(self,val,axis):
        self.ui.doubleSpinBox_fovx.blockSignals(True)
        self.ui.doubleSpinBox_fovy.blockSignals(True)
        self.ui.doubleSpinBox_fovz.blockSignals(True)
        if axis=='x':
            fov_x = val * self.volume.slices[0].shape[2]
            self.ui.doubleSpinBox_fovx.setValue(fov_x)
        elif axis=='y':
            fov_y = val * self.volume.slices[0].shape[1]
            self.ui.doubleSpinBox_fovy.setValue(fov_y)
        elif axis=='z':
            fov_z = val * self.volume.slices[0].shape[0]
            self.ui.doubleSpinBox_fovz.setValue(fov_z)

        self.ui.doubleSpinBox_fovx.blockSignals(False)
        self.ui.doubleSpinBox_fovy.blockSignals(False)
        self.ui.doubleSpinBox_fovz.blockSignals(False)

    def set_metadata(self):
        if self.ui.pushButton_SaveMetadata.text() == "OK":
            if hasattr(self, "popup"):
                self.popup.close()
            return

        displayed_spacing = [self.ui.doubleSpinBox_spacingx.value(),self.ui.doubleSpinBox_spacingy.value(),self.ui.doubleSpinBox_spacingz.value()]

        # displayed_spacing is in the CURRENTLY DISPLAYED orientation's axis
        # order (volumes[0].DICOMOrient, e.g. "RAS"), but img below is read
        # fresh from the raw file (its own native orientation, volumes[0].
        # raw_DICOMOrient) -- these can differ by an axis PERMUTATION, not
        # just sign flips, so displayed_spacing must be permuted back into
        # the raw file's own axis order before being applied to it.
        volume = self.LoadMRI.volumes[0]
        perm = self._orientation_axis_permutation(volume.DICOMOrient, volume.raw_DICOMOrient)
        new_spacing = [displayed_spacing[i] for i in perm]

        img = sitk.ReadImage(self.LoadMRI.volumes[0].file_path)
        img.SetSpacing(new_spacing)
        sitk.WriteImage(img, self.LoadMRI.volumes[0].file_path)

        if hasattr(self, "popup"):
            self.popup.close()
        self.MW.restart_gui(self.LoadMRI.volumes[0].file_path,True,False)


    def reorient_volume(self):
        data_index = 0
        if self.ui.pushButton_reorient.isChecked():
            DICOMOrient = 'LAS'
            file_name = self.LoadMRI.volumes[data_index].file_path
            self.LoadMRI.volumes[data_index] = MRIVolume.from_file(file_name,DICOMOrient)
            self.ui.pushButton_reorient.setText('Reorient to RAS')
        else:
            DICOMOrient = 'RAS'
            file_name = self.LoadMRI.volumes[data_index].file_path
            self.LoadMRI.volumes[data_index] = MRIVolume.from_file(file_name,DICOMOrient)
            self.ui.pushButton_reorient.setText('Reorient to LAS')

        # ImageLayer captures vol.slices/spacing by reference at construction
        # time (file_handling/loader.py:208-215) -- replacing volumes[data_index]
        # above leaves the already-built base layer pointing at the old, stale
        # array unless it's resynced here too.
        base_layer = self.MW.Layers[data_index][0]
        base_layer.volume = self.LoadMRI.volumes[data_index].slices
        base_layer.spacing = self.LoadMRI.volumes[data_index].spacing

        # same stale-reference issue for the intensity/cursor-value readout and
        # the contrast/windowing LUT, which are also built once at load time
        # instead of re-reading LoadMRI.volumes each use.
        self.LoadMRI.intensity_table[data_index].intensity_volumes[0] = self.LoadMRI.volumes[data_index].slices[0]
        self.LoadMRI.intensity_table[data_index].update_intensity_values(data_index)
        if data_index in self.LoadMRI.contrast:
            self.LoadMRI.contrast[data_index].recompute_luttable(0, data_index)

        # Overlay/label layers (segmentation masks, Forbidden Regions, paintbrush
        # strokes, ...) were built/resampled against the pre-reorient base grid
        # and are otherwise left unmirrored, so they'd show up spatially flipped
        # relative to the now-reoriented base image. Flip in place rather than
        # reassigning, since e.g. Paintbrush.label_volume shares the same array
        # object with its ImageLayer -- dedupe by identity in case a layer
        # aliases the same array under multiple keys (e.g. 4D paintbrush).
        slice_indices = self.LoadMRI.slice_indices[data_index]
        flipped_ids = set()
        for layer_index, layer in self.MW.Layers[data_index].items():
            if layer_index == 0:
                continue
            for arr in layer.volume.values():
                if id(arr) not in flipped_ids:
                    arr[:] = np.flip(arr, axis=2).copy()
                    flipped_ids.add(id(arr))
            layer.update_vtk(slice_indices)

        #orientation
        orient_filter = sitk.DICOMOrientImageFilter()
        current_orient = orient_filter.GetOrientationFromDirectionCosines(self.LoadMRI.volumes[data_index].oriented_ref_image.GetDirection())
        self.ui.lineEdit_DicomOrient.setText(current_orient)

        #3D
        for vn in 'axial','coronal','sagittal':
            self.LoadMRI.update_slices(0,vn)


class PopupDialog(QDialog):
    """
        Class for pop/up dialog for Metadata.
    """
    def __init__(self, parent=None, ui_widget=None):
        super().__init__(parent)
        self.setWindowTitle("Manual Control Adjustments")
        layout = QVBoxLayout(self)
        layout.addWidget(ui_widget)

    def closeEvent(self, event):
        # Instead of destroying, just hide the window
        self.hide()
        event.ignore()
