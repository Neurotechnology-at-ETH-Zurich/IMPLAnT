# This Python file uses the following encoding: utf-8
from mrid_utils import handlers, gauss_aux, warper, chmap, atlas_registry
import numpy as np
import nibabel as nib
import os
import sys
import pickle
from paths_config import _paths, save_paths
from PySide6.QtWidgets import QFileDialog
import vtk
import SimpleITK as sitk
from vtk.util import numpy_support
from PySide6 import QtWidgets
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from core.paintbrush import Paintbrush
from core.dfx_geometry_4d import Dfx4DGeometry
from file_handling.mri_volume import MRIVolume
from utils.zoom import Zoom
from gui_utils.busy_overlay import BusyOverlay


def process_in_parallel(args):
    mrid, mrid_dict, sessionpath, atlas, atlaslabelsdf, dwi_path,t2s_path,mask_path,fixed_coordinates_path, moving_coordinates_path, channel_separation, total_ch,chMap_file,channel_depths_um = args

    mrid = mrid.lower()
    savepath = os.path.join(sessionpath, 'analysed',mrid)

    # Memory-mapped loading
    fixed_coordinates = np.load(fixed_coordinates_path, mmap_mode="r")
    moving_coordinates = np.load(moving_coordinates_path, mmap_mode="r")
    if dwi_path:
        nii_dwi=nib.load(dwi_path)
        dwi=np.asanyarray(nii_dwi.dataobj)
        dwi=dwi[:,:,:,0]
    else:
        # active atlas has no DWI volume (see ATLASES[...]['has_dwi']) --
        # channel_mapper.map_channels_to_atlas skips the pyramidal-layer/
        # DWI-marker step gracefully when this is None.
        dwi=None
    nii_t2s=nib.load(t2s_path)
    t2s=np.asanyarray(nii_t2s.dataobj)
    nii_mask=nib.load(mask_path)
    mask=np.asanyarray(nii_mask.dataobj)


    fitted_points,regionNames,regionNumbers,df,barcode_r,barcode_d,CA1,dwi1Dsignal,pyrChIdx,chMap,atlasCoordinates_pkl = chmap.main(
        mrid_dict,
        mrid,
        savepath,
        sessionpath,
        atlas,
        atlaslabelsdf,
        dwi,
        t2s,
        mask,
        fixed_coordinates,
        moving_coordinates,
        channel_separation,
        total_ch,
        chMap_file,
        channel_depths_um=channel_depths_um
    )

    return fitted_points,regionNames,regionNumbers,df,barcode_r,barcode_d, mrid,CA1,dwi1Dsignal,pyrChIdx,chMap,atlasCoordinates_pkl

class ElectrodeLoc:
    """
    Class for Electrode Localisation and visualizing the found points on MRI image in 4th image.
    """
    def __init__(self,LoadMRI,MW):
        """
        Initialize the ElectrodeLoc object with a reference to LoadMRI.
        """
        self.LoadMRI = LoadMRI
        self.MW = MW
        self.savepath =  os.path.join(LoadMRI.session_path,"analysed")
        self.sessionpath = LoadMRI.session_path
        self.labelsdf = handlers.read_labels(os.path.join(self.sessionpath, "anat", "labels.txt"))
        self.electrode_actors = []


    def get_gaussian_centers(self,transformation_files):
        """
        1. Warping heatmaps, segmentation and 4D volume at first-timestamp
        2. Getting Gaussian Centers or Electrodes
        """
        for idx in range(len(self.LoadMRI.vtk_widgets[0])):
            data_view = list(self.LoadMRI.vtk_widgets[0].keys())[idx]
            self.filename = os.path.basename(self.LoadMRI.volumes[idx].file_path[:-7])
            roi_names = self.get_roinames(os.path.join(self.sessionpath, "anat", "labels.txt"))
            self.orientation = data_view

            transform_filename = transformation_files[idx]

            # Check if single transformation is provided
            if isinstance(transform_filename, str):
                transform_path = transform_filename #os.path.join(self.sessionpath, "anat", transform_filename + ".txt")
                tx = sitk.ReadTransform(transform_path)
                #not inversed transformation inverseTransform=False
                fixed_ind = transform_filename.split("-")[-1].rsplit(".", 1)[0]
            # Check if multiple transformations are provided
            elif isinstance(transform_filename, list):
                tx =  warper.create_composite_transform(transform_filename, os.path.join(self.sessionpath, "anat"))
                fixed_ind = transform_filename[-1].split("-")[-1].rsplit(".", 1)[0]
            else:
                print("No valid transformation!")

            try:
                for roi_name in roi_names:
                    heatmap_filename = ".".join((self.filename + "-" + roi_name + "-heatmap", "nii", "gz"))
                    heatmap_path = os.path.join(self.sessionpath, "analysed", roi_name,data_view,heatmap_filename)
                    if os.path.exists(heatmap_path):
                        #warps and resamples heatmaps
                        savepath = os.path.join(self.LoadMRI.session_path, 'analysed',roi_name,data_view)
                        fixed_path = warper.heatmap_warp(self.filename, roi_name, savepath, self.sessionpath, fixed_ind, tx)
                        #save gaussian centers
                        volume3d_resampled = np.asanyarray(nib.load(fixed_path).dataobj)
                        gauss_aux.run_gaussian_analysis(self.filename, savepath, roi_name, data_view, volume3d_resampled, self.labelsdf)
            except FileNotFoundError as e:
                msg = QtWidgets.QMessageBox(self.MW)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Missing resampled image")
                msg.setText(f"Gaussian analysis for the {data_view} view was skipped:\n\n{e}")
                msg.addButton("OK", QtWidgets.QMessageBox.ActionRole)
                msg.exec()
                continue


    def getCoordinates(self,on_done):
        """
        Loads a pickle file with MRID design parameters and the Gaussian centers found in self.get_gaussian_centers

        Finds best-fit to compute final  Gaussian centers and isualizes them in the warped MRI slice.

        Contact geometry (DXF bending, per tag) is defined asynchronously in
        the main GUI's "Electrode Contact Geometry" dock rather than blocking
        here (see get_atlas_points), so the rest of this method runs inside
        the on_done callback that dock hands back once every tag has
        committed geometry; on_done(None) is passed through unchanged if the
        file-selection dialog was cancelled.
        """
        roi_names = self.get_roinames(os.path.join(self.sessionpath, "anat", "labels.txt"))

        def _continue(result):
            if result is None:
                on_done(None)
                return
            pklfile_path,atlas,atlaslabelsdf,dwi_path,t2s_path,mask_path,moving_coordinates_path, fixed_coordinates_path,channel_separation,total_ch,chMap_file,channel_depths_um = result

            # buttons_gui4D closed its own overlay before this, to keep the
            # geometry dock clickable -- raise a fresh one now that the
            # (blocking) localisation work actually starts
            overlay = BusyOverlay(self.MW, message="Localising Electrodes, please wait…")
            overlay.raise_()
            overlay.show()
            overlay.repaint()
            QtWidgets.QApplication.processEvents()

            with open(pklfile_path, 'rb') as f:
                mrid_dict = pickle.load(f)

            #totalregionNumbers = []
            totalmrid = []
            totaldf = []
            totalbarcode_d = []
            totalbarcode_r = []
            totalfitted_points = []
            totalCA1 =  []
            totaldwi1Dsignal = []
            totalregionNames= []
            totalpyrChIdx= []
            totalchMap = []
            totalatlasCoordinates_pkl = []


            #over all tags -> "Pre-defined" gives a per-tag total_ch list
            #(equal-spacing path) and no channel_depths_um; "User-defined"
            #gives committed DXF-bent depths and no total_ch (chmap.main
            #only falls back to channel_separation/total_ch when
            #channel_depths_um is None)
            args_list = [
                (mrid, mrid_dict, self.sessionpath, atlas, atlaslabelsdf,
                 dwi_path,t2s_path,mask_path,fixed_coordinates_path, moving_coordinates_path,
                 channel_separation, total_ch[i] if total_ch is not None else None,chMap_file,
                 channel_depths_um.get(mrid) if channel_depths_um else None)
                for i, mrid in enumerate(roi_names)
            ]


            with ProcessPoolExecutor() as executor:
                futures = [executor.submit(process_in_parallel, args) for args in args_list]

                for future in as_completed(futures):
                    fitted_points,regionNames,regionNumbers,df,barcode_r,barcode_d,mrid,CA1,dwi1Dsignal,pyrChIdx,chMap,atlasCoordinates_pkl = future.result()
                    totalfitted_points.append(fitted_points)
                    totaldf.append(df)
                    totalbarcode_r.append(barcode_r)
                    totalbarcode_d.append(barcode_d)
                    totalmrid.append(mrid)
                    totalCA1.append(CA1)
                    totaldwi1Dsignal.append(dwi1Dsignal)
                    totalregionNames.append(regionNames)
                    totalpyrChIdx.append(pyrChIdx)
                    totalchMap.append(chMap)
                    totalatlasCoordinates_pkl.append(atlasCoordinates_pkl)


            overlay.close()
            on_done((roi_names,totaldf,totalbarcode_r,totalbarcode_d,totalmrid,totalCA1,totaldwi1Dsignal,totalregionNames,totalpyrChIdx,totalfitted_points,totalchMap,totalatlasCoordinates_pkl))

        self.get_atlas_points(roi_names, _continue)

    def get_roinames(self,filename):
        """
        Read ROI names from a label file.
        """
        labels = []
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue
                # Split by tab or spaces
                parts = line.split()
                # The last column is the quoted label name
                if len(parts) >= 8:
                    label = parts[-1].strip('"')
                    labels.append(label)
        labels.pop(0)

        roi_names = []
        pure_labels = [l.rstrip("0123456789") for l in labels]

        for i, label in enumerate(labels):
            if label.endswith("1"):
                roi_names.append((pure_labels[i]))

        return roi_names



    def add_point(self,fitted_points):
        """
        Add point of found electrode Gaussian center to 4D MRI slice.
        """
        for data_index in range(len(self.LoadMRI.vtk_widgets[0])):
            self.show_warped_volume(data_index,fitted_points)
            # redraw after every view's swap, not just once at the end: each
            # step (layer cleanup, zoom fit, etc.) touches renderers/actors,
            # so re-running this after each one is what actually keeps the
            # markers on screen instead of only ever drawing them once
            self.update_electrode_markers(fitted_points)

        self.update_electrode_markers(fitted_points)

    @staticmethod
    def _map_fitted_point(point, source_img, target_img):
        """
        fitted_points are (x,y,z) indices into source_img (the warped file as
        SimpleITK stores it - sitk index order, not array order). When a
        view's display image has been re-oriented (sagittal -> ASR, see
        show_warped_volume) target_img's array axes are permuted/flipped
        relative to source_img, so map through physical space to keep the
        point on the same anatomical location instead of the same indices.
        """
        if target_img is source_img:
            return point
        phys = source_img.TransformContinuousIndexToPhysicalPoint(
            (float(point[0]), float(point[1]), float(point[2]))
        )
        return target_img.TransformPhysicalPointToContinuousIndex(phys)

    # fitted centers are sub-voxel Gaussian fits, not exact voxel hits, so a
    # point stays visible for slices within this many voxels of its own z
    Z_VISIBILITY_TOLERANCE = 1

    def update_electrode_markers(self,fitted_points):
        """
        Draw a sphere at every fitted electrode point on top of the warped
        volume. Unlike show_warped_volume (a one-time swap, guarded by
        warped_swapped), this redraws on every call so switching tags
        replaces the markers instead of only ever showing the first tag's.
        """
        lm = self.LoadMRI
        views = list(lm.vtk_widgets[0].keys())
        warped_swapped = getattr(self,'warped_swapped', set())

        for actor, image_index, data_view, idx, point_z in self.electrode_actors:
            renderer = lm.renderers.get(image_index, {}).get(data_view)
            if renderer is not None:
                renderer.RemoveActor(actor)
        self.electrode_actors.clear()

        touched_widgets = set()
        for idx, data_view in enumerate(views):
            # only views actually holding the warped volume have fitted_points'
            # index space; a view whose warped file was missing still holds
            # the original (unwarped) volume and would place markers wrongly
            if idx not in warped_swapped or idx >= len(lm.volumes):
                continue

            volume = lm.volumes[idx]
            nz, ny, nx = volume.slices[0].shape
            spacing = volume.spacing  # zyx

            for image_index in volume.slices:
                renderer = lm.renderers.get(image_index, {}).get(data_view)
                if renderer is None:
                    continue

                for point in fitted_points:
                    # fitted_points are indices into volume.raw_ref_image; the
                    # sagittal panel's array has been re-oriented to ASR (see
                    # show_warped_volume), so map through physical space to
                    # land on the same anatomical location in either case
                    x, y, z = self._map_fitted_point(point, volume.raw_ref_image, volume.oriented_ref_image)
                    # world position accounts for fliplr: x axis is flipped in
                    # the axial-style layout every is_4d view uses (same
                    # convention as cursor.py/paintbrush.py)
                    world_x = (nx - 1 - x) * spacing[2]
                    world_y = y * spacing[1]

                    sphere = vtk.vtkSphereSource()
                    sphere.SetCenter(world_x, world_y, 1)
                    sphere.SetRadius(0.3)

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputConnection(sphere.GetOutputPort())

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetColor(1, 0, 0)  # red

                    renderer.AddActor(actor)
                    self.electrode_actors.append((actor, image_index, data_view, idx, z))

                touched_widgets.add((image_index, data_view))

        self.update_electrode_marker_visibility()

        for image_index, data_view in touched_widgets:
            lm.vtk_widgets[image_index][data_view].GetRenderWindow().Render()

    def update_electrode_marker_visibility(self):
        """
        Always-visible: electrode contacts along a shank are typically spread
        across a wide z range (tens to hundreds of voxels), and the cursor
        only centers on the first point, so gating on "is this the current
        slice" (as trajectory_planning.rendering.check_points_in_slice does)
        left nearly every other marker hidden. Kept as a hook: still called
        from LoadMRI.update_slices whenever the slice changes.
        """
        for actor, image_index, data_view, idx, point_z in self.electrode_actors:
            actor.SetVisibility(True)


    def visualize_4Dwarpedslice(self, img_slice,spacing,data_index,data_view):
        """
            Visualize a single slice of the first timestamp to then add the found electrode locations.

            Parameters
            ----------
            img_slice : ndarray
                2D numpy array representing the heatmap slice to display.
            reset_camera : bool
                Whether to reset the camera to focus on the heatmap area.
        """
        # add to vtkwidgets for rendering and zooming
        vtk_widget = self.LoadMRI.vtk_widgets[3][data_view]
        vtk_data = numpy_support.numpy_to_vtk(img_slice.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        h, w = img_slice.shape
        spacing = (spacing[2], spacing[1], 1)

        #renderer,img_vtk = self.open_mainimage(vtk_widget,vtk_data, spacing,w,h)
        img_vtk = vtk.vtkImageData()
        img_vtk.SetDimensions(w, h, 1)  # VTK expects width x height x depth
        img_vtk.SetSpacing(spacing)
        img_vtk.GetPointData().SetScalars(vtk_data)

        #create new renderer
        renderer = self.LoadMRI.renderers[0][data_view]
        #remove original image
        renderer.RemoveActor(self.MW.Layers[data_index][0].actors[data_view][0])
        #renderer.RemoveActor(self.LoadMRI.actors[0][data_view])

        nonzero_y, nonzero_x = np.nonzero(img_slice)
        spacing_x, spacing_y = spacing[1], spacing[0]  # careful: VTK x=cols, y=rows
        if len(nonzero_x) == 0 or len(nonzero_y) == 0:
            if hasattr(self.MW, 'Paintbrush'):
                ny, nx = np.nonzero(self.MW.Paintbrush.label_volume[self.LoadMRI.slice_indices[0],:,:])
                if len(nx) > 0 and len(ny) > 0:
                    x_min, x_max = nx.min(), nx.max()
                    y_min, y_max = ny.min(), ny.max()
                else:
                    x_min, x_max = 0, w - 1
                    y_min, y_max = 0, h - 1
            else:
                x_min, x_max = 0, w - 1
                y_min, y_max = 0, h - 1

            # Convert pixel coordinates to world coordinates
            self.center_x = (x_min + x_max) / 2 * spacing_x
            self.center_y = (y_min + y_max) / 2 * spacing_y
            self.width = (x_max - x_min) * spacing_x
            self.height = (y_max - y_min) * spacing_y

        else:
            # Get pixel bounds
            x_min, x_max = nonzero_x.min()-1, nonzero_x.max()+1
            y_min, y_max = nonzero_y.min()-1, nonzero_y.max()+1

            # Convert pixel coordinates to world coordinates
            self.center_x = (x_min + x_max) / 2 * spacing_x
            self.center_y = (y_min + y_max) / 2 * spacing_y
            self.width = (x_max - x_min) * spacing_x
            self.height = (y_max - y_min) * spacing_y

        camera_base = self.LoadMRI.renderers[0][data_view].GetActiveCamera()
        fp = camera_base.GetFocalPoint()
        pos = camera_base.GetPosition()

        camera = renderer.GetActiveCamera()
        camera.SetFocalPoint(self.center_x, self.center_y, fp[2])
        camera.SetPosition(self.center_x, self.center_y, pos[2])  # small offset in z
        camera.ParallelProjectionOn()
        camera.SetParallelScale(max(self.width, self.height)/2)

        # Add image to actor to then be added to renderer
        actor = vtk.vtkImageActor()
        scalar = img_vtk.GetScalarRange()
        actor.GetProperty().SetColorWindow(scalar[1])
        actor.GetProperty().SetColorLevel(scalar[1]/2)

        actor.SetInputData(img_vtk)
        actor.Modified()
        actor.GetProperty().SetInterpolationTypeToNearest() #Linear()
        actor.GetProperty().SetOpacity(1)

        vmin, vmax = np.percentile(vtk_data, [0,100])
        lut = vtk.vtkLookupTable()
        lut.SetTableRange(vmin, vmax)
        lut.SetValueRange(0.0, 1.0)
        lut.SetSaturationRange(0.0, 0.0)
        lut.Build()
        contrast_class = self.LoadMRI.contrast[data_index]
        contrast_class.lut_vtk[3]=lut

        # make low values (blue end) transparent
        # now build alpha: all zero voxels → alpha = 0
        prop = actor.GetProperty()
        prop.SetLookupTable(lut)
        prop.UseLookupTableScalarRangeOn()

        renderer.AddActor(actor)

        self.LoadMRI.heatmap = True
        self.actor_heatmap = actor

        vtk_widget.GetRenderWindow().Render()


    def show_warped_volume(self,data_index=None,fitted_points=None):
        """
        Make the warped volume the main volume of a data view, in place.

        The image on screen after the localisation comes from the warped file
        (mrid_utils.warper: first timestamp resampled into the anatomical grid),
        while volumes[data_index] is still the 4D acquisition — that mismatch is
        why the crosshair, the scrollbar, the spinboxes and the intensity readout
        do not fit the picture. This swaps the volume of the data view and re-runs
        only the parts of the load that depend on its geometry, so everything stays
        on the same page and in the same widget: no restart_gui, no layout change.

        The warped volume is wrapped as a 4D MRIVolume (is_4d=True, one view name,
        the same 3D volume in all three timestamp slots) so every `is_4d` branch in
        Cursor, update_slices and CustomInteractorStyle keeps taking the path it
        takes now - which always slices along the array's first axis, so every
        panel would show an axial-style plane. The array is used exactly as the
        file stores it, except for the sagittal panel, which is re-oriented to
        ASR first (same trick as MRIVolume.from_file for real 4D data) so that
        same first-axis slice lands on the sagittal plane instead. Because the
        fitted points are indices into the un-reoriented file, _map_fitted_point
        carries them into the re-oriented index space through physical space.

        data_index : one data view, or None for every loaded one (up to three).
        fitted_points : optional, only used with a single data_index — puts the
            cursor on the first electrode so its slice is the one shown.
        Each view is swapped once; later calls (a tag switch) are no-ops.
        """
        lm = self.LoadMRI
        if not hasattr(self,'warped_swapped'):
            self.warped_swapped = set()      # data views already swapped

        views = list(lm.vtk_widgets[0].keys())
        targets = range(len(views)) if data_index is None else [data_index]

        for idx in targets:
            if idx in self.warped_swapped or idx >= len(views):
                continue
            data_view = views[idx]
            old = lm.volumes[idx]

            filename = old.file_path[0:old.file_path.find('.')]
            filename_4d_warped = ".".join((filename + "-resampled-warped", "nii", "gz"))
            path = os.path.join(self.savepath, filename_4d_warped)
            if not os.path.exists(path):
                print(f"No warped volume for view {data_view} at {path}", flush=True)
                continue

            img = sitk.ReadImage(path)
            # is_4d forces every panel through the same z-fixed (axial-style)
            # slicing (image_layer.py setup_vtk/update_vtk), so the "sagittal"
            # panel would otherwise show an axial slice too. Re-orienting to
            # ASR first (same trick as MRIVolume.from_file for real 4D data)
            # makes that same z-fixed slice land on the sagittal plane instead.
            img_display = sitk.DICOMOrient(img, 'ASR') if data_view == 'sagittal' else img
            vol = sitk.GetArrayFromImage(img_display)
            if vol.ndim != 3:
                print(f"Warped volume for view {data_view} is not 3D", flush=True)
                continue

            lm.volumes[idx] = MRIVolume(
                file_path=path,
                slices={0: vol, 1: vol, 2: vol},
                DICOMOrient=old.DICOMOrient,
                raw_DICOMOrient=old.raw_DICOMOrient,
                view_names=[data_view],
                spacing=img_display.GetSpacing()[::-1],
                oriented_ref_image=img_display,
                raw_ref_image=img,
                is_4d=True,
                timestamp4D=old.timestamp4D,
            )
            self.warped_swapped.add(idx)

            # the warped volume is one static result duplicated into all three
            # timestamp slots (see docstring) - there is no real 4D time axis
            # left, so the timestamp controls have nothing to switch between
            for i in range(3):
                getattr(self.MW.ui, f"displaytimestamp_data{idx}{i}").setEnabled(False)
                getattr(self.MW.ui, f"changetimestamp_data{idx}{i}").setEnabled(False)

            # cursor: the first electrode when the points are known, else the middle
            nz, ny, nx = vol.shape
            if fitted_points is not None and len(fitted_points) and data_index is not None:
                p = self._map_fitted_point(fitted_points[0], img, img_display)
                lm.slice_indices[idx] = [
                    int(np.clip(round(p[2]), 0, nz - 1)),
                    int(np.clip(round(p[1]), 0, ny - 1)),
                    int(np.clip(round(p[0]), 0, nx - 1)),
                ]
            else:
                lm.slice_indices[idx] = [nz // 2, ny // 2, nx // 2]

            # the layer's vtkImageData was sized for the old shape, so its pipeline
            # has to be built again; the actors in the renderers are replaced with
            # the new ones (same LUTs, so contrast stays wired)
            layer = self.MW.Layers[idx][0]
            for image_index, actor in list(layer.actors[data_view].items()):
                renderer = lm.renderers.get(image_index, {}).get(data_view)
                if renderer is not None:
                    renderer.RemoveActor(actor)
            layer.volume = lm.volumes[idx].slices
            layer.spacing = lm.volumes[idx].spacing
            for image_index, v in layer.volume.items():
                layer.setup_vtk(lm.slice_indices[idx], image_index, v, data_view)
                renderer = lm.renderers.get(image_index, {}).get(data_view)
                if renderer is not None:
                    renderer.AddActor(layer.actors[data_view][image_index])

            # the warped result is the only thing meant to be shown from here -
            # the anat/segmentation paint layer (Paintbrush.start_paintbrush)
            # and any other overlay for this view are done their job earlier in
            # the pipeline and were never deleted; left in place they are still
            # sized to the pre-warp volume and update_slices drives them with
            # the same (now much larger) z, going out of bounds
            for other_index, other_layer in list(self.MW.Layers[idx].items()):
                if other_index == 0:
                    continue
                for view_name, actors_by_image in list(other_layer.actors.items()):
                    for image_index, actor in list(actors_by_image.items()):
                        renderer = lm.renderers.get(image_index, {}).get(view_name)
                        if renderer is not None:
                            renderer.RemoveActor(actor)
                del self.MW.Layers[idx][other_index]

            # same reason: the heatmap actor (mrid_tags.start_heatmap) is a
            # bare vtkImageActor outside the Layers system with its own
            # z range, still refreshed by update_slices - delete it outright
            # instead of leaving it to go out of bounds against the new volume
            mrid_tags = getattr(lm, 'mrid_tags', None)
            if mrid_tags is not None:
                heatmap_actor = mrid_tags.actor_heatmap.pop(idx, None)
                if heatmap_actor is not None:
                    renderer = lm.renderers.get(3, {}).get(data_view)
                    if renderer is not None:
                        renderer.RemoveActor(heatmap_actor)
                mrid_tags.heatmap_nii.pop(idx, None)

            # the ranges that were sized from the old volume
            lm.cursor_ui[f"spin_x{idx}"].setMaximum(nx)
            lm.cursor_ui[f"spin_y{idx}"].setMaximum(ny)
            lm.cursor_ui[f"spin_z{idx}"].setMaximum(nz)
            scroll = lm.cursor_ui.get(f"scroll_{idx}")
            if scroll is not None:
                scroll.blockSignals(True)
                scroll.setRange(0, nz - 1)
                scroll.setValue(lm.slice_indices[idx][0])
                scroll.blockSignals(False)
            if idx in lm.intensity_table and lm.intensity_table[idx].intensity_volumes:
                lm.intensity_table[idx].intensity_volumes[0] = vol

            # window/level: percentiles and slider maxima come from the volume
            contrast = lm.contrast.get(idx)
            if contrast is not None:
                for image_index in layer.volume:
                    contrast.recompute_luttable(image_index, idx)

            self.MW.Cursor.update_cursor_display(idx)
            self.MW.Cursor.update_cursor_lines(idx)
            lm.update_slices(idx, data_view)
            Zoom.fit_to_window(lm.vtk_widgets[0][data_view], lm.vtk_widgets.values(),
                               lm.scale_bar, lm.vtk_widgets, idx)


    def get_atlas_points(self,roi_names,on_done):
        """
        Pop-up asking for the pkl/coordinate files and the contact-geometry
        mode (radio button: Pre-defined equal spacing, or User-defined DXF
        bending). "Pre-defined" hands its values straight to on_done. For
        "User-defined" the actual DXF-bending panel is no longer crammed
        into this popup (that caused a sizing mismatch between the two
        stacked pages, leaving an empty gap) -- it's instead the "Electrode
        Contact Geometry" dock in the main GUI, same non-modal pattern as
        trajectory planning's Shank Geometry panel. on_done is called with
        the assembled result tuple once ready, or None if the dialog was
        cancelled.
        """
        dlg = ChannelVariablesInput(self.MW,roi_names)
        if dlg.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            on_done(None)
            return

        pklfile, mode, channel_separation, total_ch, moving_coordinates_path, fixed_coordinates_path, chMap_file = dlg.get_values()
        self.atlas_path=os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        nii_atlas=nib.load(self.atlas_path)
        atlas=np.asanyarray(nii_atlas.dataobj)

        labels_path=os.path.join(_paths['atlas_folder'], _paths['atlas_labels'])
        active_atlas = atlas_registry.get_active_atlas(_paths)
        if active_atlas['label_format'] == 'whs_legacy':
            atlaslabelsdf=handlers.read_whs_labels(labels_path)
        else:
            itk_labels = handlers.read_itk_snap_labels(labels_path)
            atlaslabelsdf = itk_labels.rename(
                columns={'IDX': 'Labels', 'LABEL': 'Anatomical Regions'}
            )[['Labels', 'Anatomical Regions']]

        # Not every atlas has a DWI volume (see ATLASES[...]['has_dwi']) --
        # None here, rather than a path to a nonexistent file, so downstream
        # consumers (channel_mapper.map_channels_to_atlas) can skip the
        # DWI-marker step gracefully.
        dwi_path=os.path.join(_paths['atlas_folder'], _paths['atlas_dwi']) if _paths.get('atlas_dwi') else None
        t2s_path=os.path.join(_paths['atlas_folder'], _paths['atlas_template'])
        mask_path=os.path.join(_paths['atlas_folder'], _paths['atlas_mask'])

        if mode == "uniform":
            on_done((pklfile,atlas,atlaslabelsdf,dwi_path,t2s_path,mask_path,
                      moving_coordinates_path, fixed_coordinates_path,channel_separation, total_ch,chMap_file,None))
            return

        self._show_geometry_page(roi_names, pklfile,atlas,atlaslabelsdf,dwi_path,t2s_path,mask_path,
                                  moving_coordinates_path, fixed_coordinates_path,chMap_file, on_done)

    def _show_geometry_page(self, roi_names, pklfile,atlas,atlaslabelsdf,dwi_path,t2s_path,mask_path,
                             moving_coordinates_path, fixed_coordinates_path,chMap_file, on_done):
        """Reparents the real Shank Geometry widget (page_24, inside
        stackedWidget_dfx/page_3D -- the same widget trajectory planning
        uses for its own DXF-bending step) into data_4d_3d -- the top-level
        stack that switches the whole central view between 3D mode and 4D
        mode (main_window.py's restart_gui/is_4d switch) -- instead of
        building a separate copy of that panel: 4D mode has no pre-built
        spare page like 3D mode's page_3D to nest into, and stackedWidget_4D
        lives inside the Paintbrush dock, which is already closed by this
        point in the workflow, so stackedWidget_dfx itself is pulled out of
        page_3D and swapped in one level up instead. Dfx4DGeometry rewires
        its buttons to a tag-based flow for the duration; DfxGeometry.
        reclaim_dfx_widget (trajectory_planning/dfx_geometry.py) restores
        trajectory planning's own wiring once it's handed back below."""
        stacked = self.MW.ui.data_4d_3d
        origin_index = stacked.currentIndex()

        ui = self.MW.ui
        stacked_dfx = ui.stackedWidget_dfx
        ui.gridLayout_106.removeWidget(stacked_dfx)

        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        info = QtWidgets.QLabel(
            "Import each tag's contact geometry from its DXF drawing "
            "(Shank Geometry / DXF bending). Once every tag below has "
            "committed geometry, click Continue.")
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addWidget(stacked_dfx)

        stacked.addWidget(container)
        stacked.setCurrentWidget(container)

        dfx4d = Dfx4DGeometry(ui, roi_names)
        ui.pushButton_dfx_ok.setText("Continue")
        # pushButton_dfx_ok may already be wired to trajectory planning's
        # hide_dfx_panel (if TrajPlanning was set up earlier this session) --
        # blind-disconnect before taking it over, same pattern DfxGeometry.
        # _connect_dfx_signals uses, so it doesn't fire alongside _on_continue.
        try:
            ui.pushButton_dfx_ok.clicked.disconnect()
        except (TypeError, RuntimeError):
            pass

        def _restore_dfx_widget():
            layout.removeWidget(stacked_dfx)
            ui.gridLayout_106.addWidget(stacked_dfx, 1, 0, 1, 3)
            stacked_dfx.setCurrentIndex(0)
            ui.pushButton_dfx_ok.setText("OK")
            try:
                ui.pushButton_dfx_ok.clicked.disconnect()
            except (TypeError, RuntimeError):
                pass
            traj = getattr(self.LoadMRI, 'TrajPlanning', None)
            if traj is not None:
                traj.reclaim_dfx_widget()
            stacked.setCurrentIndex(origin_index)
            stacked.removeWidget(container)
            container.deleteLater()

        def _on_continue():
            depths = dfx4d.get_depths_um()
            missing = [roi for roi, d in depths.items() if d is None]
            if missing:
                QtWidgets.QMessageBox.warning(
                    self.MW, "Missing geometry",
                    "Please run the bending model and commit geometry for "
                    "every tag before continuing. Missing: " + ", ".join(missing))
                return
            _restore_dfx_widget()
            on_done((pklfile,atlas,atlaslabelsdf,dwi_path,t2s_path,mask_path,
                      moving_coordinates_path, fixed_coordinates_path,None,None,chMap_file, depths))

        ui.pushButton_dfx_ok.clicked.connect(_on_continue)


class ChannelVariablesInput(QtWidgets.QDialog):
    """
    Dialog to select the mrid_library pkl, the fixed/moving atlas-coordinate
    npy files, a chMap file (optional), and the contact-geometry mode. For
    "User-defined" the actual DXF-bending panel is no longer shown inside
    this popup -- it used to sit in a QStackedWidget page here, taller than
    the "Pre-defined" page and leaving an empty gap whenever that one was
    selected. It now happens afterwards as trajectory planning's own Shank
    Geometry widget (stackedWidget_dfx, normally inside page_3D), reparented
    into data_4d_3d for the duration (see ElectrodeLoc._show_geometry_page /
    core/dfx_geometry_4d.py).
    """
    def __init__(self, MW, roi_names,parent=None):
        """
        Initialize the input dialog UI and connect signals.
        """
        super().__init__(parent)
        self.setWindowTitle("Input Values")
        self.setModal(True)
        self.resize(500, 500)
        self.MW = MW
        self.roi_names = roi_names
        gui_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QPlainTextEdit("Please enter all variables asked for electrode channels.")
        text.setReadOnly(True)
        #text.setFixedSize(400, 100)
        main_layout.addWidget(text)

        file_layout = QtWidgets.QHBoxLayout()
        self.file_line_pkl = QtWidgets.QTextEdit()

        self.file_name_pkl = _paths.get('mrid_library', os.path.join(gui_dir, 'mrid_library.pkl'))
        if os.path.exists(self.file_name_pkl):
            self.file_line_pkl.setText(f"File found: {self.file_name_pkl} \n Please select another pkl file if requested")
        else:
            self.file_line_pkl.setText("No mrid_library.pkl found. Please browse to select the file.")
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_pkl)
        save_button = QtWidgets.QPushButton("Save")
        save_button.setToolTip("Remember this path in paths_config.json, so it's the default next time.")
        save_button.clicked.connect(self.save_mrid_library_path)
        file_layout.addWidget(self.file_line_pkl)
        file_layout.addWidget(browse_button)
        file_layout.addWidget(save_button)
        main_layout.addLayout(file_layout)

        main_layout.addWidget(QtWidgets.QLabel("Contact geometry:"))
        self.radio_uniform = QtWidgets.QRadioButton(
            "Pre-defined - equal spacing between electrodes")
        self.radio_custom = QtWidgets.QRadioButton(
            "User-defined - import each tag's geometry (Shank Geometry / DXF bending)")
        self.radio_uniform.setChecked(True)
        main_layout.addWidget(self.radio_uniform)
        main_layout.addWidget(self.radio_custom)

        # Only "Pre-defined" values matter here -- "User-defined" geometry
        # itself is edited afterwards in the main GUI's dock. Left always
        # visible but disabled/enabled with the radio choice (rather than
        # hidden), so the dialog never resizes/jumps as you switch modes.
        self.uniform_page = QtWidgets.QWidget()
        uniform_layout = QtWidgets.QVBoxLayout(self.uniform_page)
        self.channel_separation = QtWidgets.QSpinBox()
        self.channel_separation.setRange(1, 200)
        self.channel_separation.setValue(50)
        uniform_layout.addWidget(QtWidgets.QLabel("Channel Separation [um]"))
        uniform_layout.addWidget(self.channel_separation)

        self.total_channels = {}
        group_box = QtWidgets.QGroupBox("Total Channels [per tag]")
        group_layout = QtWidgets.QVBoxLayout(group_box)
        for roi in self.roi_names:
            self.total_channels[roi] = QtWidgets.QSpinBox()
            self.total_channels[roi].setRange(1, 200)
            self.total_channels[roi].setValue(64)
            group_layout.addWidget(QtWidgets.QLabel(f"{roi.capitalize()}"))
            group_layout.addWidget(self.total_channels[roi])
        uniform_layout.addWidget(group_box)
        main_layout.addWidget(self.uniform_page)

        def _on_geometry_mode_changed():
            self.uniform_page.setEnabled(self.radio_uniform.isChecked())
        self.radio_uniform.toggled.connect(_on_geometry_mode_changed)
        self.radio_custom.toggled.connect(_on_geometry_mode_changed)
        _on_geometry_mode_changed()

        # upload matrices
        file_layout = QtWidgets.QHBoxLayout()
        self.file_line_fixed = QtWidgets.QTextEdit()
        if os.path.exists(os.path.join(self.MW.LoadMRI.session_path, 'registration','fixed_img-indeces.npy')):
            self.file_name_fixed = os.path.join(self.MW.LoadMRI.session_path, 'registration','fixed_img-indeces.npy')
            self.file_line_fixed.setText(f"File for FIXED coordinates found: {self.file_name_fixed} \n Select another file if requested")
        else:
            self.file_name_fixed = None
            self.file_line_fixed.setText("Please select the fixed coordinates. No such file found.")
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_fix)
        file_layout.addWidget(self.file_line_fixed)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)

        file_layout = QtWidgets.QHBoxLayout()
        self.file_line_mov = QtWidgets.QTextEdit()
        if os.path.exists(os.path.join(self.MW.LoadMRI.session_path, 'registration','moving_img_resampled25um-indeces.npy')):
            self.file_name_moving = os.path.join(self.MW.LoadMRI.session_path, 'registration','moving_img_resampled25um-indeces.npy')
            self.file_line_mov.setText(f"File for MOVING coordinates found: {self.file_name_moving} \n Select another file if requested")
        else:
            self.file_name_moving = None
            self.file_line_mov.setText("Please select the moving coordinates. No such file found.")
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_mov)
        file_layout.addWidget(self.file_line_mov)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)

        file_layout = QtWidgets.QHBoxLayout()
        self.file_chMap = None
        self.chMap_file_line = QtWidgets.QTextEdit()
        self.chMap_file_line.setText("If exists, please upload chMap file. \n Otherwise channels are named sequentially, starting at 1.")
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_chMap)
        file_layout.addWidget(self.chMap_file_line)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)

        #buttons
        button_layout = QtWidgets.QHBoxLayout()
        # Add a small text label
        label = QtWidgets.QLabel("Press OK if data is correct")
        label.setStyleSheet("font-size: 10pt;")  # Optional: make it smaller
        button_layout.addWidget(label)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        # Add the buttons to the same layout
        button_layout.addWidget(buttons)
        # Add the whole layout to your main layout
        main_layout.addLayout(button_layout)


    def browse_file_chMap(self):
        """
        Opens File Dialog for user to choose labels.txt
        """
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open NIfTI File",
            self.MW.LoadMRI.session_path,
            "NPY files (*.npy)"
        )

        #User cancelled
        if not file_name:
            return
        self.file_chMap = file_name
        self.chMap_file_line.setText(os.path.basename(file_name))


    def browse_file_fix(self):
        """
        Opens File Dialog for user to choose labels.txt
        """
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open NIfTI File",
            self.MW.LoadMRI.session_path,
            "NPY files (*.npy)"
        )

        #User cancelled
        if not file_name:
            return
        self.file_name_fixed = file_name
        self.file_line_fixed.setText(os.path.basename(file_name))

    def browse_file_mov(self):
        """
        Opens File Dialog for user to choose labels.txt
        """
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open NIfTI File",
            self.MW.LoadMRI.session_path,
            "NPY files (*.npy)"
        )

        #User cancelled
        if not file_name:
            return
        self.file_name_moving = file_name
        self.file_line_mov.setText(os.path.basename(file_name))

    def browse_file_pkl(self):
        # Pickle file that contains all the design parameters of each MRID tag
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Please select pkl file",
            self.MW.LoadMRI.session_path,
            "PKL files (*.pkl)"
        )
        #User cancelled
        if not file_name:
            return
        self.file_name_pkl = file_name
        self.file_line_pkl.setText(os.path.basename(file_name))

    def save_mrid_library_path(self):
        """Persist the current mrid_library path into paths_config.json,
        same as SAMRI's "Save all paths" button (samri_main.py's
        save_all_paths) does for atlas_folder/raw_base_samri -- so it's
        remembered as the default next time instead of only living in
        this dialog's in-memory self.file_name_pkl."""
        save_paths(mrid_library=self.file_name_pkl)

    def get_values(self):
        """
        Return (pklfile, mode, channel_separation, total_channels,
        moving_coordinates, fixed_coordinates, chMap_file). mode is
        "uniform" or "custom"; channel_separation/total_channels are only
        meaningful for "uniform" (None otherwise) -- "custom" geometry is
        defined afterwards in the main GUI's geometry dock, not here.
        """
        mode = "uniform" if self.radio_uniform.isChecked() else "custom"
        channel_separation = self.channel_separation.value() if mode == "uniform" else None
        total_channels = None
        if mode == "uniform":
            total_channels = [self.total_channels[roi].value() for roi in self.roi_names]
        moving_coordinates = self.file_name_moving
        fixed_coordinates = self.file_name_fixed
        pklfile = self.file_name_pkl
        chMap_file = self.file_chMap

        return pklfile, mode, channel_separation, total_channels, moving_coordinates, fixed_coordinates, chMap_file


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = ChannelVariablesInput()
    if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        data = dlg.get_values()
