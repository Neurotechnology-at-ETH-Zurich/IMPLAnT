# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QMessageBox
from during_surgery.reprojection import refresh_surgery_summary
from during_surgery.mri_preview import SurgeryMRIPreview
from during_surgery.axial_view import SurgeryAxialView


class SurgeryController:
    """Owns the Surgery tab's state and behavior, entirely independent of
    TrajectoryPlanning/LoadMRI: correcting bregma/lambda with real
    intraoperative measurements only needs the per-shank ap_mm/rl_mm/dv_mm
    offsets a saved plan's PDF already carries (FileOutput.compute()'s
    per-shank raw block, trajectory_planning/file_input_output.py) -- never
    a loaded MRI, registration, or rendering context. One instance is
    created in MainWindow.__init__ and lives for the app's whole session,
    unlike TrajectoryPlanning which only exists while an MRI is loaded.

    surgery_shank_offsets is named to match what during_surgery/
    reprojection.py's refresh_surgery_summary(tp, ...) already expects on
    its first argument (originally written for a TrajectoryPlanning
    instance) -- this class is a drop-in stand-in for that narrow purpose,
    exposing just .ui and .surgery_shank_offsets.

    .ui is a live property rather than cached at construction time: on a
    "full restart" (MainWindow's restart_gui), self.MW.ui is replaced with
    a brand new Ui_MainWindow() instance while this controller itself is
    NOT recreated -- caching the old .ui here would silently keep talking
    to torn-down widgets after a restart."""

    def __init__(self, MW):
        self.MW = MW
        self.surgery_shank_offsets = {}
        self._mri_preview = None
        self._mri_preview_container = None
        self._axial_view = None
        self._axial_view_container = None
        self._step_popup_shown = False

    @property
    def ui(self):
        return self.MW.ui

    @property
    def mri_preview(self):
        # Lazy + rebuilt-on-identity-change rather than built once in
        # __init__: on a "full restart" (MainWindow.restart_gui), self.ui
        # is replaced with a brand new Ui_MainWindow(), so self.ui.widget
        # becomes a different object too -- a QtInteractor embedded in the
        # old one would silently keep rendering into a torn-down widget.
        if self._mri_preview is None or self._mri_preview_container is not self.ui.widget:
            self._mri_preview = SurgeryMRIPreview(self.ui.widget, self.ui)
            self._mri_preview_container = self.ui.widget
        return self._mri_preview

    @property
    def axial_view(self):
        # Same lazy/rebuilt-on-restart reasoning as mri_preview above.
        if self._axial_view is None or self._axial_view_container is not self.ui.widget_axialView:
            buttons = {
                'zoom_in': self.ui.zoom_in_surgery,
                'zoom_out': self.ui.zoom_out_surgery,
                'go_up': self.ui.go_up_surgery,
                'go_down': self.ui.go_down_surgery,
                'go_left': self.ui.go_left_surgery,
                'go_right': self.ui.go_right_surgery,
                'fit': self.ui.fit_to_zoom_surgery,
            }
            self._axial_view = SurgeryAxialView(self.ui.widget_axialView, self.ui.Scroll_surgery, buttons)
            self._axial_view_container = self.ui.widget_axialView
        return self._axial_view

    def load_plan(self, data, pdf_path=None):
        """Called by LoadSurgeryPlan once a report PDF's embedded JSON has
        been parsed. Populates the summary table immediately (bregma/
        lambda default to 0,0,0 until measured), updates the "loaded plan"
        label, and -- if the MRI can be located (see SurgeryMRIPreview.
        locate_resampled_mri) -- renders the original planned trajectories
        in 3D and a scrollable 2D axial slice (SurgeryAxialView) over it.
        Both are non-fatal if the MRI can't be found, since the numeric
        table is what the surgery tab is actually for."""
        shank_keys = sorted(data["shanks"], key=lambda k: int(k.split("_")[1]))
        self.surgery_shank_offsets = {
            i: (data["shanks"][key]["raw"]["ap_mm"],
                data["shanks"][key]["raw"]["rl_mm"],
                data["shanks"][key]["raw"]["dv_mm"])
            for i, key in enumerate(shank_keys)
        }
        # TODO: tp.ui.label is the Surgery tab's placeholder "loaded plan"
        # label's current (auto-generated) objectName -- update this once
        # the Surgery tab's widgets are renamed to something more specific.
        self.ui.label.setText(f"Loaded: {data.get('mri_file', '(unknown)')}")
        self.on_bregma_lambda_changed()

        mri_path = None
        if pdf_path is not None:
            mri_path = self.mri_preview.locate_resampled_mri(
                pdf_path, data.get("individual_id"), data["raw"]["mri_spacing"])
        if mri_path is not None:
            self.mri_preview.render(mri_path, data)
            self.axial_view.load(mri_path, data)
        else:
            self.mri_preview.clear()
            self.axial_view.clear()

        if not self._step_popup_shown:
            self.show_step_popup()
            self._step_popup_shown = True

    def show_step_popup(self):
        """Wired to pushButton_questionmark_2 (re-showable on demand, same
        convention as pushButton_questionmark/_samri -> show_step_
        instructions in main_window.py), and shown once automatically the
        first time a plan is loaded."""
        msg_box = QMessageBox(self.MW)
        msg_box.setWindowTitle("Surgery Tab")
        msg_box.setText("\n".join(f"{i + 1}. {s}" for i, s in enumerate([
            "Type Bregma and Lambda as measured on the manipulator, in mm "
            "from your null point (not clicked on the MRI) -- ML/AP/DV, "
            "signed, negative values allowed.",
            "The table below updates live: each shank's target position, "
            "in that same mm-from-null frame -- dial those numbers into "
            "the manipulator.",
            "The 3D view shows the ORIGINAL planned positions only, for "
            "visual reference -- it does not update with the correction "
            "above (see the \"Original Positions\" label on it).",
        ])))
        msg_box.addButton("OK", QMessageBox.ActionRole)
        msg_box.exec()

    def on_bregma_lambda_changed(self):
        """Wired to all 6 measured-mm spinboxes' valueChanged (see
        MainWindow.add_actions). Bregma/lambda here are signed mm offsets
        from an arbitrary stereotaxic-manipulator null point -- NOT MRI
        voxel picks (see during_surgery/reprojection.py) -- so this is a
        parallel computation over its own coordinate frame, not a
        correction feeding back into any MRI-space state."""
        bregma_null_mm = [self.ui.doubleSpinBox_sag_b.value(),
                           self.ui.doubleSpinBox_cor_b.value(),
                           self.ui.doubleSpinBox_ax_b.value()]
        lambda_null_mm = [self.ui.doubleSpinBox_sag_l.value(),
                           self.ui.doubleSpinBox_cor_l.value(),
                           self.ui.doubleSpinBox_ax_l.value()]
        refresh_surgery_summary(self, bregma_null_mm, lambda_null_mm)
