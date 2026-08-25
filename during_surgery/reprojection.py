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


def reproject_target_to_null(bregma_null_mm, lambda_null_mm, ap_mm, rl_mm, dv_mm):
    """
    Mirrors compute()'s own bl_axis/plane_normal/x_axis construction
    exactly (same z_approx-based convention, no corpus-callosum landmark
    involved -- that's only needed for roll/pitch, which this rig can't
    adjust intraoperatively and so is never recomputed here), just fed
    the measured points instead of MRI-mm ones. The per-shank offset
    (ap_mm/rl_mm/dv_mm, the exact signed floats stored under a loaded
    plan's per-shank raw block) is a physical mm distance along each of
    the three anatomical directions, not tied to any one origin, so it
    carries over frame-to-frame unchanged.

    Returns the target's mm-from-null (3,) array -- what to dial into
    the manipulator -- or None if bregma/lambda are coincident
    (degenerate).
    """
    bregma_null_mm = np.asarray(bregma_null_mm, dtype=float)
    lambda_null_mm = np.asarray(lambda_null_mm, dtype=float)
    bl_vec = lambda_null_mm - bregma_null_mm
    bl_dist = float(np.linalg.norm(bl_vec))
    if bl_dist <= 1e-9:
        return None
    bl_axis = bl_vec / bl_dist

    z_approx = np.array([0.0, 0.0, 1.0])
    plane_normal = z_approx - np.dot(z_approx, bl_axis) * bl_axis
    pn_norm = float(np.linalg.norm(plane_normal))
    if pn_norm <= 1e-9:
        return None
    plane_normal /= pn_norm
    x_axis = np.cross(plane_normal, bl_axis)
    x_axis /= np.linalg.norm(x_axis)

    return bregma_null_mm + ap_mm * bl_axis + rl_mm * x_axis + dv_mm * plane_normal


def refresh_surgery_summary(tp, bregma_null_mm, lambda_null_mm):
    """
    Recompute every loaded shank's target position in the surgeon's
    manipulator-null-relative mm frame from the just-measured bregma/
    lambda (already sign-corrected by the Surgery tab's invert
    checkboxes upstream of this call), and populate the Surgery tab's
    summary table with the result.

    Reads tp.surgery_shank_offsets ({shank_idx: (ap_mm, rl_mm, dv_mm)}),
    stashed by LoadSurgeryPlan._replay (during_surgery/load_surgery_plan.py)
    when a saved plan is loaded.

    TODO: tp.ui.tableWidget is the Surgery tab's placeholder summary
    table's current (auto-generated) objectName -- update this once the
    Surgery tab's widgets are renamed to something more specific.
    """
    table = tp.ui.tableWidget
    offsets = getattr(tp, 'surgery_shank_offsets', {})
    rows = sorted(offsets)

    # "Sag/Cor/Ax" rather than an AP/ML/DV anatomical relabeling -- target's
    # 3 components already come out in the same [sag, cor, ax] order the
    # measured-mm input fields use (doubleSpinBox_sag_b/cor_b/ax_b etc.),
    # so the table should read back in the exact terms the surgeon typed,
    # not a different naming convention for the same axes.
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Shank", "Sag (mm)", "Cor (mm)", "Ax (mm)"])
    table.setRowCount(len(rows))
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    for row, shank_idx in enumerate(rows):
        ap_mm, rl_mm, dv_mm = offsets[shank_idx]
        target = reproject_target_to_null(bregma_null_mm, lambda_null_mm, ap_mm, rl_mm, dv_mm)
        shank_item = QTableWidgetItem(f"Shank {shank_idx + 1}")
        shank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(row, 0, shank_item)
        if target is None:
            for col in (1, 2, 3):
                item = QTableWidgetItem("—")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)
            continue
        for col, value in zip((1, 2, 3), target):
            item = QTableWidgetItem(f"{value:.3f}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, col, item)
