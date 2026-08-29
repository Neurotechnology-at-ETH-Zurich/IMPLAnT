# This Python file uses the following encoding: utf-8
"""MRI-space trajectory planning: TrajectoryPlanningMri.

Rather than duplicating TrajectoryPlanning's own __init__ (and its handful
of other directly-defined methods -- update_voxel_spinbox_ranges,
open_3d_window, the show_*_popup family), this class INHERITS from
TrajectoryPlanning itself, placed LAST in the base list. Python's C3 MRO
then resolves every method this rewrite overrode (in RenderingMri/
TpRegistrationMri/ElecGeometryMri/ShankRenderingMri, each listed BEFORE
TrajectoryPlanning below) to its MRI-space version, while every method
TrajectoryPlanning defines directly -- or inherits unmodified from
CoordTransform/DfxGeometry -- resolves through TrajectoryPlanning exactly
as it always has. trajectory_planning.py itself is not modified by any of
this; this class only reads it, same as every other file in this rewrite.

See /home/neurox/.claude/plans/wise-popping-nest.md for the full rationale
and https://docs.python.org/3/tutorial/classes.html#multiple-inheritance
(C3 linearization) for why placing the *Mri mixins before TrajectoryPlanning
resolves consistently even though TrajectoryPlanning itself is built from
the very (non-Mri) classes those mixins subclass -- verified by hand for
this exact base list before writing this file.
"""

from trajectory_planning.trajectory_planning import TrajectoryPlanning
from trajectory_planning.rendering_mri import RenderingMri
from trajectory_planning.registration_mri import TpRegistrationMri
from trajectory_planning.electrode_mri import ElecGeometryMri
from trajectory_planning.shank_mri import ShankRenderingMri


class TrajectoryPlanningMri(RenderingMri, TpRegistrationMri, ElecGeometryMri, ShankRenderingMri, TrajectoryPlanning):
    def __init__(self, MW, ui, file_names, transformPath):
        # None of RenderingMri/TpRegistrationMri/ElecGeometryMri/
        # ShankRenderingMri define __init__, so this resolves straight to
        # TrajectoryPlanning.__init__ unchanged -- trajectory_planning.py
        # itself is still not modified (see module docstring above).
        # setup_misalignment_controls (rendering_mri.py) wires up
        # dial_missalignment/doubleSpinBox_missalignment (page_5,
        # groupBox_80), which only exists in this MRI-space rewrite.
        super().__init__(MW, ui, file_names, transformPath)
        # The base (non-Mri) workflow sets this at every restart_gui call
        # site (do_get_shank_line, the atlas<->MRI insertion round trip,
        # the atlas switcher) since restart_gui recreates self.LoadMRI each
        # time. This workflow never calls restart_gui -- self.LoadMRI lives
        # for the whole session -- so it only needs setting once, here.
        # Without it, loader.py's binary-overlay LUT check
        # (hasattr(self.MW.LoadMRI, 'TrajPlanning') and hasattr(...,
        # 'region_to_avoid_img')) never finds this attribute at all, so the
        # Forbidden Regions overlay always falls back to red instead of grey.
        self.LoadMRI.TrajPlanning = self
        self.setup_misalignment_controls()
