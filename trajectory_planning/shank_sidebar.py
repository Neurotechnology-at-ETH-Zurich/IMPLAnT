# This Python file uses the following encoding: utf-8
import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

from trajectory_planning.shank import NEON_COLORS


class ShankSidebarWidget(QWidget):
    """Overview of the currently selected shank only: brain-region bands
    (same colours as the atlas) sized by how much of the shank sits in each
    region, each labelled with its channel count (left), region name
    (centre) and mm span (right). Electrode contacts are drawn as dots on
    top. Bottom of the column is the deepest/tip contact, top is the
    insertion end.
    """

    DOT_RADIUS = 3
    MARGIN = 0
    LEGEND_HEIGHT = 20
    LABEL_HEIGHT = 22

    def __init__(self, tp, parent=None):
        super().__init__(parent)
        self.tp = tp

    def refresh(self):
        self.update()

    @staticmethod
    def _high_contrast_color(rgb):
        """QColor(black) or QColor(white), whichever has the higher WCAG
        contrast ratio against this region colour -- contrast against white
        and against black aren't symmetric (e.g. a mid-grey can legitimately
        read better with black text than white, or vice versa), so picking
        the actual higher-contrast option is more reliable than a flat
        "is this light or dark" luminance threshold."""
        def _linear(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = rgb[:3]
        luminance = 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)
        contrast_with_white = 1.05 / (luminance + 0.05)
        contrast_with_black = (luminance + 0.05) / 0.05
        return QColor(255, 255, 255) if contrast_with_white >= contrast_with_black else QColor(0, 0, 0)

    @staticmethod
    def _region_index_for_depth(cuts, d):
        """Which region (index into the `regions`/bands list that produced
        `cuts`) a given depth falls into, so a dot can be coloured to
        contrast with the band it's actually drawn on top of."""
        idx = int(np.searchsorted(cuts, d, side='right')) - 1
        return int(np.clip(idx, 0, len(cuts) - 2))

    def _contact_depths(self, shank_idx, points):
        """Real distance from the shank's shallow end (the insertion point,
        or the shank-end point if that reaches further out -- same
        reference compute_shank_regions uses) for each electrode contact,
        for drawing the dots (region bands come from compute_shank_regions
        instead, not from these sparse contacts)."""
        if points is None or len(points) == 0:
            return None
        insert = self.tp.coords_insert_point.get(shank_idx)
        deep = self.tp.coords_deepest_point.get(shank_idx)
        if insert is None or deep is None or not hasattr(self.tp, 'fixedImg'):
            return None
        insert_arr = np.array(insert)
        deep_arr = np.array(deep)
        top_arr = insert_arr
        shank_end = self.tp.atlas_shank_end.get(shank_idx)
        if shank_end is not None:
            shank_end_arr = np.array(shank_end)
            if np.linalg.norm(shank_end_arr - deep_arr) > np.linalg.norm(insert_arr - deep_arr):
                top_arr = shank_end_arr
        spacing = np.array(self.tp.fixedImg.GetSpacing())
        return np.linalg.norm((np.asarray(points) - top_arr) * spacing, axis=1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.tp.ui.comboBox_Shanks.count() == 0 or not hasattr(self.tp, 'atlas_vol'):
            painter.end()
            return

        shank_idx = self.tp.shank_number

        label_top = self.LEGEND_HEIGHT
        top = label_top + self.LABEL_HEIGHT
        bottom = self.height() - self.MARGIN
        column_height = max(bottom - top, 1)

        # fill essentially the whole widget width, no artificial cap
        col_width = max(self.width() - 2 * self.MARGIN, 8)
        x = self.MARGIN
        rect = QRectF(x, top, col_width, column_height)

        # legend, at the very top of the widget
        legend_font = QFont()
        legend_font.setPointSize(10)
        painter.setFont(legend_font)
        painter.setPen(QColor(170, 170, 170))
        legend_rect = QRectF(x, 0, col_width, self.LEGEND_HEIGHT)
        painter.drawText(legend_rect.adjusted(4, 0, -4, 0), Qt.AlignLeft | Qt.AlignVCenter, "# Ch")
        painter.drawText(legend_rect, Qt.AlignCenter, "Region")
        painter.drawText(legend_rect.adjusted(4, 0, -4, 0), Qt.AlignRight | Qt.AlignVCenter, "mm")

        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(QColor(220, 220, 220))
        painter.drawText(QRectF(x, label_top, col_width, self.LABEL_HEIGHT),
                          Qt.AlignCenter, str(shank_idx + 1))

        points = self.tp.channel_points.get(shank_idx)
        regions = self.tp.compute_shank_regions(shank_idx, points)

        # Trim a leading/trailing "Clear Label" (atlas value 0, background)
        # band unless an actual electrode contact sits inside it -- the fine
        # line sample can poke slightly outside the labeled brain volume at
        # either end even when no contact is really there.
        while regions and regions[0]['val'] == 0 and regions[0]['count'] == 0:
            regions = regions[1:]
        while regions and regions[-1]['val'] == 0 and regions[-1]['count'] == 0:
            regions = regions[:-1]

        contact_depths_mm = self._contact_depths(shank_idx, points)

        # Never let column content (bands, dashed markers, dots) paint above
        # `top` -- that's the legend/label header's territory ("# Ch",
        # "Region", "mm", the shank number), and it becomes unreadable if
        # anything bleeds into it.
        painter.save()
        painter.setClipRect(QRectF(x, top, col_width, max(self.height() - top, 0)))

        if not regions:
            painter.setPen(QPen(QColor(90, 90, 90)))
            painter.setBrush(QColor(45, 45, 45))
            painter.drawRoundedRect(rect, 3, 3)
        else:
            # Anchor the column on the actual recording span (first contact
            # to deepest contact) rather than the insertion point/shank-end
            # reference compute_shank_regions samples from -- there's usually
            # inert shank material between the insertion point and the first
            # active contact that isn't useful to show as if it were part of
            # the recorded depth range. Falls back to the full sampled line
            # if there are no contacts yet (e.g. shank just added).
            if contact_depths_mm is not None and len(contact_depths_mm):
                depth_min = float(contact_depths_mm.min())
                depth_max = float(contact_depths_mm.max())
                # A region entirely before the first contact or entirely
                # after the last one (e.g. inert shank material, or a real
                # anatomical region with zero contacts right at the
                # insertion end) has no overlap with [depth_min, depth_max]
                # at all -- left in, its outer cut (pinned to depth_min/
                # depth_max, not to its own d_start/d_end) would land past
                # its neighbour's cut, collapsing its band to the 1px floor
                # below while still carrying its full-span, vertically
                # "centered" text -- which reads as that text sitting
                # anomalously high, jammed right under the header. Drop it
                # from the drawn column entirely instead (its contacts, if
                # any, are already re-homed onto a surviving region by
                # compute_shank_regions' own carry-forward logic).
                visible_regions = [r for r in regions if r['d_end'] > depth_min and r['d_start'] < depth_max]
                if visible_regions:
                    regions = visible_regions
            else:
                depth_min = regions[0]['d_start']
                depth_max = regions[-1]['d_end']
            depth_span = max(depth_max - depth_min, 1e-9)

            def y_for_depth(d):
                return top + (d - depth_min) / depth_span * column_height

            # Boundaries between adjacent bands sit at the midpoint between
            # the two neighbouring regions' edges, so bands share an edge
            # with no gap left uncovered.
            cuts = [depth_min]
            for k in range(len(regions) - 1):
                cuts.append((regions[k]['d_end'] + regions[k + 1]['d_start']) / 2)
            cuts.append(depth_max)

            count_font = QFont()
            count_font.setPointSize(13)
            count_font.setBold(True)
            mm_font = QFont()
            mm_font.setPointSize(10)
            count_font.setBold(True)
            name_font = QFont()
            name_font.setPointSize(8)

            for k, r in enumerate(regions):
                y_top = y_for_depth(cuts[k])
                y_bottom = y_for_depth(cuts[k + 1])
                seg_rect = QRectF(x, y_top, col_width, max(y_bottom - y_top, 1))

                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(*r['color']))
                painter.drawRect(seg_rect)

                painter.save()
                painter.setClipRect(seg_rect)
                # white text washes out on a light region colour (e.g. a
                # near-white atlas region) -- pick whichever of black/white
                # actually contrasts better against this region's colour.
                painter.setPen(self._high_contrast_color(r['color']))

                # channel count, left-aligned -- the most prominent number
                painter.setFont(count_font)
                painter.drawText(seg_rect.adjusted(4, 0, -4, 0),
                                  Qt.AlignLeft | Qt.AlignVCenter, f"{r['count']}")
                # mm span, right-aligned
                painter.setFont(mm_font)
                painter.drawText(seg_rect.adjusted(4, 0, -4, 0),
                                  Qt.AlignRight | Qt.AlignVCenter, f"{r['span_mm']:.2f}")
                # region name, centred
                painter.setFont(name_font)
                painter.drawText(seg_rect.adjusted(4, 0, -4, 0),
                                  Qt.AlignCenter | Qt.TextWordWrap, r['name'])
                painter.restore()

            # electrode contacts as dots, on top of the bands
            if contact_depths_mm is not None and len(contact_depths_mm):
                # dashed markers at the first/deepest contact -- with depth_min
                # /depth_max now anchored on the contacts themselves these sit
                # right at the top/bottom edge, but still make explicit which
                # edge is "first contact" vs. "deepest contact" rather than
                # relying on that being implicit from the column's border.
                first_idx = int(np.argmin(contact_depths_mm))
                first_y = y_for_depth(float(contact_depths_mm[first_idx]))
                last_y = y_for_depth(float(contact_depths_mm.max()))

                dash_pen = QPen(QColor(255, 255, 255, 180), 1, Qt.DashLine)
                painter.setPen(dash_pen)
                for y in (first_y, last_y):
                    painter.drawLine(QPointF(x, y), QPointF(x + col_width, y))

                # white-filled dots wash out on a light region colour (e.g.
                # a near-white atlas region) -- pick whichever of black/
                # white actually contrasts better against whichever band
                # each dot is actually drawn on top of.
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                for d in contact_depths_mm:
                    y = y_for_depth(d)
                    region_idx = self._region_index_for_depth(cuts, d)
                    painter.setBrush(self._high_contrast_color(regions[region_idx]['color']))
                    painter.drawEllipse(QPointF(x + col_width / 2, y), self.DOT_RADIUS, self.DOT_RADIUS)

        painter.restore()

        color = NEON_COLORS[self.tp.shank_colors.get(shank_idx, 0)][1]
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(*color), 2))
        painter.drawRoundedRect(rect, 3, 3)

        painter.end()
