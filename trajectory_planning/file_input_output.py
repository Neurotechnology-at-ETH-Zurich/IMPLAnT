# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QBuffer, QIODevice
import os
import re
import sys
import io
import json as _json
import numpy as np
import vtk
from vtk.util import numpy_support
import pyvista as pv
import SimpleITK as sitk
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
import sys
from gui_utils.busy_overlay import BusyOverlay
from paths_config import _paths

class FileInput(QtWidgets.QDialog):
    """
    A dialog window that allows users to specify anatomical regions and MRID tags (for 4D data).
    """
    def __init__(self, MW,parent=None):
        """
        Initialize the input dialog UI and connect signals.
        """
        super().__init__(parent)
        self.setWindowTitle("Select Files for Bregma and Lambda Detection")
        self.setModal(True)
        self.MW = MW
        self.file_name_main = []
        self.file_name_another = []

        main_layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QPlainTextEdit("Please select raw, non-registered MRI images needed for a manaul Bregma and Lambda Detection")
        text.setReadOnly(True)
        main_layout.addWidget(text)

        self.first_time = True
        file_layout = QtWidgets.QHBoxLayout()
        self.file_line_main = QtWidgets.QTextEdit()
        self.file_line_main.setText("Please select your Main Image")
        self.file_line_main.setReadOnly(True)
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_main)
        file_layout.addWidget(self.file_line_main)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)


        file_layout = QtWidgets.QHBoxLayout()
        self.file_line_another = QtWidgets.QTextEdit()
        self.file_line_another.setText("Please click to add Another Image. Otherwise only the main image will be used.")
        self.file_line_another.setReadOnly(True)
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_another)
        file_layout.addWidget(self.file_line_another)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)


        new_spacing_um = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Resampling spacing [um]")
        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.setMinimum(10)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(50)
        new_spacing_um.addWidget(label)
        new_spacing_um.addWidget(self.spinbox)
        main_layout.addLayout(new_spacing_um)

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

        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        # Add the buttons to the same layout
        button_layout.addWidget(buttons)
        # Add the whole layout to your main layout
        main_layout.addLayout(button_layout)

    def validate_and_accept(self):
        if not self.file_name_main:
            QtWidgets.QMessageBox.warning(
                self, "Missing file", "Please select the Main Image before continuing.")
            return
        self.accept()

    def browse_file_main(self):
        file_name = self.open_file()
        if file_name:
            self.file_name_main = file_name
            self.file_line_main.setText(os.path.basename(file_name))

    def browse_file_another(self):
        file_name = self.open_file()
        if file_name:
            self.file_name_another = file_name
            self.file_line_another.setText(os.path.basename(file_name))

    def open_file(self):
        # Pickle file that contains all the design parameters of each MRID tag
        if self.first_time:
            file_name, _ = QFileDialog.getOpenFileName(
                None,
                "Open NIfTI File",
                _paths['raw_base'],
                "NIfTI files (*.nii.gz)"
            )
            self.first_time = False
        else:
            file_name, _ = QFileDialog.getOpenFileName(
                None,
                "Open NIfTI File",
                "",
                "NIfTI files (*.nii.gz)"
            )

        #User cancelled
        if not file_name:
            return []
        return file_name

    def get_values(self):
        return self.file_name_main,self.file_name_another,self.spinbox.value()/1000


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = FileInput()
    if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        data = dlg.get_values()



class FileOutput(QtWidgets.QDialog):
    """Save a trajectory planning report as a multi-page PDF: one page per
    shank with its coronal + sagittal clipped views (each re-clipped to
    that shank's own trajectory, since shanks don't all lie on the same
    slice) and a numeric caption, followed by the shank geometry plot and
    a rendered-text summary page with the per-shank numbers. The same
    numbers -- plus the exact bregma/lambda/shank coordinates needed to
    reconstruct the plan -- are also embedded as a JSON file attachment
    inside the PDF (see _attach_reload_data), since the visible pages are
    flattened bitmaps with no extractable text of their own."""

    def __init__(self, MW, mri_file_path,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Trajectory Report")
        self.setModal(True)
        self.MW = MW
        self.mri_file_path = mri_file_path

        tp = self.MW.LoadMRI.TrajPlanning
        missing = [i + 1 for i in range(tp.ui.comboBox_Shanks.count())
                   if tp.coords_insert_point.get(i) is None
                   or tp.coords_deepest_point.get(i) is None]
        if missing:
            shanks_str = ", ".join(str(s) for s in missing)
            QtWidgets.QMessageBox.warning(
                self, "Incomplete trajectories",
                f"Shank(s) {shanks_str} do not have a trajectory "
                "(insertion/deepest point) yet. They will be skipped when saving.")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel(
            "Save a PDF report (view screenshots + summary) of the trajectory planning."))

        path_layout = QtWidgets.QHBoxLayout()
        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setPlaceholderText("Output file path…")
        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(self.browse)
        path_layout.addWidget(self.path_edit)
        # No dedicated subject/animal ID is tracked anywhere on the MRI-load
        # path (checked LoadMRI, Metadata -- nothing) -- fall back to the
        # scan's own filename so the report can still be tied back to
        # exactly which MRI it came from.
        subject_id = os.path.basename(mri_file_path)
        for ext in (".nii.gz", ".nii"):
            if subject_id.lower().endswith(ext):
                subject_id = subject_id[:-len(ext)]
                break
        # The full BIDS-style stem (sub-X_ses-Y_task-Z_acq-W-ind_N) is more
        # than needed for a report filename -- keep just the animal ("sub-…",
        # stopping at the next "_key-" segment so an underscore inside the
        # subject id itself, e.g. "sub-rEO_10", isn't mistaken for a
        # boundary) and the trailing "ind_N" (this scan's own per-volume
        # index, see utils/mrid_inputdialog.py's identical "ind_" convention).
        # Falls back to the full stem if either piece isn't found, rather
        # than silently producing a garbled/empty name for a differently
        # named file.
        sub_match = re.match(r'(sub-.+?)(?=_[A-Za-z]+-|$)', subject_id)
        ind_match = re.search(r'(ind_\d+)$', subject_id)
        short_id = f"{sub_match.group(1)}-{ind_match.group(1)}" if sub_match and ind_match else subject_id
        default_path = f"{os.path.dirname(mri_file_path)}/trajectory_planning-{short_id}.pdf"
        self.path_edit.setText(default_path)
        path_layout.addWidget(browse)
        layout.addLayout(path_layout)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


    def browse(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Trajectory Report", "", "PDF files (*.pdf)")
        if path:
            self.path_edit.setText(path)

    def save_and_accept(self):
        path = self.path_edit.text().strip()
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        # capture_pages -- especially the MRI-space path, which clips/
        # renders two off-screen plotters per shank -- can take a real,
        # noticeable few seconds; without this the whole dialog just
        # freezes with no feedback until it's done.
        BusyOverlay(self, "Generating PDF report…").run(self._generate_and_save, path)

    def _generate_and_save(self, path):
        tp = self.MW.LoadMRI.TrajPlanning
        try:
            summary = self.compute(tp)
        except ValueError as exc:
            QtWidgets.QMessageBox.critical(self, "Cannot compute report", str(exc))
            return
        pages = self.capture_pages(tp, summary)
        if not pages:
            QtWidgets.QMessageBox.warning(
                self, "Nothing to save", "No views could be captured.")
            return
        pages[0].save(path, save_all=True, append_images=pages[1:])
        self._attach_reload_data(path, summary)
        self.accept()

    def _attach_reload_data(self, path, summary):
        """Embed `summary` (bregma/lambda + per-shank points, in the exact
        voxel/mm values compute() worked from, under summary['raw']) as a
        real file attachment inside the just-written PDF -- the report
        pages themselves are flattened bitmaps (see _summary_page) with no
        selectable/extractable text, so this is the only way a Surgery Tab
        can later re-read this plan's exact numbers back out of the PDF
        without OCR."""
        data = _json.dumps(summary, indent=2).encode("utf-8")
        reader = PdfReader(path)
        writer = PdfWriter()
        writer.append(reader)
        writer.add_attachment("trajectory_planning_data.json", data)
        with open(path, "wb") as f:
            writer.write(f)

    def capture_pages(self, tp, summary):
        pages = []
        pages.extend(self._capture_shank_views(tp, summary))

        dfx_plot = getattr(tp, "dfx_plot", None)
        if dfx_plot is not None and getattr(tp, "dfx_shank_data", None):
            pages.append(self._label_page(self._grab_widget(dfx_plot), "Shank geometry"))

        pages.append(self._summary_page(summary))
        return pages

    _PDF_PANEL_SIZE = (600, 600)

    def _placeholder_image(self, reference_img):
        """Grey stand-in for a panel that couldn't be rendered (e.g. no
        MRI-space geometry yet for this shank) -- sized to match whichever
        other panel in the same row DID render, so the page's grid still
        lines up, or a fixed default if neither did."""
        size = reference_img.size if reference_img is not None else self._PDF_PANEL_SIZE
        img = Image.new("RGB", size, (200, 200, 200))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Not available", fill="black", font=ImageFont.load_default(size=18))
        return img

    def _capture_shank_views(self, tp, summary):
        """One page per shank: coronal (top row) + sagittal (bottom row),
        each showing the atlas-space view (left) next to the real MRI-space
        view (right) side by side, re-clipped to that shank's own
        trajectory in each space (they don't all lie on the same slice, and
        the atlas<->MRI registration is a nonlinear warp so the two spaces'
        own directions can disagree slightly). Atlas-space reuses the
        on-screen Vis3D clipped-view panes; MRI-space uses dedicated
        off-screen plotters, since it has no visible on-screen counterpart
        -- see _render_clipped_mri."""
        pages = []
        vis = getattr(tp, "Vis3D", None)
        have_mri = getattr(tp, 'movingImg_resampled', None) is not None

        # The clipped-slice VTK panes sit behind a default page in their
        # stacked widgets until a trajectory toggles them into view; force
        # them visible here or the render window is never actually shown
        # and screenshots come out black.
        prev_coronal = tp.ui.stackedWidget_coronal.currentIndex()
        prev_sagittal = tp.ui.stackedWidget_sagittal.currentIndex()
        if vis is not None:
            tp.ui.stackedWidget_coronal.setCurrentIndex(1)
            tp.ui.stackedWidget_sagittal.setCurrentIndex(1)
            QtWidgets.QApplication.processEvents()

        plotter_co = pv.Plotter(off_screen=True, window_size=self._PDF_PANEL_SIZE) if have_mri else None
        plotter_sa = pv.Plotter(off_screen=True, window_size=self._PDF_PANEL_SIZE) if have_mri else None
        up = (0.0, 0.0, 1.0)
        axis_y = np.array([0.0, 1.0, 0.0])
        axis_x = np.array([1.0, 0.0, 0.0])

        def clip_normals(direction):
            # Same "project world axis orthogonal to the shank" trick used
            # by the coronal/sagittal view toggle buttons (rendering.py:
            # change_view_coronal/sagittal) -- keeps the shank's full
            # length shown edge-on regardless of its own tilt.
            normal_co = axis_y - np.dot(axis_y, direction) * direction
            normal_co /= np.linalg.norm(normal_co)
            if normal_co[1] < 0:
                normal_co *= -1
            normal_sa = axis_x - np.dot(axis_x, direction) * direction
            normal_sa /= np.linalg.norm(normal_sa)
            if normal_sa[0] > 0:
                normal_sa *= -1
            return tuple(normal_co), tuple(normal_sa)

        try:
            for shank_num in sorted(tp.coords_insert_point):
                if (tp.coords_insert_point[shank_num] is None
                        or tp.coords_deepest_point[shank_num] is None):
                    continue
                direction = tp.direction_atlas.get(shank_num)
                if direction is None:
                    continue

                img_atlas_co = img_atlas_sa = None
                if vis is not None:
                    normal_co, normal_sa = clip_normals(direction)
                    vis.render_clipped(normal_co, 'coronal', shank_num)
                    vis.render_clipped(normal_sa, 'sagittal', shank_num)
                    QtWidgets.QApplication.processEvents()
                    # the on-screen atlas panes are whatever size their widget
                    # happens to be (usually much smaller than the MRI-space
                    # panels' fixed 600x600 off-screen render) -- normalized
                    # to the same panel size below. render_clipped itself
                    # (visualisation3D.py's _bg_colors_for_shank) already
                    # pales every region this shank does NOT pass through,
                    # so no extra pass is needed here.
                    img_atlas_co = self._screenshot_plotter(vis.plotter_co)
                    img_atlas_sa = self._screenshot_plotter(vis.plotter_sa)

                img_mri_co = img_mri_sa = None
                if have_mri:
                    mri_insert = tp.mri_insert.get(shank_num)
                    mri_deep = tp.mri_deep.get(shank_num)
                    if mri_insert is not None and mri_deep is not None:
                        spacing = np.array(tp.movingImg_resampled.GetSpacing())
                        mri_dir = (np.array(mri_insert, dtype=float) - np.array(mri_deep, dtype=float)) * spacing
                        mri_dir_norm = np.linalg.norm(mri_dir)
                        if mri_dir_norm > 1e-9:
                            mri_normal_co, mri_normal_sa = clip_normals(mri_dir / mri_dir_norm)
                            plotter_co.clear()
                            plotter_sa.clear()
                            ok_co = self._render_clipped_mri(plotter_co, tp, shank_num, mri_normal_co, up, 'coronal')
                            ok_sa = self._render_clipped_mri(plotter_sa, tp, shank_num, mri_normal_sa, up, 'sagittal')
                            # add_mesh above is always called with render=False, and
                            # Plotter.screenshot() only forces its own internal render()
                            # the very first time a given plotter is ever screenshotted --
                            # since plotter_co/plotter_sa are reused across every shank in
                            # this loop, every later shank's .clear() + re-add would never
                            # get re-rendered and screenshot() would just grab the stale/
                            # blank framebuffer left over from clear() (a black panel).
                            # Render explicitly every time instead of relying on that
                            # one-shot behavior.
                            if ok_co:
                                plotter_co.render()
                                img_mri_co = Image.fromarray(plotter_co.screenshot())
                            if ok_sa:
                                plotter_sa.render()
                                img_mri_sa = Image.fromarray(plotter_sa.screenshot())

                if not any((img_atlas_co, img_atlas_sa, img_mri_co, img_mri_sa)):
                    continue

                # normalize every panel to the same pixel size -- the
                # on-screen atlas panes come out whatever size their widget
                # happens to be, which doesn't otherwise match the MRI-space
                # panels' fixed off-screen render size.
                img_atlas_co, img_atlas_sa, img_mri_co, img_mri_sa = (
                    img.resize(self._PDF_PANEL_SIZE) if img is not None else None
                    for img in (img_atlas_co, img_atlas_sa, img_mri_co, img_mri_sa))

                top_row = self._side_by_side_page(
                    img_atlas_co if img_atlas_co is not None else self._placeholder_image(img_mri_co),
                    f"Shank {shank_num + 1} - Coronal (Atlas)",
                    img_mri_co if img_mri_co is not None else self._placeholder_image(img_atlas_co),
                    f"Shank {shank_num + 1} - Coronal (MRI)")
                bottom_row = self._side_by_side_page(
                    img_atlas_sa if img_atlas_sa is not None else self._placeholder_image(img_mri_sa),
                    f"Shank {shank_num + 1} - Sagittal (Atlas)",
                    img_mri_sa if img_mri_sa is not None else self._placeholder_image(img_atlas_sa),
                    f"Shank {shank_num + 1} - Sagittal (MRI)")

                width = max(top_row.width, bottom_row.width)
                page = Image.new("RGB", (width, top_row.height + bottom_row.height), "white")
                page.paste(top_row, (0, 0))
                page.paste(bottom_row, (0, top_row.height))

                entry = summary["shanks"].get(f"shank_{shank_num + 1}")
                if entry is not None:
                    page = self._overlay_caption(page, self._shank_caption(entry))
                pages.append(page)
        finally:
            if vis is not None:
                tp.ui.stackedWidget_coronal.setCurrentIndex(prev_coronal)
                tp.ui.stackedWidget_sagittal.setCurrentIndex(prev_sagittal)
                # Re-render whichever shank is currently selected so the
                # on-screen views are left exactly as the user had them
                # before saving.
                vis.refresh_clipped_views(tp.ui.comboBox_Shanks.currentIndex())
            if plotter_co is not None:
                plotter_co.close()
            if plotter_sa is not None:
                plotter_sa.close()

        return pages

    def _get_mri_masked_volume(self, tp):
        """Cached pv.ImageData of the subject's OWN MRI intensity data, in
        true MRI space (movingImg_resampled's own grid -- no atlas warp
        involved, this literally IS the real scan the animal was scanned
        with), masked down to just the brain via mri_grid_not_background_
        mask (excludes atlas label 0, "Clear Label"/background, reprojected
        onto this grid via the atlas<->MRI correspondence table)."""
        if getattr(self, '_mri_masked_volume', None) is not None:
            return self._mri_masked_volume
        mri_img = tp.movingImg_resampled
        data_zyx = sitk.GetArrayFromImage(mri_img).astype(np.float32)
        mask = tp.mri_grid_not_background_mask()
        data_zyx = np.where(mask, data_zyx, 0.0)
        data_xyz = np.transpose(data_zyx, (2, 1, 0))
        vol = pv.ImageData()
        vol.dimensions = np.array(data_xyz.shape) + 1
        vol.spacing = mri_img.GetSpacing()
        vol.origin = (0.0, 0.0, 0.0)
        vol.cell_data['MRI'] = data_xyz.flatten(order='F')
        self._mri_masked_volume = vol.threshold(value=1e-6, scalars='MRI')
        return self._mri_masked_volume

    def _render_clipped_mri(self, plotter, tp, shank_number, normal, up, view):
        """MRI-space analogue of Visualisation3D.render_clipped -- clips a
        thin slab out of the real, masked MRI intensity volume (see
        _get_mri_masked_volume) through the shank's own MRI-space
        position, colored by true MRI grayscale intensity rather than
        atlas region-label colors. Camera convention (up/focal point/
        clip-thickness/parallel projection) mirrors render_clipped so the
        resulting picture reads the same way. Returns False (nothing
        drawn) if this shank has no MRI-space geometry yet or the clip
        misses the volume entirely."""
        mri_insert = tp.mri_insert.get(shank_number)
        mri_deep = tp.mri_deep.get(shank_number)
        if mri_insert is None or mri_deep is None:
            return False
        spacing = np.array(tp.movingImg_resampled.GetSpacing())
        insert_mm = np.array(mri_insert, dtype=float) * spacing
        deep_mm = np.array(mri_deep, dtype=float) * spacing
        focal_point = tuple((insert_mm + deep_mm) / 2)

        vol = self._get_mri_masked_volume(tp)
        distance = 60
        position = tuple(np.array(focal_point) + np.array(normal) * distance)
        plotter.camera.up = up
        plotter.camera.focal_point = focal_point
        plotter.camera.clipping_range = (1e-5, 1e5)
        plotter.disable_parallel_projection()
        plotter.set_position(position)
        plotter.enable_parallel_projection()

        # Clip from both sides to get a thin slab -- clip(normal) keeps the
        # side behind `origin` along -normal, so clipping again from the
        # opposite side at a small offset trims it down to a few voxels
        # thick, same technique as render_clipped's "Front slab".
        thickness = float(np.dot(np.abs(normal), 3 * spacing))
        back_origin = tuple(np.array(focal_point) - np.array(normal) * thickness)
        slab = vol.clip(normal=normal, origin=focal_point)
        slab = slab.clip(normal=tuple(-n for n in normal), origin=back_origin)
        if slab.n_cells == 0:
            return False

        plotter.add_mesh(
            slab, scalars='MRI', cmap='gray', show_scalar_bar=False,
            opacity=1, style='surface', pickable=False, name='mri_slab',
            reset_camera=False, render=False,
        )
        self._draw_electrode_lines_mri(plotter, tp, shank_number)
        return True

    _MRI_SHANK_TIP_EXTENSION_MM = 4.0  # matches draw_electrode_lines' atlas-space convention

    def _draw_electrode_lines_mri(self, plotter, tp, active_shank):
        """MRI-space analogue of Visualisation3D.draw_electrode_lines --
        without this, the MRI-space report pages showed a bare anatomical
        slice with no indication of the planned trajectory at all. Draws
        every shank's own line, extended past the insertion point (outside
        the brain, same distance/convention as the atlas-space version),
        plus channel-point dots for the non-active shanks; the active
        shank is left dot-free and drawn thicker, exactly matching
        draw_electrode_lines' own convention."""
        spacing = np.array(tp.movingImg_resampled.GetSpacing())
        atlas_spacing = np.array(tp.fixedImg.GetSpacing())
        dark_grey = (0.3, 0.3, 0.3)
        for shank_idx in sorted(tp.mri_deep):
            deep = tp.mri_deep.get(shank_idx)
            insert = tp.mri_insert.get(shank_idx)
            if deep is None or insert is None:
                continue
            deep_mm = np.array(deep, dtype=float) * spacing
            insert_mm = np.array(insert, dtype=float) * spacing
            direction = insert_mm - deep_mm
            length = np.linalg.norm(direction)
            if length < 1e-6:
                continue
            direction /= length
            end_mm = insert_mm + direction * self._MRI_SHANK_TIP_EXTENSION_MM

            is_active = (shank_idx == active_shank)
            color = tp.get_shank_vtk_color(shank_idx) if hasattr(tp, 'get_shank_vtk_color') else (0.0, 1.0, 28 / 255)

            plotter.add_mesh(
                pv.Line(deep_mm, end_mm), color=color, opacity=1.0,
                line_width=4 if is_active else 2, name=f"mri_electrode_line_{shank_idx}",
                render=False, reset_camera=False,
            )
            label_pt = pv.PolyData(end_mm.reshape(1, 3))
            plotter.add_point_labels(
                label_pt, [f"Shank {shank_idx + 1}"],
                text_color='white', font_size=16, shape=None, bold=True, shadow=False,
                show_points=False, always_visible=True,
                name=f"mri_shank_label_{shank_idx}", render=False, reset_camera=False,
            )

            if not is_active:
                pts = tp.channel_points.get(shank_idx)
                if pts is not None and len(pts) > 0:
                    # channel_points are stored in atlas voxel coordinates --
                    # same atlas-mm -> mri-idx -> mri-mm conversion used
                    # throughout the codebase for warping points into MRI
                    # space (see atlas_points_to_mri_indices's own docstring).
                    pts_mm = np.asarray(pts, dtype=float) * atlas_spacing
                    mri_pts_mm = tp.atlas_points_to_mri_indices(pts_mm) * spacing
                    plotter.add_mesh(
                        pv.PolyData(mri_pts_mm.astype(np.float32)), color=dark_grey,
                        point_size=6, name=f"mri_channel_points_{shank_idx}",
                        render_points_as_spheres=True, render=False,
                        show_scalar_bar=False, reset_camera=False,
                    )

    def _screenshot_plotter(self, plotter):
        """Grab pixels straight from the render window's back buffer rather
        than pyvista's default screenshot(), which reads the front buffer --
        that comes back black whenever the widget is covered (e.g. by this
        very save dialog) or not the currently visible page."""
        plotter.render()
        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(plotter.render_window)
        w2i.ReadFrontBufferOff()
        w2i.ShouldRerenderOn()
        w2i.Update()
        vtk_image = w2i.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        arr = numpy_support.vtk_to_numpy(vtk_image.GetPointData().GetScalars())
        arr = arr.reshape(height, width, -1)[::-1]
        if arr.shape[-1] == 4:
            arr = arr[:, :, :3]
        return Image.fromarray(arr.astype(np.uint8))

    def _grab_widget(self, widget):
        pixmap = widget.grab()
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "PNG")
        return Image.open(io.BytesIO(bytes(buffer.data())))

    def _label_page(self, img, title):
        img = img.convert("RGB")
        band_h = 40
        canvas = Image.new("RGB", (img.width, img.height + band_h), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), title, fill="black", font=ImageFont.load_default(size=22))
        canvas.paste(img, (0, band_h))
        return canvas

    def _side_by_side_page(self, img_left, label_left, img_right, label_right):
        left = self._label_page(img_left, label_left)
        right = self._label_page(img_right, label_right)
        height = max(left.height, right.height)
        canvas = Image.new("RGB", (left.width + right.width, height), "white")
        canvas.paste(left, (0, 0))
        canvas.paste(right, (left.width, 0))
        return canvas

    def _shank_caption(self, entry):
        point = entry["insertion_point"]
        return [
            f"Insertion point:  AP {point['AP_mm']}    RL {point['RL_mm']}"
            f"    Depth: {entry['insertion_depth_mm']} mm",
            f"Roll (bregma-lambda-CC plane): {entry['roll_deg']} deg    "
            f"Pitch (horizontal plane): {entry['pitch_deg']} deg",
        ]

    def _overlay_caption(self, canvas, lines):
        """Burn the caption into the screenshot itself: a semi-transparent
        bar over the bottom of the image, rather than extra whitespace
        appended below it."""
        font_body = ImageFont.load_default(size=18)
        line_h = 24
        band_h = 12 + line_h * len(lines)

        rgba = canvas.convert("RGBA")
        overlay = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([0, rgba.height - band_h, rgba.width, rgba.height],
                        fill=(0, 0, 0, 170))
        y = rgba.height - band_h + 6
        for line in lines:
            draw.text((10, y), line, fill="white", font=font_body)
            y += line_h
        return Image.alpha_composite(rgba, overlay).convert("RGB")

    def _summary_page(self, summary):
        font_title = ImageFont.load_default(size=22)
        font_body = ImageFont.load_default(size=16)
        canvas = Image.new("RGB", (850, 1100), "white")
        draw = ImageDraw.Draw(canvas)
        y = 30
        draw.text((30, y), "Trajectory Planning Summary", fill="black", font=font_title)
        y += 40
        draw.text((30, y), f"Bregma-Lambda distance: {summary['bregma_lambda_distance_mm']:.3f} mm",
                   fill="black", font=font_body)
        y += 26
        bregma_mm = summary["raw"]["bregma_mm"]
        lambda_mm = summary["raw"]["lambda_mm"]
        draw.text((30, y), f"Bregma (mm): {bregma_mm[0]:.3f}, {bregma_mm[1]:.3f}, {bregma_mm[2]:.3f}"
                            f"    Lambda (mm): {lambda_mm[0]:.3f}, {lambda_mm[1]:.3f}, {lambda_mm[2]:.3f}",
                   fill="black", font=font_body)
        y += 40
        for name, entry in summary["shanks"].items():
            point = entry["insertion_point"]
            draw.text((30, y), name.replace("_", " ").title(), fill="black", font=font_title)
            y += 26
            draw.text((50, y), f"Insertion point:  AP {point['AP_mm']}    "
                                f"RL {point['RL_mm']}",
                       fill="black", font=font_body)
            y += 22
            draw.text((50, y), f"Roll (bregma-lambda-CC plane): {entry['roll_deg']} deg    "
                                f"Pitch (horizontal plane): {entry['pitch_deg']} deg",
                       fill="black", font=font_body)
            y += 22
            draw.text((50, y), f"Depth (deepest point to insertion point): "
                                f"{entry['insertion_depth_mm']} mm",
                       fill="black", font=font_body)
            y += 22
            if "dxf_file" in entry:
                draw.text((50, y), f"DXF file: {entry['dxf_file']}", fill="black", font=font_body)
                y += 22
            y += 20
        return canvas

    def compute(self, tp):
        mri_spacing = np.array(tp.movingImg_resampled.GetSpacing())  # XYZ mm/voxel

        # "-ind_N" is this lab's existing convention for which animal a scan
        # belongs to within a multi-animal session (mrid_utils/handlers.py:
        # find_ind_data/find_resampled_img already parse it the same way).
        # Stored here so a Surgery Tab can auto-locate the raw scan from just
        # the saved PDF's folder + this id, with no manual file picking --
        # matched on "-ind_N" (dash) rather than a bare substring so a
        # derived/aligned file like "..._to_ind_2..." (underscore before
        # "ind_", referencing ind_2 as a target, not its own index) doesn't
        # get misread as this scan's own id.
        individual_match = re.search(r'-(ind_\d+)', os.path.basename(self.mri_file_path))
        individual_id = individual_match.group(1) if individual_match else None

        # Bregma and lambda in physical mm
        bregma_mm = np.array(tp.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(tp.coords_lambda, dtype=float) * mri_spacing

        if not np.isfinite(bregma_mm).all() or not np.isfinite(lambda_mm).all():
            raise ValueError(
                f"Bregma/Lambda produced a non-finite coordinate.\n"
                f"coords_bregma={tp.coords_bregma!r}  coords_lambda={tp.coords_lambda!r}\n"
                f"mri_spacing={mri_spacing.tolist()!r}\n"
                f"bregma_mm={bregma_mm.tolist()!r}  lambda_mm={lambda_mm.tolist()!r}")

        # Bregma-lambda axis and distance
        bl_vec = lambda_mm - bregma_mm
        bl_dist = float(np.linalg.norm(bl_vec))
        if bl_dist <= 1e-9:
            raise ValueError(
                f"Bregma and Lambda resolve to the same physical point "
                f"(distance={bl_dist}).\n"
                f"coords_bregma={tp.coords_bregma!r}  coords_lambda={tp.coords_lambda!r}\n"
                f"bregma_mm={bregma_mm.tolist()!r}  lambda_mm={lambda_mm.tolist()!r}")
        bl_axis = bl_vec / bl_dist  # unit vector bregma → lambda

        # Plane through bregma-lambda with normal closest to Z (dorso-ventral)
        z_approx = np.array([0.0, 0.0, 1.0])
        plane_normal = z_approx - np.dot(z_approx, bl_axis) * bl_axis
        plane_normal /= np.linalg.norm(plane_normal)
        # Second in-plane axis: perpendicular to bl_axis, in the horizontal plane
        x_axis = np.cross(plane_normal, bl_axis)
        x_axis /= np.linalg.norm(x_axis)

        shanks = {}
        for shank_num in sorted(tp.coords_insert_point):
            if tp.coords_insert_point[shank_num] is None or tp.coords_deepest_point[shank_num] is None:
                continue
            if tp.mri_insert[shank_num] is None or tp.mri_deep[shank_num] is None:
                continue

            insert_mm = np.array(tp.mri_insert[shank_num], dtype=float) * mri_spacing
            deep_mm   = np.array(tp.mri_deep[shank_num],   dtype=float) * mri_spacing

            if not np.isfinite(insert_mm).all() or not np.isfinite(deep_mm).all():
                raise ValueError(
                    f"Shank {shank_num + 1}: insertion/deepest point produced a "
                    f"non-finite coordinate.\n"
                    f"coords_insert_point={tp.coords_insert_point[shank_num]!r}  "
                    f"coords_deepest_point={tp.coords_deepest_point[shank_num]!r}\n"
                    f"mri_insert={tp.mri_insert[shank_num]!r}  mri_deep={tp.mri_deep[shank_num]!r}\n"
                    f"mri_spacing={mri_spacing.tolist()!r}\n"
                    f"insert_mm={insert_mm.tolist()!r}  deep_mm={deep_mm.tolist()!r}")

            # Insertion point in bregma-lambda plane coordinate system (origin = bregma)
            v = insert_mm - bregma_mm
            coord_along_bl  = float(np.dot(v, bl_axis))       # X: along bregma → lambda (AP)
            coord_perp_bl   = float(np.dot(v, x_axis))        # Y: lateral, perpendicular to bl (ML)
            coord_dv_bl     = float(np.dot(v, plane_normal))  # Z: dorsal/ventral offset from the bl plane

            # Depth between the deepest point and the insertion point
            shank_vec  = insert_mm - deep_mm
            shank_dist = float(np.linalg.norm(shank_vec))

            # Roll and pitch: the shank's angle to two bregma/lambda/corpus-
            # callosum-anchored planes -- roll is the angle to the bregma-
            # lambda-CC plane itself (how far the shank leans out of the
            # true sagittal plane, shown in the coronal view), pitch is the
            # angle to the bregma-lambda plane parallel to RL (how far the
            # shank tilts off horizontal, shown in the sagittal view).
            # Single source of truth in compute_shank_roll_pitch_mri
            # (coord_transform.py), shared with the 2D/3D view angle
            # indicators so the two can't silently disagree again.
            roll_pitch = tp.compute_shank_roll_pitch_mri(shank_num)
            roll_deg, pitch_deg = roll_pitch if roll_pitch is not None else (0.0, 0.0)

            ap_str = f"{abs(coord_along_bl):.3f}{'P' if coord_along_bl >= 0 else 'A'}"
            rl_str = f"{abs(coord_perp_bl):.3f}{'R' if coord_perp_bl <= 0 else 'L'}"
            dv_str = f"{abs(coord_dv_bl):.3f}{'D' if coord_dv_bl >= 0 else 'V'}"

            shank_entry = {
                "insertion_point": {"AP_mm": ap_str, "RL_mm": rl_str, "DV_mm": dv_str},
                "roll_deg":  round(roll_deg, 3),
                "pitch_deg": round(pitch_deg, 3),
                "insertion_depth_mm": round(shank_dist, 3),
                # Exact values a Surgery Tab needs to reproduce this plan and
                # recompute roll/pitch after bregma/lambda are corrected with
                # real intraoperative coordinates -- everything above this is
                # rounded/formatted for human reading and isn't precise
                # enough to reconstruct the plan from.
                "raw": {
                    "coords_insert_point": [float(x) for x in tp.coords_insert_point[shank_num]],
                    "coords_deepest_point": [float(x) for x in tp.coords_deepest_point[shank_num]],
                    "mri_insert": [float(x) for x in tp.mri_insert[shank_num]],
                    "mri_deep": [float(x) for x in tp.mri_deep[shank_num]],
                    # Signed mm offset of the insertion point from bregma along
                    # the bl_axis/x_axis/plane_normal frame above -- unlike
                    # AP_mm/RL_mm/DV_mm (rounded, direction-suffixed strings for
                    # human reading), these are exact and sign-preserving, which
                    # is what a Surgery Tab needs to re-anchor this shank's
                    # position to a different (intraoperatively measured)
                    # bregma/lambda without reparsing formatted text.
                    "ap_mm": coord_along_bl,
                    "rl_mm": coord_perp_bl,
                    "dv_mm": coord_dv_bl,
                },
            }

            dfx_data = tp.dfx_shank_data.get(shank_num)
            if dfx_data is not None and dfx_data.get("dxf_file"):
                shank_entry["dxf_file"] = os.path.basename(dfx_data["dxf_file"])

            shanks[f"shank_{shank_num + 1}"] = shank_entry

        return {
            "mri_file": os.path.basename(self.mri_file_path),
            "individual_id": individual_id,
            "bregma_lambda_distance_mm": bl_dist,
            "shanks": shanks,
            "raw": {
                "coords_bregma": [float(x) for x in tp.coords_bregma],
                "coords_lambda": [float(x) for x in tp.coords_lambda],
                "mri_spacing": mri_spacing.tolist(),
                # Physical mm, i.e. coords_bregma/lambda * mri_spacing -- stored
                # directly (rather than left for a reader to re-derive) since
                # it's the anchor point a Surgery Tab's mm-from-null
                # reprojection needs.
                "bregma_mm": bregma_mm.tolist(),
                "lambda_mm": lambda_mm.tolist(),
            },
        }