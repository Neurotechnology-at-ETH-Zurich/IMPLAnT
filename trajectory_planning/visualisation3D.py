# This Python file uses the following encoding: utf-8
import os
import sys
import json as _json
import SimpleITK as sitk
import pyvista as pv
from pyvistaqt import QtInteractor
from pathlib import Path
import pandas as pd
from matplotlib.colors import ListedColormap
import numpy as np
from PySide6.QtWidgets import QVBoxLayout, QApplication
from PySide6.QtCore import Qt
import nibabel as nib
import vtk
from concurrent.futures import ThreadPoolExecutor
_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)


class Visualisation3D:
    def __init__(self,MW):
        self.MW = MW
        self.ui = MW.ui
        self.enable_picking = False
        self.norm_vec = None
        self.parallel_projection = True
        self.poly_otherMrids = {}
        self.clipped_meshes = False
        self.camera_params = {}

        #set up layout
        #coronal
        widget = self.ui.vtkWidget_trajPlan_1
        pv.global_theme.background = 'black'
        layout = QVBoxLayout(widget) #)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter_co = QtInteractor(widget)
        layout.addWidget(self.plotter_co)
        self.hover_label_co = vtk.vtkTextActor()
        self.hover_label_co.SetInput("")
        self.hover_label_co.GetTextProperty().SetFontSize(14)
        self.hover_label_co.GetTextProperty().SetColor(1, 1, 1)  # white
        self.plotter_co.iren.add_observer('MouseMoveEvent', self.on_hover_co)
        self.plotter_co.iren.add_observer('LeftButtonPressEvent', self.on_click_co)
        self.plotter_co.renderer.AddActor2D(self.hover_label_co)
        #sagittal
        widget = self.ui.vtkWidget_trajPlan_2
        pv.global_theme.background = 'black'
        layout = QVBoxLayout(widget) #)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter_sa = QtInteractor(widget)
        layout.addWidget(self.plotter_sa)
        self.hover_label_sa = vtk.vtkTextActor()
        self.hover_label_sa.SetInput("")
        self.hover_label_sa.GetTextProperty().SetFontSize(14)
        self.hover_label_sa.GetTextProperty().SetColor(1, 1, 1)  # white
        self.plotter_sa.iren.add_observer('MouseMoveEvent', self.on_hover_sa)
        self.plotter_sa.iren.add_observer('LeftButtonPressEvent', self.on_click_sa)
        self.plotter_sa.renderer.AddActor2D(self.hover_label_sa)
        #axial
        widget = self.ui.vtkWidget_trajPlan_3
        pv.global_theme.background = 'black'
        layout = QVBoxLayout(widget) #)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter_ax = QtInteractor(widget)
        layout.addWidget(self.plotter_ax)
        self.hover_label_ax = vtk.vtkTextActor()
        self.hover_label_ax.SetInput("")
        self.hover_label_ax.GetTextProperty().SetFontSize(14)
        self.hover_label_ax.GetTextProperty().SetColor(1, 1, 1)  # white
        self.plotter_ax.iren.add_observer('MouseMoveEvent', self.on_hover_ax)
        self.plotter_ax.iren.add_observer('LeftButtonPressEvent', self.on_click_ax)
        self.plotter_ax.renderer.AddActor2D(self.hover_label_ax)

        for plotter in (self.plotter_co, self.plotter_sa, self.plotter_ax):
            plotter.render_window.SetMultiSamples(0)
            plotter.renderer.SetUseDepthPeeling(False)
            plotter.render_window.GetInteractor().SetDesiredUpdateRate(30)

        self.load_atlas()
        img = sitk.ReadImage(self.MW.LoadMRI.volumes[0].file_path)
        self.spacing = np.array(img.GetSpacing()) #self.spacing = img.GetSpacing()[0]

        self.MW.ui.pushButton_resetSagittal.clicked.connect(self.reset_sa)
        self.MW.ui.pushButton_resetCoronal.clicked.connect(self.reset_co)
        self.MW.ui.pushButton_resetAxial.clicked.connect(self.reset_ax)


    def on_hover_co(self, obj, event):
        self.pick_label(self.plotter_co,self.hover_label_co)

    def on_hover_sa(self, obj, event):
        self.pick_label(self.plotter_sa,self.hover_label_sa)

    def on_hover_ax(self, obj, event):
        self.pick_label(self.plotter_ax,self.hover_label_ax)

    def on_click_co(self, obj, event):
        self.pick_shank(self.plotter_co)

    def on_click_sa(self, obj, event):
        self.pick_shank(self.plotter_sa)

    def on_click_ax(self, obj, event):
        self.pick_shank(self.plotter_ax)

    def pick_shank(self, plotter):
        x, y = plotter.iren.get_event_position()
        electrode_actors = {name: actor for name, actor in plotter.actors.items()
                            if name.startswith('electrode_line_')}
        if not electrode_actors:
            return

        # tolerant cell pick for lines
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.01)
        picker.InitializePickList()
        for actor in electrode_actors.values():
            picker.AddPickList(actor)
        picker.SetPickFromList(True)
        picker.Pick(x, y, 0, plotter.renderer)
        hit = picker.GetActor()

        shank_idx = None
        if hit is not None:
            for name, actor in electrode_actors.items():
                if actor == hit:
                    try:
                        shank_idx = int(name.split('_')[-1])
                    except ValueError:
                        pass
                    break

        # fall back: check proximity to label tip in screen space
        if shank_idx is None:
            tp = self.MW.LoadMRI.TrajPlanning
            LABEL_RADIUS_PX = 60
            closest = LABEL_RADIUS_PX
            for s_idx in sorted(tp.coords_deepest_point):
                deep = tp.coords_deepest_point[s_idx]
                insert = tp.coords_insert_point[s_idx]
                if deep is None or insert is None:
                    continue
                deep_mm = np.array(deep, dtype=float) * self.spacing
                insert_mm = np.array(insert, dtype=float) * self.spacing
                direction = insert_mm - deep_mm
                length = np.linalg.norm(direction)
                if length < 1e-6:
                    continue
                direction /= length
                tip_mm = insert_mm + direction * 4.0
                coord = vtk.vtkCoordinate()
                coord.SetCoordinateSystemToWorld()
                coord.SetValue(*tip_mm.tolist())
                sx, sy = coord.GetComputedDisplayValue(plotter.renderer)
                dist = np.hypot(x - sx, y - sy)
                if dist < closest:
                    closest = dist
                    shank_idx = s_idx

        if shank_idx is None:
            return

        self.MW.LoadMRI.TrajPlanning.ui.comboBox_Shanks.setCurrentIndex(shank_idx)
        self.refresh_clipped_views(shank_idx)

    def refresh_clipped_views(self, shank_idx):
        tp = self.MW.LoadMRI.TrajPlanning
        direction = tp.direction_atlas.get(shank_idx)
        if direction is None:
            return

        if 'coronal' in self.camera_params:
            axis_y = np.array([0.0, 1.0, 0.0])
            n = axis_y - np.dot(axis_y, direction) * direction
            nl = np.linalg.norm(n)
            if nl > 1e-6:
                n /= nl
                if n[1] < 0:
                    n *= -1
                self.render_clipped(n, 'coronal', shank_idx)

        if 'sagittal' in self.camera_params:
            axis_x = np.array([1.0, 0.0, 0.0])
            n = axis_x - np.dot(axis_x, direction) * direction
            nl = np.linalg.norm(n)
            if nl > 1e-6:
                n /= nl
                if n[0] > 0:
                    n *= -1
                self.render_clipped(n, 'sagittal', shank_idx)

        if 'axial' in self.camera_params:
            n = np.array([0.0, 0.0, 1.0])
            depth = (tp.ui.horizontalSlider_axial3D.value()
                     if hasattr(tp, 'axial_slider_connect') else 0)
            self.render_clipped(n, 'axial', shank_idx, depth=depth)

    def pick_label(self,plotter,hover_label):
        if 'background' not in plotter.actors:
            return
        if QApplication.mouseButtons() != Qt.NoButton:
            return
        x, y = plotter.iren.get_event_position()
        picker = vtk.vtkPropPicker()
        picker.InitializePickList()
        picker.AddPickList(plotter.actors['background'])
        picker.SetPickFromList(True)
        picker.PickProp(x, y, plotter.renderer)
        actor = picker.GetViewProp()
        point = picker.GetPickPosition()

        if actor==plotter.actors['background']:
            mesh = actor.mapper.dataset
            idx = mesh.find_closest_cell(point)
            nifti_value = mesh.cell_data['NIFTI'][idx]
        else:
            hover_label.SetInput("")
            return

        row_index = self.atlaslabelsdf[self.atlaslabelsdf['IDX'] == nifti_value].index[0]
        label = self.atlaslabelsdf['LABEL'].values[row_index]
        hover_label.SetPosition(x + 5, y + 5)
        hover_label.SetInput(f"{label}")
        plotter.render()

    def load_atlas(self):
        def load_background_mesh(scale):
            background_path = self.MW.LoadMRI.volumes[0].file_path
            img = nib.load(background_path)
            data = img.get_fdata().astype(int)[::scale, ::scale, ::scale]
            zooms = img.header.get_zooms()[:3]
            mesh = pv.ImageData()
            mesh.dimensions = np.array(data.shape) + 1
            mesh.spacing = tuple(s * scale for s in zooms)
            mesh.origin = tuple(-s for s in zooms)
            mesh.cell_data['NIFTI'] = data.flatten(order='F')
            return mesh

        def load_labels():
            labels_path = os.path.join(_paths['atlas_folder'], _paths['atlas_labels'])
            if Path(labels_path).is_file():
                return pd.read_csv(labels_path, comment='#', sep='\s+',
                                   names=['IDX', 'R', 'G', 'B', 'A', 'VIS', 'MSH', 'LABEL'])
            return None

        def load_background_full_numpy():
            background_path = self.MW.LoadMRI.volumes[0].file_path
            img = nib.load(background_path)
            return np.array(img.header.get_zooms()[:3])

        def load_skull_mesh(scale):
            # the skull mask (see SegmentationGUI._compute_skull_th_vol /
            # Registration.warp_skull_mask) already lives in memory on the
            # same atlas grid as background_small (warp_skull_mask warps it
            # onto the atlas image directly) -- no file to read here, just
            # match load_background_mesh's array convention: sitk gives
            # (z,y,x), nib's get_fdata() (used above) gives (x,y,z).
            tp = getattr(self.MW.LoadMRI, 'TrajPlanning', None)
            skull_img = getattr(tp, 'skull_mask_img', None) if tp is not None else None
            if skull_img is None:
                return None
            data = sitk.GetArrayFromImage(skull_img)
            data = np.transpose(data, (2, 1, 0))[::scale, ::scale, ::scale]
            zooms = skull_img.GetSpacing()
            mesh = pv.ImageData()
            mesh.dimensions = np.array(data.shape) + 1
            mesh.spacing = tuple(s * scale for s in zooms)
            mesh.origin = tuple(-s for s in zooms)
            mesh.cell_data['MASK'] = data.flatten(order='F')
            return mesh

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_small  = executor.submit(load_background_mesh, 3) #2
            future_full   = executor.submit(load_background_full_numpy)
            future_labels = executor.submit(load_labels)

            self.atlaslabelsdf       = future_labels.result()
            self.background_small    = future_small.result().threshold(value=0.5)
            self.brain_surface_small = self.background_small.extract_surface(algorithm='dataset_surface')
            self.brain_surface_small = self.brain_surface_small.smooth_taubin(n_iter=50, pass_band=0.1)
            self.background_full_zooms = future_full.result()

        self.skull_surface_small = None
        skull_mesh = load_skull_mesh(3)
        if skull_mesh is not None:
            self.skull_surface_small = skull_mesh.threshold(value=0.5)
            self.skull_surface_small = self.skull_surface_small.extract_surface(algorithm='dataset_surface')
            self.skull_surface_small = self.skull_surface_small.smooth_taubin(n_iter=50, pass_band=0.1)

        max_idx = int(self.atlaslabelsdf['IDX'].max())
        self.rgba = np.zeros((max_idx + 1, 4))
        rgba_background = np.zeros((max_idx + 1, 4))

        for _, row in self.atlaslabelsdf.iterrows():
            r, g, b = row['R']/255, row['G']/255, row['B']/255
            rgba_background[int(row['IDX'])] = [r, g, b, 0.1]

        self.cmap = ListedColormap(self.rgba)
        self.cmap_background = ListedColormap(rgba_background)
        # pre-built numpy arrays for fast vectorised colour lookup
        self.cmap_bg_colors = (np.array(self.cmap_background.colors)[:, :3] * 255).astype(np.uint8)

        self.plotter_co.add_axes()
        self.plotter_sa.add_axes()
        self.plotter_ax.add_axes()


    def render_clipped(self,normal,view,shank_number,depth=0):
        p = self.MW.LoadMRI.TrajPlanning.coords_insert_point[shank_number]
        self.insertion_point = np.array(p)
        p = self.MW.LoadMRI.TrajPlanning.coords_deepest_point[shank_number]
        self.deepest_point = np.array(p)
        self.coords_list = [np.array(p) for p in self.MW.LoadMRI.TrajPlanning.channel_points[shank_number]]

        x0 = (self.coords_list[0][0])*self.spacing[0]
        y0 = (self.coords_list[0][1])*self.spacing[1]
        z0 = depth * self.spacing[2] if view == 'axial' else (self.coords_list[0][2])*self.spacing[2]

        up_vectors = {'sagittal': (0, 0, 1), 'coronal': (0, 0, 1), 'axial': (0, 1, 0)}
        if view == 'sagittal':
            plotter = self.plotter_sa
        elif view == 'coronal':
            plotter = self.plotter_co
        elif view == 'axial':
            plotter = self.plotter_ax

        up = up_vectors[view]
        focal_point = tuple(self.coords_list[0] * self.spacing)
        distance = 60
        position = tuple(np.array(focal_point) + np.array(normal) * distance)

        self.camera_params[view] = {
            'up': up,
            'focal': focal_point,
            'position': position,
        }

        plotter.camera.up = up
        plotter.camera.focal_point = focal_point
        plotter.camera.clipping_range = (1e-5, 1e5)
        if self.parallel_projection:
            plotter.disable_parallel_projection()
        plotter.set_position(position)
        if self.parallel_projection:
            plotter.enable_parallel_projection()

        # --- Front slab: clip from both sides to get a 1-voxel-thick strip ---
        # clip(normal) keeps the NEGATIVE side, so clip(normal) gives brain at origin,
        # then clip(-normal) at back_origin trims to 1 voxel on the brain side
        thickness = float(np.dot(np.abs(normal), 3 * self.background_full_zooms))
        back_origin = (x0 - normal[0]*thickness, y0 - normal[1]*thickness, z0 - normal[2]*thickness)

        slab = self.background_small.clip(normal=normal, origin=(x0, y0, z0))
        slab = slab.clip(normal=tuple(-n for n in normal), origin=back_origin)

        if slab.n_cells == 0:
            return
        nifti_vals = np.clip(np.round(slab.cell_data['NIFTI']).astype(int), 0, len(self.cmap_bg_colors) - 1)
        slab.cell_data['colors'] = self.cmap_bg_colors[nifti_vals]

        plotter.add_mesh(
            slab,
            scalars='colors',
            rgb=True,
            show_scalar_bar=False,
            opacity=1,
            style='surface',
            pickable=True,
            name='background',
            reset_camera=False,
            render=False,
        )

        # --- Hollow outer shell (scale 2): clipped brain boundary ---
        shell = self.brain_surface_small.clip(normal=normal, origin=(x0, y0, z0))


        if shell.n_cells > 0:
            if 'NIFTI' in shell.cell_data:
                nifti_sh = np.clip(np.round(shell.cell_data['NIFTI']).astype(int), 0, len(self.cmap_bg_colors) - 1)
                shell.cell_data['colors'] = self.cmap_bg_colors[nifti_sh]
                plotter.add_mesh(
                    shell,
                    scalars='colors',
                    rgb=True,
                    opacity=1,
                    show_scalar_bar=False,
                    pickable=False,
                    name='brain_shell',
                    reset_camera=False,
                    render=False,
                )
            else:
                plotter.add_mesh(
                    shell,
                    color=[0.25, 0.25, 0.25],
                    opacity=1,
                    show_scalar_bar=False,
                    pickable=False,
                    name='brain_shell',
                    reset_camera=False,
                    render=False,
                )

        # --- Skull shell: clipped skull-mask surface, same dark grey as
        # its 2D-slice overlay (see registration.py's binary_color) ---
        if self.skull_surface_small is not None:
            skull_shell = self.skull_surface_small.clip(normal=normal, origin=(x0, y0, z0))
            if skull_shell.n_cells > 0:
                plotter.add_mesh(
                    skull_shell,
                    color=[0.3, 0.3, 0.3],
                    opacity=1,
                    show_scalar_bar=False,
                    pickable=False,
                    name='skull_shell',
                    reset_camera=False,
                    render=False,
                )

        insertion_poly = pv.PolyData(np.array(self.insertion_point, dtype=np.float32)*self.spacing)
        plotter.add_mesh(
            insertion_poly,
            color='red',
            point_size=10,
            name="insertion_point",
            render_points_as_spheres=True,
            render=False,
            show_scalar_bar=False,
            reset_camera=False,
        )

        poly = pv.PolyData(np.array(self.coords_list, dtype=np.float32)*self.spacing)
        plotter.add_mesh(
            poly,
            color='white',
            point_size=10,
            name="electrode_points",
            render_points_as_spheres=True,
            render=False,
            show_scalar_bar=False,
            reset_camera=False,
        )

        deep_poly = pv.PolyData(np.array(self.deepest_point, dtype=np.float32)*self.spacing)
        plotter.add_mesh(
            deep_poly,
            color='green',
            point_size=10,
            name="deepest_point",
            render_points_as_spheres=True,
            render=False,
            show_scalar_bar=False,
            reset_camera=False,
        )

        self.draw_electrode_lines(plotter, shank_number)

        if view in ('coronal', 'sagittal'):
            self._draw_atlas_reference_plane(plotter, view, (x0, y0, z0))
            self._draw_shank_angle_indicator(plotter, view, shank_number)

        plotter.render()

        self.clipped_meshes = True

    def _atlas_sagittal_plane_normal_and_point(self, tp):
        """Normal (unit vector) and a point (both mm) of the plane formed
        by sweeping the atlas bregma-lambda LINE -- sagittal's actual 2D
        reference, see compute_shank_reference_angle -- along the ML (x)
        axis, rather than reusing the bregma/lambda/CC plane (which is
        coronal's reference, not sagittal's). Sweeping along x means the
        plane contains both the bregma-lambda vector and the x-axis
        direction, so its normal is their cross product -- always of the
        form (0, y, z) since crossing anything with (1,0,0) zeroes the
        x-component, i.e. the x-axis lies IN the plane by construction."""
        bregma = getattr(tp, 'atlas_bregma_coords', None)
        lam = getattr(tp, 'atlas_lambda_coords', None)
        if bregma is None or lam is None:
            return None, None
        b = np.array(bregma, dtype=float) * self.spacing
        l = np.array(lam, dtype=float) * self.spacing
        bl_vec = l - b
        normal = np.cross(np.array([1.0, 0.0, 0.0]), bl_vec)
        norm = np.linalg.norm(normal)
        if norm < 1e-9:
            return None, None
        return normal / norm, b

    def _draw_atlas_reference_plane(self, plotter, view, origin_mm):
        """The full atlas reference plane -- not just its 1D crossing of
        some slice -- drawn as a semi-transparent yellow quad in true 3D
        space. Coronal uses the bregma/lambda/corpus-callosum plane
        (matching compute_shank_reference_angle's coronal reference);
        sagittal uses the bregma-lambda line swept along the ML axis (see
        _atlas_sagittal_plane_normal_and_point), matching sagittal's own
        2D reference instead of coronal's plane. Positioned to pass
        through THIS view's own clip origin (origin_mm, i.e. the current
        shank's own slicing reference point, projected onto the true
        plane) so it actually shows up near the currently selected shank
        instead of sitting wherever the plane's defining atlas points
        happen to be -- projecting only moves the quad's center along the
        plane, so every point drawn still lies exactly on the real
        reference plane."""
        name = f'atlas_ref_plane_{view}'
        tp = self.MW.LoadMRI.TrajPlanning
        if view == 'sagittal':
            normal, plane_point = self._atlas_sagittal_plane_normal_and_point(tp)
        else:
            if getattr(tp, 'atlas_cc_centroid', None) is None:
                if name in plotter.actors:
                    plotter.remove_actor(name, render=False)
                return
            normal, plane_point = tp._atlas_plane_normal_and_point()
        if normal is None:
            if name in plotter.actors:
                plotter.remove_actor(name, render=False)
            return

        origin_mm = np.array(origin_mm, dtype=float)
        center = origin_mm - np.dot(origin_mm - plane_point, normal) * normal

        bounds = self.background_small.bounds  # (xmin,xmax,ymin,ymax,zmin,zmax), mm
        size = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])

        plane = pv.Plane(center=center, direction=normal, i_size=size, j_size=size)
        plotter.add_mesh(
            plane, color='yellow', opacity=0.25, show_edges=False,
            name=name, render=False, reset_camera=False,
        )

    def _draw_shank_angle_indicator(self, plotter, view, shank_number=None):
        """3D counterpart of TrajectoryPlanning._update_shank_angle_display_
        view: the same shank-vs-atlas-reference angle (caption + arc) shown
        in the 2D view, reusing compute_shank_reference_angle so the angle
        math lives in exactly one place. shank_number defaults to the
        currently selected shank if not passed -- render_clipped (called
        per-shank during PDF export) passes its own shank_number explicitly
        so each exported page shows THAT shank's angle, not whichever shank
        happens to be selected in the GUI at export time. Drawn as a plain
        unclipped arc +
        label anchored at the shank's deepest point in true world space --
        embedded back into 3D using this view's own fixed anatomical plane
        (sagittal holds X fixed, coronal holds Y fixed), NOT the clip
        plane's tilted (right, up_in_plane) basis _draw_atlas_plane_
        indicator uses, since this angle is measured against a fixed
        anatomical plane, not render_clipped's shank-trajectory-relative
        clip plane."""
        names = (f'shank_angle_label_{view}',)
        if not hasattr(self, 'shank_angle_arc2d_actors'):
            self.shank_angle_arc2d_actors = {}

        def _clear():
            for nm in names:
                if nm in plotter.actors:
                    plotter.remove_actor(nm, render=False)
            old_arc2d = self.shank_angle_arc2d_actors.pop(view, None)
            if old_arc2d is not None:
                plotter.renderer.RemoveActor2D(old_arc2d)

        tp = self.MW.LoadMRI.TrajPlanning
        result = tp.compute_shank_reference_angle(view, shank_number)
        if result is None:
            _clear()
            return

        angle, proj = result['angle'], result['proj']
        ref_2d, shank_2d = result['ref_2d'], result['shank_2d']
        deep_vox, insert_vox, spacing = result['deep_vox'], result['insert_vox'], result['spacing']
        ref_point_vox = result['ref_point_vox']

        def _embed(vec2d):
            v3 = np.zeros(3)
            v3[list(proj)] = vec2d
            return v3

        shank_dir, ref_dir = _embed(shank_2d), _embed(ref_2d)
        shank_norm, ref_norm = np.linalg.norm(shank_dir), np.linalg.norm(ref_dir)
        if shank_norm < 1e-9 or ref_norm < 1e-9:
            _clear()
            return
        shank_dir, ref_dir = shank_dir / shank_norm, ref_dir / ref_norm

        # arc centered where the shank line actually crosses the reference
        # line, computed in this view's fixed anatomical (proj) plane, not
        # at the deepest point (which sits ON the shank line but generally
        # nowhere near the reference line -- see the identical fix in
        # TrajectoryPlanning._update_shank_angle_display_view)
        center_2d = None
        if ref_point_vox is not None:
            center_2d = self.MW.LoadMRI.TrajPlanning._line_intersection_2d(
                deep_vox[list(proj)], shank_2d / np.linalg.norm(shank_2d),
                ref_point_vox[list(proj)], ref_2d / np.linalg.norm(ref_2d))
        held_axis = ({0, 1, 2} - set(proj)).pop()
        center = np.zeros(3)
        center[held_axis] = deep_vox[held_axis] * spacing[held_axis]
        if center_2d is None:
            center[list(proj)] = deep_vox[list(proj)] * spacing[list(proj)]  # lines ~parallel -- fall back
        else:
            center[list(proj)] = center_2d * spacing[list(proj)]

        # pointa = i - (i-d)/2 = (i+d)/2, where i = vector from center to
        # the insertion point and d = vector from center to the deepest
        # point -- i.e. center's vector straight to the midpoint between
        # insertion and deepest point (equivalently: pointa IS that
        # midpoint). radius is just this vector's own length -- see the
        # identical fix in TrajectoryPlanning._update_shank_angle_display_
        # view. pointb = pointa rotated by exactly `angle` degrees within
        # the (proj) plane -- clockwise for sagittal, counter-clockwise
        # for coronal, matching the 2D indicator.
        deep_mm_2d = deep_vox[list(proj)] * spacing[list(proj)]
        insert_mm_2d = insert_vox[list(proj)] * spacing[list(proj)]
        i_vec_2d = insert_mm_2d - center[list(proj)]
        d_vec_2d = deep_mm_2d - center[list(proj)]
        p1_vec_2d = i_vec_2d - (i_vec_2d - d_vec_2d) / 2
        radius = max(np.linalg.norm(p1_vec_2d), 1e-6)
        point1_dir_2d = p1_vec_2d / radius

        # pointb = Point1 rotated by EXACTLY `angle` degrees -- matching
        # TrajectoryPlanning._update_shank_angle_display_view's (2D) arc
        # construction exactly, instead of using ref_dir directly (whose
        # own true angle from point1_dir can be `angle` or `180-angle`
        # depending on which side of the shank's midpoint the arc center
        # falls on, silently mismatching the caption on one side). The 2D
        # indicator picks its rotation_sign from a cross product computed
        # in ITS OWN mirrored display frame; this function works in the
        # raw (unflipped) frame throughout, and the display-mirror's own
        # reversal of rotation direction exactly cancels the sign flip the
        # mirror itself introduces -- so the same rule, applied here to the
        # raw (un-mirrored) vectors with no flip step at all, reproduces
        # the identical arc.
        ref_dir_2d = ref_2d / ref_norm
        if view == 'sagittal':
            # compute_shank_reference_angle reports 180-minus-the-raw
            # angle for sagittal; keep ref_dir_2d consistent with that
            # supplement (see its docstring).
            ref_dir_2d = -ref_dir_2d
        cross_z = point1_dir_2d[0] * ref_dir_2d[1] - point1_dir_2d[1] * ref_dir_2d[0]
        rotation_sign = -1.0 if cross_z >= 0 else 1.0

        # Coronal only: if the deepest point sits BETWEEN the
        # reference-plane crossing (center) and the insertion point --
        # i.e. center is on the opposite side of deep_mm_2d from
        # insert_mm_2d along the shank line -- the cross-product rule
        # above picks the wrong side; negate rotation_sign in that case
        # (matching the identical fix in TrajectoryPlanning.
        # _update_shank_angle_display_view).
        if view == 'coronal':
            shank_dir_2d = shank_2d / shank_norm
            t_center = np.dot(center[list(proj)] - deep_mm_2d, shank_dir_2d)
            if t_center < 0:
                rotation_sign = -rotation_sign

        theta = rotation_sign * np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        point2_dir_2d = np.array([
            c * point1_dir_2d[0] - s * point1_dir_2d[1],
            s * point1_dir_2d[0] + c * point1_dir_2d[1],
        ])

        point1_dir = _embed(point1_dir_2d)
        point2_dir = _embed(point2_dir_2d)

        arc = pv.CircularArc(pointa=center + point1_dir * radius, pointb=center + point2_dir * radius, center=center)
        old_arc2d = self.shank_angle_arc2d_actors.pop(view, None)
        if old_arc2d is not None:
            plotter.renderer.RemoveActor2D(old_arc2d)
        # A plain add_mesh actor is depth-tested like any other 3D
        # geometry -- polygon-offset only fixes z-fighting between
        # near-coincident surfaces, it does NOT stop the arc from being
        # hidden behind the clipped brain surface whenever it's genuinely
        # further back. To make it truly always visible, draw it as a
        # vtkActor2D instead: its polydata is fed through a vtkCoordinate
        # set to WORLD, so it still tracks the arc's real 3D position and
        # moves correctly with the camera, but vtkActor2D itself is an
        # overlay -- rendered after the 3D scene with no depth test at
        # all, the same mechanism corner annotations/orientation markers
        # use to always stay on top.
        arc_coordinate = vtk.vtkCoordinate()
        arc_coordinate.SetCoordinateSystemToWorld()
        arc_mapper2d = vtk.vtkPolyDataMapper2D()
        arc_mapper2d.SetInputData(arc)
        arc_mapper2d.SetTransformCoordinate(arc_coordinate)
        # vtkPolyDataMapper2D defaults to scalar-coloring, and
        # pv.CircularArc bakes in a "Distance" scalar array for
        # parametrization -- without this, the mapper colors the arc
        # through a rainbow lookup table instead of the actor's solid
        # white color set below.
        arc_mapper2d.ScalarVisibilityOff()
        arc_actor2d = vtk.vtkActor2D()
        arc_actor2d.SetMapper(arc_mapper2d)
        arc_actor2d.GetProperty().SetColor(1, 1, 1)
        arc_actor2d.GetProperty().SetLineWidth(2)
        plotter.renderer.AddActor2D(arc_actor2d)
        self.shank_angle_arc2d_actors[view] = arc_actor2d

        # label position = the arc's own angle bisector (halfway between
        # pointa/pointb, direction-wise), at roughly the same distance
        # from center as the arc itself (radius) -- see the identical fix
        # in TrajectoryPlanning._update_shank_angle_display_view. Falls
        # back to a perpendicular of point1_dir only in the degenerate
        # case where pointa/pointb are exactly opposite (a 180 degree
        # sweep, where the sum cancels to zero).
        bisector_vec = point1_dir + point2_dir
        bisector_norm = np.linalg.norm(bisector_vec)
        if bisector_norm > 1e-9:
            bisector_dir = bisector_vec / bisector_norm
        else:
            held_axis_vec = np.zeros(3)
            held_axis_vec[held_axis] = 1.0
            bisector_dir = np.cross(held_axis_vec, point1_dir)
        label_pt = pv.PolyData((center + bisector_dir * radius).reshape(1, 3))
        plotter.add_point_labels(
            label_pt, [f"{angle:.1f}°"],
            text_color='white', font_size=16, shape=None, bold=True, shadow=False,
            show_points=False, always_visible=True,
            name=f'shank_angle_label_{view}', render=False, reset_camera=False,
        )

    def draw_electrode_lines(self, plotter, active_shank):
        tp = self.MW.LoadMRI.TrajPlanning
        dark_grey  = (0.3, 0.3, 0.3)

        for shank_idx in sorted(tp.coords_deepest_point):
            deep = tp.coords_deepest_point[shank_idx]
            insert = tp.coords_insert_point[shank_idx]
            if deep is None or insert is None:
                continue

            deep_mm   = np.array(deep,   dtype=float) * self.spacing
            insert_mm = np.array(insert, dtype=float) * self.spacing
            direction = insert_mm - deep_mm
            length = np.linalg.norm(direction)
            if length < 1e-6:
                continue
            direction /= length
            end_mm = insert_mm + direction * 4.0

            is_active = (shank_idx == active_shank)
            shank_color = tp.get_shank_vtk_color(shank_idx) if hasattr(tp, 'get_shank_vtk_color') else (0.0, 1.0, 28/255)

            # shank line
            line = pv.Line(deep_mm, end_mm)
            plotter.add_mesh(
                line,
                color=shank_color,
                opacity=1.0,
                line_width=4 if is_active else 2,
                name=f"electrode_line_{shank_idx}",
                render=False,
                reset_camera=False,
            )

            # label at the tip of the extended line
            label_pt = pv.PolyData(end_mm.reshape(1, 3))
            plotter.add_point_labels(
                label_pt,
                [f"Shank {shank_idx + 1}"],
                text_color='white',
                font_size=16,
                shape=None,
                bold=True,
                shadow=False,
                show_points=False,
                always_visible=True,
                name=f"shank_label_{shank_idx}",
                render=False,
                reset_camera=False,
            )

            # channel points for non-selected shanks
            if not is_active:
                pts = tp.channel_points.get(shank_idx)
                if pts is not None and len(pts) > 0:
                    ch_poly = pv.PolyData(np.array(pts, dtype=np.float32) * self.spacing)
                    plotter.add_mesh(
                        ch_poly,
                        color=dark_grey,
                        point_size=6,
                        name=f"channel_points_{shank_idx}",
                        render_points_as_spheres=True,
                        render=False,
                        show_scalar_bar=False,
                        reset_camera=False,
                    )

    def reset_view(self, plotter, view):
        if view not in self.camera_params:
            plotter.reset_camera()
            return
        p = self.camera_params[view]
        plotter.camera.up = p['up']
        plotter.camera.focal_point = p['focal']
        plotter.set_position(p['position'])
        if self.parallel_projection:
            plotter.enable_parallel_projection()
        plotter.render()

    def reset_sa(self):
        self.reset_view(self.plotter_sa, 'sagittal')

    def reset_co(self):
        self.reset_view(self.plotter_co, 'coronal')

    def reset_ax(self):
        self.reset_view(self.plotter_ax, 'axial')