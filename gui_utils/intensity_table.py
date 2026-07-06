# This Python file uses the following encoding: utf-8
import os
from PySide6.QtWidgets import (
    QTableWidgetItem, QToolButton, QDoubleSpinBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu
from vtk.util import numpy_support
import numpy as np
import SimpleITK as sITK
from PySide6.QtWidgets import QFileDialog
from PySide6 import QtWidgets
from PySide6.QtWidgets import QSlider,QAbstractItemView
from PySide6.QtCore import QObject, QEvent
from PySide6.QtGui import QIcon

class IntensityTable(QObject):
    """GUI table for managing and visualizing MRI image layers with VTK integration."""
    def __init__(self, MW,data_index,table,vol,parent=None):
        """
            Initialize the IntensityTable for the given main data_index.

            Args:
                MW: The main application window containing UI and MRI data references.
        """
        super().__init__(parent)
        self.initialize_class(MW,data_index,table,vol)
        self.data_index = data_index
        #self.table.viewport().installEventFilter(self)
        #self._event_filter_table_viewport = self.table.viewport()
        #self._event_filter_table_viewport.installEventFilter(self)


    def initialize_class(self, MW,data_index,table,vol):
        """
            Initialize the IntensityTable for the given data_index.
        """
        self.MW = MW
        self.index = 0
        self.MW.LoadMRI.intensity = {}
        self.intensity_volumes = []
        self.intensity_volumes.append(vol)
        self.original_image = []
        self.file_name = []
        self.opacity_index = []
        self.table = table
        self.opacity_values = []
        self.overlay_contrasts = {}      # non_mainindex -> window/level state dict
        self.contrast_combo_map = []     # combobox position (1+) -> non_mainindex

        icon_dir = os.path.join(os.path.dirname(os.path.dirname((__file__))), "Icons/mri")
        self.icon_visible = QIcon(os.path.join(icon_dir, "eye_open.png"))
        self.icon_hidden = QIcon(os.path.join(icon_dir, "eye_closed.png"))

        self.create_table(data_index)
        self.setup_slider_overlay()
        self.MW.ui.comboBox_Contrastimage.currentIndexChanged.connect(
            self.on_contrast_selection_changed
        )


    def update_intensity_values(self,data_index):
        """
        Update the voxel intensity values displayed in the table based on the current slice index.
        """
        for i, vol in enumerate(self.intensity_volumes):
            z, y, x = self.MW.LoadMRI.slice_indices[data_index]
            intensity = vol[z,y,x]
            item = self.table.item(i, 2)
            if item is not None:
                item.setText(f"{intensity:.3f}")

    def create_table(self,data_index,row=0):
        """
        Initialize and populate the intensity table with the first loaded MRI volume.
        """
        if row==0:
            if not self.MW.LoadMRI.volumes[0].is_4d:
                self.table.customContextMenuRequested.connect(lambda idx: self.show_context_menu(idx,data_index))
            else:
                self.table.customContextMenuRequested.connect(lambda idx: self.show_context_menu(idx,data_index))

            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)   # BIG COLUMN
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.table.setRowCount(self.index+1)

        btn = QToolButton()
        btn.setCheckable(False)
        btn.setChecked(True)  # visible by default
        btn.setEnabled(False)
        btn.setIcon(self.icon_visible)
        btn.setToolTip("Toggle visibility")
        btn.setAutoRaise(True)
        btn.clicked.connect(lambda checked , b=btn: self.MW.Layers[self.data_index][self.index].toggle_visibility(checked,b))
        btn.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
            }
            QToolButton:checked {
                background: transparent;
            }
        """)
        self.table.setCellWidget(self.index , 0, btn)

        # Column 1: Layer name
        layer_item = QTableWidgetItem(os.path.basename(self.MW.LoadMRI.volumes[data_index].file_path))
        layer_item.setFlags(layer_item.flags() & ~Qt.ItemIsEditable)
        layer_item.setToolTip(layer_item.text())
        self.table.setItem(self.index , 1, layer_item)
        self.table.setTextElideMode(Qt.ElideNone)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table.setWordWrap(False)
        self.table.resizeColumnToContents(1)

        # Column 2: Intensity
        z,y,x = self.MW.LoadMRI.slice_indices[data_index]
        intensity_item = QTableWidgetItem(f"{self.intensity_volumes[0][z,y,x]:.3f}")
        intensity_item.setTextAlignment(Qt.AlignCenter)
        intensity_item.setFlags(intensity_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(self.index , 2, intensity_item)

        self.MW.LoadMRI.intensity[self.index]=[]
        self.MW.LoadMRI.intensity[self.index] = self.table.item(self.index , 2)
        self.MW.LoadMRI.cursor_ui[f"intensity{self.index}"] = self.table.item(self.index , 2)

        # Column 3: Opacity [%]
        opacity_spin = QDoubleSpinBox()
        opacity_spin.setRange(0.0, 100.0)
        opacity_spin.setSingleStep(5.0)
        opacity_spin.setDecimals(1)
        opacity_spin.setValue(100)
        opacity_spin.setSuffix(" %")
        opacity_spin.setAlignment(Qt.AlignCenter)
        opacity_spin.setToolTip("Adjust layer opacity")
        opacity_spin.setEnabled(False)
        self.table.setCellWidget(self.index , 3, opacity_spin)
        self.MW.LoadMRI.cursor_ui[f"opacity{self.index }"] = opacity_spin

        self.opacity_values.append([100,False,data_index])

        # Layout
        self.original_image.append(None)
        self.file_name.append(os.path.basename(self.MW.LoadMRI.volumes[data_index].file_path))
        self.opacity_index.append(0)

        # Populate contrast combobox with the main image
        self.MW.ui.comboBox_Contrastimage.blockSignals(True)
        self.MW.ui.comboBox_Contrastimage.clear()
        self.MW.ui.comboBox_Contrastimage.addItem(os.path.basename(self.MW.LoadMRI.volumes[data_index].file_path))
        self.MW.ui.comboBox_Contrastimage.blockSignals(False)

        # Show opactity slidebar
        #self.table.cellClicked.connect(self.on_table_clicked)
        self.table.selectionModel().selectionChanged.connect(self.on_table_clicked)



    def update_table(self,layer_name:str,vol, data_index,layer_index,org_img=None, visibility_enabled=True):
        """
        Add a new layer (e.g., heatmap, label, another file, etc.) to the table.
        """

        self.original_image.append(org_img)
        self.intensity_volumes.append(vol)
        self.file_name.append(layer_name)
        self.index+=1
        self.table.insertRow(self.index)

        self.opacity_index.append(layer_index)

        # Register contrast state for non-main overlay images
        if layer_index != 0:
            idx = layer_index-1
            if idx not in self.overlay_contrasts:
                vmin, vmax = np.percentile(vol, [0, 99.999])
                vmin_a, vmax_a = np.percentile(vol, [0.01, 99.9])
                self.overlay_contrasts[idx] = {
                    'window':          vmax - vmin,
                    'level':           (vmax + vmin) / 2,
                    'initial_window':  vmax - vmin,
                    'initial_level':   (vmax + vmin) / 2,
                    'window_auto':     vmax_a - vmin_a,
                    'level_auto':      (vmax_a + vmin_a) / 2,
                    'data_max':        max(1, int(vol.max())),
                }
                self.contrast_combo_map.append(idx)
                self.MW.ui.comboBox_Contrastimage.addItem(layer_name)

        row_index = self.index
        btn = QToolButton()
        btn.setCheckable(True)
        btn.setChecked(True)
        btn.setEnabled(visibility_enabled)
        btn.setIcon(self.icon_visible)
        btn.setToolTip("Toggle visibility")
        btn.setAutoRaise(True)
        btn.clicked.connect(lambda checked, b=btn, r=row_index: self.MW.Layers[self.data_index][row_index].toggle_visibility(checked,b))
        btn.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
            }
            QToolButton:checked {
                background: transparent;
            }
        """)
        self.table.setCellWidget(self.index , 0, btn)

        # Column 1: Layer name
        layer_item = QTableWidgetItem(layer_name)
        layer_item.setFlags(layer_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(self.index , 1, layer_item)
        layer_item.setToolTip(layer_item.text())

        # Column 2: Intensity
        z, y, x = self.MW.LoadMRI.slice_indices[data_index]
        intensity_item = QTableWidgetItem(f"{vol[z,y,x]:.3f}")
        intensity_item.setTextAlignment(Qt.AlignCenter)
        intensity_item.setFlags(intensity_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(self.index , 2, intensity_item)

        self.MW.LoadMRI.intensity[self.index]=[]
        self.MW.LoadMRI.intensity[self.index] = self.table.item(self.index , 2)
        self.MW.LoadMRI.cursor_ui[f"intensity{self.index}"] = self.table.item(self.index , 2)

        # Column 3: Opacity [%]
        opacity_spin = QDoubleSpinBox()
        opacity_spin.setRange(0.0, 100.0) # percentage (0–100)
        opacity_spin.setSingleStep(5.0)
        opacity_spin.setDecimals(1)
        opacity_spin.setValue(0.6 * 100)  # assume stored 0.0–1.0 internally
        opacity_spin.setSuffix(" %")
        opacity_spin.setAlignment(Qt.AlignCenter)
        opacity_spin.setEnabled(visibility_enabled)
        opacity_spin.setToolTip("Adjust layer opacity")
        opacity_spin.valueChanged.connect(lambda value, slider=self.overlay_slider, box=opacity_spin: (
            self.opacity_values[row_index].__setitem__(0, value),
            self.MW.Layers[self.data_index][row_index].set_opacity(value, slider, box)
        ))

        #self.update_opacity(value, i, r))
        self.table.setCellWidget(self.index , 3, opacity_spin)
        self.MW.LoadMRI.cursor_ui[f"opacity{self.index }"] = opacity_spin

        if visibility_enabled:
            self.opacity_values.append([0.6*100,visibility_enabled,data_index])
        else:
            self.opacity_values.append([1*100,visibility_enabled,data_index])

        return btn

    def show_context_menu(self, pos,data_index):
        """
        Display right-click menu for saving or removing layers.
        """
        item = self.table.itemAt(pos)
        if not item:
            return
        row = item.row()

        menu = QMenu(self.MW)
        menu.addAction(f"Save image {self.file_name[row]}", lambda: self.save_layer(row))
        menu.addAction("Remove image", lambda: self.remove_layer(row,data_index))
        menu.exec(self.table.mapToGlobal(pos))


    def save_layer(self,row):
        """
        Save selected image layer (anat, seg, or generic) as a NIfTI file.
        """
        img_to_save = self.original_image[row]
        file_name = self.file_name[row]

        if img_to_save is None:
            vol_to_save = self.intensity_volumes[row]
            if self.table.item(row,1).text()=='Label':
                if self.MW.LoadMRI.volumes[0].is_4d:
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Choose which data to save")
                    msg_box.setText("Which data do you want to save?")
                    btn_anat = msg_box.addButton("Anat", QMessageBox.ActionRole)
                    btn_seg = msg_box.addButton("Segmentation", QMessageBox.ActionRole)
                    msg_box.exec_()

                    label_volume = self.MW.Paintbrush.label_volume.copy()
                    if btn_anat:
                        file_name = self.file_name[0][:-7]
                        file_name = f"{file_name}-anat.nii.gz"
                        vol_to_save[label_volume > self.MW.LoadMRI.mrid_tags.num_regions] = 0
                    elif btn_seg:
                        file_name = self.file_name[0][:-7]
                        file_name = f"{file_name}-segmentation.nii.gz"
                        vol_to_save[label_volume <= self.MW.LoadMRI.mrid_tags.num_regions] = 0
                else:
                    file_name = self.file_name[0][:-7]
                    file_name = f"{file_name}-label"

            img_to_save = sITK.GetImageFromArray(vol_to_save)
            size = list(self.intensity_volumes[row].shape[::-1]) + [0]

            # Extract 1 time frame
            img = sITK.ReadImage(self.MW.LoadMRI.volumes[0].file_path)
            img = sITK.DICOMOrient(img, self.MW.LoadMRI.volumes[0].DICOMOrient)
            reference_image = sITK.Extract(
                img,
                size=size,
                index=[0, 0, 0, 0]  # take time=0 frame
            )
            img_to_save.CopyInformation(reference_image)

        save_path, _ = QFileDialog.getSaveFileName(
            self.MW,
            "Save NIfTI File",
            file_name,
            "NIfTI Files (*.nii.gz);;All Files (*)"
        )

        if not save_path:
            return

        # Ensure the filename ends with .nii.gz
        if not save_path.lower().endswith(".nii.gz"):
            save_path += ".nii.gz"

        sITK.WriteImage(img_to_save, save_path)




    def remove_layer(self,row,data_index):
        """
        Remove a layer from VTK renderers and update the GUI table.

        !!! Only tested with 3D data!!!
        """
        if self.table.item(row,1).text()=='Label':
            #for idx in range(len(self.MW.LoadMRI.renderers)):
            layer = self.MW.Layers[data_index][self.MW.Paintbrush.layer_index[data_index]]
            for vn, actor in layer.actors.items():
                self.MW.LoadMRI.renderers[data_index][vn].RemoveActor(actor)
                #actor = self.overlay_actors[vn][idx]
                #renderer.RemoveActor(actor)
            for vn in 'axial','coronal','sagittal':
                renderer = self.MW.LoadMRI.renderers[data_index][vn]
                self.MW.LoadMRI.vtk_widgets[0][vn].GetRenderWindow().Render()
                self.MW.LoadMRI.update_slices(0,0,data_view=vn)
        else:
            for vn in 'axial','coronal','sagittal':
                if vn=='axial':
                    slice = np.fliplr(self.intensity_volumes[row][self.MW.LoadMRI.slice_indices[data_index][0],:,:])
                elif vn=='coronal':
                    slice = np.fliplr(self.intensity_volumes[row][:,self.MW.LoadMRI.slice_indices[data_index][1],:])
                elif vn=='sagittal': #different with .T flip; etc.
                    slice = np.fliplr(self.intensity_volumes[row][:,:,self.MW.LoadMRI.slice_indices[data_index][2]])

                renderer = self.MW.LoadMRI.renderers[data_index][vn]
                actors = renderer.GetViewProps()
                actors.InitTraversal()

                for _ in range(actors.GetNumberOfItems()):
                    actor = actors.GetNextProp()
                    if actor.GetClassName()=="vtkOpenGLTextActor" or actor.GetClassName()=="vtkOpenGLActor" or actor.GetClassName()=="vtkActor2D":
                        continue
                    image_data = actor.GetInput()

                    vtk_array = numpy_support.vtk_to_numpy(image_data.GetPointData().GetScalars())
                    vtk_array = vtk_array.reshape(image_data.GetDimensions()[1], image_data.GetDimensions()[0])
                    if np.allclose(vtk_array, slice):
                        renderer.RemoveActor(actor)
                        self.MW.LoadMRI.vtk_widgets[0][vn].GetRenderWindow().Render()
                        self.MW.LoadMRI.update_slices(0,0,data_view=vn)
                        break

        #update table
        self.table_delete_row(row)




    def table_delete_row(self,row=int):
        """
        Remove a row from the GUI table and internal data lists.
        """
        #remove row in table
        self.table.removeRow(row)

        #remove from lists
        self.intensity_volumes.pop(row)
        self.original_image.pop(row)
        self.file_name.pop(row)
        self.index-=1

        self.opacity_values.pop(row)


    def on_contrast_selection_changed(self, combo_idx):
        """
        Reconnect the shared contrast sliders/buttons to whichever image
        is selected in comboBox_Contrastimage.
        combo_idx == 0  → main image (lm.contrast[0])
        combo_idx >= 1  → overlay at self.contrast_combo_map[combo_idx - 1]
        """
        lm = self.MW.LoadMRI
        if not hasattr(lm, 'contrast') or 0 not in lm.contrast:
            return
        ui = lm.contrast_ui_elements[0]

        # Disconnect existing bindings (PySide6 raises RuntimeWarning, not RuntimeError)
        for key in ("contrast0", "brightness0"):
            try:
                ui[key].valueChanged.disconnect()
            except Exception:
                pass
        for key in ("auto0", "reset0"):
            try:
                ui[key].clicked.disconnect()
            except Exception:
                pass

        def _set_sliders(window, level, data_max, block=True):
            for key in ("contrast0", "brightness0"):
                ui[key].blockSignals(block)
            ui["contrast0"].setMaximum(data_max)
            ui["brightness0"].setMaximum(data_max)
            ui["contrast0"].setValue(int(window))
            ui["brightness0"].setValue(int(level))
            ui["display_window0"].setValue(int(window))
            ui["display_level0"].setValue(int(level))
            for key in ("contrast0", "brightness0"):
                ui[key].blockSignals(False)

        if combo_idx == 0:
            c = lm.contrast[0]
            data_max = max(1, int(lm.volumes[0].slices[0].max()))
            _set_sliders(c.window[0], c.level[0], data_max)
            ui["contrast0"].valueChanged.connect(lambda val: c.changed_sliders(val, 0))
            ui["brightness0"].valueChanged.connect(lambda val: c.changed_sliders(val, 0))
            ui["auto0"].clicked.connect(lambda: c.auto(0))
            ui["reset0"].clicked.connect(lambda: c.reset(0))
        else:
            #non_main_idx = combo_idx #self.contrast_combo_map[combo_idx - 1]
            state = self.overlay_contrasts[combo_idx-1]
            _set_sliders(state['window'], state['level'], state['data_max'])

            def _changed(val, s=state, i=combo_idx):
                s['window'] = ui["contrast0"].value()
                s['level']  = ui["brightness0"].value()
                ui["display_window0"].setValue(int(s['window']))
                ui["display_level0"].setValue(int(s['level']))
                vmin = s['level'] - s['window'] / 2
                vmax = s['level'] + s['window'] / 2
                self.MW.Layers[self.data_index][combo_idx].update_lut(i, vmin, vmax)

            def _auto(_checked=False, s=state, i=combo_idx):
                s['window'] = s['window_auto']
                s['level']  = s['level_auto']
                _set_sliders(s['window'], s['level'], s['data_max'])
                self.MW.Layers[self.data_index][combo_idx].update_lut(i, s['level'] - s['window']/2, s['level'] + s['window']/2)

            def _reset(_checked=False, s=state, i=combo_idx):
                s['window'] = s['initial_window']
                s['level']  = s['initial_level']
                _set_sliders(s['window'], s['level'], s['data_max'])
                self.MW.Layers[self.data_index][combo_idx].update_lut(i, s['level'] - s['window']/2, s['level'] + s['window']/2)


            ui["contrast0"].valueChanged.connect(_changed)
            ui["brightness0"].valueChanged.connect(_changed)
            ui["auto0"].clicked.connect(_auto)
            ui["reset0"].clicked.connect(_reset)

    def setup_slider_overlay(self):
        self.overlay_slider = QSlider(Qt.Horizontal, self.table.viewport())
        self.overlay_slider.setRange(0, 100)
        self.overlay_slider.setFixedWidth(self.table.columnWidth(3))
        self.overlay_slider.setSingleStep(5.0)
        self.overlay_slider.hide()

    def on_table_clicked(self, selected,deselected):
        if not selected.indexes():
            return

        index = selected.indexes()[0]
        row = index.row()
        column = index.column()

        if column==3 and self.opacity_values[row][1]==True:
            index = self.table.model().index(row, column)
            rect = self.table.visualRect(index)

            slider = self.overlay_slider
            # Fix: disconnect any previous connections first
            try:
                slider.valueChanged.disconnect()
            except RuntimeError:
                pass

            slider.setValue(self.opacity_values[row][0])
            slider.move(rect.left()-(rect.right()-rect.left())+20, rect.center().y())
            slider.show()
            slider.valueChanged.connect(lambda value, slider=slider, box=self.MW.LoadMRI.cursor_ui[f"opacity{row}"]: (
                self.opacity_values[row].__setitem__(0, value),
                self.MW.Layers[self.data_index][row].set_opacity(value,slider,box)
            ))

    def eventFilter(self, obj, event):
        if obj is getattr(self, "_event_filter_table_viewport", None):
            if event.type() == QEvent.MouseButtonPress:
                if hasattr(self, "overlay_slider") and self.overlay_slider.isVisible():
                    self.overlay_slider.hide()
        return False
