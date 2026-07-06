# This Python file uses the following encoding: utf-8
import os
import json as _json
import SimpleITK as sitk
import pyvista as pv
from pyvistaqt import QtInteractor
from pathlib import Path
import pandas as pd
from matplotlib.colors import ListedColormap
import numpy as np
from PySide6.QtWidgets import QVBoxLayout
import nibabel as nib
import vtk
from concurrent.futures import ThreadPoolExecutor
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'paths_config.json')) as _f:
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
        self._camera_params = {}

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
        self.plotter_ax.renderer.AddActor2D(self.hover_label_ax)

        self.load_atlas()
        img = sitk.ReadImage(self.MW.LoadMRI.volumes[0].file_path)
        self.spacing = np.array(img.GetSpacing()) #self.spacing = img.GetSpacing()[0]

        self.MW.ui.pushButton_resetSagittal.clicked.connect(self.reset_sa)
        self.MW.ui.pushButton_resetCoronal.clicked.connect(self.reset_co)
        self.MW.ui.pushButton_resetAxial.clicked.connect(self.reset_ax)



        self.plotter_co.add_key_event('c', lambda: self._print_camera(self.plotter_co))
        self.plotter_sa.add_key_event('c', lambda: self._print_camera(self.plotter_sa))
        self.plotter_ax.add_key_event('c', lambda: self._print_camera(self.plotter_ax))



    def _print_camera(self, plotter):
        print("position:   ", plotter.camera.position, flush=True)
        print("focal_point:", plotter.camera.focal_point, flush=True)
        print("up:         ", plotter.camera.up, flush=True)
        print("azimuth:    ", plotter.camera.azimuth, flush=True)
        print("elevation:  ", plotter.camera.elevation, flush=True)
        print("roll:       ", plotter.camera.roll, flush=True)




    def on_hover_co(self, obj, event):
        self.pick_label(self.plotter_co,self.hover_label_co)

    def on_hover_sa(self, obj, event):
        self.pick_label(self.plotter_sa,self.hover_label_sa)

    def on_hover_ax(self, obj, event):
        self.pick_label(self.plotter_ax,self.hover_label_ax)

    def pick_label(self,plotter,hover_label):
        if 'background' not in plotter.actors:
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
        def load_background_mesh():
            background_path = self.MW.LoadMRI.volumes[0].file_path
            img = nib.load(background_path)
            scale_background = 1 #3
            data = img.get_fdata().astype(int)[::scale_background, ::scale_background, ::scale_background]
            zooms = img.header.get_zooms()[:3]
            mesh_small = pv.ImageData()
            mesh_small.dimensions = np.array(data.shape) + 1
            mesh_small.spacing = tuple(s * scale_background for s in zooms)
            mesh_small.origin = tuple(-s for s in zooms)  # shift so cell centers land on NIfTI voxel positions
            mesh_small.cell_data['NIFTI'] = data.flatten(order='F')
            return mesh_small

        def load_labels():
            labels_path = os.path.join(_paths['atlas_folder'], _paths['atlas_labels'])
            if Path(labels_path).is_file():
                return pd.read_csv(labels_path, comment='#', sep='\s+',
                                   names=['IDX', 'R', 'G', 'B', 'A', 'VIS', 'MSH', 'LABEL'])
            return None

        # Run all three file reads in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_background = executor.submit(load_background_mesh)
            future_labels = executor.submit(load_labels)

            self.atlaslabelsdf = future_labels.result()
            background_mesh = future_background.result()
            self.background_small = background_mesh.threshold(value=0.5)

        max_idx = int(self.atlaslabelsdf['IDX'].max())
        self.rgba = np.zeros((max_idx + 1, 4))
        rgba_background = np.zeros((max_idx + 1, 4))

        for _, row in self.atlaslabelsdf.iterrows():
            r, g, b = row['R']/255, row['G']/255, row['B']/255
            rgba_background[int(row['IDX'])] = [r, g, b, 0.1]

        self.cmap = ListedColormap(self.rgba)
        self.cmap_background = ListedColormap(rgba_background)
        # pre-built numpy arrays for fast vectorised colour lookup
        self._cmap_bg_colors = (np.array(self.cmap_background.colors)[:, :3] * 255).astype(np.uint8)

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

        up_vectors = {'sagittal': (1, 0, 0), 'coronal': (0, 0, 1), 'axial': (0, 1, 0)}
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

        self._camera_params[view] = {
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

        clipped_background = self.background_small.clip(normal=normal, origin=(x0, y0, z0))
        clipped_background = clipped_background.extract_surface(algorithm='dataset_surface')
        if clipped_background.n_cells == 0 or 'NIFTI' not in clipped_background.cell_data:
            return
        clipped_background = clipped_background.smooth_taubin(n_iter=50, pass_band=0.1)
        clipped_background = clipped_background.triangulate().decimate(0.6)  # keep 40% of triangles

        nifti_vals = np.round(clipped_background.cell_data['NIFTI']).astype(int)
        clipped_background.cell_data['colors'] = self._cmap_bg_colors[nifti_vals]

        plotter.add_mesh(
            clipped_background,
            scalars='colors',
            rgb=True,
            show_scalar_bar=False,
            opacity=1,
            style='surface',
            line_width=0.5,
            pickable=True,
            name='background',
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

        self._draw_electrode_lines(plotter, shank_number)
        plotter.render()

        self.clipped_meshes = True

    def _draw_electrode_lines(self, plotter, active_shank):
        tp = self.MW.LoadMRI.TrajPlanning
        neon_green = (0.0, 1.0, 28/255)
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

            # shank line
            line = pv.Line(deep_mm, end_mm)
            plotter.add_mesh(
                line,
                color=neon_green,
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

    def _reset_view(self, plotter, view):
        if view not in self._camera_params:
            plotter.reset_camera()
            return
        p = self._camera_params[view]
        plotter.camera.up = p['up']
        plotter.camera.focal_point = p['focal']
        plotter.set_position(p['position'])
        if self.parallel_projection:
            plotter.enable_parallel_projection()
        plotter.render()

    def reset_sa(self):
        self._reset_view(self.plotter_sa, 'sagittal')

    def reset_co(self):
        self._reset_view(self.plotter_co, 'coronal')

    def reset_ax(self):
        self._reset_view(self.plotter_ax, 'axial')