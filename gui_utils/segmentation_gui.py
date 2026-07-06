# This Python file uses the following encoding: utf-8
from segmentation.segmentation_utils import Segmentation, SegmentationInitialization
from segmentation.evolution import SegmentationEvolution
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QDockWidget
from utils.zoom import zoom_notifier
from core.image_layer import ImageLayer
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
    def __init__(self,MW,samri=False):
        """Initialize the segmentation GUI and connect UI elements to corresponding handlers."""
        self.LoadMRI = MW.LoadMRI
        self.MW = MW
        self.ui = MW.ui
        self.initialization_first_time = True
        self.ui.checkBox_threshold.stateChanged.connect(self.on_threshold_changed)
        self.ui.pushButton_Next1.clicked.connect(self.active_bubbles)
        self.ui.pushButton_Back2.clicked.connect(self.threshold_seg)
        self.ui.pushButton_Next2.clicked.connect(self.evolution)
        self.ui.pushButton_Back3.clicked.connect(self.active_bubbles)
        self.ui.pushButton_Finish.clicked.connect(self.seg_finish)
        if samri:
            self.ui.pushButton_Back1.setEnabled(True)
        self.ui.pushButton_Back1.clicked.connect(self.seg_finish)
        self.samri = samri
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
        layer = self.LoadMRI.MW.Layers[0][self.layer_index]
        layer.toggle_visibility(checked,None)


    def threshold_seg(self):
        """Display the threshold adjustment page."""
        self.ui.stackedWidget_segmentation.setCurrentIndex(0)
        self.update_threshold_display()


    def update_threshold_display(self):
        """Refresh the thresholded image display according to current mode and bounds."""
        if self.LoadMRI.Segmentation.threshold_mode == 'bounded':
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
            lut = self.setup_lut(th_vol)
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
            vmin, vmax = th_vol.min(), th_vol.max()
            layer.update_lut(0, vmin, vmax)
            #self.LoadMRI.render()

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
            print('row_selected',row_index,radius,self.LoadMRI.SegInitialization.actor_bubble,flush=True)
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
            button = self.ui.toolButton_runEvo
            spin_iterations = self.ui.doubleSpinBox_Segiter
            btn_resetCamera = self.ui.pushButton_seg3D
            self.LoadMRI.SegEvolution = SegmentationEvolution(self.LoadMRI,self.LoadMRI.SegInitialization,self.LoadMRI.Segmentation,button,spin_iterations,btn_resetCamera)

            button.clicked.connect(self.LoadMRI.SegEvolution.on_play_pause)
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

        return


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