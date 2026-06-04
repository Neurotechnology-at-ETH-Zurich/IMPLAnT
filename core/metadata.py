# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QDialog, QVBoxLayout
import SimpleITK as sitk
from core.mri_volume import MRIVolume

class Metadata:
    def __init__(self,MW):
        self.MW = MW
        self.ui = MW.ui
        self.LoadMRI = MW.LoadMRI
        self.ui.pushButton_metadata.clicked.connect(self.show_metadata)
        self.ui.pushButton_changeSpacing.clicked.connect(self.change_spacing)
        self.ui.pushButton_SaveSpacing.clicked.connect(self.save_new_spacing)
        self.ui.pushButton_SaveMetadata.clicked.connect(self.set_metadata)
        self.ui.pushButton_reorient.clicked.connect(self.reorient_volume)

        self.ui.doubleSpinBox_spax.valueChanged.connect(lambda val: self.changed_parameters_spacing(val,'x'))
        self.ui.doubleSpinBox_spay.valueChanged.connect(lambda val: self.changed_parameters_spacing(val,'y'))
        self.ui.doubleSpinBox_spaz.valueChanged.connect(lambda val: self.changed_parameters_spacing(val,'z'))
        self.ui.doubleSpinBox_fovx.valueChanged.connect(lambda val: self.changed_parameters_fov(val,'x'))
        self.ui.doubleSpinBox_fovy.valueChanged.connect(lambda val: self.changed_parameters_fov(val,'y'))
        self.ui.doubleSpinBox_fovz.valueChanged.connect(lambda val: self.changed_parameters_fov(val,'z'))


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
        image = self.LoadMRI.volumes[0].ref_image
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



    def save_new_spacing(self):
        self.ui.doubleSpinBox_spacingx.setValue(self.ui.doubleSpinBox_spax.value())
        self.ui.doubleSpinBox_spacingy.setValue(self.ui.doubleSpinBox_spay.value())
        self.ui.doubleSpinBox_spacingz.setValue(self.ui.doubleSpinBox_spaz.value())

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
        new_spacing = [self.ui.doubleSpinBox_spacingz.value(),self.ui.doubleSpinBox_spacingy.value(),self.ui.doubleSpinBox_spacingx.value()]

        img = sitk.ReadImage(self.LoadMRI.volumes[0].file_path)
        img.SetSpacing(new_spacing)
        sitk.WriteImage(img, self.LoadMRI.volumes[0].file_path)

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
        #orientation
        orient_filter = sitk.DICOMOrientImageFilter()
        current_orient = orient_filter.GetOrientationFromDirectionCosines(self.LoadMRI.volumes[data_index].ref_image.GetDirection())
        self.ui.lineEdit_DicomOrient.setText(current_orient)

        #3D
        for vn in 'axial','coronal','sagittal':
            self.LoadMRI.update_slices(0,0,vn)


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
