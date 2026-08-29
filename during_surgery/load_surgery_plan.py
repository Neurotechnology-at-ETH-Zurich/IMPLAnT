# This Python file uses the following encoding: utf-8
import json as _json
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from pypdf import PdfReader
from paths_config import _paths
from gui_utils.busy_overlay import BusyOverlay


class LoadSurgeryPlan(QtWidgets.QDialog):
    """Reads a previously saved trajectory report PDF's embedded
    trajectory_planning_data.json (see FileOutput._attach_reload_data,
    trajectory_planning/file_input_output.py) and hands the parsed plan to
    MW.surgery (during_surgery/surgery_controller.py's SurgeryController).

    Deliberately independent of TrajectoryPlanning/LoadMRI: correcting
    bregma/lambda with real intraoperative measurements only needs the
    per-shank ap_mm/rl_mm/dv_mm offsets already stored in the plan, never a
    loaded MRI, registration, or rendering context -- the surgeon only ever
    picks a PDF here, nothing else."""

    def __init__(self, MW, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load Surgery Plan")
        self.setModal(True)
        self.MW = MW

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel(
            "Select a previously saved Trajectory Report PDF to load its "
            "planned shank offsets."))

        path_layout = QtWidgets.QHBoxLayout()
        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setPlaceholderText("Report PDF path…")
        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(self.browse)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse)
        layout.addLayout(path_layout)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.load_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Trajectory Report",
            _paths['raw_base'],
            "PDF files (*.pdf)"
        )
        if path:
            self.path_edit.setText(path)

    def load_and_accept(self):
        path = self.path_edit.text().strip()
        if not path:
            return

        try:
            reader = PdfReader(path)
            attachment = reader.attachments["trajectory_planning_data.json"][0]
        except (KeyError, IndexError, FileNotFoundError):
            QtWidgets.QMessageBox.critical(
                self, "No trajectory data found",
                "This PDF has no embedded trajectory data -- it may have "
                "been saved before this feature was added, or isn't a "
                "trajectory report.")
            return
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Could not read PDF", str(exc))
            return

        data = _json.loads(attachment)
        self.MW._save_session_state('surgery', path=path)
        # Close this dialog first rather than blocking it on the (possibly
        # slow -- locating + reading the MRI file, building the 3D preview)
        # load_plan() call -- a BusyOverlay over the main window gives
        # feedback instead of the picker just sitting there unresponsive.
        self.accept()
        self.MW.overlay = BusyOverlay(self.MW, message="Loading surgery plan, please wait…")
        self.MW.overlay.run(self.MW.surgery.load_plan, data, pdf_path=path)
