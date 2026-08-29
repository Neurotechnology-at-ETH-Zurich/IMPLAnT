# This Python file uses the following encoding: utf-8
import numpy as np
from itertools import groupby
from PySide6.QtGui import QPixmap, QIcon, QColor

NEON_COLORS = [
    ("Neon Green",  (0,   255,  28), (0.0,        1.0,  28/255)),
    ("Neon Pink",   (255,  20, 147), (1.0,   20/255, 147/255)),
    ("Neon Blue",   (0,   191, 255), (0.0,  191/255,     1.0)),
    ("Neon Yellow", (255, 255,   0), (1.0,        1.0,     0.0)),
    ("Neon Purple",   (138,  0, 196), (138/255, 0.0, 196/255)),
    ("Neon Orange",   (255,  92, 0), (1.0,   92/255, 0.0)),
    ("White",       (255, 255, 255), (1.0,        1.0,     1.0)),
]

def _make_color_icon(color_idx, size=14):
    r, g, b = NEON_COLORS[color_idx][1]
    px = QPixmap(size, size)
    px.fill(QColor(r, g, b))
    return QIcon(px)


class ShankRendering:
    def add_shank(self):
        n = self.ui.comboBox_Shanks.count()
        self.shank_number = n
        # Cycle through the 5 available colours as shanks are added, so
        # e.g. shanks 1, 6, 11, ... share colour 0, shanks 2, 7, 12, ...
        # share colour 1, etc.
        color_idx = n % len(NEON_COLORS)
        self.shank_colors[n] = color_idx
        self.line_actor[n] = {}
        self.label_actor[n] = {}
        self.channel_points[n] = []
        for combo in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks, self.ui.comboBox_insertion_shank):
            combo.addItem(f"Shank {n+1}")
            combo.setItemData(n, n)
            combo.setItemIcon(n, _make_color_icon(color_idx))
        self.ui.comboBox_Shanks.setCurrentIndex(n)  # triggers select_shank, which syncs comboBox_geometry_shanks
        self.point_actor_deep[n] = {}
        self.point_actor_insert[n] = {}
        self.mri_deep[n] = None
        self.mri_insert[n] = None
        self.coords_deepest_point[n] = None
        self.coords_insert_point[n] = None
        self.direction_atlas[n] = None
        self.atlas_shank_end[n] = None
        self.reset_shank_gui()

        # Re-arm the one-time popups so they're available again for this new
        # shank instead of staying permanently "used up" -- but don't pop
        # one open immediately, that's an unwanted interruption on every
        # "+ Add Shank" click. The '?' button (show_current_step_popup) and
        # the DXF panel's own entry point still show the right thing on
        # demand once this is reset.
        if self.ui.stackedWidget_trajectoryplanning.currentIndex() == 1:
            self._geometry_popup_shown = False
            self._insertion_popup_shown = False

        if self.tp3d_window is not None:
            self.tp3d_window.refresh_shanks()

    def remove_shank(self):
        if self.ui.comboBox_Shanks.count() <= 1:
            return  # always keep at least one
        shank_idx = self.shank_number
        for view_name in ('axial', 'sagittal', 'coronal'):
            if view_name in self.line_actor.get(shank_idx, {}):
                for a in self.line_actor[shank_idx][view_name]:
                    self.LoadMRI.renderers[0][view_name].RemoveActor(a)
                self.LoadMRI.renderers[0][view_name].RemoveActor(self.label_actor[shank_idx][view_name])
                self.LoadMRI.vtk_widgets[0][view_name].GetRenderWindow().Render()

        per_shank_dicts = (
            self.line_actor, self.label_actor, self.channel_points, self.dfx_shank_data,
            self.point_actor_deep, self.point_actor_insert, self.mri_deep, self.mri_insert,
            self.coords_deepest_point, self.coords_insert_point, self.direction_atlas,
            self.atlas_shank_end, self.shank_colors,
        )
        for d in per_shank_dicts:
            d.pop(shank_idx, None)

        # block signals to avoid select_shank firing mid-cleanup
        current_pos = self.ui.comboBox_Shanks.currentIndex()
        for combo in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks, self.ui.comboBox_insertion_shank):
            combo.blockSignals(True)
            combo.removeItem(current_pos)
            combo.blockSignals(False)

        # ids are assigned 0..count-1 in creation order (add_shank) and
        # never reused -- removing one leaves a gap, so every higher id
        # shifts down by 1 here to restore "id == combo position", which
        # comboBox_Shanks.currentIndexChanged -> select_shank (and several
        # other spots) rely on. Left unrenumbered, every shank after the
        # removed one keeps its old (now too-high) id while still sitting
        # at a combo position one lower -- selecting it then looks up the
        # per-shank dicts under the wrong key (e.g. check_points_in_slice's
        # KeyError). Combo item order is always ascending by id (add_shank
        # only ever appends), so walking positions in order visits old ids
        # in ascending order too -- each dict slot a shank moves OUT of is
        # therefore always freed before anything moves INTO it.
        for pos in range(self.ui.comboBox_Shanks.count()):
            old_id = self.ui.comboBox_Shanks.itemData(pos)
            new_id = pos
            if old_id == new_id:
                continue
            for combo in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks, self.ui.comboBox_insertion_shank):
                combo.setItemData(pos, new_id)
                combo.setItemText(pos, f"Shank {new_id + 1}")
            for d in per_shank_dicts:
                if old_id in d:
                    d[new_id] = d.pop(old_id)

        self.shank_number = self.ui.comboBox_Shanks.currentData()
        # removing a shank shifts every higher id down by one (see above),
        # which would otherwise leave stale/mismatched indices in here
        self._insertion_confirmed = set()
        self.select_shank(self.shank_number)

        if self.tp3d_window is not None:
            self.tp3d_window.refresh_shanks()



    def select_shank(self, index):
        self.shank_number = index
        # comboBox_Shanks, comboBox_geometry_shanks and comboBox_insertion_shank
        # always show the same shank; whichever one the user just changed
        # drives, the others follow (blocked so they don't re-enter this method).
        for combo in (self.ui.comboBox_Shanks, self.ui.comboBox_geometry_shanks, self.ui.comboBox_insertion_shank):
            if combo.currentIndex() != index:
                combo.blockSignals(True)
                combo.setCurrentIndex(index)
                combo.blockSignals(False)
        self.ui.comboBox_tpColor.blockSignals(True)
        self.ui.comboBox_tpColor.setCurrentIndex(self.shank_colors.get(index, 0))
        self.ui.comboBox_tpColor.blockSignals(False)
        for shank_idx in self.line_actor:
            is_active = (shank_idx == index)
            color = self.get_shank_vtk_color(shank_idx) if is_active else (0.35, 0.35, 0.35)
            opacity = 1.0 if is_active else 0.4
            for view_name, actors in self.line_actor[shank_idx].items():
                for a in actors:
                    a.GetProperty().SetColor(*color)
                    a.GetProperty().SetOpacity(opacity * a.GetProperty().GetOpacity())
                self.label_actor[shank_idx][view_name].GetCaptionTextProperty().SetColor(*color)
                self.LoadMRI.vtk_widgets[0][view_name].GetRenderWindow().Render()

        # update spinboxes
        insert = self.coords_insert_point.get(index)
        deep   = self.coords_deepest_point.get(index)
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(True)
        if insert is not None:
            self.set_value(list(insert), self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z)
        else:
            self.ui.spinBox_tp_insert_x.setValue(0)
            self.ui.spinBox_tp_insert_y.setValue(0)
            self.ui.spinBox_tp_insert_z.setValue(0)
        if deep is not None:
            self.set_value(list(deep), self.ui.spinBox_tp_deep_x, self.ui.spinBox_tp_deep_y, self.ui.spinBox_tp_deep_z)
        else:
            self.ui.spinBox_tp_deep_x.setValue(0)
            self.ui.spinBox_tp_deep_y.setValue(0)
            self.ui.spinBox_tp_deep_z.setValue(0)
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(False)

        # update distance spinbox -- MUST match calculate_distance's (and
        # the PDF report's compute()) convention: MRI-space mri_insert/
        # mri_deep with the MRI-resampled spacing, not the raw atlas
        # coords_insert_point/coords_deepest_point with atlas spacing.
        # The atlas->MRI registration transform isn't distance-preserving,
        # so those two conventions disagree, and whichever one last wrote
        # to this spinbox is not necessarily the one the PDF report uses --
        # showing a different depth for the same shank in the GUI vs. the
        # exported PDF.
        mri_insert = self.mri_insert.get(index)
        mri_deep = self.mri_deep.get(index)
        dist = 0.0
        if mri_insert is not None and mri_deep is not None:
            spacing = np.array(self.movingImg_resampled.GetSpacing())
            dist = float(np.linalg.norm((np.array(mri_insert) - np.array(mri_deep)) * spacing))
        self.ui.doubleSpinBox_distance_shank.setValue(dist)

        self.refresh_dfx_channel_display()
        if hasattr(self, 'shank_sidebar'):
            self.shank_sidebar.refresh()
        if hasattr(self, 'atlas_bregma_coords'):
            self.update_shank_angle_display()
        if hasattr(self, 'Vis3D'):
            if insert is None or deep is None:
                # this shank has no insert/deepest points yet -- there's no
                # trajectory to clip a 3D view around, so switch any panel
                # currently in 3D mode back to its plain 2D slice view --
                # the real toggle each pushButton_*View/change_view_*
                # already uses (index 0 = 2D for all three; the 3D/clipped
                # page is 1 for sagittal/axial, but 2 for coronal -- see
                # change_view_coronal), not just a layout/column-width
                # change.
                for stacked, btn in (
                    (self.ui.stackedWidget_coronal, self.ui.pushButton_coronalView),
                    (self.ui.stackedWidget_sagittal, self.ui.pushButton_sagittalView),
                    (self.ui.stackedWidget_axial, self.ui.pushButton_axialView),
                ):
                    stacked.setCurrentIndex(0)
                    btn.setChecked(True)
            else:
                self.Vis3D.refresh_clipped_views(index)

        if self.tp3d_window is not None:
            # just the selection/bold-highlight, not a full refresh --
            # switching which shank is selected happens often (e.g.
            # clicking through them to review) and doesn't itself change
            # any shank's geometry, so recomputing compute_shank_regions
            # for every shank here would reintroduce the exact per-click
            # lag that caching it in refresh_shanks was meant to avoid.
            self.tp3d_window._select_shank(index, sync_combo=True, sync_table=True)

        # Switching shanks changes which insert point the oblique
        # constraint view(s) should be anchored on -- without this, picking
        # a different shank left the panel showing the PREVIOUS shank's
        # anchor (or reset to the plain 2D page by the insert-is-None
        # branch above), even though the constraint checkbox was still
        # checked. _refresh_oblique_views_for_insert (ElecGeometryMri,
        # electrode_mri.py) already does exactly this re-anchor + re-open
        # -- hasattr-guarded since select_shank is shared with the plain
        # (non-MRI) TrajectoryPlanning, which has no oblique views at all.
        if hasattr(self, '_refresh_oblique_views_for_insert'):
            self._refresh_oblique_views_for_insert(index)

    def compute_shank_regions(self, shank_idx, points):
        """List of dicts, one per brain region the shank physically passes
        through, ordered shallow/insertion-end first to deep/tip-end last:
        {'val', 'name', 'count', 'span_mm', 'd_start', 'd_end'}.

        The region boundaries come from sampling the ENTIRE physical line
        between the insertion and deepest points at ~1-voxel resolution
        (same approach as check_region_to_avoid) -- using only the sparse
        electrode contacts would size regions off of whichever contacts
        happen to land in them, and silently drop a thin region with no
        contact inside it at all. 'count' is still the number of actual
        electrode contacts that fall within the region's real extent.

        Used by the shank sidebar.
        """
        insert = self.coords_insert_point.get(shank_idx)
        deep = self.coords_deepest_point.get(shank_idx)
        if points is None or len(points) == 0 or insert is None or deep is None:
            return []

        spacing = np.array(self.fixedImg.GetSpacing())
        insert_arr = np.array(insert)
        deep_arr = np.array(deep)

        # The shank's actual shallow end (based on channel count/spacing) can
        # sit further out than the marked insertion point -- in that case the
        # sampled line, and everything measured against it, should reach all
        # the way to the shank end instead of being cut off at the insertion
        # point.
        shank_end = self.atlas_shank_end.get(shank_idx)
        top_arr = insert_arr
        if shank_end is not None:
            shank_end_arr = np.array(shank_end)
            if np.linalg.norm(shank_end_arr - deep_arr) > np.linalg.norm(insert_arr - deep_arr):
                top_arr = shank_end_arr

        n_steps = int(np.max(np.abs(top_arr - deep_arr))) + 1
        line_points = np.linspace(top_arr, deep_arr, n_steps)  # shallow -> deep
        line_depths = np.linalg.norm((line_points - top_arr) * spacing, axis=1)
        line_atlas_values = [self.atlas_vol[tuple(np.round(p[::-1]).astype(int))] for p in line_points]

        # actual electrode contact depths, just to count how many fall in
        # each region -- the region's own extent no longer depends on them
        contact_depths = np.linalg.norm((np.asarray(points) - top_arr) * spacing, axis=1)

        grouped = [(val, sum(1 for _ in g)) for val, g in groupby(line_atlas_values)]

        segs = []  # (val, d_start, d_end)
        cursor = 0
        for val, count in grouped:
            segs.append((val, line_depths[cursor], line_depths[cursor + count - 1]))
            cursor += count

        # Partition the WHOLE depth axis with no gaps/overlaps -- adjacent
        # segments meet at the midpoint between them, same construction the
        # sidebar already uses for drawing bands -- so every electrode
        # contact is assigned to exactly one segment. A plain
        # [d_start, d_end] inclusion test can strand a contact in the crack
        # between two segments if its depth (measured independently of the
        # line-sample grid) doesn't land inside either, silently
        # undercounting the total (e.g. showing 59 instead of 64 channels).
        cut_points = [-np.inf]
        for k in range(len(segs) - 1):
            cut_points.append((segs[k][2] + segs[k + 1][1]) / 2)
        cut_points.append(np.inf)
        contact_seg_idx = np.clip(
            np.searchsorted(cut_points, contact_depths, side='right') - 1,
            0, len(segs) - 1)
        counts = np.bincount(contact_seg_idx, minlength=len(segs))

        regions = []
        for i, (val, d_start, d_end) in enumerate(segs):
            label = self.tp_labels.get(val)
            if val == 0:
                # atlas index 0 is the conventional "Clear Label"/background
                # value -- build_label_lut() already force-hides it (alpha 0)
                # in the real MRI views regardless of what the label file
                # calls it, so treat it the same way here instead of showing
                # whatever raw name/colour (often black) the file happens to
                # have on record for it.
                name, color = "Clear Label", (60, 60, 60)
            elif label is not None:
                name, color = label[4], tuple(int(round(c * 255)) for c in label[:3])
            else:
                name, color = "Outside / unlabeled", (90, 90, 90)
            regions.append({
                'val': val, 'name': name, 'color': color, 'count': int(counts[i]),
                'span_mm': float(d_end - d_start),
                'd_start': float(d_start), 'd_end': float(d_end),
            })

        # Drop slivers that would display as "0.00" mm anyway -- these come
        # from single-voxel boundary artefacts in the atlas, not a real
        # region the shank passes through. Fold any contacts assigned to a
        # dropped sliver into the next surviving region instead of just
        # losing them, so the displayed counts still add up to len(points).
        kept = []
        carry = 0
        for r in regions:
            if r['span_mm'] < 0.005:
                carry += r['count']
                continue
            if carry:
                r['count'] += carry
                carry = 0
            kept.append(r)
        if carry and kept:
            kept[-1]['count'] += carry

        # Adjacent regions with the same name (e.g. the same bilateral
        # structure under two different atlas indices) are one block, not
        # two -- merge them so the sidebar doesn't draw a pointless border
        # down the middle of what is visually a single band.
        merged = []
        for r in kept:
            if merged and merged[-1]['name'] == r['name']:
                prev = merged[-1]
                prev['count'] += r['count']
                prev['span_mm'] += r['span_mm']
                prev['d_end'] = r['d_end']
            else:
                merged.append(dict(r))
        return merged

    def get_shank_vtk_color(self, shank_idx):
        return NEON_COLORS[self.shank_colors.get(shank_idx, 0)][2]

    def update_shank_icon(self, shank_number):
        icon = _make_color_icon(self.shank_colors.get(shank_number, 0))
        for i in range(self.ui.comboBox_Shanks.count()):
            if self.ui.comboBox_Shanks.itemData(i) == shank_number:
                self.ui.comboBox_Shanks.setItemIcon(i, icon)
                break

    def change_shank_color(self, color_idx):
        self.shank_colors[self.shank_number] = color_idx
        vtk_color = NEON_COLORS[color_idx][2]
        for view_name, actors in self.line_actor[self.shank_number].items():
            for a in actors:
                a.GetProperty().SetColor(*vtk_color)
            self.label_actor[self.shank_number][view_name].GetCaptionTextProperty().SetColor(*vtk_color)
        self.update_shank_icon(self.shank_number)
        self.render()
        if hasattr(self, 'Vis3D'):
            self.Vis3D.refresh_clipped_views(self.shank_number)
        # both colour shanks from self.shank_colors at draw time, not
        # continuously -- neither repaints on its own just because the dict
        # changed, so without this they'd keep showing the old colour until
        # something unrelated happened to trigger a redraw.
        if self.dfx_shank_data:
            self.draw_dfx_probe_overview()
        if hasattr(self, 'shank_sidebar'):
            self.shank_sidebar.refresh()
        if self.tp3d_window is not None:
            self.tp3d_window.refresh_shanks()

    def reset_shank_gui(self):
        for sb in (self.ui.spinBox_tp_insert_x, self.ui.spinBox_tp_insert_y, self.ui.spinBox_tp_insert_z,
                   self.ui.spinBox_tp_deep_x,   self.ui.spinBox_tp_deep_y,   self.ui.spinBox_tp_deep_z):
            sb.blockSignals(True)
            sb.setValue(0)
            sb.blockSignals(False)
        self.ui.doubleSpinBox_distance_shank.setValue(0.0)
        if hasattr(self, 'shank_sidebar'):
            self.shank_sidebar.refresh()
