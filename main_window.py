# This Python file uses the following encoding: utf-8
# Important: You need to run the following command to generate the ui_form.py file: pyside6-uic form.ui -o ui_form.py
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'xcb')
import sys
import json as _json
_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_form import Ui_MainWindow
from utils.zoom import zoom_notifier
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog, QDockWidget
import SimpleITK as sitk
from gui_utils.busy_overlay import BusyOverlay
from PySide6 import QtWidgets
from ephys.init_ephys import InitEphys
from PySide6.QtCore import Qt, QCoreApplication, QResource
import qdarkstyle
from utils.zoom import Zoom
import shutil
from samri.samri_main import InitSAMRI,SAMRI_InputDialog,SAMRI_InputDock
from samri.samri_logging import LogAdapter,SamriWorker
import logging
from PySide6.QtWidgets import QWidget
from trajectory_planning.trajectory_planning import TrajectoryPlanning
from trajectory_planning.file_input_output import FileInput
import vtk
import pandas as pd
from file_handling.loader import FileLoader
from file_handling.resample_data import ResampleData
from PySide6.QtGui import QIcon


class MainWindow(QMainWindow):
    """
    Main application window for MRI visualization.
    """
    def __init__(self, parent=None):
        """
        Initialize the main window
        """
        super().__init__(parent)
        self.resize_bool=True
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("IMPLAnT")
        self.setWindowIcon(QIcon(os.path.join(_base_dir, "Icons/Github/IMPLAnT_logo.png")))
        self.add_actions()

    def add_actions(self):
        """
        Initializes action triggers, GUI layout and setup UI elements.
        """
        #hide tab bars
        self.ui.tabWidget.tabBar().setVisible(False)
        self.ui.tabWidget_visualisation.tabBar().setVisible(False)

        #only show one row of views and center the three visible widgets
        box = self.ui.page_3D
        layout = box.layout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)
        self.ui.groupBox_data2.setVisible(False)
        self.ui.groupBox_data1.setVisible(False)
        self.ui.heatmap_data0.setVisible(False)
        self.ui.groupBox_barcode.setVisible(False)
        self.ui.groupbox_legend0.setVisible(False)
        self.ui.contrast_data.setItemEnabled(0, True)
        self.ui.contrast_data.setCurrentIndex(0)
        self.ui.contrast_data.setItemEnabled(1, False)
        self.ui.contrast_data.setItemEnabled(2, False)
        self.ui.dockWidget_ephys.setVisible(False)
        self.ui.lineEdit_vis3D.setVisible(False)
        self.ui.frame_vis3D.setVisible(False)
        self.ui.textEdit_SAMRI_reg.setVisible(False)
        self.ui.stackedWidget_3d.setVisible(False)
        self.ui.stackedWidget_axial.setCurrentIndex(0)
        self.ui.stackedWidget_coronal.setCurrentIndex(0)
        self.ui.stackedWidget_sagittal.setCurrentIndex(0)

        #resize to inital size
        self.resize(1600, 900)
        self.setMinimumSize(1500,800)

        # Connect all buttons to open file
        self.ui.actionOpen.triggered.connect(self.initialize_mri_session)
        self.ui.actionOpen_ephys_Data.triggered.connect(self.open_ephys_data)
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionStart_SAMRI_process.triggered.connect(self.initialize_samri)
        self.ui.actionTrajectory_Planning.triggered.connect(self.initialize_trajectory_planning)

        # Re-render if tab changed
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)


    def open_ephys_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open ephys Data File",
            _paths['raw_base'],
            "Data files (*.dat)"
        )

        #User cancelled
        if not file_name:
            return

        #pop up asking for the view if 4D data used
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Open Main File")
        msg_box.setText(f"Do you want to open the file \n {file_name}?")
        msg_box.addButton("Yes", QMessageBox.ActionRole)
        btn_no = msg_box.addButton("No, other File", QMessageBox.ActionRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.ActionRole)
        msg_box.exec()
        if msg_box.clickedButton()==btn_cancel:
            return
        elif msg_box.clickedButton()==btn_no:
            self.open_ephys_data()
            return

        self.ui.dockWidget_ephys.setVisible(True)
        self.ui.stackedWidget_video.setCurrentIndex(1)
        self.ui.textEdit_ephys.setText(f"File loaded: {file_name}")
        self.ui.tabWidget.setCurrentIndex(3)
        self.overlay = BusyOverlay(self, message="Processing, please wait…")
        self.overlay.run(self.do_ephys_heavy, file_name)

    def do_ephys_heavy(self, file_name):
        self.Ephys = InitEphys(self, file_name)
        self.Ephys.open_dat(file_name)


    def resizeEvent(self, event):
        """
        re-rendering of vtk widgets if GUI resizes
        """
        super().resizeEvent(event)
        # Call on_gui_resize to re-render the vtk widgets
        if self.resize_bool==True:
            self.on_gui_resize()

    def initialize_mri_session(self):
        """
        Open the initial User Dialog when the application starts.
        """
        self.FileLoader = FileLoader(self)
        file_name, data_view = self.FileLoader.open_user_dialog()
        if file_name is None:
            return
        zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
        if not self.FileLoader.is_4d:
            Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)

        self.ui.comboBox_resamplefiles.addItem(os.path.basename(file_name)) #add to combobox for resampling
        if self.FileLoader.is_4d:
            self.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")
        else:
            data_view = "coronal"

        tab_idx = 0 if self.FileLoader.is_4d else 1
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.data_4d_3d.setCurrentIndex(tab_idx)


    def on_gui_resize(self):
        """
        Re-render VTK widgets when GUI size changes.
        """
        self.ui.vtkWidget_data_sagittal.GetRenderWindow().Render()
        self.ui.vtkWidget_data_coronal.GetRenderWindow().Render()
        self.ui.vtkWidget_data_axial.GetRenderWindow().Render()
        self.ui.vtkWidget_data_seg3D.GetRenderWindow().Render()
        self.ui.vtkWidget_data00.GetRenderWindow().Render()
        self.ui.vtkWidget_data01.GetRenderWindow().Render()
        self.ui.vtkWidget_data02.GetRenderWindow().Render()
        self.ui.vtkWidget_data03.GetRenderWindow().Render()
        self.ui.vtkWidget_legend0.GetRenderWindow().Render()
        self.ui.vtkWidget_data10.GetRenderWindow().Render()
        self.ui.vtkWidget_data11.GetRenderWindow().Render()
        self.ui.vtkWidget_data12.GetRenderWindow().Render()
        self.ui.vtkWidget_data13.GetRenderWindow().Render()
        self.ui.vtkWidget_legend1.GetRenderWindow().Render()
        self.ui.vtkWidget_data10.GetRenderWindow().Render()
        self.ui.vtkWidget_data11.GetRenderWindow().Render()
        self.ui.vtkWidget_data12.GetRenderWindow().Render()
        self.ui.vtkWidget_data13.GetRenderWindow().Render()
        self.ui.vtkWidget_legend2.GetRenderWindow().Render()
        self.ui.vtkWidget_trajPlan_1.GetRenderWindow().Render()
        #barcode sachen
        self.ui.vtkWidget_ephys.GetRenderWindow().Render()


        if hasattr(self, 'LoadMRI'):
            if hasattr(self.LoadMRI,'minimap') and not self.LoadMRI.volumes[0].is_4d:
                for data_index, layers in self.Layers.items():
                    #for layer_index, layer in layers.items():
                    img_vtk = layers[0].img_vtks["axial"][0]
                    self.LoadMRI.minimap.add_minimap('axial',img_vtk,0,self.LoadMRI.vtk_widgets[0]["axial"],0,data_3d=True)
                    img_vtk = layers[0].img_vtks["coronal"][0]
                    self.LoadMRI.minimap.add_minimap('coronal',img_vtk,0,self.LoadMRI.vtk_widgets[0]["coronal"],0,data_3d=True)
                    img_vtk = layers[0].img_vtks["sagittal"][0]
                    self.LoadMRI.minimap.add_minimap('sagittal',img_vtk,0,self.LoadMRI.vtk_widgets[0]["sagittal"],0,data_3d=True)
            else:
                if hasattr(self.LoadMRI, 'vtk_widgets'):
                    for data_index in range(len(self.LoadMRI.vtk_widgets[0])):
                        for image_index,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
                            if "CORONAL" in self.ui.groupBox_data0.title():
                                view_name = "coronal"
                            elif "AXIAL" in self.ui.groupBox_data0.title():
                                view_name = "axial"
                            elif "SAGITTAL" in self.ui.groupBox_data0.title():
                                view_name = "sagittal"
                            img_vtk = self.Layers[data_index][0].img_vtks[view_name][image_index]
                            self.LoadMRI.minimap.add_minimap(view_name,img_vtk,image_index,vtk_widget_image[view_name],data_index)


    def add_another_file(self):
        """
        Triggered if another file is uploaded by the user, saves it as highest layer.
        """
        self.FileLoader.layer_index += 1
        file_name, data_view = self.FileLoader.open_user_dialog(layer_index=self.FileLoader.layer_index,add_another_file=True)
        if file_name is None:
            return

        if not self.LoadMRI.volumes[0].is_4d:
            #add to registration combobox
            self.ui.comboBox_movingimg.addItem(os.path.basename(file_name))
            self.LoadMRI.combo_Regimgname = self.ui.comboBox_movingimg
            self.LoadMRI.movingimg_filename.append(file_name)
        else:
            img = sitk.ReadImage(file_name)
            vol = sitk.GetArrayFromImage(img)
            #add to intensity table
            keys = list(self.LoadMRI.vtk_widgets[0].keys())
            idx = keys.index(data_view)
            tabclass = self.LoadMRI.intensity_table[idx]
            tabclass.update_table(os.path.basename(file_name), vol,idx)
            self.ui.contrast_data.setItemEnabled(idx, False)



    def initialize_samri(self):
        #Pop up for bruker2bids
        self.ui.tabWidget.setCurrentIndex(5)
        SAMRI_InputDialog(self)

    def fetch_data(self,samri_input):
        def work_init():
            self.Samri = InitSAMRI(samri_input)
        # Clean up previous worker if it exists
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.done.disconnect()
            self.worker.failed.disconnect()
            self.worker = None

        # Reinstall log adapter fresh
        if hasattr(self, 'log_adapter') and self.log_adapter:
            self.log_adapter.uninstall()

        self.log_adapter = LogAdapter(self.ui.plainTextEdit_SAMRI)
        self.log_adapter.install(level=logging.INFO)

        self.worker = SamriWorker(work_init, self)
        self.worker.done.connect(lambda: logging.info("Ready for Biascorrection or Registration"))
        self.worker.done.connect(self.on_bruker2bids_done)
        self.worker.failed.connect(lambda tb: logging.error(tb))
        self.worker.start()

    def on_bruker2bids_done(self):
        #Pop up for registration
        self.ui.frame_samri.setEnabled(True)
        self.Samri_input = SAMRI_InputDock(self)


    def start_registration(self,samri_input):
        def work_registration():
            self.ui.dockWidget_ephys.setEnabled(False)
            self.Samri.output_filepath =  self.Samri.start_registration(samri_input)

        # Clean up previous worker if it exists
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.done.disconnect()
            self.worker.failed.disconnect()
            self.worker = None

        if samri_input['register']:
            csv_path = f"{self.Samri.bids_base}/results/generic_work/data_selection.csv"
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, index_col=0)

                idx = df.loc[df['session'] == samri_input['working_session'][0]].index[0] #original_path?
                path = f"{self.Samri.bids_base}/results/generic_work/_ind_type_{idx}/s_register"
                if os.path.exists(path):
                    #pop up asking for the view if 4D data used
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Registration found")
                    msg_box.setText("Registration already found!")
                    msg_box.addButton("Cancel", QMessageBox.ActionRole)
                    btn_ok = msg_box.addButton("Re-Run", QMessageBox.ActionRole)
                    msg_box.exec()
                    if msg_box.clickedButton()==btn_ok:
                        shutil.rmtree(path)
                    else:
                        return
            def on_registration_failed(tb, threads):
                logging.error(tb)
                oom_keywords = ['memoryerror', 'out of memory', 'cannot allocate', 'std::bad_alloc', 'killed']
                if any(kw in tb.lower() for kw in oom_keywords) and threads > 1:
                    new_threads = max(1, threads // 2)
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("SAMRI crashed (memory)")
                    msg_box.setText(
                        f"SAMRI ran out of memory with {threads} thread(s).\n"
                        f"Retry with {new_threads} thread(s)?"
                    )
                    btn_retry = msg_box.addButton("Retry", QMessageBox.ActionRole)
                    msg_box.addButton("Cancel", QMessageBox.ActionRole)
                    msg_box.exec()
                    if msg_box.clickedButton() == btn_retry:
                        samri_input['num_threads'] = new_threads
                        self.start_registration(samri_input)

            self.worker = SamriWorker(work_registration, self)
            #visualize end data
            self.worker.done.connect(
                lambda: self.Samri.visualize_results(self,logging)
            )
            self.worker.failed.connect(
                lambda tb: on_registration_failed(tb, samri_input['num_threads'])
            )
            self.worker.start()
        elif samri_input["biascorrection"]:
            self.ui.dockWidget_ephys.setEnabled(False)
            self.Samri.biascorrection(samri_input)

        #ask to start trajectory planning
        #debugging purpose
        #self.Samri.visualize_results(self)

    def initialize_trajectory_planning(self):
        dlg = FileInput(self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dlg.get_values()

            folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(data[0])))))
            csv_path = f"{folder}/results/generic_work/data_selection.csv"
            df = pd.read_csv(csv_path, index_col=0)
            matches = df.loc[df['path'] == data[0]]
            if matches.empty:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("No Transformation File found")
                msg_box.setText("No Transformation File found, please first do SAMRI Registration.")
                msg_box.addButton("OK", QMessageBox.ActionRole)
                msg_box.exec()
                self.initialize_samri()
                return
            idx = matches.index[0]
            transformPath = f"{folder}/results/generic_work/_ind_type_{idx}/s_register/output_Composite.h5"
            if not os.path.exists(transformPath):
                msg_box = QMessageBox()
                msg_box.setWindowTitle("No Transformation File found")
                msg_box.setText("No Transformation File found, please first do SAMRI Registration.")
                msg_box.addButton("OK", QMessageBox.ActionRole)
                msg_box.exec()
                self.initialize_samri()
                return

            self.overlay = BusyOverlay(self, message="Processing, please wait…")
            self.overlay.run(self.finish_trajectory_work,data, transformPath)


    def finish_trajectory_work(self, data, transformPath):
        resampled_path = f"{data[0][:-7]}_resampled{data[2]*1000:.10g}um.nii.gz"
        self.data_pre_resampled = data[0]
        if not os.path.exists(resampled_path):
            #self.LoadMRI.Resample = ResampleData(self.LoadMRI)
            ResampleData.resampling50um_trajectoryPlanning(data[0], new_spacing_mm=data[2])
        if not hasattr(self,'LoadMRI'):
            self.FileLoader = FileLoader(self)
            self.FileLoader.is_4d = False #3d file
            self.FileLoader.initialize_file(resampled_path,0,'coronal',0)
            zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
            Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0]["coronal"], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)
            self.ui.comboBox_resamplefiles.addItem(os.path.basename(resampled_path)) #add to combobox for resampling
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.data_4d_3d.setCurrentIndex(1)
        else:
            self.restart_gui(resampled_path,data_view='coronal')

        data = list(data)
        data[0] = resampled_path

        self.LoadMRI.TrajPlanning = TrajectoryPlanning(self,self.ui,data,transformPath)

        self.ui.stackedWidget_3d.setVisible(True)
        self.ui.stackedWidget_3d.setCurrentIndex(0)
        box = self.ui.page_3D
        layout = box.layout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 1)

        #self.overlay.close()

    def restart_gui(self, file_name, full_restart=True,label_file=False,data_view='coronal'):
        """
        Restart GUI if new main image is loaded.
        """
        if hasattr(self,'LoadMRI'):
            #deactivate interactor
            for image_index,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
                for view_name, vtk_widget in vtk_widget_image.items():
                    interactor = vtk_widget.GetRenderWindow().GetInteractor()
                    interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
            #delete measurement actors
            if hasattr(self,'Measurement'):
                for view_name, line_actor,line_slice_index,text_actor,_,dashed_lines,points in self.Measurement.measurement_lines:
                    renderer = self.Measurement.measurement_renderer[view_name]
                    renderer.RemoveActor(line_actor)
                    text_actor.SetVisibility(0)
                    renderer.RemoveActor(dashed_lines[1])
                    renderer.RemoveActor(dashed_lines[3])
                    renderer.RemoveActor(points[2])
                self.Measurement.measurement_lines = []
            for idx in self.LoadMRI.minimap.minimap_renderers:
                for vn in self.LoadMRI.minimap.minimap_renderers[idx]:
                    self.LoadMRI.minimap.minimap_renderers[idx][vn].RemoveAllViewProps()
                self.LoadMRI.minimap.minimap_renderers[idx] = {}
            for idx in self.LoadMRI.renderers:
                for vn in self.LoadMRI.renderers[idx]:
                    self.LoadMRI.renderers[idx][vn].RemoveAllViewProps()
                self.LoadMRI.renderers[idx] = {}

            for data_index in range(len(self.LoadMRI.vtk_widgets[0])):
                if hasattr(self.LoadMRI, f"intensity_table{data_index}"):
                    intensity_class = self.LoadMRI.intensity_table[data_index]
                    intensity_class.table.viewport().removeEventFilter(self)
            #remove cursor and minimap connections
            for key in ["scroll_0", "scroll_1", "scroll_2"]:
                try:
                    self.LoadMRI.cursor_ui[key].valueChanged.disconnect()
                except RuntimeError:
                    pass
            if not self.LoadMRI.volumes[0].is_4d: #3d
                self.ui.spinBox_x_data3d.valueChanged.disconnect()
                self.ui.spinBox_y_data3d.valueChanged.disconnect()
                self.ui.spinBox_z_data3d.valueChanged.disconnect()
                for idx in 0,1,2:
                    getattr(self.ui, f"go_down_data3d{idx}").clicked.disconnect()
                    getattr(self.ui, f"go_up_data3d{idx}").clicked.disconnect()
                    getattr(self.ui, f"go_right_data3d{idx}").clicked.disconnect()
                    getattr(self.ui, f"go_left_data3d{idx}").clicked.disconnect()
            else:    #4d
                for image_index in 0,1,2:
                    self.LoadMRI.cursor_ui[f"spin_{image_index}"].valueChanged.disconnect()
                    #self.LoadMRI.cursor_ui[f"spin_y_data{image_index}"].valueChanged.disconnect()
                    #self.LoadMRI.cursor_ui[f"spin_z_data{image_index}"].valueChanged.disconnect()
                    for idx in 0,1,2:
                        getattr(self.ui, f"go_down_data{idx}{image_index}").clicked.disconnect()
                        getattr(self.ui, f"go_up_data{idx}{image_index}").clicked.disconnect()
                        getattr(self.ui, f"go_right_data{idx}{image_index}").clicked.disconnect()
                        getattr(self.ui, f"go_left_data{idx}{image_index}").clicked.disconnect()

            #remove old renderers
            for image_index,vtk_widget_image in self.LoadMRI.vtk_widgets.items():
                for view_name, vtk_widget in vtk_widget_image.items():
                    ren_win = vtk_widget.GetRenderWindow()
                    ren_coll = ren_win.GetRenderers()

                    renderers_to_remove = [ren_coll.GetItemAsObject(i) for i in range(ren_coll.GetNumberOfItems())]

                    for old_renderer in renderers_to_remove:
                        ren_win.RemoveRenderer(old_renderer)


            # Disconnect any important signals
            if hasattr(self.LoadMRI, "minimap"):
                try:
                    zoom_notifier.factorChanged.disconnect(self.LoadMRI.minimap.create_small_rectangle)
                except RuntimeError:
                    pass

        for dock_name in "dock_paintbrush4d","dock_segmentation":
            dock = self.findChild(QDockWidget, dock_name)
            if dock:
                dock.close()
                if full_restart:
                    dock.deleteLater()

        existing_layout = QWidget.layout(self.ui.widget_pgEphys)   # call as unbound
        if existing_layout is not None:
            QWidget().setLayout(existing_layout)

        # Clear stored references
        self.LoadMRI = None

        #restart GUI
        if full_restart:
            from ui_form import Ui_MainWindow
            self.resize_bool=False
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.add_actions()
            self.show()

        QApplication.processEvents()
        self.resize_bool=True

        #self.LoadMRI = LoadMRI(self)
        image = sitk.ReadImage(file_name)
        volume = sitk.GetArrayFromImage(image)
        self.FileLoader = FileLoader(self)
        if volume.ndim==4:
            self.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")
            self.FileLoader.is_4d = True
        else:
            self.FileLoader.is_4d = False #3d file
        self.FileLoader.initialize_file(file_name,0,data_view,0,full_restart=full_restart,label_file=label_file)

        zoom_notifier.factorChanged.connect(self.LoadMRI.minimap.create_small_rectangle)
        Zoom.fit_to_window(self.LoadMRI.vtk_widgets[0][data_view], self.LoadMRI.vtk_widgets.values(), self.LoadMRI.scale_bar, self.LoadMRI.vtk_widgets,0,data_3d=True)
        return


    def quit(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    # Register the .qrc file dynamically

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "resources.rcc")
    os.chdir(os.path.dirname(__file__))

    QResource.registerResource(file_path)
    #to mix vtk and QtQuick3D
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    #dark mode
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    app.setApplicationName("IMPLAnT")
    app.setWindowIcon(QIcon(os.path.join(_base_dir, "Icons/Github/IMPLAnT_logo.png")))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

