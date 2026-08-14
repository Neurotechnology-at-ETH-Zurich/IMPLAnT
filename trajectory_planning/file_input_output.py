# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QBuffer, QIODevice
import os
import sys
import io
import json as _json
import numpy as np
import vtk
from vtk.util import numpy_support
from PIL import Image, ImageDraw, ImageFont
import sys
_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = _json.load(_f)

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
        self.spinbox.setValue(50)
        self.spinbox.setMaximum(1000)
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
    a text summary page with the per-shank numbers formerly saved to JSON."""

    def __init__(self, MW, mri_file_path,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Trajectory Report")
        self.setModal(True)
        self.MW = MW

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
        default_path = f"{os.path.dirname(mri_file_path)}/trajectory_planning.pdf"
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
        self.accept()

    def capture_pages(self, tp, summary):
        pages = []
        vis = getattr(tp, "Vis3D", None)
        if vis is not None:
            pages.extend(self._capture_shank_views(tp, vis, summary))

        dfx_plot = getattr(tp, "dfx_plot", None)
        if dfx_plot is not None and getattr(tp, "dfx_shank_data", None):
            pages.append(self._label_page(self._grab_widget(dfx_plot), "Shank geometry"))

        pages.append(self._summary_page(summary))
        return pages

    def _capture_shank_views(self, tp, vis, summary):
        """One page per shank: coronal + sagittal, each re-clipped to that
        shank's own trajectory (they don't all lie on the same slice)."""
        pages = []

        # The clipped-slice VTK panes sit behind a default page in their
        # stacked widgets until a trajectory toggles them into view; force
        # them visible here or the render window is never actually shown
        # and screenshots come out black.
        prev_coronal = tp.ui.stackedWidget_coronal.currentIndex()
        prev_sagittal = tp.ui.stackedWidget_sagittal.currentIndex()
        tp.ui.stackedWidget_coronal.setCurrentIndex(1)
        tp.ui.stackedWidget_sagittal.setCurrentIndex(1)
        QtWidgets.QApplication.processEvents()

        try:
            for shank_num in sorted(tp.coords_insert_point):
                if (tp.coords_insert_point[shank_num] is None
                        or tp.coords_deepest_point[shank_num] is None):
                    continue
                direction = tp.direction_atlas.get(shank_num)
                if direction is None:
                    continue

                # Same clip-plane normals as the coronal/sagittal view
                # toggle buttons (rendering.py: change_view_coronal/sagittal).
                axis_y = np.array([0.0, 1.0, 0.0])
                normal_co = axis_y - np.dot(axis_y, direction) * direction
                normal_co /= np.linalg.norm(normal_co)
                if normal_co[1] < 0:
                    normal_co *= -1

                axis_x = np.array([1.0, 0.0, 0.0])
                normal_sa = axis_x - np.dot(axis_x, direction) * direction
                normal_sa /= np.linalg.norm(normal_sa)
                if normal_sa[0] > 0:
                    normal_sa *= -1

                vis.render_clipped(normal_co, 'coronal', shank_num)
                vis.render_clipped(normal_sa, 'sagittal', shank_num)
                QtWidgets.QApplication.processEvents()

                img_co = self._screenshot_plotter(vis.plotter_co)
                img_sa = self._screenshot_plotter(vis.plotter_sa)
                page = self._side_by_side_page(
                    img_co, f"Shank {shank_num + 1} - Coronal",
                    img_sa, f"Shank {shank_num + 1} - Sagittal")

                entry = summary["shanks"].get(f"shank_{shank_num + 1}")
                if entry is not None:
                    page = self._overlay_caption(page, self._shank_caption(entry))
                pages.append(page)
        finally:
            tp.ui.stackedWidget_coronal.setCurrentIndex(prev_coronal)
            tp.ui.stackedWidget_sagittal.setCurrentIndex(prev_sagittal)
            # Re-render whichever shank is currently selected so the on-screen
            # views are left exactly as the user had them before saving.
            vis.refresh_clipped_views(tp.ui.comboBox_Shanks.currentIndex())

        return pages

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
            f"Roll: {entry['roll_deg']} deg    Pitch: {entry['pitch_deg']} deg",
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
        y += 40
        for name, entry in summary["shanks"].items():
            point = entry["insertion_point"]
            draw.text((30, y), name.replace("_", " ").title(), fill="black", font=font_title)
            y += 26
            draw.text((50, y), f"Insertion point:  AP {point['AP_mm']}    "
                                f"RL {point['RL_mm']}",
                       fill="black", font=font_body)
            y += 22
            draw.text((50, y), f"Roll: {entry['roll_deg']} deg    Pitch: {entry['pitch_deg']} deg",
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

            # Roll and pitch: the shank's tilt off vertical (DV axis), as
            # seen in the coronal plane (ML-DV, i.e. roll) and in the
            # sagittal plane (AP-DV, i.e. pitch) -- the two angles used to
            # dial in the insertion on a stereotaxic frame. A zero-length
            # shank vector (insert == deepest point) has no direction, so
            # the angles default to 0.0 instead of a nan from a 0/0
            # division.
            if shank_dist > 1e-9:
                shank_dir = shank_vec / shank_dist
                ap_component = float(np.dot(shank_dir, bl_axis))
                ml_component = float(np.dot(shank_dir, x_axis))
                dv_component = float(np.dot(shank_dir, plane_normal))
                roll_deg  = float(np.degrees(np.arctan2(abs(ml_component), abs(dv_component))))
                pitch_deg = float(np.degrees(np.arctan2(abs(ap_component), abs(dv_component))))
            else:
                roll_deg = 0.0
                pitch_deg = 0.0

            ap_str = f"{abs(coord_along_bl):.3f}{'P' if coord_along_bl >= 0 else 'A'}"
            rl_str = f"{abs(coord_perp_bl):.3f}{'R' if coord_perp_bl <= 0 else 'L'}"
            dv_str = f"{abs(coord_dv_bl):.3f}{'D' if coord_dv_bl >= 0 else 'V'}"

            shank_entry = {
                "insertion_point": {"AP_mm": ap_str, "RL_mm": rl_str, "DV_mm": dv_str},
                "roll_deg":  round(roll_deg, 3),
                "pitch_deg": round(pitch_deg, 3),
                "insertion_depth_mm": round(shank_dist, 3),
            }

            dfx_data = tp.dfx_shank_data.get(shank_num)
            if dfx_data is not None and dfx_data.get("dxf_file"):
                shank_entry["dxf_file"] = os.path.basename(dfx_data["dxf_file"])

            shanks[f"shank_{shank_num + 1}"] = shank_entry

        return {
            "bregma_lambda_distance_mm": bl_dist,
            "shanks": shanks,
        }