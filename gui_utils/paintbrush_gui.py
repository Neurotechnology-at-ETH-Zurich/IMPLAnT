# This Python file uses the following encoding: utf-8
from PySide6.QtGui import QPixmap, QIcon, QColor
from PySide6.QtCore import QSize
from core.mrid_tags import MRID_tags
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt
from core.interactor_style import CustomInteractorStyle
from PySide6 import QtWidgets

class PaintbrushGUI:
    """
        GUI controller class for managing the paintbrush functionality
        used for manual MRI tagging or segmentation.

        This class handles:
        - Paintbrush configuration (size, shape, color)
        - Label table population
        - Post-surgery paintbrush activation/deactivation
        - UI connections between brush controls and MRI data
    """
    def __init__(self,MW,state:bool,label=True,red_only=False):
        """
            Initialize the PaintbrushGUI class.

            Args:
                MW: MainWindow object containing UI and MRI data.
                state (bool): Whether the brush should be active initially.
        """
        self.MW = MW
        self.initialize_class(MW,state,label,red_only)

    def initialize_class(self,MW,state,label,red_only):
        """
            Initialize the PaintbrushGUI class.
        """
        histogram_needed = not red_only
        self.ui = MW.ui
        self.LoadMRI = MW.LoadMRI
        self.MW.Paintbrush.size = 5
        if not self.LoadMRI.volumes[0].is_4d:
            paint_over = self.paintbrush_function_3D(red_only)
            self.paintbrush_gui(paint_over,red_only)
            self.brush_3D(state,histogram_needed)
        else:
            paint_over = self.paintbrush_function_4D()
            self.paintbrush_gui(paint_over)
            self.brush_4D(state,label)
            self.activate_labels('anat')


    def paintbrush_function_3D(self,red_only):
        """
            Configure paintbrush controls for 3D MRI data.
            Includes label setup and brush type selection.
        """
        #set up labels and colors
        tag_data = []
        if red_only:
            regions = [('Label 1', 1)]
        else:
            regions = [('Label 1', 1), ('Label 2', 1), ('Label 3', 1),('Label 4', 1), ('Label 5', 1),('Label 6', 1)]
        num_regions = 6
        self.LoadMRI.mrid_tags = MRID_tags(self.MW, tag_data,num_regions,regions)
        self.LoadMRI.mrid_tags.create_labels()

        #pushButtons Type of Brush
        square_btn = self.ui.paint_square
        round_btn = self.ui.paint_round
        self.ui.paint_square.clicked.connect(
            lambda checked=False: (setattr(self.MW.Paintbrush, 'brush_type', 'square'),square_btn.setChecked(True), round_btn.setChecked(False))
        )
        self.ui.paint_round.clicked.connect(
            lambda checked=False: ( setattr(self.MW.Paintbrush, 'brush_type', 'round'),square_btn.setChecked(False), round_btn.setChecked(True))
        )
        # Fill combo Label box with color and names
        paint_over = self.ui.comboBox_paintOver

        return paint_over


    def paintbrush_function_4D(self):
        """
            Configure paintbrush controls for 4D MRI data
        """
        square_btn = self.ui.paint_square_Post
        round_btn = self.ui.paint_round_Post
        self.ui.paint_square_Post.clicked.connect(
            lambda checked=False: ( setattr(self.MW.Paintbrush, 'brush_type', 'square'),square_btn.setChecked(True), round_btn.setChecked(False))
        )
        self.ui.paint_round_Post.clicked.connect(
            lambda checked=False: (setattr(self.MW.Paintbrush, 'brush_type', 'round'),square_btn.setChecked(False), round_btn.setChecked(True))
        )
        paint_over = self.ui.comboBox_paintOver_Post
        return paint_over

    def paintbrush_gui(self,paint_over,red_only=False):
        """
            Set up the main paintbrush user interface:
            - Size sliders and spinboxes
            - Label occupancy controls
            - Paint-over color selector
            - Histogram color mapping
        """
        self.LoadMRI.brush['size'].setValue(self.MW.Paintbrush.size)
        self.LoadMRI.brush['size'].setRange(1,20)
        self.LoadMRI.brush['size'].valueChanged.connect(self.MW.Paintbrush.set_size)
        self.LoadMRI.brush['size_slider'].setValue(self.MW.Paintbrush.size)
        self.LoadMRI.brush['size_slider'].setRange(1,20)
        self.LoadMRI.brush['size_slider'].valueChanged.connect(self.MW.Paintbrush.set_size)
        #Label Occupancy
        self.MW.Paintbrush.label_occ = 0.5
        self.LoadMRI.brush['label_occ'].setValue(self.MW.Paintbrush.label_occ)
        self.LoadMRI.brush['label_occ'].setRange(0,1)
        self.LoadMRI.brush['label_occ'].valueChanged.connect(self.MW.Paintbrush.set_label_occupancy)
        self.LoadMRI.brush['label_occ_slider'].setValue(self.MW.Paintbrush.label_occ*100)
        self.LoadMRI.brush['label_occ_slider'].setRange(0,100)
        self.LoadMRI.brush['label_occ_slider'].valueChanged.connect(self.MW.Paintbrush.set_label_occupancy)

        # Fill Combobox with Colors
        self.label_table()

        # Fill paintover Box with Colors
        paint_over.clear()
        for i, color_name in enumerate(self.MW.Paintbrush.color_paintover):
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(color_name))
            icon = QIcon(pixmap)
            paint_over.addItem(icon, self.MW.Paintbrush.labels_paintover[i])

        paint_over.setIconSize(QSize(20, 20))
        paint_over.show()
        if red_only:
            paint_over.setCurrentIndex(0) #set all labels as default
            self.MW.Paintbrush.paintover_color = "black"
        else:
            paint_over.setCurrentIndex(1) #set clear labels as default

        paint_over.currentIndexChanged.connect(
            lambda index: setattr(self.MW.Paintbrush, "paintover_color", self.MW.Paintbrush.color_paintover[index])
        )

        #if paintbrush is clicked
        self.ui.checkBox_Brush_MRID.stateChanged.connect(self.brush_4D)
        self.ui.checkBox_Brush.stateChanged.connect(self.brush_3D)

        # Histogram
        self.MW.Paintbrush.widget_histogram = self.ui.widget_histogram

        histo = self.ui.histogram_label
        histo.clear()

        pixmap = QPixmap(20, 20)
        pixmap.fill(QColor('white'))
        icon = QIcon(pixmap)
        histo.addItem(icon, 'All anat Regions')

        for i, color_name in enumerate(self.MW.Paintbrush.color_histogram):
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(color_name))
            icon = QIcon(pixmap)
            histo.addItem(icon, self.MW.Paintbrush.labels_histogram[i])

        self.MW.Paintbrush.color_histogram.insert(0,'all anat')

        histo.setIconSize(QSize(20, 20))
        self.ui.widget_histogram.setLabel("left", "Number of Voxels")
        self.ui.widget_histogram.setLabel("bottom", "Intensity")
        histo.show()
        histo.setCurrentIndex(0) #set red as default
        self.ui.histogram_label.currentIndexChanged.connect(
            lambda index: (setattr(self.MW.Paintbrush, "histogram_color", self.MW.Paintbrush.color_histogram[index]),
                           self.MW.Paintbrush.histogram())  # call histogram immediately
        )
        self.ui.histogram_label.currentIndexChanged.connect(
            lambda index: (setattr(self.MW.Paintbrush, "histogram_color", self.MW.Paintbrush.color_histogram[index]),
                           self.MW.Paintbrush.histogram())  # call histogram immediately
        )
        self.ui.paintbrush_dataview.currentIndexChanged.connect(
            lambda index: (setattr(self.MW.Paintbrush, "label_volume_index", index),
                            self.MW.Paintbrush.histogram())
        )

    def activate_labels(self,mrid_stage):
        if mrid_stage == 'anat':
            for i, color_name in enumerate(self.MW.Paintbrush.color_paintover):
                index_item = self.table_lab.item(i, 0)
                icon_item = self.table_lab.item(i, 1)
                label_item = self.table_lab.item(i, 2)
                model = self.ui.comboBox_paintOver_Post.model()
                item = model.item(i)
                if i > self.LoadMRI.mrid_tags.num_regions+1:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    if index_item is not None:
                        index_item.setFlags(index_item.flags() & ~Qt.ItemIsEnabled)
                        icon_item.setFlags(icon_item.flags() & ~Qt.ItemIsEnabled)
                        label_item.setFlags(label_item.flags() & ~Qt.ItemIsEnabled)
                else:
                    item.setFlags(item.flags() | Qt.ItemIsEnabled)
                    if i > self.LoadMRI.mrid_tags.num_regions:
                        if index_item is not None:
                            index_item.setFlags(index_item.flags() & ~Qt.ItemIsEnabled)
                            icon_item.setFlags(icon_item.flags() & ~Qt.ItemIsEnabled)
                            label_item.setFlags(label_item.flags() & ~Qt.ItemIsEnabled)
                    else:
                        if index_item is not None:
                            index_item.setFlags(index_item.flags() | Qt.ItemIsEnabled)
                            icon_item.setFlags(icon_item.flags() | Qt.ItemIsEnabled)
                            label_item.setFlags(label_item.flags()| Qt.ItemIsEnabled)
        elif mrid_stage == 'segmentation':
            for i, color_name in enumerate(self.MW.Paintbrush.color_paintover):
                index_item = self.table_lab.item(i, 0)
                icon_item = self.table_lab.item(i, 1)
                label_item = self.table_lab.item(i, 2)
                model = self.ui.comboBox_paintOver_Post.model()
                item = model.item(i)
                item.setFlags(item.flags() | Qt.ItemIsEnabled) #paint over all labels
                if index_item is not None:
                    index_item.setFlags(index_item.flags() | Qt.ItemIsEnabled)
                    icon_item.setFlags(icon_item.flags() | Qt.ItemIsEnabled)
                    label_item.setFlags(label_item.flags()| Qt.ItemIsEnabled)

    def brush_3D(self,state:bool,histogram_needed:bool=True):
        """
        Enable or disable the paintbrush in 3D data GUI.
        """
        self.LoadMRI.brush_on = state
        if state:
            self.ui.checkBox_Brush.setText("Brush ON   ")
            if not self.LoadMRI.paint:
                self.LoadMRI.paint = True
                self.MW.Paintbrush.start_paintbrush(is_4d=False,histogram_needed=histogram_needed)
                self.LoadMRI.intensity_table[0].update_table("Label",self.MW.Paintbrush.label_volume[0],0,self.MW.Paintbrush.layer_index[0],visibility_enabled=False)
            #else:
            #self.MW.Paintbrush.start_paintbrush()
        else:
            self.ui.checkBox_Brush.setText("Brush OFF")
            #delete brush
            for i, renderers in self.LoadMRI.renderers.items():
                for view_name, renderer in renderers.items():
                    if self.MW.Paintbrush.brush_actors.get(view_name) is not None:
                        renderer.RemoveActor(self.MW.Paintbrush.brush_actors[view_name])
                    self.LoadMRI.vtk_widgets[i][view_name].GetRenderWindow().Render() ## FOR ALL IMAGES
            self.MW.Paintbrush.brush_actors[view_name] = None


    def brush_4D(self,state:bool,label=True):
        """
        Enable or disable the paintbrush in 4D data GUI.
        """
        self.LoadMRI.brush_on = state
        if state:
            self.MW.Paintbrush.start_paintbrush(is_4d=True)
            self.ui.checkBox_Brush_MRID.setText("Brush ON  ")
            if not self.LoadMRI.paint:
                self.LoadMRI.paint = True
                for idx in range(len(self.LoadMRI.vtk_widgets[0])):
                    table = self.LoadMRI.intensity_table[0]
                    if label:
                        table.update_table("Label",self.MW.Paintbrush.label_volume[idx],idx,visibility_enabled=False)
        else:
            self.ui.checkBox_Brush_MRID.setText("Brush OFF")
            if self.LoadMRI.heatmap:
                for idx in range(len(self.LoadMRI.vtk_widgets[0])):
                    data_view = list(self.LoadMRI.vtk_widgets[0].keys())[idx]
                    vtk_widget = self.LoadMRI.vtk_widgets[3][data_view]
                    interactor = vtk_widget.GetRenderWindow().GetInteractor()
                    interactor.SetInteractorStyle(None)
                    interactor.SetInteractorStyle(CustomInteractorStyle(self.MW.Cursor, data_view,3,None,idx))

            #delete brush
            for i, renderers in self.LoadMRI.renderers.items():
                for view_name, renderer in renderers.items():
                    if self.MW.Paintbrush.brush_actors.get(view_name) is not None:
                        renderer.RemoveActor(self.MW.Paintbrush.brush_actors[view_name])
                    self.LoadMRI.vtk_widgets[i][view_name].GetRenderWindow().Render() ## FOR ALL IMAGES
            self.MW.Paintbrush.brush_actors[view_name] = None


    def label_table(self):
        """
            Populate the label table with color icons and corresponding label names.
        """
        if not self.LoadMRI.volumes[0].is_4d:
            self.table_lab = self.ui.tableWidget_labels3D
        else:
            self.table_lab = self.ui.tableWidget_labels

        self.table_lab.setColumnWidth(0, 30)
        self.table_lab.setColumnWidth(1, 30)
        self.table_lab.setColumnWidth(2, 92)
        header = self.table_lab.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table_lab.setRowCount(len(self.MW.Paintbrush.color_combobox))

        for idx, color_name in enumerate(self.MW.Paintbrush.color_combobox):
            index_item = QTableWidgetItem(str(idx))
            index_item.setTextAlignment(Qt.AlignCenter)
            index_item.setFlags(index_item.flags() & ~Qt.ItemIsEditable)  # read-only
            self.table_lab.setItem(idx, 0, index_item)

            #Color icon
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(color_name))
            icon_item = QTableWidgetItem()
            icon_item.setIcon(QIcon(pixmap))
            icon_item.setTextAlignment(Qt.AlignCenter)
            icon_item.setFlags(icon_item.flags() & ~Qt.ItemIsEditable)
            self.table_lab.setItem(idx, 1, icon_item)

            #Label name
            label_item = QTableWidgetItem(self.MW.Paintbrush.labels_combobox[idx])
            label_item.setFlags(label_item.flags() & ~Qt.ItemIsEditable)  # read-only
            self.table_lab.setItem(idx, 2, label_item)

        self.table_lab.setFocus()
        self.table_lab.selectRow(1)
        self.table_lab.itemSelectionChanged.connect(
            lambda: setattr(
                self.MW.Paintbrush,
                "brush_color",
                self.MW.Paintbrush.color_combobox[self.table_lab.currentRow()]
            )
        )


