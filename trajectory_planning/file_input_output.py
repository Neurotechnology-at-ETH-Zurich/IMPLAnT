# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
import os
import sys
import json as _json
import json
import numpy as np
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'paths_config.json')) as _f:
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
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file_main)
        file_layout.addWidget(self.file_line_main)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)


        file_layout = QtWidgets.QHBoxLayout()
        self.file_line_another = QtWidgets.QTextEdit()
        self.file_line_another.setText("Please click to add Another Image. Otherwise only the main image will be used.")
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

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Add the buttons to the same layout
        button_layout.addWidget(buttons)
        # Add the whole layout to your main layout
        main_layout.addLayout(button_layout)

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
    """Save trajectory planning data per shank as a JSON file."""

    def __init__(self, MW, mri_file_path,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Trajectory Data")
        self.setModal(True)
        self.MW = MW

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Save trajectory planning data (per shank) to JSON."))

        path_layout = QtWidgets.QHBoxLayout()
        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setPlaceholderText("Output file path…")
        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(self._browse)
        path_layout.addWidget(self.path_edit)
        default_path = f"{os.path.dirname(mri_file_path)}/trajectory_planning.json"
        self.path_edit.setText(default_path)
        path_layout.addWidget(browse)
        layout.addLayout(path_layout)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


    def _browse(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Trajectory Data", "", "JSON files (*.json)")
        if path:
            self.path_edit.setText(path)

    def _save_and_accept(self):
        path = self.path_edit.text().strip()
        if not path:
            return
        tp = self.MW.LoadMRI.TrajPlanning
        data = self._compute(tp)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        self.accept()

    def _compute(self, tp):
        mri_spacing = np.array(tp.movingImg_resampled.GetSpacing())  # XYZ mm/voxel

        # Bregma and lambda in physical mm
        bregma_mm = np.array(tp.coords_bregma, dtype=float) * mri_spacing
        lambda_mm = np.array(tp.coords_lambda, dtype=float) * mri_spacing

        # Bregma-lambda axis and distance
        bl_vec = lambda_mm - bregma_mm
        bl_dist = float(np.linalg.norm(bl_vec))
        bl_axis = bl_vec / bl_dist  # unit vector bregma → lambda

        # Plane through bregma-lambda with normal closest to Z (dorso-ventral)
        z_approx = np.array([0.0, 0.0, 1.0])
        plane_normal = z_approx - np.dot(z_approx, bl_axis) * bl_axis
        plane_normal /= np.linalg.norm(plane_normal)
        # Second in-plane axis: perpendicular to bl_axis, in the horizontal plane
        y_axis = np.cross(plane_normal, bl_axis)
        y_axis /= np.linalg.norm(y_axis)

        shanks = {}
        for shank_num in sorted(tp.coords_insert_point):
            if tp.coords_insert_point[shank_num] is None or tp.coords_deepest_point[shank_num] is None:
                continue
            if tp.mri_insert[shank_num] is None or tp.mri_deep[shank_num] is None:
                continue

            insert_mm = np.array(tp.mri_insert[shank_num], dtype=float) * mri_spacing
            deep_mm   = np.array(tp.mri_deep[shank_num],   dtype=float) * mri_spacing

            # Insertion point in bregma-lambda plane coordinate system (origin = bregma)
            v = insert_mm - bregma_mm
            coord_along_bl  = float(np.dot(v, bl_axis))   # X: along bregma → lambda
            coord_perp_bl   = float(np.dot(v, y_axis))    # Y: lateral, perpendicular to bl

            # Shank angle with the bregma-lambda plane
            shank_vec  = insert_mm - deep_mm
            shank_dist = float(np.linalg.norm(shank_vec))
            shank_dir  = shank_vec / shank_dist
            # angle between shank and plane = arcsin(|shank · plane_normal|)
            angle_deg  = float(np.degrees(np.arcsin(np.clip(abs(np.dot(shank_dir, plane_normal)), 0.0, 1.0))))

            ap_str = f"{abs(coord_along_bl):.3f}{'P' if coord_along_bl >= 0 else 'A'}"
            rl_str = f"{abs(coord_perp_bl):.3f}{'R' if coord_perp_bl >= 0 else 'L'}"

            shanks[f"shank_{shank_num + 1}"] = {
                "AP_mm":                    ap_str,
                "RL_mm":                    rl_str,
                "shank_angle_to_plane_deg": round(angle_deg, 3),
                "insertion_depth_mm":       round(shank_dist, 3),
            }

        return {
            "bregma_lambda_distance_mm": bl_dist,
            "shanks": shanks,
        }