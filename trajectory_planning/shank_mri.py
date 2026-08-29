# This Python file uses the following encoding: utf-8
"""MRI-space override of ShankRendering (trajectory_planning/shank.py) --
only compute_shank_regions depends on which volume/grid is displayed
(atlas spacing + the atlas' own native-grid label array); everything else
(add_shank, remove_shank, select_shank, get_shank_vtk_color,
update_shank_icon, change_shank_color, reset_shank_gui) already reads
generic/already-MRI-space state (coords_*/mri_*/self.movingImg_resampled,
the latter already used by ElecGeometry/ShankRendering's own select_shank)
and is inherited unchanged."""

from itertools import groupby
import numpy as np

from trajectory_planning.shank import ShankRendering


class ShankRenderingMri(ShankRendering):
    def compute_shank_regions(self, shank_idx, points):
        """Same as ShankRendering.compute_shank_regions, against the MRI's
        own spacing and the atlas-labels-on-MRI-grid overlay (mri_label_vol)
        instead of the atlas' own native-grid array (atlas_vol)."""
        insert = self.coords_insert_point.get(shank_idx)
        deep = self.coords_deepest_point.get(shank_idx)
        if points is None or len(points) == 0 or insert is None or deep is None:
            return []

        spacing = np.array(self.movingImg_resampled.GetSpacing())
        insert_arr = np.array(insert)
        deep_arr = np.array(deep)

        shank_end = self.atlas_shank_end.get(shank_idx)
        top_arr = insert_arr
        if shank_end is not None:
            shank_end_arr = np.array(shank_end)
            if np.linalg.norm(shank_end_arr - deep_arr) > np.linalg.norm(insert_arr - deep_arr):
                top_arr = shank_end_arr

        n_steps = int(np.max(np.abs(top_arr - deep_arr))) + 1
        line_points = np.linspace(top_arr, deep_arr, n_steps)  # shallow -> deep
        line_depths = np.linalg.norm((line_points - top_arr) * spacing, axis=1)
        line_mri_values = [self.mri_label_vol[tuple(np.round(p[::-1]).astype(int))] for p in line_points]

        contact_depths = np.linalg.norm((np.asarray(points) - top_arr) * spacing, axis=1)

        grouped = [(val, sum(1 for _ in g)) for val, g in groupby(line_mri_values)]

        segs = []  # (val, d_start, d_end)
        cursor = 0
        for val, count in grouped:
            segs.append((val, line_depths[cursor], line_depths[cursor + count - 1]))
            cursor += count

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
