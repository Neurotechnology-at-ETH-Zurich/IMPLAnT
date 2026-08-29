# This Python file uses the following encoding: utf-8
"""
Surgery-day counterpart to FileOutput.compute()'s position math
(trajectory_planning/file_input_output.py): re-anchors each shank's
saved bregma-relative offset to bregma/lambda measured intraoperatively
as signed mm offsets from an arbitrary stereotaxic-manipulator null
point, instead of picked on the MRI.

Kept in its own package (mirroring trajectory_planning_3d/'s standalone-
class pattern rather than trajectory_planning/'s mixin-composition one)
since none of this needs to be mixed into TrajectoryPlanning -- it only
ever needs a `tp` instance passed in explicitly.
"""
import numpy as np
from PySide6.QtWidgets import QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtCore import Qt


def reproject_target_to_null(bregma_null_ml_ap, lambda_null_ml_ap, ap_mm, rl_mm, bl_dist_plan_mm):
    """
    2D counterpart to compute()'s own bl_axis/x_axis construction
    (trajectory_planning/file_input_output.py's compute()): this rig no
    longer measures a DV/vertical position for Bregma/Lambda (see
    main_window.py's add_actions -- the "ax" spinboxes were removed), so
    there's no intraoperative data left to re-level roll/pitch or a DV
    component with; both are simply carried over from the saved plan
    unchanged (see refresh_surgery_summary). Dropping the DV component
    makes z_approx=(0,0,1) EXACTLY perpendicular to this whole problem
    (rather than merely approximately, as when a real DV measurement
    could tilt bl_axis out of the horizontal plane) -- so this is an
    exact reduction of compute()'s 3D math to 2D, not an approximation.

    bregma_null_ml_ap/lambda_null_ml_ap: (ML/RL, AP) mm-from-null pairs,
    in that order -- matching the "sag"=ML/RL, "cor"=AP dial convention
    shared with the main viewer's own sagittal/coronal slice-index
    ordering (main_window.py's add_actions comment).

    bl_dist_plan_mm: this plan's own Bregma-Lambda distance in true
    anatomical mm (summary['bregma_lambda_distance_mm'], trajectory_
    planning/file_input_output.py's compute()). Dial-mm and anatomical-mm
    are the same PHYSICAL unit, but aren't guaranteed to be the same
    NUMBER for the same real distance: the surgeon's own MEASURED
    Bregma-Lambda separation on the rig (bl_dist_null below) can differ
    from the MRI-planned one (probe-placement precision, scan distortion,
    calibration drift), and that ratio is exactly the same per-animal
    scale correction _mri_to_photo_affine already applies for the
    skull-photo markers (during_surgery/buttons_gui_surgery.py) --
    applying it here too keeps each shank's target POSITION accurate
    even when the measured distance doesn't exactly match the plan, not
    just its direction.

    Returns (ml_target, ap_target): the mm-from-null values to dial into
    the manipulator's own ML/RL and AP stages -- or None if bregma/
    lambda are coincident, or bl_dist_plan_mm is degenerate.
    """
    bregma = np.asarray(bregma_null_ml_ap, dtype=float)
    lambda_pt = np.asarray(lambda_null_ml_ap, dtype=float)
    bl_vec = lambda_pt - bregma
    bl_dist_null = float(np.linalg.norm(bl_vec))
    if bl_dist_null <= 1e-9 or bl_dist_plan_mm <= 1e-9:
        return None
    bl_axis = bl_vec / bl_dist_null  # (ML, AP) unit vector, bregma -> lambda

    # Exact 2D reduction of cross((0,0,1), bl_axis) with the DV slot
    # dropped -- see docstring above.
    x_axis = np.array([-bl_axis[1], bl_axis[0]])

    scale = bl_dist_null / bl_dist_plan_mm  # dial-mm per anatomical-mm
    target = bregma + scale * (ap_mm * bl_axis + rl_mm * x_axis)
    return float(target[0]), float(target[1])


def null_point_ap_rl(bregma_null_mm, lambda_null_mm, bl_dist_plan_mm):
    """The manipulator's own null point (dial reading (0,0)), expressed as
    an (ap_mm, rl_mm) offset from BREGMA in true anatomical mm -- i.e. the
    INVERSE of reproject_target_to_null's own bregma + scale*(ap_mm*
    bl_axis + rl_mm*x_axis) construction (see its docstring for what
    bl_dist_plan_mm/scale are and why), solved for (ap_mm, rl_mm) given
    target = (0, 0). bl_axis/x_axis are orthonormal, so this is just two
    dot products (plus undoing the scale), not a real matrix inversion.

    Used to draw a marker for the null point on the Surgery tab's skull
    photo (during_surgery/buttons_gui_surgery.py's update_null_point) --
    it's purely a rig-calibration choice, unrelated to the animal's own
    anatomy, so it often lands well outside the photo entirely.

    Returns None if bregma/lambda are coincident, or bl_dist_plan_mm is
    degenerate."""
    bregma_null_mm = np.asarray(bregma_null_mm, dtype=float)
    lambda_null_mm = np.asarray(lambda_null_mm, dtype=float)
    bl_vec = lambda_null_mm - bregma_null_mm
    bl_dist_null = float(np.linalg.norm(bl_vec))
    if bl_dist_null <= 1e-9 or bl_dist_plan_mm <= 1e-9:
        return None
    bl_axis = bl_vec / bl_dist_null
    x_axis = np.array([-bl_axis[1], bl_axis[0]])

    scale = bl_dist_null / bl_dist_plan_mm
    to_null = -bregma_null_mm / scale
    ap_mm = float(np.dot(to_null, bl_axis))
    rl_mm = float(np.dot(to_null, x_axis))
    return ap_mm, rl_mm


def _direction_suffix(ap_mm=None, rl_mm=None):
    """Same sign convention as file_input_output.py's compute() own
    ap_str/rl_str formatting (positive ap_mm -> Posterior, negative ->
    Anterior; positive rl_mm -> Left, negative/zero -> Right) -- reused
    here as a plain letter suffix rather than copied/re-derived, so a
    positive number always means the same direction everywhere in the
    app."""
    if ap_mm is not None:
        return 'P' if ap_mm >= 0 else 'A'
    return 'R' if rl_mm <= 0 else 'L'


def refresh_surgery_summary(tp, bregma_null_mm, lambda_null_mm):
    """
    Recompute every loaded shank's target position in the surgeon's
    manipulator-null-relative mm frame from the just-measured bregma/
    lambda (already sign-corrected by the Surgery tab's invert
    checkboxes upstream of this call), scaled by this plan's own
    Bregma-Lambda distance (see reproject_target_to_null's own docstring),
    and populate the Surgery tab's summary table with the result,
    alongside each shank's angle to the AP/RL plane (pitch_deg -- see
    _set(row, 3, ...) below) and insertion depth -- carried over unchanged
    from the saved plan (see reproject_target_to_null's own docstring for
    why: no DV measurement means it can't be intraoperatively re-leveled).
    roll_deg is loaded but intentionally not shown here -- this rig has no
    intraoperative way to re-level either angle, and one number is enough
    for the surgeon to dial in the manipulator's pitch axis.

    Reads tp.surgery_shank_offsets ({shank_idx: {"ap_mm", "rl_mm",
    "roll_deg", "pitch_deg", "depth_mm"}}) and tp.surgery_bl_dist_mm,
    stashed by SurgeryController.load_plan when a saved plan is loaded.

    TODO: tp.ui.tableWidget is the Surgery tab's placeholder summary
    table's current (auto-generated) objectName -- update this once the
    Surgery tab's widgets are renamed to something more specific.
    """
    table = tp.ui.tableWidget
    offsets = getattr(tp, 'surgery_shank_offsets', {})
    bl_dist_plan_mm = getattr(tp, 'surgery_bl_dist_mm', None)
    rows = sorted(offsets)

    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(
        ["Shank", "AP (mm)", "RL (mm)", "Angle to AP/RL plane (deg)", "Depth (mm)"])
    table.setRowCount(len(rows))
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _set(row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(row, col, item)

    for row, shank_idx in enumerate(rows):
        entry = offsets[shank_idx]
        _set(row, 0, f"Shank {shank_idx + 1}")

        target = None if bl_dist_plan_mm is None else reproject_target_to_null(
            bregma_null_mm, lambda_null_mm, entry["ap_mm"], entry["rl_mm"], bl_dist_plan_mm)
        if target is None:
            _set(row, 1, "—")
            _set(row, 2, "—")
        else:
            ml_target, ap_target = target
            _set(row, 1, f"{ap_target:.3f} ({_direction_suffix(ap_mm=ap_target)})")
            _set(row, 2, f"{ml_target:.3f} ({_direction_suffix(rl_mm=ml_target)})")

        # pitch_deg IS the angle between the shank and the AP/RL plane (the
        # bregma-lambda plane parallel to RL, normal = SI) -- see
        # compute_shank_roll_pitch_mri's own docstring (trajectory_planning/
        # coord_transform.py) -- so no separate roll column is shown here.
        _set(row, 3, f"{entry['pitch_deg']:.3f}")
        _set(row, 4, f"{entry['depth_mm']:.3f}")
