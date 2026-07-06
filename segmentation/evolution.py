# This Python file uses the following encoding: utf-8

import numpy as np
import SimpleITK as sitk
from PySide6.QtWidgets import QStyle
from scipy import ndimage as ndi
from PySide6.QtCore import QThread, Signal, QObject, Slot
import vtk
from scipy.ndimage import median_filter

class SegmentationEvolution(QObject):
    def __init__(self,LoadMRI,SegInitialization,Threshold,button,spin_iterations,btn_resetCamera,samri=False):
        super().__init__()

        if samri:
            self.volumes = LoadMRI
            self.btn_resetCamera = btn_resetCamera
            return

        self.LoadMRI = LoadMRI
        self.volumes = LoadMRI.volumes
        self.SegInit = SegInitialization
        self.Thres = Threshold
        self.th_vol = self.LoadMRI.MW.Layers[0][self.LoadMRI.SegmentationGUI.layer_index].volume[0]
        self.actor_bubble = self.SegInit.actor_bubble.copy()
        self.button  = button
        self.spin_iterations = spin_iterations
        self.btn_resetCamera = btn_resetCamera

        self._play_icon  = button.style().standardIcon(QStyle.SP_MediaPlay)
        self._pause_icon = button.style().standardIcon(QStyle.SP_MediaPause)

        self.thread  = None
        self.worker  = None
        self.running = False

        self.last_phi   = None   # sitk.Image, signed level-set state
        self.last_speed = None
        self.last_update3d = 0

        self.evolution_actors = {}
        self.evolved_actors = {
            'coronal': [],
            'axial': [],
            'sagittal': []
        }

        # TO BE ADJUSTED
        self.BALLOON      = 3.0 #8.0 (7.5: stuck at 104599)
        self.CURVATURE    = 0.3 #0.3
        self.ADVECTION    = 1.5 #1.5

        self.MAX_ITERS    = 10000
        self.CHUNK        = 150
        self.RMS_TOL      = 1e-5
        self.total_iterations = 0
        self._3d_first    = True

        ## make selected circle invisible
        for actor_cirlce in self.SegInit.actor_selected:
            actor_cirlce[2].SetVisibility(0)


    def on_play_pause(self):
        self.MAX_ITERS    = 10000
        if self.running:
            self.button.setIcon(self._pause_icon)
            self.stop_evolution()
        else:
            self.button.setIcon(self._play_icon)
            self.start_evolution()

    def play_oneStep(self):
        self.MAX_ITERS    = self.total_iterations+self.CHUNK
        self.button.setIcon(self._play_icon)
        self.start_evolution()


    def bubbles_to_initial_levelset(self,shape_zyx, spacing_xyz, bubbles):
        sx, sy, sz = spacing_xyz
        zz, yy, xx = np.indices(shape_zyx).astype(np.float32)
        inside = np.zeros(shape_zyx, dtype=bool)
        for cz, cy, cx, r in bubbles:
            d2 = ((zz - cz)*sz)**2 + ((yy - cy)*sy)**2 + ((xx - cx)*sx)**2
            inside |= d2 <= r*r
        # signed distance: negative inside, positive outside
        dist_out = ndi.distance_transform_edt(~inside, sampling=(sz, sy, sx))
        dist_in  = ndi.distance_transform_edt( inside, sampling=(sz, sy, sx))
        phi = (dist_out - dist_in).astype(np.float32)
        phi_img = sitk.GetImageFromArray(phi)
        phi_img.SetSpacing(spacing_xyz)
        return phi_img

    def _build_speed_and_init(self):
        # dedupe (each 3D bubble stored 3× — once per view)
        unique = {}
        for view_name, _a, _c, radius, c_px, _ in self.SegInit.actor_bubble:
            unique[(c_px[0], c_px[1], c_px[2], radius)] = None

        bubbles = list(unique.keys())
        if not bubbles:
           return None, None, None, None

        shape_zyx   = self.th_vol.shape
        spacing_xyz = tuple(self.LoadMRI.volumes[0].spacing[::-1])
        sx, sy, sz  = spacing_xyz

        phi0 = self.bubbles_to_initial_levelset(shape_zyx, spacing_xyz, bubbles)

        ##only thing that changed
        th_smooth = median_filter(self.th_vol, size=3)
        speed_np = th_smooth.astype(np.float32) / 32767.0

        struct_inplane = np.zeros((1, 3, 3), dtype=bool)
        struct_inplane[0] = ndi.generate_binary_structure(2, 1)
        positive = ndi.binary_opening(speed_np > 0,structure=struct_inplane, iterations=8)
        positive = ndi.binary_closing(positive, iterations=1)

        lbl, _ = ndi.label(positive)
        keep = set()
        for cz, cy, cx, r in bubbles:
            l = int(lbl[int(cz), int(cy), int(cx)])
            if l > 0:
                keep.add(l)
        positive = np.isin(lbl, list(keep))

        speed_np = np.where(positive, speed_np, -1.0).astype(np.float32)
        speed = sitk.GetImageFromArray(speed_np)
        ## spacing of y decrease! [0]*2
        speed.SetSpacing([spacing_xyz[2],spacing_xyz[1],spacing_xyz[0]])
        phi0.SetSpacing([spacing_xyz[2],spacing_xyz[1],spacing_xyz[0]])

        return phi0, speed, bubbles, shape_zyx

    def _postprocess(self, mask_bool,min_voxels=20, min_mean_speed=0.1):
        m = ndi.binary_opening(mask_bool, iterations=3)
        m = ndi.binary_closing(m, iterations=1)
        #m = mask_bool
        lbl, n = ndi.label(m)
        if n > 1:
            # mean speed value per component
            sizes = ndi.sum(m, lbl, range(1, n + 1))
            speed = self.th_vol.astype(np.float32) / 32767.0
            mean_speed = ndi.mean(speed, lbl, range(1, n + 1))

            keep = np.where(
                (sizes >= min_voxels) & (mean_speed > min_mean_speed)
            )[0] + 1
            m = np.isin(lbl, keep)
        m = ndi.binary_fill_holes(m)

        return m.astype(bool)

    # -------- play / stop --------
    def start_evolution(self):
        self.running = True
        if self.thread is not None:
            return  # already running

        if self.last_phi is not None and self.last_speed is not None:
            phi0, speed = self.last_phi, self.last_speed
        else:
            phi0, speed, _,_ = self._build_speed_and_init() #bubbles, shape_zyx
            self.last_phi   = phi0
            self.last_speed = speed

        if phi0 is None:
            return

        params = {
            "balloon":   self.BALLOON,
            "curvature": self.CURVATURE,
            "advection": self.ADVECTION,
            "rms_tol":   self.RMS_TOL,
            "chunk":     self.CHUNK,
            "max_iters": self.MAX_ITERS,
        }

        self.thread = QThread()
        self.worker = EvolutionWorker(self,phi0, speed, params, self.total_iterations)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(lambda msg: print("Evolution error:", msg))

        # proper cleanup: wait until the thread actually exits before nulling refs
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self._after_thread_stopped)

        self.thread.start()


    def stop_evolution(self):
        if self.worker is not None:
            self.worker.abort()

    @Slot()
    def _after_thread_stopped(self):
        if self.worker is not None:
            self.worker.deleteLater()
        if self.thread is not None:
            self.thread.deleteLater()
        self.worker = None
        self.thread = None

    # -------- slots (run on GUI thread) --------
    @Slot(object)
    def on_progress(self, mask,phi,iterations):
        self.last_phi = phi
        # live preview during evolution; no post-processing yet
        self.LoadMRI.segmentation_mask = mask
        self.save_mask(mask)
        self.spin_iterations.setValue(iterations)

    @Slot(object)
    def on_finished(self, mask,phi,iterations):
        self.last_phi = phi
        self.running = False
        self.spin_iterations.setValue(iterations)
        self.total_iterations = iterations
        self.button.setIcon(self._pause_icon)
        self.LoadMRI.segmentation_mask = mask
        self.save_mask(mask,visualisation_3d=True)


    def save_mask(self,mask,visualisation_3d=False):
        mask = self._postprocess(mask)
        self.LoadMRI.segmentation_mask = mask
        if mask is None:
            return
        img = sitk.GetImageFromArray(mask.astype(np.uint8))
        img.CopyInformation(self.LoadMRI.volumes[0].oriented_ref_image)
        mask_oriented = sitk.DICOMOrient(img, "".join(self.LoadMRI.volumes[0].raw_DICOMOrient))
        mask_path = self.LoadMRI.volumes[0].file_path[:-7] + "-mask.nii.gz"
        sitk.WriteImage(mask_oriented, mask_path)
        z, y, x = self.LoadMRI.slice_indices[0].copy()
        self.visualize(np.fliplr(mask[z, :, :]), self.LoadMRI.vtk_widgets[0]["axial"], "axial")
        self.visualize(np.fliplr(mask[:, y, :]), self.LoadMRI.vtk_widgets[0]["coronal"], "coronal")
        self.visualize(np.fliplr(mask[:, :, x]), self.LoadMRI.vtk_widgets[0]["sagittal"], "sagittal")
        if visualisation_3d or (self.spin_iterations.value()-self.last_update3d)>100:
            self.visualize_3d(mask, self.LoadMRI.SegEvolution.vtkwidget_3d)
            self.last_update3d = self.spin_iterations.value()

    def update_evolution_initializtion(self):
        mask = self.LoadMRI.segmentation_mask
        z, y, x = self.LoadMRI.slice_indices[0].copy()
        self.visualize(np.fliplr(mask[z, :, :]), self.LoadMRI.vtk_widgets[0]["axial"], "axial")
        self.visualize(np.fliplr(mask[:, y, :]), self.LoadMRI.vtk_widgets[0]["coronal"], "coronal")
        self.visualize(np.fliplr(mask[:, :, x]), self.LoadMRI.vtk_widgets[0]["sagittal"], "sagittal")

    def visualize_3d(self, mask, vtk_widget):
        """Render the mask as a 3D isosurface in a QVTKRenderWindowInteractor."""
        # 1. numpy → vtkImageData
        m = np.ascontiguousarray(mask.astype(np.uint8))   # (Nz, Ny, Nx), x fastest — good
        nz, ny, nx = m.shape

        if not hasattr(self, "_3d_renderer"):
            self._build_3d_pipeline(vtk_widget)

        imp = self._3d_importer
        imp.SetDataScalarTypeToUnsignedChar()
        imp.SetNumberOfScalarComponents(1)
        imp.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        imp.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        #imp.SetDataExtentToWholeExtent()
        imp.SetDataSpacing(self.volumes[0].spacing[::-1])
        imp.SetDataOrigin(self.volumes[0].oriented_ref_image.GetOrigin())
        imp.CopyImportVoidPointer(m.tobytes(), m.nbytes)
        imp.Modified()
        imp.Update()

        # keep numpy buffer alive — VTK only holds the pointer
        self._3d_mask_buf = m

        # optional: reset camera only on the very first dataset
        if getattr(self, "_3d_first", True):
            self._3d_renderer.ResetCamera()
            self._3d_first = False
            self.btn_resetCamera.clicked.connect(lambda: self._3d_renderer.ResetCamera())

        vtk_widget.GetRenderWindow().Render()

    def _build_3d_pipeline(self, vtk_widget):
        importer = vtk.vtkImageImport()
        importer.SetDataScalarTypeToUnsignedChar()
        importer.SetNumberOfScalarComponents(1)
        mc = vtk.vtkDiscreteMarchingCubes()
        mc.SetInputConnection(importer.GetOutputPort())
        mc.GenerateValues(1, 1, 1)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(mc.GetOutputPort())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.85, 0.30, 0.30)
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(0.1, 0.1, 0.1)
        renderer.AddActor(actor)

        rw = vtk_widget.GetRenderWindow()
        rw.AddRenderer(renderer)

        # stash everything on self
        self._3d_importer = importer
        self._3d_mc       = mc
        self._3d_mapper   = mapper
        self._3d_actor    = actor
        self._3d_renderer = renderer

        mri_importer, mri_arr = self._sitk_to_vtk_image(self.volumes[0].oriented_ref_image)

        # Opacity transfer function: dark voxels invisible, brighter tissue faintly visible
        opacity_tf = vtk.vtkPiecewiseFunction()
        opacity_tf.AddPoint(0,    0.00)
        opacity_tf.AddPoint(40,   0.00)
        opacity_tf.AddPoint(80,   0.05)
        opacity_tf.AddPoint(180,  0.15)
        opacity_tf.AddPoint(255,  0.25)

        # Colour transfer function: grayscale
        color_tf = vtk.vtkColorTransferFunction()
        color_tf.AddRGBPoint(0,   0.0, 0.0, 0.0)
        color_tf.AddRGBPoint(255, 1.0, 1.0, 1.0)

        vol_prop = vtk.vtkVolumeProperty()
        vol_prop.SetColor(color_tf)
        vol_prop.SetScalarOpacity(opacity_tf)
        vol_prop.ShadeOff()                 # shading makes it look noisy; turn off for MRI
        vol_prop.SetInterpolationTypeToLinear()

        vol_mapper = vtk.vtkSmartVolumeMapper()
        vol_mapper.SetInputConnection(mri_importer.GetOutputPort())

        volume = vtk.vtkVolume()
        volume.SetMapper(vol_mapper)
        volume.SetProperty(vol_prop)

        renderer.AddVolume(volume)

        # keep refs alive so Python doesn't GC them mid-render
        self._3d_mri_importer = mri_importer
        self._3d_mri_array    = mri_arr
        self._3d_volume       = volume
        self._3d_vol_prop     = vol_prop


    def _sitk_to_vtk_image(self, sitk_img):
        """SimpleITK Image → vtkImageData (uint8, 1 component)."""
        arr = sitk.GetArrayFromImage(sitk_img)          # (z, y, x)
        # normalise to 0..255 for fast GPU sampling
        arr = arr.astype(np.float32)
        lo, hi = np.percentile(arr, (1, 99))
        arr = np.clip((arr - lo) / max(hi - lo, 1e-6), 0, 1)
        arr = (arr * 255).astype(np.uint8)
        arr = np.ascontiguousarray(arr)

        nz, ny, nx = arr.shape
        imp = vtk.vtkImageImport()
        imp.SetDataScalarTypeToUnsignedChar()
        imp.SetNumberOfScalarComponents(1)
        imp.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        imp.SetDataExtent (0, nx - 1, 0, ny - 1, 0, nz - 1)
        imp.SetDataSpacing(*sitk_img.GetSpacing())      # sitk already (x, y, z)
        imp.SetDataOrigin(*sitk_img.GetOrigin())
        imp.CopyImportVoidPointer(arr.tobytes(), arr.nbytes)
        imp.Update()
        return imp, arr


    def visualize(self, evolved_slice, vtk_widget, view_name):
        """
        Visualize only the evolved bubbles as red overlay in VTK.

        Parameters:
        - evolved_slice: 2D numpy array of the slice (negative = inside bubble)
        - vtk_widget: the corresponding VTK widget
        - view_name: string name for the view ("axial", "coronal", "sagittal")
        """
        if self._3d_first:
            for i,[_, actor,center,radius,c_px,_] in enumerate(self.SegInit.actor_bubble):
                actor.SetVisibility(0)
            for actor_cirlce in self.SegInit.actor_selected:
                actor_cirlce[2].SetVisibility(0)

        h, w = evolved_slice.shape

        # Create empty RGB image (black background)
        rgba = np.zeros((h, w, 4), dtype=np.uint8)

        # Bubble mask: negative values are inside
        #bubble_mask = evolved_slice < 0
        bubble_mask = evolved_slice.astype(bool)

        # Color bubbles red
        rgba[bubble_mask, 0] = 139 #255  # R
        rgba[bubble_mask, 1] = 0    # G
        rgba[bubble_mask, 2] = 0    # B
        rgba[bubble_mask, 3] = 180    # A

        # Convert to VTK image
        importer = vtk.vtkImageImport()
        importer.SetDataScalarTypeToUnsignedChar()
        importer.SetNumberOfScalarComponents(4)
        importer.SetWholeExtent(0, w - 1, 0, h - 1, 0, 0)
        importer.SetDataExtentToWholeExtent()
        rgba_bytes = rgba.tobytes()
        importer.CopyImportVoidPointer(rgba_bytes, len(rgba_bytes))

        # Correct spacing per view
        if view_name == "axial":      # z fixed -> (y,x)
            spacing = (self.LoadMRI.volumes[0].spacing[2], self.LoadMRI.volumes[0].spacing[1], 1.0)
        elif view_name == "coronal": # y fixed -> (z,x)
            spacing = (self.LoadMRI.volumes[0].spacing[2], self.LoadMRI.volumes[0].spacing[0], 1.0)
        elif view_name == "sagittal":# x fixed -> (y,z)
            spacing = (self.LoadMRI.volumes[0].spacing[1], self.LoadMRI.volumes[0].spacing[0], 1.0)
        importer.SetDataSpacing(spacing)
        importer.SetDataOrigin(0.0, 0.0, 0.01)   # tiny nudge to win Z-fight
        importer.Update()

        # Create actor
        renderer = self.LoadMRI.renderers[0][view_name]
        old = self.evolved_actors.get(view_name)
        if isinstance(old, vtk.vtkImageActor):
            renderer.RemoveActor(old)

        actor = vtk.vtkImageActor()
        actor.GetMapper().SetInputData(importer.GetOutput())

        # Add actor to renderer
        renderer.AddActor(actor)

        # Keep reference
        self.evolved_actors[view_name] = actor

        vtk_widget.GetRenderWindow().Render()

    def reset(self):
        # 1. stop any running worker and wait for the thread
        if self.thread is not None:
            if self.worker is not None:
                self.worker.progress.disconnect()
                self.worker.finished.disconnect()
                self.worker.abort()
            self.thread.quit()
            self.thread.wait(2000)      # give it up to 2 s to exit

        # 2. remove 2D overlay actors
        for view_name in ('axial', 'coronal', 'sagittal'):
            renderer = self.LoadMRI.renderers[0][view_name]
            old = self.evolved_actors.get(view_name)
            if isinstance(old, vtk.vtkImageActor):
                renderer.RemoveActor(old)
            self.evolved_actors[view_name] = []   # back to initial

        # 3. remove 3D isosurface + volume (if built)
        if hasattr(self, "_3d_renderer"):
            if hasattr(self, "_3d_actor"):
                self._3d_renderer.RemoveActor(self._3d_actor)
            if hasattr(self, "_3d_volume"):
                self._3d_renderer.RemoveViewProp(self._3d_volume)
            self.vtkwidget_3d.GetRenderWindow().Render() if hasattr(self, "vtkwidget_3d") else None
            # force pipeline rebuild next time
            for attr in ("_3d_renderer", "_3d_importer", "_3d_mc", "_3d_mapper",
                         "_3d_actor", "_3d_mri_importer", "_3d_mri_array",
                         "_3d_volume", "_3d_vol_prop", "_3d_mask_buf"):
                if hasattr(self, attr):
                    delattr(self, attr)
            self._3d_first = True

        # 4. clear cached evolution state so next run starts from new bubbles
        self.last_phi = None
        self.last_speed = None
        self.total_iterations = 0
        self.spin_iterations.setValue(0)

        # 5. clear the mask on LoadMRI
        if hasattr(self.LoadMRI, "segmentation_mask"):
            del self.LoadMRI.segmentation_mask

        #update to show bubbles again
        self.LoadMRI.update_slices(0,0,'coronal')


class EvolutionWorker(QObject):
    progress = Signal(object,object,object)   # emits current mask (numpy bool array)
    finished = Signal(object,object,object)   # emits final mask
    error    = Signal(str)

    def __init__(self, SegmentationEvolution, phi0, speed, params,total_iter):
        super().__init__()
        self.SegmentationEvolution = SegmentationEvolution
        self.phi0   = phi0
        self.speed  = speed
        self.params = params
        self._abort = False
        self.last_total = total_iter

    @Slot()
    def abort(self):
        self._abort = True

    @Slot()
    def run(self):
        try:
            p = self.params
            gac = sitk.GeodesicActiveContourLevelSetImageFilter()
            gac.SetPropagationScaling(p["balloon"])
            gac.SetCurvatureScaling(p["curvature"])
            gac.SetAdvectionScaling(p["advection"])
            gac.SetMaximumRMSError(p["rms_tol"])
            gac.SetNumberOfIterations(p["chunk"])

            phi = self.phi0
            total = self.last_total
            while total < p["max_iters"] and not self._abort:
                phi = gac.Execute(phi, self.speed)
                total += gac.GetElapsedIterations()
                self.mask = sitk.GetArrayFromImage(phi) < 0
                self.progress.emit(self.mask,phi,total)
                if gac.GetElapsedIterations() < p["chunk"]:
                    break  # converged

            final = sitk.GetArrayFromImage(phi) < 0
            self.finished.emit(final,phi,total)
        except Exception as e:
            self.error.emit(str(e))
