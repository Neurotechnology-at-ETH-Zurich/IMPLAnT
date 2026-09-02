# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QBuffer, QIODevice, Qt
import os
import re
import sys
import io
import json as _json
import numpy as np
import vtk
from vtk.util import numpy_support
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
import sys
from gui_utils.busy_overlay import BusyOverlay
from paths_config import get_raw_base
from during_surgery.buttons_gui_surgery import build_skull_reference_scene, _PHOTO_CREDIT
from utils.zoom import Zoom

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
                get_raw_base(self),
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
    shank with an atlas-space clipped view (re-clipped to that shank's own
    trajectory, since shanks don't all lie on the same slice) next to a
    screenshot of the real on-screen MRI reslice view, for both coronal and
    sagittal, plus that shank's region sidebar and a numeric caption,
    followed by a rendered-text summary page with the per-shank numbers.
    Each page shows only the focused shank's own geometry (other shanks are
    hidden or dimmed), and the reference plane + roll/pitch angle indicator
    is drawn on the atlas panel (see Visualisation3D.render_clipped). The
    same numbers -- plus the exact bregma/lambda/shank coordinates needed
    to reconstruct the plan -- are also embedded as a JSON file attachment
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
        # boundary)
        # Falls back to the full stem if animal id isn't found, rather
        # than silently producing a garbled/empty name
        sub_match = re.match(r'(sub-.+?)(?=_[A-Za-z]+-|$)', subject_id)
        short_id = f"{sub_match.group(1)}" if sub_match else subject_id
        default_path = f"{os.path.dirname(mri_file_path)}/{short_id}-trajectory_planning.pdf"
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
        # capture_pages -- especially the atlas-space path, which re-clips
        # the Vis3D view per shank -- can take a real, noticeable few
        # seconds; without this the whole dialog just freezes with no
        # feedback until it's done.
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
        pages.append(self._cover_page(summary))
        pages.extend(self._capture_shank_views(tp, summary))
        pages.append(self._summary_page(summary))
        return pages

    _PDF_PANEL_SIZE = (600, 600)

    def _render_scene(self, scene):
        """Same QBuffer/PNG/PIL conversion as _grab_widget, but for a
        QGraphicsScene with no backing widget to .grab() (see _cover_page)."""
        rect = scene.sceneRect()
        pixmap = QtGui.QPixmap(int(rect.width()), int(rect.height()))
        pixmap.fill(Qt.white)
        painter = QtGui.QPainter(pixmap)
        scene.render(painter)
        painter.end()
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "PNG")
        return Image.open(io.BytesIO(bytes(buffer.data())))

    def _wrap_text_to_width(self, draw, text, font, max_width):
        """Greedy word-wrap by actual rendered pixel width (via draw.
        textlength), not a fixed character count -- textwrap.wrap's char
        count assumes a fixed page width, but this page's width is driven
        by the skull photo's own (portrait, narrow) aspect ratio, not a
        constant."""
        words = text.split()
        lines, current = [], ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and draw.textlength(candidate, font=font) > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines

    def _cover_page(self, summary):
        """First page of the report: the exact same skull-reference photo
        (Bregma/Lambda markers, AP/RL axis indicator, per-shank insertion-
        point markers) the Surgery tab's widget_axialView shows -- built
        from during_surgery/buttons_gui_surgery.py's own scene-construction
        code (build_skull_reference_scene), not a re-derivation of it, so
        this page can never drift out of sync with what the Surgery tab
        actually displays. Rendered once, statically, so the plan carries
        this reference even before/without the Surgery tab ever being
        opened for this animal.

        The photo itself is narrow/portrait (a dorsal skull crop), so the
        page canvas is padded out to at least as wide as the other report
        pages (_summary_page's own 850px) rather than staying photo-width
        -- otherwise the title/citation text has nowhere to fit and this
        page reads as a tiny sliver next to the rest of the report."""
        scene, _photo_item = build_skull_reference_scene(summary)
        img = self._render_scene(scene).convert("RGB")

        font_title = ImageFont.load_default(size=22)
        font_caption = ImageFont.load_default(size=14)
        page_width = max(850, img.width + 40)
        title_band_h = 40

        canvas_probe = Image.new("RGB", (1, 1))
        wrapped_credit = self._wrap_text_to_width(
            ImageDraw.Draw(canvas_probe), _PHOTO_CREDIT, font_caption, page_width - 40)
        credit_band_h = 10 + 18 * len(wrapped_credit)

        canvas = Image.new("RGB", (page_width, title_band_h + img.height + credit_band_h), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), "Skull Reference", fill="black", font=font_title)
        canvas.paste(img, ((page_width - img.width) // 2, title_band_h))

        y = title_band_h + img.height + 6
        for line in wrapped_credit:
            w = draw.textlength(line, font=font_caption)
            draw.text(((canvas.width - w) / 2, y), line, fill=(120, 120, 120), font=font_caption)
            y += 18
        return canvas

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
        each showing the atlas-space view (left) next to a screenshot of
        the real on-screen MRI reslice view (right) side by side. Atlas-
        space reuses the on-screen Vis3D clipped-view panes, re-clipped to
        this shank's own atlas-space trajectory (shanks don't all lie on
        the same slice). MRI-space is simply whatever stackedWidget_
        coronal/stackedWidget_sagittal currently show once this shank is
        selected -- the plain axis-aligned reslice, scrolled to a slice
        through this shank's own insert/deepest points, or, while the
        90deg constraint is on for that axis, the constrained oblique
        reslice -- see _capture_mri_screenshot. Every panel is restricted
        to just the focused shank (other shanks' lines/dots/labels are
        hidden or dimmed), and the page ends with that shank's region
        sidebar appended alongside the four panels."""
        pages = []
        vis = getattr(tp, "Vis3D", None)
        have_mri = getattr(tp, 'movingImg_resampled', None) is not None
        # Which axis, if any, is currently 90deg-constrained (mutually
        # exclusive, see ElecGeometryMri.enforce_constraint_90deg/
        # _coronal) -- when set, that axis's MRI panel below shows the
        # real on-screen oblique/constrained view instead of the plain
        # axis-aligned reslice, since a constrained shank's cutting plane
        # is fixed to the true AP=0/RL=0 axis.
        ap_on = tp.ui.checkBox_constraint_90deg.isChecked()
        rl_on = tp.ui.checkBox_constraint_90deg_coronal.isChecked()

        # The clipped-slice VTK panes sit behind a default page in their
        # stacked widgets until a trajectory toggles them into view; force
        # them visible here or the render window is never actually shown
        # and screenshots come out black. This is the baseline page for
        # the rest of this loop -- _capture_mri_screenshot temporarily
        # swaps to whichever page it needs and always restores this one.
        prev_coronal = tp.ui.stackedWidget_coronal.currentIndex()
        prev_sagittal = tp.ui.stackedWidget_sagittal.currentIndex()
        if vis is not None:
            # page 1 now holds the oblique-reslice widgets for
            # checkBox_constraint_90deg (coronal) / _coronal (sagittal) --
            # the clipped-3D-view pages moved to page 2 on both, see
            # change_view_coronal/change_view_sagittal.
            tp.ui.stackedWidget_coronal.setCurrentIndex(2)
            tp.ui.stackedWidget_sagittal.setCurrentIndex(2)
            QtWidgets.QApplication.processEvents()

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
                    # only_shank hides every other shank's line/label/dots so
                    # this page shows just the focused shank. show_plane_and_
                    # angle defaults to True here -- the MRI panel is now a
                    # plain on-screen screenshot with no overlay of its own
                    # (see _capture_mri_screenshot), so the atlas panel is
                    # the only place left to draw the reference plane/angle
                    # indicator.
                    vis.render_clipped(normal_co, 'coronal', shank_num, only_shank=shank_num)
                    vis.render_clipped(normal_sa, 'sagittal', shank_num, only_shank=shank_num)
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
                    img_mri_co = self._capture_mri_screenshot(tp, shank_num, 'coronal', ap_on)
                    img_mri_sa = self._capture_mri_screenshot(tp, shank_num, 'sagittal', rl_on)

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
                    f"Shank {shank_num + 1} - Coronal (MRI, Constrained)" if ap_on
                    else f"Shank {shank_num + 1} - Coronal (MRI)")
                bottom_row = self._side_by_side_page(
                    img_atlas_sa if img_atlas_sa is not None else self._placeholder_image(img_mri_sa),
                    f"Shank {shank_num + 1} - Sagittal (Atlas)",
                    img_mri_sa if img_mri_sa is not None else self._placeholder_image(img_atlas_sa),
                    f"Shank {shank_num + 1} - Sagittal (MRI, Constrained)" if rl_on
                    else f"Shank {shank_num + 1} - Sagittal (MRI)")

                width = max(top_row.width, bottom_row.width)
                page = Image.new("RGB", (width, top_row.height + bottom_row.height), "white")
                page.paste(top_row, (0, 0))
                page.paste(bottom_row, (0, top_row.height))

                entry = summary["shanks"].get(f"shank_{shank_num + 1}")
                if entry is not None:
                    page = self._overlay_caption(page, self._shank_caption(entry))

                sidebar_img = self._grab_shank_sidebar(tp, shank_num)
                if sidebar_img is not None:
                    sidebar_panel = self._label_page(sidebar_img, f"Shank {shank_num + 1} - Regions")
                    scale = page.height / sidebar_panel.height
                    sidebar_panel = sidebar_panel.resize(
                        (max(int(sidebar_panel.width * scale), 1), page.height))
                    combined = Image.new("RGB", (page.width + sidebar_panel.width, page.height), "white")
                    combined.paste(page, (0, 0))
                    combined.paste(sidebar_panel, (page.width, 0))
                    page = combined

                pages.append(page)
        finally:
            if vis is not None:
                tp.ui.stackedWidget_coronal.setCurrentIndex(prev_coronal)
                tp.ui.stackedWidget_sagittal.setCurrentIndex(prev_sagittal)
                # Re-render whichever shank is currently selected so the
                # on-screen views are left exactly as the user had them
                # before saving.
                vis.refresh_clipped_views(tp.ui.comboBox_Shanks.currentIndex())
            # _capture_mri_screenshot restores tp.shank_number after each
            # call, but leaves the oblique reslice plane/markers themselves
            # pointed at whichever shank was captured last -- re-anchor them
            # on the now-restored (originally selected) shank so the on-
            # screen constrained view isn't left showing a different shank's
            # plane than what the user had selected before saving.
            if ap_on:
                tp.update_oblique_coronal_view()
                tp.update_oblique_coronal_crossing_line()
                tp.refresh_oblique_markers('coronal')
            if rl_on:
                tp.update_oblique_sagittal_view()
                tp.update_oblique_sagittal_crossing_line()
                tp.refresh_oblique_markers('sagittal')

        return pages

    def _screenshot_plotter(self, plotter):
        """Grab pixels straight from the render window's back buffer rather
        than pyvista's default screenshot(), which reads the front buffer --
        that comes back black whenever the widget is covered (e.g. by this
        very save dialog) or not the currently visible page."""
        plotter.render()
        return self._screenshot_render_window(plotter.render_window)

    def _screenshot_render_window(self, render_window):
        """Same back-buffer-read technique as _screenshot_plotter, for a raw
        vtkRenderWindow (e.g. the oblique constraint-view widgets, which
        aren't wrapped in a pyvista Plotter)."""
        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(render_window)
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

    def _capture_mri_screenshot(self, tp, shank_num, view, oblique):
        """Screenshot of the actual on-screen MRI reslice widget for
        shank_num. While oblique (checkBox_constraint_90deg/_coronal
        checked for this axis), that's the constrained reslice
        (vtkWidget_data_coronal_3/_sagittal_3) -- a constrained shank's
        cutting plane is fixed to the true AP=0/RL=0 axis (see
        ElecGeometryMri.enforce_constraint_90deg/_coronal), so only this
        on-screen view matches what the constraint actually shows.
        Otherwise it's the plain axis-aligned reslice (vtkWidget_data_
        coronal/_sagittal), first scrolled to a slice through the midpoint
        of this shank's own insert/deepest points -- selecting a shank
        does NOT move the displayed slice on its own (see Cursor.
        scroll_slice/core/load_MRI_file.py's slice_indices), so without
        this every shank's page would show whatever slice was left over
        from the live session -- and, via _fit_to_window, the same
        "fit to window" the GUI's own toolbar button triggers (Zoom.
        fit_to_window), rather than a bare renderer.ResetCamera(): fit_
        to_window also keeps the minimap and scale bar in sync with the
        new zoom, which a plain camera reset would leave stale/wrong.
        Either way, the MRI's window/level is also temporarily switched
        to its auto-computed value (see _apply_auto_contrast) so the
        export isn't washed out by whatever contrast the live session
        happened to be left at. The "Brain Regions"/"Forbidden Regions"
        atlas-color overlays are also temporarily hidden (see
        _save_and_hide_region_layers/_save_and_hide_oblique_label_actors)
        -- a panel titled "(MRI)"/"(MRI, Constrained)" promises a plain
        scan, and the atlas-space panel right next to it already shows
        the colored regions -- and so is the insertion-picking guide line
        (_save_and_hide_insertion_guide), both for the same "plain scan"
        reason and because it can otherwise blow up Zoom.fit_to_window's
        bounds (see draw_electrode_line's matching dim_line clamp in
        rendering_mri.py). Swaps tp.shank_number to shank_num
        (every helper below anchors on self.shank_number) and restores
        it, along with the slice index, camera/minimap/scale bar,
        contrast, overlay visibility, and whatever stacked-widget page
        was showing, before returning -- _capture_shank_views forces
        that page to index 2 (the atlas clipped-3D-view) for every OTHER
        panel in this same per-shank loop, so leaving it on a different
        page here would break the next panel's screenshot."""
        stacked = tp.ui.stackedWidget_coronal if view == 'coronal' else tp.ui.stackedWidget_sagittal
        target_index = 1 if oblique else 0
        prev_index = stacked.currentIndex()
        if prev_index != target_index:
            stacked.setCurrentIndex(target_index)
            QtWidgets.QApplication.processEvents()

        # coords_insert_point/coords_deepest_point are [x, y, z];
        # LoadMRI.slice_indices[0] is [z, y, x].
        point_axis = 1 if view == 'coronal' else 0
        slice_axis = 1 if view == 'coronal' else 2
        prev_slice = tp.LoadMRI.slice_indices[0][slice_axis]

        saved_cameras = None if oblique else self._save_view_cameras(tp)

        prev_shank = tp.shank_number
        tp.shank_number = shank_num
        saved_contrast = self._apply_auto_contrast(tp)
        saved_region_layers = self._save_and_hide_region_layers(tp)
        saved_insertion_guide = self._save_and_hide_insertion_guide(tp)
        saved_oblique_labels = []
        try:
            if oblique:
                widget = tp.ui.vtkWidget_data_coronal_3 if view == 'coronal' else tp.ui.vtkWidget_data_sagittal_3
                if view == 'coronal':
                    tp.update_oblique_coronal_view()
                    tp.update_oblique_coronal_crossing_line()
                else:
                    tp.update_oblique_sagittal_view()
                    tp.update_oblique_sagittal_crossing_line()
                tp.refresh_oblique_markers(view)
                # oblique_label_actor/oblique_sagittal_label_actor are plain
                # vtkActors added straight to the oblique renderer (rendering_
                # mri.py's _build_oblique_label_overlay), not registered as an
                # ImageLayer -- _save_and_hide_region_layers above doesn't
                # reach them, so they're hidden separately here.
                saved_oblique_labels = self._save_and_hide_oblique_label_actors(tp)
            else:
                widget = tp.ui.vtkWidget_data_coronal if view == 'coronal' else tp.ui.vtkWidget_data_sagittal
                insert = tp.coords_insert_point[shank_num]
                deep = tp.coords_deepest_point[shank_num]
                mid = int(round((insert[point_axis] + deep[point_axis]) / 2))
                self.MW.Cursor.scroll_slice(view, 0, 0, val=mid)
                tp.check_points_in_slice()
                Zoom.fit_to_window(widget, tp.LoadMRI.vtk_widgets.values(), tp.LoadMRI.scale_bar,
                                    tp.LoadMRI.vtk_widgets, 0, data_3d=True)
            QtWidgets.QApplication.processEvents()
            return self._screenshot_render_window(widget.GetRenderWindow())
        finally:
            tp.shank_number = prev_shank
            self._restore_contrast(saved_contrast)
            self._restore_region_layers(saved_region_layers)
            self._restore_insertion_guide(saved_insertion_guide)
            self._restore_oblique_label_actors(saved_oblique_labels)
            if not oblique:
                self.MW.Cursor.scroll_slice(view, 0, 0, val=prev_slice)
                tp.check_points_in_slice()
                self._restore_view_cameras(tp, saved_cameras)
            if stacked.currentIndex() != prev_index:
                stacked.setCurrentIndex(prev_index)

    _MRI_VIEW_NAMES = ('axial', 'coronal', 'sagittal')

    def _save_view_cameras(self, tp):
        """Save every 2D view's camera state -- Zoom.fit_to_window
        rescales axial/coronal/sagittal TOGETHER (to keep their relative
        zoom in sync, same as the GUI's own toolbar button), not just
        whichever single view is being screenshotted, so all three need
        saving/restoring around a capture, not just the one in use."""
        saved = {}
        for vn in self._MRI_VIEW_NAMES:
            renderer = tp.LoadMRI.renderers[0][vn]
            camera = renderer.GetActiveCamera()
            saved[vn] = (renderer, camera.GetParallelScale(), camera.GetPosition(),
                         camera.GetFocalPoint(), camera.GetViewUp())
        return saved

    def _restore_view_cameras(self, tp, saved):
        """Undo _save_view_cameras, including re-syncing each view's scale
        bar (fit_to_window updates it to the new zoom; without this it
        would be left showing the export's zoom, not the restored one)."""
        for vn, (renderer, scale, position, focal_point, view_up) in saved.items():
            camera = renderer.GetActiveCamera()
            camera.SetParallelScale(scale)
            camera.SetPosition(position)
            camera.SetFocalPoint(focal_point)
            camera.SetViewUp(view_up)
            renderer.ResetCameraClippingRange()
            bar = getattr(tp.LoadMRI, 'scale_bar', {}).get(vn)
            if bar is not None:
                bar.update_bar(renderer, vn, length_cm=1.0)

    def _apply_auto_contrast(self, tp):
        """Temporarily switch the MRI's window/level to its auto-computed
        value (utils/contrast.py's Contrast.auto -- the same thing the
        GUI's own "Auto" button/Ctrl+J does), so a PDF screenshot isn't
        washed out if the live session happened to be windowed oddly at
        export time. Returns (contrast, (prev_window, prev_level)) for
        _restore_contrast to undo, or None if no Contrast object exists
        for the main MRI (image_index 0)."""
        contrast = getattr(tp.LoadMRI, 'contrast', {}).get(0)
        if contrast is None or 0 not in contrast.window:
            return None
        prev = (contrast.window[0], contrast.level[0])
        contrast.auto(image_index=0)
        return contrast, prev

    def _restore_contrast(self, saved):
        """Undo _apply_auto_contrast, restoring the exact window/level
        (and sliders) the live session had before export."""
        if saved is None:
            return
        contrast, (prev_window, prev_level) = saved
        contrast.window[0] = prev_window
        contrast.level[0] = prev_level
        contrast.block_signals(0, True)
        contrast.display_level_sliders[0].setValue(int(prev_level))
        contrast.display_window_sliders[0].setValue(int(prev_window))
        contrast.level_sliders[0].setValue(int(prev_level))
        contrast.window_sliders[0].setValue(int(prev_window))
        contrast.block_signals(0, False)
        contrast.update_lut_window_level(0)

    def _save_and_hide_region_layers(self, tp):
        """Temporarily hide the "Brain Regions"/"Forbidden Regions" atlas
        overlays (ElecGeometryMri._set_insertion_refinement_layers_visible)
        for a clean, plain-MRI screenshot -- these are orientation aids for
        placing/constraining a shank, not part of what a panel titled
        "(MRI)"/"(MRI, Constrained)" promises. Returns the (layer,
        was_visible) pairs for _restore_region_layers to undo; was_visible
        is read off the layer's own actors (toggle_visibility itself keeps
        no boolean of its own)."""
        saved = []
        for layer_index in (getattr(tp, '_mri_label_overlay_layer_index', None),
                             getattr(tp, '_region_to_avoid_layer_index', None)):
            if layer_index is None:
                continue
            layer = tp.LoadMRI.MW.Layers[0].get(layer_index)
            if layer is None:
                continue
            was_visible = any(actor.GetVisibility()
                               for actors_by_index in layer.actors.values()
                               for actor in actors_by_index.values())
            saved.append((layer, was_visible))
        tp._set_insertion_refinement_layers_visible(False)
        return saved

    def _restore_region_layers(self, saved):
        for layer, was_visible in saved:
            layer.toggle_visibility(was_visible, getattr(layer, 'visibility_btn', None))

    def _save_and_hide_oblique_label_actors(self, tp):
        """Same idea as _save_and_hide_region_layers, but for the oblique/
        constrained views' own atlas-label overlay actors (rendering_mri.
        py's _build_oblique_label_overlay) -- these are separate vtkActors
        added directly to the oblique renderers, NOT registered as an
        ImageLayer, so they aren't covered by the "Brain Regions" toggle
        above and stay visible regardless of it. Returns the actors (with
        their prior visibility) for _restore_oblique_label_actors."""
        actors = [a for a in (getattr(tp, 'oblique_label_actor', None),
                               getattr(tp, 'oblique_sagittal_label_actor', None))
                  if a is not None]
        saved = [(a, a.GetVisibility()) for a in actors]
        for a in actors:
            a.SetVisibility(False)
        return saved

    def _restore_oblique_label_actors(self, saved):
        for actor, was_visible in saved:
            actor.SetVisibility(was_visible)

    def _save_and_hide_insertion_guide(self, tp):
        """Temporarily hide the insertion-picking guide line/markers
        (ElecGeometry._draw_insertion_guide_line_mri's _insertion_guide_
        actor, electrode.py:163-201) for a clean MRI screenshot -- it's a
        page_31-only picking aid (a dashed line out to 1.3x the insert-
        point distance along the shank direction), irrelevant to the
        report and, whenever it lands outside the MRI's own imaged FOV,
        capable of the same Zoom.fit_to_window bounds-inflation bug this
        function also guards against for draw_electrode_line's dim_line
        (see rendering_mri.py's draw_electrode_line). on_next_shank_
        clicked opens this FileOutput dialog BEFORE _return_to_atlas_
        space (the only thing that normally removes this actor set), so
        it's guaranteed to still be attached to both renderers throughout
        the whole per-shank report loop, not just for whichever shank
        happens to still be selected."""
        actors = [actor
                  for view_actors in getattr(tp, '_insertion_guide_actor', {}).values()
                  for actor in view_actors.values()]
        saved = [(a, a.GetVisibility()) for a in actors]
        for a in actors:
            a.SetVisibility(False)
        return saved

    def _restore_insertion_guide(self, saved):
        for actor, was_visible in saved:
            actor.SetVisibility(was_visible)

    def _grab_widget(self, widget):
        pixmap = widget.grab()
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "PNG")
        return Image.open(io.BytesIO(bytes(buffer.data())))

    def _grab_shank_sidebar(self, tp, shank_num):
        """Screenshot of the region sidebar (ShankSidebarWidget) for
        shank_num specifically -- it only ever paints tp.shank_number (the
        currently GUI-selected shank), so the selection is swapped to
        shank_num, repainted synchronously, grabbed, then restored. Setting
        shank_number is a plain attribute assignment with no signal/slot
        side effects of its own (see select_shank in shank.py for the real
        UI-driven path); repaint() forces an immediate synchronous paint so
        no stray Qt event can be processed while the selection is swapped."""
        sidebar = getattr(tp, "shank_sidebar", None)
        if sidebar is None:
            return None
        prev_shank_number = tp.shank_number
        try:
            tp.shank_number = shank_num
            sidebar.repaint()
            return self._grab_widget(sidebar)
        finally:
            tp.shank_number = prev_shank_number
            sidebar.repaint()

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
            f"Roll (bregma-lambda plane): {entry['roll_deg']} deg    "
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
            draw.text((50, y), f"Roll (bregma-lambda plane): {entry['roll_deg']} deg    "
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
            coord_along_bl  = -float(np.dot(v, bl_axis))      # X: along lambda → bregma → anterior (AP); positive = Anterior
            coord_perp_bl   = float(np.dot(v, x_axis))        # Y: lateral, perpendicular to bl (ML)
            coord_dv_bl     = float(np.dot(v, plane_normal))  # Z: dorsal/ventral offset from the bl plane

            # Depth between the deepest point and the insertion point
            shank_vec  = insert_mm - deep_mm
            shank_dist = float(np.linalg.norm(shank_vec))

            # Roll and pitch: the shank's angle to two bregma/lambda/
            # misalignment-anchored planes (ap_rl_si_frame_from_misalignment)
            # -- roll is the angle to the bregma-lambda reference plane
            # itself (how far the shank leans out of the true sagittal
            # plane, shown in the coronal view), pitch is the angle to the
            # bregma-lambda plane parallel to RL (how far the shank tilts
            # off horizontal, shown in the sagittal view).
            # Single source of truth in compute_shank_roll_pitch_mri
            # (coord_transform.py), shared with the 2D/3D view angle
            # indicators so the two can't silently disagree again.
            roll_pitch = tp.compute_shank_roll_pitch_mri(shank_num)
            roll_deg, pitch_deg = roll_pitch if roll_pitch is not None else (0.0, 0.0)

            ap_str = f"{abs(coord_along_bl):.3f}{'A' if coord_along_bl >= 0 else 'P'}"
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