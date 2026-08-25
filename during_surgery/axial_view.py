# This Python file uses the following encoding: utf-8
"""
2D axial-slice reference view for the Surgery tab: widget_axialView shows
one axial slice of the subject's own MRI scan, with the same core pieces
as the app's own 2D viewer (core/load_MRI_file.py + core/image_layer.py):
a real vtkImageActor/vtkLookupTable pipeline in a QVTKRenderWindowInteractor
(not a QImage/QPixmap), zoom/pan/fit buttons, a scale bar, orientation
labels, and a minimap with a "current view" rectangle.

Deliberately NOT reusing utils/zoom.py's Zoom, utils/scale_bar.py's Scale,
or utils/minimap_handler.py's Minimap directly: all three are tied to
LoadMRI's own renderers/vtk_widgets dict shapes, and Zoom in particular
keeps its state in class-level globals (Zoom.global_zoom_factor,
Zoom.bounds) shared across the WHOLE app -- reusing it here would
cross-contaminate the main viewer's own zoom/pan state. This mirrors the
same core VTK camera-manipulation techniques (confirmed against
gui_utils/buttons_gui3D.py's exact wiring) as a self-contained,
independent instance instead.
"""
import numpy as np
import SimpleITK as sitk
import vtk
from vtk.util import numpy_support
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide6.QtWidgets import QVBoxLayout
from during_surgery.mri_preview import _SHANK_COLORS


class SurgeryAxialView:
    # Matches gui_utils/buttons_gui3D.py's own zoom_in/zoom_out/pan_distance
    # convention exactly, so this view feels consistent with the rest of
    # the app even though it's an independent instance.
    _ZOOM_IN_FACTOR = 1.2
    _ZOOM_OUT_FACTOR = 0.8
    _PAN_DISTANCE = 0.4  # mm per click

    def __init__(self, container_widget, slider, buttons):
        """buttons: dict with keys 'zoom_in','zoom_out','go_up','go_down',
        'go_left','go_right','fit' -> the corresponding QAbstractButton."""
        self.slider = slider
        self.vtk_widget = QVTKRenderWindowInteractor(container_widget)
        layout = QVBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.vtk_widget)

        render_window = self.vtk_widget.GetRenderWindow()
        render_window.SetNumberOfLayers(2)

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0, 0, 0)
        self.renderer.SetLayer(0)
        render_window.AddRenderer(self.renderer)

        # Small inset viewport, same idea as utils/minimap_handler.py's
        # Minimap but self-contained -- a second renderer showing the same
        # image at a fixed, always-fit zoom, plus a rectangle outlining the
        # main renderer's current visible area.
        self.minimap_renderer = vtk.vtkRenderer()
        self.minimap_renderer.SetBackground(0.15, 0.15, 0.15)
        self.minimap_renderer.SetViewport(0.02, 0.02, 0.28, 0.28)
        self.minimap_renderer.SetLayer(1)
        self.minimap_renderer.InteractiveOff()
        render_window.AddRenderer(self.minimap_renderer)

        interactor = render_window.GetInteractor()
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())

        self.lut = vtk.vtkLookupTable()
        self.lut.SetValueRange(0.0, 1.0)
        self.lut.SetSaturationRange(0.0, 0.0)
        self.lut.Build()

        self.image_actor = vtk.vtkImageActor()
        self.image_actor.GetProperty().SetLookupTable(self.lut)
        self.image_actor.GetProperty().UseLookupTableScalarRangeOn()
        self.image_actor.VisibilityOff()
        self.renderer.AddActor(self.image_actor)

        # Same image data, second actor -- the minimap always shows the
        # WHOLE slice; only the main renderer's camera zooms/pans.
        self.minimap_actor = vtk.vtkImageActor()
        self.minimap_actor.GetProperty().SetLookupTable(self.lut)
        self.minimap_actor.GetProperty().UseLookupTableScalarRangeOn()
        self.minimap_actor.VisibilityOff()
        self.minimap_renderer.AddActor(self.minimap_actor)

        # "Current view" rectangle, drawn directly in the minimap's own
        # world coordinates (both actors show the same image at the same
        # physical location, so the main renderer's visible world bounds
        # are meaningful coordinates inside the minimap too).
        self._minimap_rect_poly = vtk.vtkPolyData()
        rect_mapper = vtk.vtkPolyDataMapper()
        rect_mapper.SetInputData(self._minimap_rect_poly)
        self.minimap_rect_actor = vtk.vtkActor()
        self.minimap_rect_actor.SetMapper(rect_mapper)
        # Same red + width 2 as the app's own minimap rectangle
        # (Minimap.rectangle_render, utils/minimap_handler.py:273-274).
        self.minimap_rect_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
        self.minimap_rect_actor.GetProperty().SetLineWidth(2)
        self.minimap_rect_actor.GetProperty().SetRepresentationToWireframe()
        self.minimap_rect_actor.VisibilityOff()
        self.minimap_renderer.AddActor(self.minimap_rect_actor)

        # Orientation labels -- same axial convention as core/load_MRI_
        # file.py's add_axes (L at screen-right/R at screen-left --
        # radiological convention -- A at top, P at bottom).
        self._axis_label_actors = []
        for text, x, y in (("L", 0.95, 0.5), ("R", 0.05, 0.5), ("A", 0.5, 0.92), ("P", 0.5, 0.06)):
            actor = vtk.vtkTextActor()
            actor.SetInput(text)
            actor.GetTextProperty().SetColor(1.0, 1.0, 0.0)
            actor.GetTextProperty().SetFontSize(16)
            actor.GetTextProperty().SetBold(True)
            actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
            actor.GetPositionCoordinate().SetValue(x, y)
            actor.VisibilityOff()
            self.renderer.AddActor2D(actor)
            self._axis_label_actors.append(actor)

        # Scale bar: reimplements utils/scale_bar.py's Scale class's math
        # standalone (see module docstring for why it isn't reused
        # directly), recomputed on every zoom/pan.
        self._scale_line = vtk.vtkLineSource()
        scale_mapper = vtk.vtkPolyDataMapper2D()
        scale_mapper.SetInputConnection(self._scale_line.GetOutputPort())
        self.scale_actor = vtk.vtkActor2D()
        self.scale_actor.SetMapper(scale_mapper)
        self.scale_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
        self.scale_actor.GetProperty().SetLineWidth(3)
        self.scale_actor.SetPositionCoordinate(vtk.vtkCoordinate())
        self.scale_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        # Right-aligned (position recomputed in _refresh_scale_bar to
        # account for the bar's current on-screen length -- same "0.95 -
        # length" right-alignment convention as utils/scale_bar.py's own
        # Scale.create_bar) -- opposite corner from the minimap.
        self.scale_actor.GetPositionCoordinate().SetValue(0.90, 0.06)
        self.scale_actor.VisibilityOff()
        self.renderer.AddActor2D(self.scale_actor)

        self.scale_text = vtk.vtkTextActor()
        self.scale_text.GetTextProperty().SetColor(0.0, 1.0, 0.0)
        self.scale_text.GetTextProperty().SetFontSize(13)
        self.scale_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        self.scale_text.GetPositionCoordinate().SetValue(0.90, 0.09)
        self.scale_text.VisibilityOff()
        self.renderer.AddActor2D(self.scale_text)

        self._arr_zyx = None
        self._spacing = None  # (sx, sy, sz), SimpleITK order
        self._camera_initialized = False
        self._plan_data = None  # parsed plan JSON, for bregma/lambda/shanks
        self._dynamic_actors = []  # bregma/lambda markers + shank lines,
        # rebuilt every _show_slice call (same idea as check_points_in_
        # slice/draw_electrode_line re-running per slice, trajectory_
        # planning/rendering.py)

        self.slider.valueChanged.connect(self._on_slider_changed)
        buttons['zoom_in'].clicked.connect(lambda: self.zoom(self._ZOOM_IN_FACTOR))
        buttons['zoom_out'].clicked.connect(lambda: self.zoom(self._ZOOM_OUT_FACTOR))
        buttons['go_up'].clicked.connect(lambda: self.pan(0, self._PAN_DISTANCE))
        buttons['go_down'].clicked.connect(lambda: self.pan(0, -self._PAN_DISTANCE))
        buttons['go_left'].clicked.connect(lambda: self.pan(-self._PAN_DISTANCE, 0))
        buttons['go_right'].clicked.connect(lambda: self.pan(self._PAN_DISTANCE, 0))
        buttons['fit'].clicked.connect(self.fit_to_window)

        # vtkInteractorStyleImage's own default bindings already give
        # right-drag/scroll = zoom and middle-drag = pan for free (left-drag
        # is window/level -- brightness/contrast -- not pan); double-click
        # resets, and both button- and mouse-driven interaction keep the
        # minimap rectangle/scale bar in sync.
        interactor.AddObserver('LeftButtonDoubleClickEvent', lambda o, e: self.fit_to_window())
        interactor.AddObserver('InteractionEvent', lambda o, e: self._refresh_overlays())
        interactor.AddObserver('EndInteractionEvent', lambda o, e: self._refresh_overlays())
        interactor.Initialize()

    def load(self, mri_path, data=None):
        """data: the parsed plan JSON (FileOutput.compute()'s output,
        trajectory_planning/file_input_output.py), used to draw bregma/
        lambda and shank trajectories on top of the slice -- optional
        purely so this class stays usable without a plan (matches
        SurgeryMRIPreview.render's own data requirement, but this view can
        still show the bare scan if data is somehow unavailable)."""
        img = sitk.ReadImage(mri_path)
        # Axis0/1/2 = axial/coronal/sagittal, and mri_insert/mri_deep voxel
        # indices, only line up once the image is canonically RAS-oriented
        # -- same as every other consumer of this scan's grid (LoadMRI.
        # volumes[0].oriented_ref_image, file_handling/mri_volume.py:56).
        img = sitk.DICOMOrient(img, "RAS")
        self._spacing = img.GetSpacing()
        self._arr_zyx = sitk.GetArrayFromImage(img).astype(np.float32)
        self._plan_data = data
        depth = self._arr_zyx.shape[0]  # z (axial slice count)
        self.slider.blockSignals(True)
        self.slider.setMinimum(0)
        self.slider.setMaximum(max(depth - 1, 0))
        self.slider.setValue(depth // 2)
        self.slider.blockSignals(False)
        self._camera_initialized = False
        self._show_slice(depth // 2)

    def clear(self):
        self._arr_zyx = None
        self._plan_data = None
        self._clear_dynamic_actors()
        for actor in (self.image_actor, self.minimap_actor, self.scale_actor,
                      self.scale_text, self.minimap_rect_actor, *self._axis_label_actors):
            actor.VisibilityOff()
        self.slider.blockSignals(True)
        self.slider.setMinimum(0)
        self.slider.setMaximum(0)
        self.slider.blockSignals(False)
        self.vtk_widget.GetRenderWindow().Render()

    def _on_slider_changed(self, value):
        if self._arr_zyx is not None:
            self._show_slice(value)

    def _show_slice(self, z_index):
        z_index = int(np.clip(z_index, 0, self._arr_zyx.shape[0] - 1))
        # Only a left-right flip, matching ImageLayer's own flip=True
        # default exactly (core/image_layer.py:9,47) -- NOT the flipud this
        # view's earlier QImage-based version also needed. QImage treats
        # row 0 as the top of the display; vtkImageData treats row 0 as the
        # BOTTOM (Y-up world convention) -- opposite conventions, so the
        # vertical flip that corrected the QImage version would silently
        # re-invert this one. The app's own real VTK pipeline never
        # applies a vertical flip, only this horizontal one.
        sl = np.fliplr(self._arr_zyx[z_index, :, :])  # (Y, X)
        sl = np.ascontiguousarray(sl)
        h, w = sl.shape
        sx, sy, _sz = self._spacing

        vtk_arr = numpy_support.numpy_to_vtk(sl.ravel(order='C'), deep=True, array_type=vtk.VTK_FLOAT)
        img_vtk = vtk.vtkImageData()
        img_vtk.SetDimensions(w, h, 1)
        img_vtk.SetSpacing(sx, sy, 1.0)
        img_vtk.GetPointData().SetScalars(vtk_arr)

        self.image_actor.SetInputData(img_vtk)
        self.image_actor.VisibilityOn()
        self.minimap_actor.SetInputData(img_vtk)
        self.minimap_actor.VisibilityOn()
        for actor in (self.scale_actor, self.scale_text, self.minimap_rect_actor, *self._axis_label_actors):
            actor.VisibilityOn()

        # Same default "reset" window as the main viewer's Contrast class
        # (utils/contrast.py: vminmax_perc = [0, 0.99999]).
        vmin, vmax = np.percentile(sl, [0, 99.999])
        self.lut.SetTableRange(float(vmin), float(vmax))
        self.lut.Build()

        if not self._camera_initialized:
            self.renderer.ResetCamera()
            self.renderer.GetActiveCamera().ParallelProjectionOn()
            self.minimap_renderer.ResetCamera()
            self.minimap_renderer.GetActiveCamera().ParallelProjectionOn()
            self._camera_initialized = True

        self._update_landmarks(z_index)
        self._refresh_overlays()
        self.vtk_widget.GetRenderWindow().Render()

    # ---- bregma/lambda + shank trajectories, re-drawn every slice change
    # -- mirrors trajectory_planning/rendering.py's check_points_in_slice
    # (exact voxel-index equality for point visibility) and
    # draw_electrode_line (always-visible dim projected line + a bright
    # segment only where the trajectory crosses a +/-0.5 voxel band around
    # the current slice), adapted to this view's own left-right flip and
    # single fixed axial orientation ----

    def _clear_dynamic_actors(self):
        for actor in self._dynamic_actors:
            self.renderer.RemoveActor(actor)
        self._dynamic_actors = []

    def _flip_x(self, x_voxel):
        """mri_insert/mri_deep/coords_bregma/coords_lambda are voxel indices
        into the UNFLIPPED array (self._arr_zyx); the displayed image had
        np.fliplr applied, so a point's displayed X index is the mirror of
        its stored one -- same relationship _show_slice's own display
        uses, just applied to a single coordinate instead of a whole row."""
        x_size = self._arr_zyx.shape[2]
        return (x_size - 1) - x_voxel

    def _update_landmarks(self, z_index):
        self._clear_dynamic_actors()
        if self._plan_data is None:
            return
        sx, sy, _sz = self._spacing
        raw = self._plan_data["raw"]

        for voxel_key, mm_key, color in (
            ("coords_bregma", "bregma_mm", (1.0, 0.0, 0.0)),
            ("coords_lambda", "lambda_mm", (0.0, 1.0, 0.0)),
        ):
            voxel = raw[voxel_key]
            # Exact index equality, same as check_points_in_slice
            # (rendering.py:46-57) -- a point either sits on this slice or
            # it doesn't, no dimmed "nearby" state for a single point.
            if round(voxel[2]) != z_index:
                continue
            mm = raw[mm_key]
            x_mm = self._flip_x(mm[0] / sx) * sx
            self._add_point_marker(x_mm, mm[1], color)

        shank_keys = sorted(self._plan_data["shanks"], key=lambda k: int(k.split("_")[1]))
        for i, key in enumerate(shank_keys):
            shank_raw = self._plan_data["shanks"][key]["raw"]
            insert_vox = np.array(shank_raw["mri_insert"], dtype=float)
            deep_vox = np.array(shank_raw["mri_deep"], dtype=float)
            color = _SHANK_COLORS[i % len(_SHANK_COLORS)]
            self._add_shank_line(insert_vox, deep_vox, z_index, color, sx, sy)

    def _add_point_marker(self, x_mm, y_mm, color, radius=0.3):
        src = vtk.vtkRegularPolygonSource()
        src.SetNumberOfSides(24)
        src.SetRadius(radius)
        src.SetCenter(x_mm, y_mm, 0.5)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(src.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetOpacity(0.9)
        self.renderer.AddActor(actor)
        self._dynamic_actors.append(actor)

    def _add_shank_line(self, a_vox, b_vox, z_index, color, sx, sy):
        """a_vox/b_vox: mri_insert/mri_deep, (x,y,z) voxel indices in the
        UNFLIPPED grid. Draws a dim full-length projection (always) plus a
        bright segment clipped to wherever the trajectory crosses the
        current slice's +/-0.5 voxel band -- direct port of
        draw_electrode_line's parametric clip (rendering.py:790-818), just
        working in this view's own mm/flip convention instead of atlas
        voxels with a per-view axis permutation."""
        def to_xy_mm(v):
            return self._flip_x(v[0]) * sx, v[1] * sy

        pa = to_xy_mm(a_vox)
        pb = to_xy_mm(b_vox)

        dim_line = vtk.vtkLineSource()
        dim_line.SetPoint1(pa[0], pa[1], 0.3)
        dim_line.SetPoint2(pb[0], pb[1], 0.3)
        dim_mapper = vtk.vtkPolyDataMapper()
        dim_mapper.SetInputConnection(dim_line.GetOutputPort())
        dim_actor = vtk.vtkActor()
        dim_actor.SetMapper(dim_mapper)
        dim_actor.GetProperty().SetColor(*color)
        dim_actor.GetProperty().SetOpacity(0.4)
        dim_actor.GetProperty().SetLineWidth(3)
        self.renderer.AddActor(dim_actor)
        self._dynamic_actors.append(dim_actor)

        denom = b_vox[2] - a_vox[2]
        if abs(denom) < 1e-6:
            if abs(a_vox[2] - z_index) <= 0.5:
                t_min, t_max = 0.0, 1.0
            else:
                t_min, t_max = 0.0, 0.0
        else:
            t_min = ((z_index - 0.5) - a_vox[2]) / denom
            t_max = ((z_index + 0.5) - a_vox[2]) / denom
            if t_min > t_max:
                t_min, t_max = t_max, t_min
        t_min = max(0.0, t_min)
        t_max = min(1.0, t_max)

        if t_min < t_max:
            p1 = to_xy_mm(a_vox + t_min * (b_vox - a_vox))
            p2 = to_xy_mm(a_vox + t_max * (b_vox - a_vox))
            bright_line = vtk.vtkLineSource()
            bright_line.SetPoint1(p1[0], p1[1], 0.4)
            bright_line.SetPoint2(p2[0], p2[1], 0.4)
            bright_mapper = vtk.vtkPolyDataMapper()
            bright_mapper.SetInputConnection(bright_line.GetOutputPort())
            bright_actor = vtk.vtkActor()
            bright_actor.SetMapper(bright_mapper)
            bright_actor.GetProperty().SetColor(*color)
            bright_actor.GetProperty().SetLineWidth(6)
            self.renderer.AddActor(bright_actor)
            self._dynamic_actors.append(bright_actor)

    # ---- zoom / pan / fit, self-contained versions of utils/zoom.py's
    # Zoom.zoom/Zoom.fit_to_window and utils/minimap_handler.py's Minimap.
    # pan_arrows (same math, confirmed against gui_utils/buttons_gui3D.py's
    # exact wiring) without their app-wide shared state ----

    def zoom(self, factor):
        if self._arr_zyx is None:
            return
        camera = self.renderer.GetActiveCamera()
        camera.SetParallelScale(camera.GetParallelScale() / factor)
        self.renderer.ResetCameraClippingRange()
        self._refresh_overlays()
        self.vtk_widget.GetRenderWindow().Render()

    def pan(self, diff_x, diff_y):
        if self._arr_zyx is None:
            return
        camera = self.renderer.GetActiveCamera()
        fp = camera.GetFocalPoint()
        pos = camera.GetPosition()
        camera.SetFocalPoint(fp[0] + diff_x, fp[1] + diff_y, fp[2])
        camera.SetPosition(pos[0] + diff_x, pos[1] + diff_y, pos[2])
        self.renderer.ResetCameraClippingRange()
        self._refresh_overlays()
        self.vtk_widget.GetRenderWindow().Render()

    def fit_to_window(self, *_args):
        if self._arr_zyx is None:
            return
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.ResetCameraClippingRange()
        self._refresh_overlays()
        self.vtk_widget.GetRenderWindow().Render()

    def _refresh_overlays(self):
        if self._arr_zyx is None:
            return
        self._refresh_scale_bar()
        self._refresh_minimap_rect()

    def _refresh_scale_bar(self, length_mm=1.0):
        camera = self.renderer.GetActiveCamera()
        window_width, window_height = self.vtk_widget.GetRenderWindow().GetSize()
        if not window_width or not window_height:
            return
        half_height_world = camera.GetParallelScale()
        world_per_px = (2 * half_height_world) / window_height
        if world_per_px <= 0:
            return

        # Keep the bar a reasonable on-screen fraction regardless of zoom
        # level by stepping the represented length up/down in decades,
        # same idea as Scale.create_bar's cm/mm switch.
        length_px = length_mm / world_per_px
        frac = length_px / window_width
        while frac > 0.4 and length_mm < 1000:
            length_mm *= 10
            length_px = length_mm / world_per_px
            frac = length_px / window_width
        while frac < 0.05 and length_mm > 1e-3:
            length_mm /= 10
            length_px = length_mm / world_per_px
            frac = length_px / window_width

        self._scale_line.SetPoint1(0, 0, 0)
        self._scale_line.SetPoint2(length_px, 0, 0)
        self._scale_line.Update()

        # Right-align: anchor the bar so it ends near the right edge
        # regardless of its current length, same "0.95 - length" technique
        # utils/scale_bar.py's own Scale.create_bar uses.
        x_anchor = 0.95 - frac
        self.scale_actor.GetPositionCoordinate().SetValue(x_anchor, 0.06)
        self.scale_text.GetPositionCoordinate().SetValue(x_anchor, 0.09)

        if length_mm >= 10:
            self.scale_text.SetInput(f"{length_mm / 10:g} cm")
        else:
            self.scale_text.SetInput(f"{length_mm:g} mm")

    def _refresh_minimap_rect(self):
        camera = self.renderer.GetActiveCamera()
        half_h = camera.GetParallelScale()
        w, h = self.vtk_widget.GetRenderWindow().GetSize()
        if not h:
            return
        half_w = half_h * (w / h)
        cx, cy, _cz = camera.GetFocalPoint()
        xmin, xmax = cx - half_w, cx + half_w
        ymin, ymax = cy - half_h, cy + half_h

        points = vtk.vtkPoints()
        # Slightly in front of the image plane (z=0) so the rectangle
        # doesn't z-fight with the minimap's own image actor.
        for x, y in ((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)):
            points.InsertNextPoint(x, y, 0.1)
        lines = vtk.vtkCellArray()
        for i in range(4):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, (i + 1) % 4)
            lines.InsertNextCell(line)
        self._minimap_rect_poly.SetPoints(points)
        self._minimap_rect_poly.SetLines(lines)
        self._minimap_rect_poly.Modified()
