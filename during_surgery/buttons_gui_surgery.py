# This Python file uses the following encoding: utf-8
"""
Surgery tab's skull-photo reference view: a fixed dorsal rat-skull photo
(showing Bregma, Lambda, and the interaural line) displayed in widget_
axialView, rotated 90 degrees to match the animal's orientation on the
stereotaxic frame. This replaced the previous per-plan axial MRI slice
view (which reused the app's real LoadMRI/ImageLayer pipeline to reslice
the subject's own resampled MRI) -- the photo is a fixed reference image,
independent of whatever plan is loaded, so there is no MRI to load/reslice
here any more.

Bregma (red) and Lambda (blue) are drawn once, always, at their hand-
calibrated pixel positions in the photo (_BREGMA_PX/_LAMBDA_PX). Each
shank's planned insertion point (from a loaded plan's ap_mm/rl_mm offset
from Bregma) is drawn on load(), in that shank's own color -- purely
plan-derived, no MRI file needed, unlike mri_preview.py's 3D view.
"""
import os
import numpy as np
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPixmap, QTransform, QColor, QBrush, QPen, QFont
from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem,
                                QGraphicsSimpleTextItem, QGraphicsRectItem, QVBoxLayout, QApplication, QLabel)
from during_surgery.mri_preview import _SHANK_COLORS
from during_surgery.reprojection import null_point_ap_rl

_SKULL_PHOTO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Icons", "csm_SBIR_rat_skull_overhead_01_93d6774e3d.jpg.webp")

_PHOTO_CREDIT = (
    "Location of Bregma and Lambda as defined by Dr. George Paxinos (George "
    "Paxinos and Charles Watson: The Rat Brain in Stereotaxic Coordinates, "
    "Academic Press, New York, 1998, p. 11). Courtesy of Academic Press.")

# Pixel coordinates of Bregma/Lambda in the photo ABOVE, in the already-
# 90-degree-rotated frame (i.e. against QPixmap(_SKULL_PHOTO).transformed
# (QTransform().rotate(90)), same as the pixmap built below) -- picked by
# hand with a click-to-print helper against this exact image file. Re-pick
# both if the photo is ever swapped for a different crop/rotation.
_BREGMA_PX = (168, 425)
_LAMBDA_PX = (165, 567)


def _photo_axes():
    """The photo's own (AP, RL) unit-vector directions in pixel space,
    fixed purely by the two calibration points _BREGMA_PX/_LAMBDA_PX --
    scale-independent (unlike _mri_to_photo_affine's matrix), so this is
    the same regardless of which plan (if any) is loaded. AP is just the
    Bregma->Lambda pixel direction, matching ap_mm's own positive-toward-
    Lambda convention.

    RL's sign is fixed by an INDEPENDENT anatomical fact, not "assume a
    pure rotation": positive rl_mm is anatomical LEFT, not right
    (trajectory_planning/file_input_output.py's compute(): `rl_str =
    f"...{'R' if coord_perp_bl <= 0 else 'L'}"`, the SAME coord_perp_bl
    that becomes a shank's raw rl_mm) -- that part is settled, straight
    from the app's own existing code. WHICH SIDE of this particular
    (rotated) photo counts as image-left is a separate question this
    formula answers empirically, not by re-deriving it from RAS geometry
    (an earlier "dorsal + anterior-up -> no mirroring" assumption here
    was confirmed backwards against the app's own 3D trajectory-planning
    view) -- so the sign below is picked to match that real reference,
    not first-principles reasoning about the photo's orientation.
    Returns (ap_axis_px, rl_axis_px), or None if Bregma/Lambda coincide."""
    bregma_px = np.asarray(_BREGMA_PX, dtype=float)
    lambda_px = np.asarray(_LAMBDA_PX, dtype=float)
    bl_vec_px = lambda_px - bregma_px
    bl_dist_px = np.linalg.norm(bl_vec_px)
    if bl_dist_px <= 1e-6:
        return None
    ap_axis_px = bl_vec_px / bl_dist_px
    rl_axis_px = np.array([ap_axis_px[1], -ap_axis_px[0]])
    return ap_axis_px, rl_axis_px


def _mri_to_photo_affine(bregma_mm, lambda_mm):
    """The unique similarity transform (2x2 matrix + translation) taking a
    shank's (ap_mm, rl_mm) -- already an orthonormal frame centered on
    Bregma, with Lambda by construction at (bl_dist_mm, 0), see
    trajectory_planning/file_input_output.py's per-shank raw block -- to
    this photo's own pixel space. Returns (matrix, translation) such that
    pixel = matrix @ [ap_mm, rl_mm] + translation, or None if Bregma/
    Lambda coincide in either space.

    Two point correspondences (Bregma, Lambda) are exactly enough to
    determine a similarity transform: 4 degrees of freedom (2 translation
    + 1 rotation + 1 UNIFORM scale) from 4 constraints (2 point pairs x 2
    coordinates each). That is what this builds -- NOT a full 6-dof affine
    (independent x/y scale + shear), which would need a third, off-axis
    landmark pair we don't have. The transform is a REFLECTION, not a pure
    rotation (its matrix has determinant -1) -- see _photo_axes for why."""
    axes = _photo_axes()
    bregma_mm = np.asarray(bregma_mm, dtype=float)
    lambda_mm = np.asarray(lambda_mm, dtype=float)
    bl_dist_mm = np.linalg.norm(lambda_mm - bregma_mm)
    if axes is None or bl_dist_mm <= 1e-6:
        return None
    ap_axis_px, rl_axis_px = axes

    bregma_px = np.asarray(_BREGMA_PX, dtype=float)
    lambda_px = np.asarray(_LAMBDA_PX, dtype=float)
    bl_dist_px = np.linalg.norm(lambda_px - bregma_px)
    scale_px_per_mm = bl_dist_px / bl_dist_mm  # calibrated per-animal from
    # this plan's own real Bregma-Lambda distance, not a generic atlas
    # figure -- the photo itself is a fixed generic schematic, but the
    # scale applied to it isn't.
    matrix = scale_px_per_mm * np.column_stack([ap_axis_px, rl_axis_px])
    return matrix, bregma_px


def _add_marker(scene, px, color, radius=5):
    x, y = px
    marker = QGraphicsEllipseItem(QRectF(x - radius, y - radius, radius * 2, radius * 2))
    marker.setBrush(QBrush(color))
    marker.setPen(QPen(Qt.NoPen))
    marker.setZValue(1)  # always on top of the photo itself
    scene.addItem(marker)
    return marker


def _edge_point(rect, direction, margin=15):
    """Point where a ray from the photo's own center in `direction` exits
    its bounding rect, inset by `margin` px -- lets each A/P/R/L letter
    sit right at the edge of the image in its OWN true direction (see
    _add_edge_letters), even though the photo's Bregma-Lambda line isn't
    perfectly axis-aligned (_BREGMA_PX/_LAMBDA_PX), rather than assuming
    "AP is vertical, RL is horizontal" and hardcoding top/bottom/left/
    right positions."""
    cx, cy = rect.width() / 2, rect.height() / 2
    dx, dy = direction
    half_w, half_h = rect.width() / 2 - margin, rect.height() / 2 - margin
    t_candidates = []
    if abs(dx) > 1e-9:
        t_candidates.append(half_w / abs(dx))
    if abs(dy) > 1e-9:
        t_candidates.append(half_h / abs(dy))
    t = min(t_candidates)
    return cx + dx * t, cy + dy * t


def _add_edge_letters(scene, color=QColor(20, 20, 20)):
    """A/P/R/L letters at the corresponding edge of the photo -- the same
    orientation-labeling convention MRI viewers use (one letter at the
    edge each anatomical direction points toward), replacing a compass-
    arrow legend. Uses the exact same _photo_axes directions the shank
    markers are placed with, so the letters and the markers can never
    disagree about which way is which."""
    axes = _photo_axes()
    if axes is None:
        return
    ap_axis_px, rl_axis_px = axes
    rect = scene.sceneRect()
    for direction, label in ((-ap_axis_px, "A"), (ap_axis_px, "P"),
                              (rl_axis_px, "L"), (-rl_axis_px, "R")):
        pos = _edge_point(rect, direction)
        text = QGraphicsSimpleTextItem(label)
        font = QFont()
        font.setBold(True)
        font.setPointSize(13)
        text.setFont(font)
        text.setBrush(QBrush(color))
        text_rect = text.boundingRect()
        text.setPos(pos[0] - text_rect.width() / 2, pos[1] - text_rect.height() / 2)
        text.setZValue(2)

        # A plain white background chip behind the letter -- some edge
        # positions (e.g. "A", right at the skull's own nose peak) land
        # on top of the illustration's own dark linework otherwise,
        # where a same-color letter is unreadable.
        padding = 2
        backing = QGraphicsRectItem(text.pos().x() - padding, text.pos().y() - padding,
                                     text_rect.width() + 2 * padding, text_rect.height() + 2 * padding)
        backing.setBrush(QBrush(QColor(255, 255, 255, 220)))
        backing.setPen(QPen(Qt.NoPen))
        backing.setZValue(1.5)
        scene.addItem(backing)
        scene.addItem(text)


def _add_shank_markers(scene, data):
    """data: the parsed plan JSON (FileOutput.compute()'s output,
    trajectory_planning/file_input_output.py). Places each shank's planned
    insertion point at its ap_mm/rl_mm offset from Bregma, mapped into this
    photo's pixel space via the Bregma/Lambda-calibrated affine transform
    (see _mri_to_photo_affine). Returns the list of marker items added."""
    affine = _mri_to_photo_affine(data["raw"]["bregma_mm"], data["raw"]["lambda_mm"])
    if affine is None:
        return []
    matrix, origin_px = affine

    markers = []
    shank_keys = sorted(data["shanks"], key=lambda k: int(k.split("_")[1]))
    for i, key in enumerate(shank_keys):
        raw = data["shanks"][key]["raw"]
        insert_px = origin_px + matrix @ np.array([raw["ap_mm"], raw["rl_mm"]])
        r, g, b = _SHANK_COLORS[i % len(_SHANK_COLORS)]
        color = QColor(round(r * 255), round(g * 255), round(b * 255))
        markers.append(_add_marker(scene, tuple(insert_px), color))
    return markers


def build_skull_reference_scene(data=None):
    """Builds the Surgery tab's skull-reference QGraphicsScene: the photo,
    Bregma (red)/Lambda (blue) markers, and A/P/R/L edge letters, always;
    plus each shank's planned insertion-point marker if a parsed plan JSON
    is passed (see _add_shank_markers). Returns (scene, photo_item).

    Shared by the live Surgery tab widget (ButtonsGUI_Surgery, below) and
    the trajectory-planning PDF's cover page (trajectory_planning/
    file_input_output.py's _cover_page) -- both show identical content,
    rendered from the exact same drawing code."""
    scene = QGraphicsScene()
    pixmap = QPixmap(_SKULL_PHOTO).transformed(QTransform().rotate(90))
    photo_item = QGraphicsPixmapItem(pixmap)
    scene.addItem(photo_item)
    scene.setSceneRect(photo_item.boundingRect())

    _add_marker(scene, _BREGMA_PX, QColor(255, 0, 0))
    _add_marker(scene, _LAMBDA_PX, QColor(0, 0, 255))
    _add_edge_letters(scene)
    if data is not None:
        _add_shank_markers(scene, data)
    return scene, photo_item


class _FitOnResizeView(QGraphicsView):
    """Re-fits the photo on every one of the view's OWN resizes -- fitInView's
    scale depends on the viewport's CURRENT pixel size, which is only
    actually up to date once QGraphicsView's own resizeEvent has run
    (installing an event filter to react to the raw QEvent.Resize instead
    fires too early, before the viewport's internal geometry catches up,
    which silently baked in a stale fit on every real GUI resize -- this
    override runs AFTER super().resizeEvent(), when the new size is live)."""

    def __init__(self, scene, item):
        super().__init__(scene)
        self.item = item

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.item, Qt.KeepAspectRatio)


class ButtonsGUI_Surgery:
    """No zoom/pan/fit buttons any more -- widget_axialView is just the
    photo, always kept fit-to-window by _FitOnResizeView's own resizeEvent
    override."""

    def __init__(self, MW, container_widget):
        self.MW = MW
        self.scene, self.photo_item = build_skull_reference_scene()
        self._shank_markers = []
        self._null_marker = None
        self._plan_data = None

        self.view = _FitOnResizeView(self.scene, self.photo_item)
        layout = QVBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        # Stretch factor 1 on the view only -- without it, a cramped
        # widget_axialView (e.g. a small/unmaximized window) can squeeze
        # the credit_label down to zero visible height instead of shrinking
        # the view first, since QGraphicsView's default size policy is
        # Expanding on both axes and will greedily claim tight space too.
        layout.addWidget(self.view, 1)

        self.credit_label = QLabel(_PHOTO_CREDIT, container_widget)
        self.credit_label.setWordWrap(True)
        self.credit_label.setAlignment(Qt.AlignCenter)
        self.credit_label.setStyleSheet("color: gray; font-size: 9px;")
        layout.addWidget(self.credit_label)

        QApplication.processEvents()
        self.fit_to_window()

    def fit_to_window(self, *_args):
        self.view.fitInView(self.photo_item, Qt.KeepAspectRatio)

    def load(self, data=None):
        """data: the parsed plan JSON (FileOutput.compute()'s output,
        trajectory_planning/file_input_output.py) -- see _add_shank_markers.
        Stashed on self so a later update_null_point() (from live bregma/
        lambda spinbox edits) has this plan's own Bregma/Lambda calibration
        to place the null-point marker with."""
        self.clear()
        self._plan_data = data
        if data is not None:
            self._shank_markers = _add_shank_markers(self.scene, data)

    def clear(self):
        for marker in self._shank_markers:
            self.scene.removeItem(marker)
        self._shank_markers = []
        if self._null_marker is not None:
            self.scene.removeItem(self._null_marker)
            self._null_marker = None

    def update_null_point(self, bregma_null_mm, lambda_null_mm):
        """Draws a black dot at the stereotaxic manipulator's own null
        point (dial reading (0, 0)), mapped onto the photo through the
        currently loaded plan's Bregma/Lambda calibration (see
        reprojection.null_point_ap_rl + _mri_to_photo_affine) -- only if
        it actually falls inside the photo's own bounds. The null point is
        an arbitrary rig-calibration choice, unrelated to the animal's own
        anatomy, so it often lands nowhere near the skull at all; no
        marker is drawn (any previous one removed) whenever that's the
        case, or before a plan is loaded, or while bregma/lambda are still
        at their default (0, 0) (degenerate -- see null_point_ap_rl)."""
        if self._null_marker is not None:
            self.scene.removeItem(self._null_marker)
            self._null_marker = None
        if self._plan_data is None:
            return
        ap_rl = null_point_ap_rl(bregma_null_mm, lambda_null_mm,
                                  self._plan_data["bregma_lambda_distance_mm"])
        if ap_rl is None:
            return
        affine = _mri_to_photo_affine(self._plan_data["raw"]["bregma_mm"],
                                       self._plan_data["raw"]["lambda_mm"])
        if affine is None:
            return
        matrix, origin_px = affine
        null_px = origin_px + matrix @ np.array(ap_rl)
        if not self.scene.sceneRect().contains(QPointF(*null_px)):
            return
        self._null_marker = _add_marker(self.scene, tuple(null_px), QColor(0, 0, 0))
