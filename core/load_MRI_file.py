# This Python file uses the following encoding: utf-8

import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QWidget
import vtk
from vtk.util import numpy_support
import numpy as np
import SimpleITK as sitk
from utils.zoom import Zoom, zoom_notifier
from utils.scale_bar import Scale
from file_handling.mri_volume import MRIVolume
from gui_utils.intensity_table import IntensityTable
from utils.contrast import Contrast

class LoadMRI(QObject):
    """
    Handles loading, managing, and displaying MRI volumes (3D and 4D).
    """
    def __init__(self, MW,parent=None):
        super().__init__(parent)
        # Core volume data
        self.MW = MW
        self.volumes: dict[int, MRIVolume] = {}
        self.slice_indices = {}
        self.slice_indices[0] = [0, 0, 0]  # z y x (for cursor +1)

        # GUI-related
        self.contrast_ui_elements = {}
        self.zoom_tf ={}
        self.zoom_tf['axial']=False
        self.zoom_tf['coronal']=False
        self.zoom_tf['sagittal']=False
        self.scale_bar = {}
        self.threshold_on = False

        # Rendering
        self.renderers = {}
        self.renderers[0] = {}
        self.is_first_slice = True

        self.intensity_table: dict[int, IntensityTable] = {}
        self.contrast: dict[int, Contrast] = {}

        self.Layers = MW.Layers



    def setup_layer(self,data_view,data_index,layer_index,visibility_at_start=True):
        """
        Initialize data structures after data is loaded.
        Emits `fileLoaded` signal once data is loaded.
        """
        if data_index not in self.renderers:
            self.renderers[data_index] = {}
        #for layer_index, layer in layers.items():
        main_layer = self.Layers[data_index][0]
        new_renderer = False
        for view_name in main_layer.view_names:
            if view_name not in self.renderers[data_index]:
                new_renderer = True
                if not self.volumes[0].is_4d:
                    self.setup_renderer(data_index,view_name)
                    self.setup_extras(data_index,view_name,data_view)
                else:
                    for img_idx in range(len(self.vtk_widgets)):
                        self.setup_renderer(img_idx,view_name)
                        self.setup_extras(data_index,view_name,data_view,img_idx=img_idx)

            #3d
            layer = self.Layers[data_index][layer_index]
            if not self.volumes[0].is_4d:
                self.renderers[data_index][view_name].AddActor(layer.actors[view_name][0])
                if not visibility_at_start:
                    layer.actors[view_name][0].SetVisibility(visibility_at_start)
                #Update renderer
                if self.is_first_slice or new_renderer:
                    self.renderers[data_index][view_name].ResetCamera()
                    self.zoom_tf[view_name]=False
            #4d
            else:
                for img_idx in range(len(self.vtk_widgets)):
                    self.renderers[img_idx][view_name].AddActor(layer.actors[view_name][img_idx])
                    if not visibility_at_start:
                        layer.actors[view_name][img_idx].SetVisibility(visibility_at_start)
                    #Update renderer
                    if self.is_first_slice or new_renderer:
                        self.renderers[img_idx][view_name].ResetCamera()
                        self.zoom_tf[view_name]=False

        if self.is_first_slice or new_renderer:
            #fit to window to make it look nice
            if self.volumes[0].is_4d:
                Zoom.fit_to_window(self.vtk_widgets[0][data_view], self.vtk_widgets.values(), self.scale_bar, self.vtk_widgets, data_index)
            else: #3d
                Zoom.fit_to_window(self.vtk_widgets[0]["coronal"], self.vtk_widgets.values(), self.scale_bar, self.vtk_widgets, data_index)
            self.is_first_slice = False

        self.render()


    def setup_renderer(self,data_index,view_name):
        vtk_widget = self.vtk_widgets[data_index][view_name]
        renderer = vtk.vtkRenderer()
        vtk_widget.GetRenderWindow().AddRenderer(renderer)
        vtk_widget.GetRenderWindow().SetMultiSamples(16)
        self.renderers[data_index][view_name] = renderer

        camera = renderer.GetActiveCamera()
        cx, cy, cz = camera.GetFocalPoint()
        pos = camera.GetPosition()
        camera.SetPosition(cx, cy, pos[2])
        ##TEST
        #transform = vtk.vtkTransform()
        #transform.Scale(-1, 1, 1)
        #camera.SetUserTransform(transform)
        ##TEST
        half_height = camera.GetParallelScale()
        width_px, height_px = renderer.GetSize()
        if height_px == 0:
            return
        half_width = half_height * width_px / height_px
        Zoom.bounds[view_name] = [cx - half_width, cx + half_width, cy - half_height, cy + half_height]


    def setup_extras(self,data_index,view_name,data_view,img_idx=None):
        if not self.volumes[0].is_4d:
            img_idx = data_index
            img_vtk = self.Layers[data_index][0].img_vtks[view_name][0]
        else:
            img_vtk = self.Layers[data_index][0].img_vtks[view_name][img_idx]
        renderer = self.renderers[img_idx][view_name]
        vtk_widget = self.vtk_widgets[img_idx][view_name]

        #Add axes to each widget
        self.add_axes(renderer, img_vtk, view_name)
        self.minimap.add_minimap(view_name,img_vtk,img_idx,vtk_widget,data_index)

        # Add scale_bar and minimap
        if self.volumes[0].is_4d and data_view!=view_name:
            pass #continue
        else:
            if not self.volumes[0].is_4d or img_idx == len(self.vtk_widgets) - 1:
                renderer = self.renderers[data_index][view_name]
                if view_name not in self.scale_bar:
                    self.scale_bar[view_name] = Scale(self)
                self.scale_bar[view_name].create_bar(renderer,view_name,length_cm=1.0)



    def update_slices(self,data_index,data_view):
        """
        Refresh all slice views (axial, coronal, sagittal) based on current slice indices.
        Handles threshold overlays and distance measurement visibility.
        """
        z, y, x = self.slice_indices[data_index].copy() if hasattr(self, 'slice_indices') else [0, 0, 0]

        if self.threshold_on == True:
            layer = self.Layers[0][self.SegmentationGUI.layer_index]
            layer.update_vtk([z,y,x])
        else:
            # only the data set that moved: [z,y,x] is slice_indices[data_index],
            # so applying it to every data set's layers would drag the other 4D
            # views along when one of them is scrolled. Each layer updates all of
            # its own image panels (timestamps) itself, see ImageLayer.update_vtk.
            for layer in self.Layers[data_index].values():
                layer.update_vtk([z,y,x])

        #measurement
        if hasattr(self.MW,'Measurement'):
            self.MW.Measurement.update_measurement_visibility([z,y,x])

        #Trajectory Planning
        if hasattr(self,'TrajPlanning'):
            self.TrajPlanning.check_points_in_slice()

        #Electrode Localization
        if hasattr(self,'ElectrodeLoc'):
            self.ElectrodeLoc.update_electrode_marker_visibility()

        #Segmentation
        if hasattr(self,'segmentation_mask'):
            self.SegEvolution.update_evolution_initializtion()
        elif hasattr(self,'SegInitialization'):
            self.SegInitialization.update_bubbles_visible()

        #Heatmap
        # actor_heatmap is filled per data set as each heatmap is built, so the
        # attribute existing says nothing about THIS data set having one — a data
        # view without a heatmap simply has nothing to refresh here.
        mrid_tags = getattr(self, 'mrid_tags', None)
        heatmap_actor = getattr(mrid_tags, 'actor_heatmap', {}).get(data_index)
        if heatmap_actor is not None and data_index in self.mrid_tags.heatmap_nii:
            raw = self.mrid_tags.heatmap_nii[data_index][z, :, :]
            slice_img = np.fliplr(raw) if self.Layers[data_index][0].flip else raw
            # Always flatten in Fortran order for VTK
            vtk_data = numpy_support.numpy_to_vtk(slice_img.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
            h, w = slice_img.shape
            spacing = (self.volumes[data_index].spacing[2], self.volumes[data_index].spacing[1], 1)
            img_vtk = vtk.vtkImageData()
            img_vtk.SetDimensions(w, h, 1)  # VTK expects width x height x depth
            img_vtk.SetSpacing(spacing)
            img_vtk.GetPointData().SetScalars(vtk_data)

            heatmap_actor.SetInputData(img_vtk)
            heatmap_actor.Modified()
            #self.vtk_widgets_heatmap['axial'].GetRenderWindow().Render()
            self.mrid_tags.add_legend(slice_img,False,data_index)


        self.render()


    def add_axes(self, renderer: vtk.vtkRenderer, img_vtk: vtk.vtkImageData, view_name:str):
        """
        Add L/R/A/P/S/I axes to the given view for orientation.
        """
        center = 0.5
        up = 0.9
        if view_name == "coronal":      # slice in XY plane
            texts = [("L", 0.95, center),
                     ("R", 0.05, center),
                     ("S", center, up),
                     ("I", center, 0.05)]

        elif view_name == "axial":  # slice in XZ plane
            texts = [("L", 0.95, center),
                     ("R", 0.05, center),
                     ("A", center, up),
                     ("P", center, 0.05)]

        elif view_name == "sagittal": # slice in YZ plane
            texts = [("P", 0.95, center),
                     ("A", 0.05, center),
                     ("S", center, up),
                     ("I", center, 0.05)]

        for text, x, y in texts:
            actor = vtk.vtkTextActor()
            actor.SetInput(text)
            prop = actor.GetTextProperty()
            if self.volumes[0].is_4d and view_name != 'axial':
                prop.SetFontSize(10)
            else:
                prop.SetFontSize(16)
            prop.SetColor(1, 1, 0)  # red text
            prop.BoldOn()
            actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
            actor.SetPosition(x, y)

            renderer.AddActor2D(actor)


    def render(self):
        for _,vtk_widget_image in self.vtk_widgets.items():
            for view_name, widget in vtk_widget_image.items():
                # A view's vtk widget can be hidden (e.g. its stacked widget
                # switched to a different page) without being removed from
                # vtk_widgets -- Rendering a widget that isn't actually
                # mapped can hang the GL driver waiting on an X11/DRI3
                # buffer swap that never arrives (confirmed via gdb: blocked
                # in vtkXOpenGLRenderWindow::MakeCurrent ->
                # loader_dri3_get_buffers -> xcb_wait_for_special_event),
                # freezing the whole GUI -- see trajectory_planning/
                # rendering.py's identical guard.
                if not widget.isVisible():
                    continue
                widget.GetRenderWindow().Render()


# ----------------------------------------------------------------------
# MainWindow-level orchestration around LoadMRI: tearing one down (whether
# to replace it with another or to just give it up), and restart_gui()
# itself. Lives here (next to the class these operate on) rather than in
# main_window.py, which just keeps thin restart_gui()/_teardown_load_mri()/
# _evict_load_mri() wrapper methods that delegate to these -- every existing
# external caller (samri/samri_main.py, file_handling/loader.py,
# file_handling/metadata.py, file_handling/resample_data.py all call
# MW.restart_gui(...)/self.restart_gui(...)) keeps working unchanged.
# ----------------------------------------------------------------------

def teardown_load_mri(mw, delete_windows):
    """
    Tears down whatever mw.LoadMRI currently holds -- VTK
    interactors/renderers, Measurement's actors, minimap, cursor/scroll
    signal connections, TrajPlanning's separate 3D window -- and clears
    mw.LoadMRI. A no-op if there's no LoadMRI yet.

    Called from restart_gui() below (which then goes on to load a
    replacement file into a possibly-rebuilt mw.ui) and from
    evict_load_mri() (nothing replaces it there) -- one implementation of
    this VTK/signal cleanup, not two.

    `delete_windows`: also deleteLater()s TrajPlanning's separate 3D window
    (trajectory_planning_3d/window.py's TrajectoryPlanning3DWindow) instead
    of merely closing/hiding it -- pass True whenever nothing downstream
    still needs it (restart_gui's full_restart, or an eviction, where
    TrajPlanning itself is being given up entirely).
    """
    if not hasattr(mw, 'LoadMRI') or mw.LoadMRI is None:
        return
    #deactivate interactor
    for image_index,vtk_widget_image in mw.LoadMRI.vtk_widgets.items():
        for view_name, vtk_widget in vtk_widget_image.items():
            interactor = vtk_widget.GetRenderWindow().GetInteractor()
            interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
    # Measurement's own actor/state cleanup is Measurement.teardown(), called
    # generically via _teardown_registered_modules() (register_module) above
    # -- its measurement_renderer is a separate overlay vtkRenderer per view,
    # already covered by the "remove old renderers" sweep below (every
    # renderer gets removed from each view's render window wholesale, this
    # overlay included), so there's nothing measurement-specific left to do
    # here.
    for idx in mw.LoadMRI.minimap.minimap_renderers:
        for vn in mw.LoadMRI.minimap.minimap_renderers[idx]:
            mw.LoadMRI.minimap.minimap_renderers[idx][vn].RemoveAllViewProps()
        mw.LoadMRI.minimap.minimap_renderers[idx] = {}
    for idx in mw.LoadMRI.renderers:
        for vn in mw.LoadMRI.renderers[idx]:
            mw.LoadMRI.renderers[idx][vn].RemoveAllViewProps()
        mw.LoadMRI.renderers[idx] = {}

    for data_index in range(len(mw.LoadMRI.vtk_widgets[0])):
        if hasattr(mw.LoadMRI, f"intensity_table{data_index}"):
            intensity_class = mw.LoadMRI.intensity_table[data_index]
            intensity_class.table.viewport().removeEventFilter(mw)
    #remove cursor and minimap connections
    for key in ["scroll_0", "scroll_1", "scroll_2"]:
        try:
            mw.LoadMRI.cursor_ui[key].valueChanged.disconnect()
        except RuntimeError:
            pass
    if not mw.LoadMRI.volumes[0].is_4d: #3d
        mw.ui.spinBox_x_data3d.valueChanged.disconnect()
        mw.ui.spinBox_y_data3d.valueChanged.disconnect()
        mw.ui.spinBox_z_data3d.valueChanged.disconnect()
        for idx in 0,1,2:
            getattr(mw.ui, f"go_down_data3d{idx}").clicked.disconnect()
            getattr(mw.ui, f"go_up_data3d{idx}").clicked.disconnect()
            getattr(mw.ui, f"go_right_data3d{idx}").clicked.disconnect()
            getattr(mw.ui, f"go_left_data3d{idx}").clicked.disconnect()
    else:    #4d
        # The widgets of all three data views exist in the .ui, but only
        # the loaded ones ever got connected (Cursor.init_widgets and
        # initialize_zoom_controls run per data view), and disconnect()
        # raises RuntimeError on a signal with no connections — same
        # reason the scroll bars above are wrapped.
        def _disconnect(signal):
            try:
                signal.disconnect()
            except RuntimeError:
                pass

        for image_index in 0,1,2:
            for axis in ('x','y','z'):
                _disconnect(mw.LoadMRI.cursor_ui[f"spin_{axis}{image_index}"].valueChanged)
            for idx in 0,1,2:
                _disconnect(getattr(mw.ui, f"go_down_data{idx}{image_index}").clicked)
                _disconnect(getattr(mw.ui, f"go_up_data{idx}{image_index}").clicked)
                _disconnect(getattr(mw.ui, f"go_right_data{idx}{image_index}").clicked)
                _disconnect(getattr(mw.ui, f"go_left_data{idx}{image_index}").clicked)

    #remove old renderers
    for image_index,vtk_widget_image in mw.LoadMRI.vtk_widgets.items():
        for view_name, vtk_widget in vtk_widget_image.items():
            ren_win = vtk_widget.GetRenderWindow()
            ren_coll = ren_win.GetRenderers()

            renderers_to_remove = [ren_coll.GetItemAsObject(i) for i in range(ren_coll.GetNumberOfItems())]

            for old_renderer in renderers_to_remove:
                ren_win.RemoveRenderer(old_renderer)

    # Disconnect any important signals
    if hasattr(mw.LoadMRI, "minimap"):
        try:
            zoom_notifier.factorChanged.disconnect(mw.LoadMRI.minimap.create_small_rectangle)
        except RuntimeError:
            pass

    # TrajectoryPlanning3DWindow (trajectory_planning_3d/window.py) sets no
    # objectName -- just a window title -- so it can't be found via
    # findChild(QDockWidget, name) the way MainWindow._close_tool_docks
    # finds its docks; go through TrajPlanning.tp3d_window directly instead
    # (None if the 3D window was never opened this session).
    tp3d_window = getattr(getattr(mw.LoadMRI, 'TrajPlanning', None), 'tp3d_window', None)
    if tp3d_window is not None:
        tp3d_window.close()
        if delete_windows:
            tp3d_window.deleteLater()

    mw.LoadMRI = None
    # Same reasoning as MainWindow._free_previous_workflow_state: dropping
    # LoadMRI here would otherwise leave a stale 'LoadMRI.TrajPlanning'
    # entry in the registry, pointing at a TrajectoryPlanningMri instance
    # that no longer exists anywhere else.
    mw._registered_modules.pop('LoadMRI.TrajPlanning', None)


def evict_load_mri(mw):
    """
    Frees mw.LoadMRI (and everything hanging off it -- VTK renderers,
    Measurement, TrajPlanning) when the user switches to a workflow that
    doesn't need it (ephys/samri/surgery), instead of keeping the whole VTK
    render pipeline for the current main image alive in memory for however
    long they're away.

    Does NOT rebuild mw.ui (unlike restart_gui) and does NOT remember
    anything to auto-reload later -- getting back to the same image works
    the same way SAMRI/ephys already do after
    MainWindow._free_previous_workflow_state: the path was already saved by
    mw._save_session_state('mri', ...) when it was loaded, so "Load Previous
    Session" reopens it (a real reload from disk, not a resume of the exact
    prior in-memory state -- see snapshot_view_state below for the one piece
    of state that IS preserved across that reload).

    No-op if there's no LoadMRI to evict, or if trajectory planning is
    active (mw.LoadMRI.TrajPlanning exists): that state is expensive to
    rebuild (a real resample step, a full 3D scene), so evicting it just
    because the user peeked at SAMRI/ephys would be a bad trade -- unlike
    the main image itself, which just needs a plain reload.
    """
    if not hasattr(mw, 'LoadMRI') or mw.LoadMRI is None:
        return
    if getattr(mw.LoadMRI, 'TrajPlanning', None) is not None:
        return
    # cached under the file's path in mw._session_view_cache -- picked back
    # up by mw.reapply_view_state() whenever this path loads again,
    # restart_gui()/FileLoader.restore_file() included.
    mw.snapshot_view_state()
    teardown_load_mri(mw, delete_windows=True)


def restart_gui(mw, file_name, full_restart=True, label_file=False, data_view='coronal'):
    """
    Restart GUI if new main image is loaded. See MainWindow.restart_gui,
    which just delegates here.
    """
    mw._teardown_registered_modules()
    teardown_load_mri(mw, delete_windows=full_restart)
    mw._close_tool_docks(full_restart)

    if full_restart:
        # only tear down widget_pgEphys's plot when mw.ui is about to be
        # rebuilt below -- otherwise this permanently kills its ViewBox
        # since the same widget_pgEphys is kept around
        existing_layout = QWidget.layout(mw.ui.widget_pgEphys)   # call as unbound
        if existing_layout is not None:
            QWidget().setLayout(existing_layout)

    #restart GUI
    if full_restart:
        # Deferred imports: these all reach back into main_window.py-adjacent
        # modules (ui_form, the split-out popup/dock Ui_* classes) that
        # aren't needed anywhere else in this file, and FileLoader below
        # would otherwise be a circular import (file_handling/loader.py
        # imports LoadMRI from this module already) -- both are only ever
        # needed once restart_gui() actually runs, well after import time.
        from ui_form import Ui_MainWindow
        from ephys.ui_dock_ephys import Ui_Dock_ephys
        from ephys.ui_tab_main_ephys import Ui_tab_ephys
        from gui_utils.ui_tab_popups_time_series import Ui_tab_15 as Ui_tab_popups_time_series
        from file_handling.ui_tab_popups_time_series_ii import Ui_tab_6 as Ui_tab_popups_time_series_ii
        from ephys.ui_tab_popups_ephys import Ui_tab as Ui_tab_popups_ephys
        from intraoperative.ui_tab_intraoperative import Ui_Form as Ui_tab_surgery
        from samri.ui_tab_samri import Ui_tab_samri

        mw.resize_bool=False
        mw.ui = Ui_MainWindow()
        mw.ui.setupUi(mw)
        mw.load_split_ui(Ui_Dock_ephys, mw.ui.dockWidget_ephys.setWidget)
        mw.load_split_ui(
            Ui_tab_popups_time_series,
            lambda w: mw.register_tab(w, "Popups for Time-Series Data", index=1),
        )
        mw.load_split_ui(
            Ui_tab_popups_time_series_ii,
            lambda w: mw.register_tab(w, "Popups for Time-Series Data II", index=2),
        )
        mw.load_split_ui(
            Ui_tab_ephys,
            lambda w: mw.register_tab(w, "Ephys", index=3),
        )
        mw.load_split_ui(
            Ui_tab_popups_ephys,
            lambda w: mw.register_tab(w, "Popups for ephys", index=4),
        )
        # tab_samri and surgery (Intraoperative tab) -- same reasoning as
        # __init__: appended last, in this order, matching their original
        # positions in form.ui's static tab order.
        mw.load_split_ui(
            Ui_tab_samri,
            lambda w: mw.register_tab(w, "SAMRI"),
        )
        mw.load_split_ui(
            Ui_tab_surgery,
            lambda w: mw.register_tab(w, "Intraoperative"),
        )
        mw.add_actions()
        mw.show()
        # setupUi() creates a brand new stackedWidget_3d_tp with none of
        # __init__'s signal connections -- reconnect this one or its height
        # cap silently reverts to the .ui's static default.
        mw.ui.stackedWidget_3d_tp.currentChanged.connect(mw._update_3d_tp_height_cap)
        mw._update_3d_tp_height_cap(mw.ui.stackedWidget_3d_tp.currentIndex())

    QApplication.processEvents()
    mw.resize_bool=True

    from file_handling.loader import FileLoader
    image = sitk.ReadImage(file_name)
    volume = sitk.GetArrayFromImage(image)
    mw.FileLoader = FileLoader(mw)
    if volume.ndim==4:
        mw.ui.groupBox_data0.setTitle(f"View: {data_view.upper()}")
        mw.FileLoader.is_4d = True
    else:
        mw.FileLoader.is_4d = False #3d file
    mw.FileLoader.initialize_file(file_name,0,data_view,0,full_restart=full_restart,label_file=label_file)
    # Every other 'mri' load path (MainWindow._finish_mri_load) adds the file
    # here too -- this one didn't, so replacing the main image via File >
    # Open never showed up in the resample dropdown until now.
    mw.ui.comboBox_resamplefiles.addItem(os.path.basename(file_name))
    mw.ui.data_4d_3d.setCurrentIndex(0 if mw.FileLoader.is_4d else 1)
    mw.ui.tabWidget.setCurrentIndex(0)

    zoom_notifier.factorChanged.connect(mw.LoadMRI.minimap.create_small_rectangle)
    Zoom.fit_to_window(mw.LoadMRI.vtk_widgets[0][data_view], mw.LoadMRI.vtk_widgets.values(), mw.LoadMRI.scale_bar, mw.LoadMRI.vtk_widgets,0,data_3d=True)
    #the widgets have a size only after the rebuilt UI has been laid out, so build the minimaps now
    QApplication.processEvents()
    mw.on_gui_resize()
    mw._notify_session_loaded('mri')