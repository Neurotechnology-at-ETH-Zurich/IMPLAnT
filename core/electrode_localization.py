# This Python file uses the following encoding: utf-8
from mrid_utils import handlers, gauss_aux, warper, chmap, atlas_registry
import numpy as np
import pandas as pd
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
from core.image_layer import ImageLayer
from core.cursor import Cursor
from file_handling.mri_volume import MRIVolume
from utils.zoom import Zoom, zoom_notifier
from utils.minimap_handler import Minimap
from utils.contrast import Contrast
from gui_utils.intensity_table import IntensityTable
from gui_utils.busy_overlay import BusyOverlay
from trajectory_planning.mri_label_overlay import parse_itk_snap_label_file, build_discrete_label_lut
from gui_utils.busy_worker import BusyWorker, show_worker_error


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


    fitted_points,regionNames,regionNumbers,df,barcode_r,barcode_d,CA1,dwi1Dsignal,pyrChIdx,chMap,atlasCoordinates_pkl,bundle_fit_converged = chmap.main(
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

    return fitted_points,regionNames,regionNumbers,df,barcode_r,barcode_d, mrid,CA1,dwi1Dsignal,pyrChIdx,chMap,atlasCoordinates_pkl,bundle_fit_converged

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
        self.electrode_actor_gates = {}


    def get_gaussian_centers(self,transformation_files):
        """
        1. Warping heatmaps, segmentation and 4D volume at first-timestamp
        2. Getting Gaussian Centers or Electrodes

        Pure computation -- no Qt object is touched -- so this is safe to
        run off the GUI thread (see activate_get_gaussian_analysis). Returns
        a list of (data_view, FileNotFoundError) pairs for views whose ROI
        loop hit a missing resampled image (skipped, not fatal) for the
        caller to warn about once back on the GUI thread; raises
        FileNotFoundError itself if labels.txt (get_roinames) is missing,
        since there is nothing to iterate over in that case.
        """
        skipped = []
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
                skipped.append((data_view, e))
                continue

        return skipped


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

            # buttons_gui_time_series closed its own overlay before this, to keep the
            # geometry dock clickable -- raise a fresh one now that the
            # localisation work actually starts
            overlay = BusyOverlay(self.MW, message="Localising Electrodes, please wait…")
            overlay.raise_()
            overlay.show()

            worker_result = {}

            def work():
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
                unconverged_mrids = []

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
                        fitted_points,regionNames,regionNumbers,df,barcode_r,barcode_d,mrid,CA1,dwi1Dsignal,pyrChIdx,chMap,atlasCoordinates_pkl,bundle_fit_converged = future.result()
                        if not bundle_fit_converged:
                            unconverged_mrids.append(mrid)
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

                worker_result['payload'] = (
                    roi_names,totaldf,totalbarcode_r,totalbarcode_d,totalmrid,totalCA1,
                    totaldwi1Dsignal,totalregionNames,totalpyrChIdx,totalfitted_points,
                    totalchMap,totalatlasCoordinates_pkl)
                worker_result['unconverged_mrids'] = unconverged_mrids

            def on_worker_done():
                # Keep the overlay up through the warning below and through on_done
                # itself -- on_done (_finish_electrode_localisation) still does real,
                # synchronous work (barcode plotting, GUI updates) on this thread, so
                # closing here (right when the compute loop finishes, before any of
                # that has run) would uncover the GUI while it's still busy. A failed
                # convergence check is not a reason to cut that indication short either
                # -- close only once everything on_done does is actually done.
                unconverged_mrids = worker_result.get('unconverged_mrids') or []
                if unconverged_mrids:
                    # fit_res.success/fun were already computed by chmap.register_bundle
                    # and saved to bundle_fit_diagnostics.npy per tag, but nothing read
                    # that file back -- surface it here instead of silently discarding it.
                    QtWidgets.QMessageBox.warning(
                        self.MW, "Bundle registration did not converge",
                        "The point-set registration reported failure to converge for: "
                        + ", ".join(unconverged_mrids)
                        + "\n\nThe fitted channel positions for these tags may be unreliable."
                    )
                try:
                    on_done(worker_result['payload'])
                finally:
                    overlay.close()

            def on_worker_failed(tb):
                overlay.close()
                show_worker_error(self.MW, "Electrode localisation failed", tb)

            self._localisation_worker = BusyWorker(work, self.MW)
            self._localisation_worker.done.connect(on_worker_done)
            self._localisation_worker.failed.connect(on_worker_failed)
            self._localisation_worker.start()

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



    def add_point(self,fitted_points,atlas_points,mrid_tag=None):
        """
        Show the electrode contacts on the WHS atlas, in atlas space --
        not fitted_points (kept as a parameter since callers still have it,
        but that's the subject's own scan's voxel space, a different grid
        the atlas is never resampled onto here). Displayed in page_3D's
        real axial/coronal/sagittal viewer (see show_atlas_3d), not the
        single-panel "echo" view groupBox_data0 normally shows.

        atlas_points alone is only the tag's own few barcode-geometry
        reference points (fitted_mrid_points, mapped to atlas space in
        channel_mapper.map_channels_to_atlas -- not per-contact positions).
        The actual per-electrode-contact positions are the ones already
        saved to channel_atlas_coordinates.xlsx for this tag, read here (see
        _load_channel_atlas_points) and shown alongside atlas_points rather
        than instead of it.
        """
        channel_points = self._load_channel_atlas_points(mrid_tag) if mrid_tag else []
        self.show_atlas_3d(list(atlas_points) + channel_points)

    def _load_channel_atlas_points(self, mrid_tag):
        """channel_atlas_coordinates.xlsx (mrid_utils/channel_mapper.py's
        map_channels_to_atlas own per-channel export, one row per electrode
        contact, already atlas-space) for this tag -- every contact, not
        just atlas_points' handful of tag-geometry reference points."""
        path = os.path.join(self.savepath, mrid_tag.lower(), "channel_atlas_coordinates.xlsx")
        if not os.path.exists(path):
            print(f"[atlas-underlay] no channel_atlas_coordinates.xlsx for {mrid_tag} at {path}", flush=True)
            return []
        try:
            df = pd.read_excel(path)
            return df[["Atlas x", "Atlas y", "Atlas z"]].values.tolist()
        except Exception as e:
            print(f"[atlas-underlay] failed reading {path}: {e}", flush=True)
            return []

    # fitted centers are sub-voxel Gaussian fits, not exact voxel hits, so a
    # point stays visible for slices within this many voxels of its own
    # matching coordinate
    Z_VISIBILITY_TOLERANCE = 1

    @staticmethod
    def _atlas_point_display_xy(point_xyz, view_name, spacing, shape):
        """
        In-plane (x_display, y_display) world coordinates for an atlas-space
        (x,y,z) point in the given real orthogonal view, matching exactly
        how ImageLayer.setup_vtk slices/flips a non-4d volume for that same
        view_name (same formula trajectory_planning/rendering.py's
        _atlas_point_display_xy already uses for its own atlas-space points).
        spacing/shape are volume.spacing/volume.slices[0].shape (zyx).
        Returns (x_display, y_display, gate_axis, gate_value) where gate_axis
        is the index into slice_indices ([z,y,x]) this view holds fixed, and
        gate_value is the point's own coordinate on that axis (for
        visibility gating against the current cursor position).
        """
        x, y, z = point_xyz
        nz, ny, nx = shape
        if view_name == "axial":      # z fixed -> (x,y)
            return (nx - 1 - x) * spacing[2], y * spacing[1], 0, z
        elif view_name == "coronal":  # y fixed -> (z,x)
            return (nx - 1 - x) * spacing[2], z * spacing[0], 1, y
        else:                          # sagittal, x fixed -> (y,z)
            return (ny - 1 - y) * spacing[1], z * spacing[0], 2, x

    def _update_atlas_markers_3d(self, atlas_points):
        """
        Draw a sphere at every atlas-space electrode point on top of the
        atlas volume, once per real view (axial/coronal/sagittal). Redraws
        on every call so switching tags replaces the markers instead of
        only ever showing the first tag's; visibility is refreshed
        separately (see _update_atlas_marker_visibility_3d) whenever the
        slice changes, so a marker only shows on the slice it's actually on.
        """
        lm = self.LoadMRI
        if not getattr(self, 'atlas_3d_ready', False):
            return

        for actor, view_name in self.electrode_actors:
            renderer = lm.renderers.get(0, {}).get(view_name)
            if renderer is not None:
                renderer.RemoveActor(actor)
        self.electrode_actors.clear()
        self.electrode_actor_gates.clear()

        volume = lm.volumes[0]
        shape = volume.slices[0].shape
        spacing = volume.spacing  # zyx

        for view_name in ('axial', 'coronal', 'sagittal'):
            renderer = lm.renderers.get(0, {}).get(view_name)
            if renderer is None:
                continue
            for point in atlas_points:
                world_x, world_y, gate_axis, gate_value = self._atlas_point_display_xy(
                    point, view_name, spacing, shape)

                sphere = vtk.vtkSphereSource()
                sphere.SetCenter(world_x, world_y, 1)
                sphere.SetRadius(0.3)

                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection(sphere.GetOutputPort())

                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(1, 0, 0)  # red

                renderer.AddActor(actor)
                self.electrode_actors.append((actor, view_name))
                self.electrode_actor_gates[actor] = (gate_axis, gate_value)

        self._update_atlas_marker_visibility_3d()

        for view_name in ('axial', 'coronal', 'sagittal'):
            widget = lm.vtk_widgets.get(0, {}).get(view_name)
            if widget is not None:
                widget.GetRenderWindow().Render()

    def _update_atlas_marker_visibility_3d(self):
        """
        Shows each marker only on the slice it actually sits on (within
        Z_VISIBILITY_TOLERANCE voxels, since fitted centers are sub-voxel
        Gaussian fits, not exact voxel hits) -- scrolling through slices
        then reveals each electrode contact at its own depth instead of
        every contact along the whole shank showing regardless of where it
        actually is. Called from update_electrode_marker_visibility
        (LoadMRI.update_slices' existing hook) whenever the slice changes.
        """
        if not getattr(self, 'atlas_3d_ready', False):
            return
        lm = self.LoadMRI
        current = lm.slice_indices.get(0)
        if current is None:
            return
        gates = getattr(self, 'electrode_actor_gates', {})
        touched = set()
        for actor, view_name in self.electrode_actors:
            gate_axis, gate_value = gates.get(actor, (None, None))
            visible = gate_axis is not None and abs(gate_value - current[gate_axis]) <= self.Z_VISIBILITY_TOLERANCE
            actor.SetVisibility(visible)
            touched.add(view_name)
        for view_name in touched:
            widget = lm.vtk_widgets.get(0, {}).get(view_name)
            if widget is not None:
                widget.GetRenderWindow().Render()

    def update_electrode_marker_visibility(self):
        """Hook LoadMRI.update_slices already calls whenever the slice
        changes (core/load_MRI_file.py)."""
        self._update_atlas_marker_visibility_3d()


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


    def show_atlas_3d(self, atlas_points):
        """
        Shows the WHS atlas as a real 3-orthogonal-view (axial/coronal/
        sagittal) volume in page_3D -- the same viewer trajectory planning
        uses (vtkWidget_data_axial/coronal/sagittal, spinBox_x/y/z_data3d,
        etc.) -- with atlas-space electrode dots on it, instead of the
        single-panel "echo" view groupBox_data0 normally shows during
        electrode localization. atlas_points is the current tag's atlas-
        space coordinates (totalatlasCoordinates_pkl / channel_atlas_
        coordinates.xlsx's "Atlas x/y/z"), already indexing directly into
        this exact atlas volume -- no resampling needed (see
        _atlas_point_display_xy).

        data_index 0 is deliberately repurposed here: vtk_widgets[0]
        currently holds the is_4d echo-acquisition widgets (vtkWidget_data00
        etc., one entry per loaded acquisition, keyed by acquisition name).
        Both that mode and this one are hard-wired to reuse the SAME
        data_index==0 slot (ButtonsGUI_TimeSeries.buttons_4D and
        ButtonsGUI_Structural.buttons_3D each unconditionally reset
        lm.vtk_widgets themselves), so switching to this atlas display
        necessarily retires the echo view for the rest of this session --
        there is no code path in this app that keeps both alive at once for
        the same data_index (confirmed: restart_gui, the app's only other
        mode-switch, does a full teardown for exactly this reason). This
        only rebuilds what's scoped to data_index 0 (vtk_widgets, renderers,
        cursor_ui, contrast, intensity table, Layers[0]/volumes[0]), not a
        full restart_gui teardown, so the barcode panel and everything else
        already set up during electrode localization is left alone.

        Only does the actual load once (guarded by atlas_3d_ready); a tag
        switch after that just redraws the markers via _update_atlas_markers_3d.
        """
        lm = self.LoadMRI
        ui = self.MW.ui

        if getattr(self, 'atlas_3d_ready', False):
            ui.data_4d_3d.setCurrentIndex(1)
            # jump the cursor to the new tag's own first point -- otherwise
            # the view stays on the previous tag's slice, and this tag's
            # markers (gated to their own slice, see _update_atlas_markers_3d)
            # might not be on it at all
            if atlas_points is not None and len(atlas_points):
                vol = lm.volumes[0].slices[0]
                nz, ny, nx = vol.shape
                x0, y0, z0 = atlas_points[0]
                lm.slice_indices[0] = [
                    int(np.clip(round(z0), 0, nz - 1)),
                    int(np.clip(round(y0), 0, ny - 1)),
                    int(np.clip(round(x0), 0, nx - 1)),
                ]
                self.MW.Cursor.update_cursor_display(0)
                lm.update_slices(0, 'coronal')
            self._update_atlas_markers_3d(atlas_points)
            return

        atlas_template_path = getattr(self, 'atlas_template_path', None)
        if not atlas_template_path or not os.path.exists(atlas_template_path):
            print(f"No atlas template available (atlas_template_path={atlas_template_path!r})", flush=True)
            return

        # the echo view's own spin_x0/y0/z0/scroll_0 connections would
        # otherwise keep firing against now-stale state once their (now
        # hidden) widgets change for any other reason
        old_cursor_ui = getattr(lm, 'cursor_ui', {})
        for key in ("spin_x0", "spin_y0", "spin_z0", "scroll_0"):
            old_widget = old_cursor_ui.get(key)
            if old_widget is not None:
                try:
                    old_widget.valueChanged.disconnect()
                except RuntimeError:
                    pass

        # mode switch, matching ButtonsGUI_Structural.buttons_3D's own reset
        # (see docstring) -- vtk_widgets[0] goes from "one entry per is_4d
        # acquisition" to "one entry per real anatomical plane"
        page3d_widgets = {
            "axial": ui.vtkWidget_data_axial,
            "sagittal": ui.vtkWidget_data_sagittal,
            "coronal": ui.vtkWidget_data_coronal,
        }
        # these widgets may already carry a renderer from an earlier
        # trajectory-planning pass in this same session (same LoadMRI
        # process, page_3D's own normal use) -- setup_renderer only ever
        # ADDs a renderer, so a stale one left in place would double up and
        # composite underneath/behind the atlas instead of being replaced
        for widget in page3d_widgets.values():
            render_window = widget.GetRenderWindow()
            for renderer in list(render_window.GetRenderers()):
                render_window.RemoveRenderer(renderer)

        lm.vtk_widgets = {0: page3d_widgets}
        lm.renderers[0] = {}

        # a stale Minimap object (e.g. left over from an earlier trajectory-
        # planning pass in this same session, which also used 'coronal' as
        # a view name for data_index 0) still remembers 'coronal' as an
        # already-added minimap -- add_minimap would then treat re-adding it
        # as an update (removing+recreating its rectangle) before 'axial'/
        # 'sagittal' exist yet, and create_small_rectangle's non-4d branch
        # unconditionally needs all three already present, causing a
        # KeyError. A fresh Minimap (same object initialize_zoom_controls
        # would build for a genuinely first-time data_index 0 load) has no
        # such stale entries.
        if hasattr(lm, 'minimap'):
            try:
                zoom_notifier.factorChanged.disconnect(lm.minimap.create_small_rectangle)
            except RuntimeError:
                pass
        lm.minimap = Minimap(lm)
        zoom_notifier.factorChanged.connect(lm.minimap.create_small_rectangle)

        lm.volumes[0] = MRIVolume.from_file(atlas_template_path)
        vol = lm.volumes[0].slices[0]
        nz, ny, nx = vol.shape

        if atlas_points is not None and len(atlas_points):
            x0, y0, z0 = atlas_points[0]
            lm.slice_indices[0] = [
                int(np.clip(round(z0), 0, nz - 1)),
                int(np.clip(round(y0), 0, ny - 1)),
                int(np.clip(round(x0), 0, nx - 1)),
            ]
        else:
            lm.slice_indices[0] = [nz // 2, ny // 2, nx // 2]

        lm.contrast_ui_elements[0] = {
            "contrast0": ui.changeContrast_data3d,
            "brightness0": ui.changeBrightness_data3d,
            "display_level0": ui.display_level_data3d,
            "display_window0": ui.display_window_data3d,
            "auto0": ui.pushButton_auto_data3d,
            "reset0": ui.pushButton_reset_data3d,
        }
        lm.contrast[0] = Contrast(lm, data_index=0, label_file=False)
        for widget, slot in (
            (ui.changeBrightness_data3d.valueChanged, lambda v: lm.contrast[0].changed_sliders(v, image_index=0)),
            (ui.changeContrast_data3d.valueChanged, lambda v: lm.contrast[0].changed_sliders(v, image_index=0)),
            (ui.pushButton_auto_data3d.clicked, lambda: lm.contrast[0].auto(image_index=0)),
            (ui.pushButton_reset_data3d.clicked, lambda: lm.contrast[0].reset(image_index=0)),
        ):
            try:
                widget.disconnect()
            except RuntimeError:
                pass
            widget.connect(slot)

        lm.Layers[0] = {0: ImageLayer(
            lm.volumes[0].slices, lm.volumes[0].spacing, lm.volumes[0].view_names,
            lm.slice_indices[0], False, lm.render, contrast_class=lm.contrast[0],
        )}
        lm.setup_layer('coronal', 0, 0)

        lm.intensity_table[0] = IntensityTable(self.MW, 0, ui.tableintensity_data3d, vol)

        lm.cursor_ui = dict(old_cursor_ui)
        lm.cursor_ui.update({
            'spin_x0': ui.spinBox_x_data3d,
            'spin_y0': ui.spinBox_y_data3d,
            'spin_z0': ui.spinBox_z_data3d,
            'intensity0': ui.tableintensity_data3d.item(0, 2),
            'scroll_0': ui.Scroll_data3d0,
            'scroll_1': ui.Scroll_data3d1,
            'scroll_2': ui.Scroll_data3d2,
        })

        self.MW.Cursor = Cursor(self.MW, lm.cursor_ui, 0, 'coronal')
        self.MW.Cursor.update_cursor_display(0)
        self.MW.Cursor.start_cursor(True, 0, 'coronal')

        ui.data_4d_3d.setCurrentIndex(1)
        Zoom.fit_to_window(lm.vtk_widgets[0]["coronal"], lm.vtk_widgets.values(),
                            lm.scale_bar, lm.vtk_widgets, 0, data_3d=True)

        self.atlas_3d_ready = True
        self._populate_atlas_switch_combo()
        self._update_atlas_markers_3d(atlas_points)

    def _populate_atlas_switch_combo(self):
        """
        Fills comboBox_atlasSwitch with every atlas image file already on
        disk that shares the default WHS atlas' own voxel grid (see
        atlas_registry.py: the microscopy atlas and DWI are both resampled/
        packaged onto that same grid specifically so this holds) -- so
        picking one just swaps the array show_atlas_3d's layer displays, no
        rebuild of the viewer/cursor/renderers needed (see
        _switch_atlas_display). Atlases not yet fetched onto disk are left
        out rather than triggering a silent download.
        """
        ui = self.MW.ui
        combo = ui.comboBox_atlasSwitch
        combo.blockSignals(True)
        combo.clear()
        # each option: (image_path, label_file_path or None). label_file_path
        # set only for the categorical "atlas (labels)" options, so
        # _switch_atlas_display knows to colour it (see build_discrete_label_lut)
        # instead of treating it as a continuous grayscale image.
        self._atlas_switch_options = []

        def add_option(label, path, label_file_path=None):
            if path and os.path.exists(path) and (label_file_path is None or os.path.exists(label_file_path)):
                self._atlas_switch_options.append((path, label_file_path))
                combo.addItem(label)

        whs = atlas_registry.ATLASES[atlas_registry.DEFAULT_ATLAS]
        whs_files = whs['files']
        folder = _paths['atlas_folder']
        add_option("WHS T2* template", os.path.join(folder, whs_files['atlas_template']))
        add_option("WHS atlas (labels)", os.path.join(folder, whs_files['atlas_volume']),
                   label_file_path=os.path.join(folder, whs_files['atlas_labels']))
        if whs['has_dwi']:
            # this file's 4th (diffusion-direction) axis is a trailing
            # singleton for WHS's own DWI (confirmed against the real file),
            # which SimpleITK already collapses on read, same as any other
            # plain 3D volume here -- no special extraction needed
            add_option("WHS DWI", os.path.join(folder, whs_files['atlas_dwi']))

        micro = atlas_registry.ATLASES.get('whs_sd_swc_female_rat')
        if micro is not None:
            micro_folder = os.path.join(folder, micro.get('subfolder') or '')
            add_option(micro['display_name'], os.path.join(micro_folder, micro['files']['atlas_template']))

        current_index = next(
            (i for i, (path, _) in enumerate(self._atlas_switch_options) if path == self.atlas_template_path), 0)
        combo.setCurrentIndex(current_index)
        combo.blockSignals(False)
        combo.currentIndexChanged.connect(self._switch_atlas_display)

    def _switch_atlas_display(self, index):
        """comboBox_atlasSwitch.currentIndexChanged -- swaps the image data
        of the already-built atlas layer in place (same array object, so
        ImageLayer/volumes stay linked, matching the "mutate in place"
        trick core/paintbrush.py's own comment documents), rather than
        rebuilding the viewer. Only valid because every option in the combo
        shares the same voxel grid (see _populate_atlas_switch_combo).
        Reading a full-resolution atlas volume off disk is slow enough to
        freeze the GUI for a moment, so the read itself runs on a
        BusyWorker thread; only the (fast) VTK-touching part after runs on
        the GUI thread in on_done."""
        if not (0 <= index < len(getattr(self, '_atlas_switch_options', []))):
            return
        path, label_file_path = self._atlas_switch_options[index]

        result = {}

        def work():
            img = sitk.ReadImage(path)
            result['array'] = sitk.GetArrayFromImage(img)

        def on_done():
            overlay.close()
            new_arr = result.get('array')
            lm = self.LoadMRI
            current = lm.volumes[0].slices[0]
            if new_arr.shape != current.shape:
                print(f"[atlas-underlay] {path} has shape {new_arr.shape}, expected "
                      f"{current.shape} (different grid) -- skipped", flush=True)
                return

            current[:] = new_arr
            self.atlas_template_path = path

            lut = lm.contrast[0].lut_vtk[0]
            if label_file_path is not None:
                # categorical: colour by region instead of the usual
                # continuous grayscale ramp, mutating the same LUT object in
                # place (build_discrete_label_lut's own "refresh" mode) so
                # nothing needs re-attaching to the already-built actors
                labels = parse_itk_snap_label_file(label_file_path)
                build_discrete_label_lut(labels, lut=lut)
                lm.update_slices(0, 'coronal')
            else:
                # continuous: recompute_luttable both rebuilds the grayscale
                # ramp (undoing any earlier discrete colouring) and updates
                # the window/level sliders for this image's own intensity range.
                # vtkLookupTable.Build() is a no-op once SetTableValue has been
                # called directly on it (build_discrete_label_lut's doing, for
                # a previous "labels" selection) -- it only rebuilds from the
                # Hue/Saturation/Value ranges when its own InsertTime is older
                # than its last Build, which SetTableValue bumps past. Without
                # ForceBuild() here, recompute_luttable's Build() calls (and
                # update_lut_window_level's later on) silently keep the old
                # per-region colours forever, on every subsequent atlas too.
                lm.contrast[0].recompute_luttable(0, 0)
                lut.ForceBuild()
                lm.update_slices(0, 'coronal')

        def on_failed(tb):
            overlay.close()
            show_worker_error(self.MW, "Switching atlas display failed", tb)

        overlay = BusyOverlay(self.MW, message="Switching atlas display, please wait…")
        overlay.raise_()
        overlay.show()
        self._atlas_switch_worker = BusyWorker(work, self.MW)
        self._atlas_switch_worker.done.connect(on_done)
        self._atlas_switch_worker.failed.connect(on_failed)
        self._atlas_switch_worker.start()


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
        # Channel-to-region mapping is always built against WHS specifically,
        # never whatever _paths['active_atlas'] happens to be -- same pin as
        # samri/samri_main.py and trajectory_planning/registration_mri.py (a
        # global, switchable atlas must never leak into a persistent,
        # per-subject analysis result).
        whs_atlas = atlas_registry.ATLASES[atlas_registry.DEFAULT_ATLAS]
        whs_files = whs_atlas['files']
        self.atlas_path=os.path.join(_paths['atlas_folder'], whs_files['atlas_volume'])
        nii_atlas=nib.load(self.atlas_path)
        atlas=np.asanyarray(nii_atlas.dataobj)

        labels_path=os.path.join(_paths['atlas_folder'], whs_files['atlas_labels'])
        if whs_atlas['label_format'] == 'whs_legacy':
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
        dwi_path=os.path.join(_paths['atlas_folder'], whs_files['atlas_dwi']) if whs_atlas['has_dwi'] else None
        t2s_path=os.path.join(_paths['atlas_folder'], whs_files['atlas_template'])
        mask_path=os.path.join(_paths['atlas_folder'], whs_files['atlas_mask'])
        # kept for show_atlas_3d, which displays this same WHS template
        # once results are shown -- always WHS specifically, same pin as
        # self.atlas_path above (never _paths['active_atlas'])
        self.atlas_template_path = t2s_path

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
