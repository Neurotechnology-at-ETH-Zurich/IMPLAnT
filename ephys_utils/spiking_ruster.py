# This Python file uses the following encoding: utf-8
import numpy as np
import scipy.io as sio
import h5py
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout


UNIT_COLORS = [
    (31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),
    (148, 103, 189), (140, 86, 75), (227, 119, 194), (127, 127, 127),
    (188, 189, 34), (23, 190, 207),
]


class TimeAxisItem(pg.AxisItem):
    """X-axis that shows seconds as m:ss.mmm (min:sec:msec)."""
    def tickStrings(self, values, scale, spacing):
        out = []
        for v in values:
            v = max(v, 0.0)
            m = int(v // 60)
            s = int(v % 60)
            ms = int(round((v - int(v)) * 1000))
            out.append(f'{m}:{s:02d}.{ms:03d}')
        return out


class SpikeRuster(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._spike_times = None   # in seconds, shape (N,)
        self._spike_units = None   # unit index per spike, shape (N,)
        self._unit_ids    = None   # sorted unique unit IDs
        self._unit_labels = None   # display label per unit
        self._scatter_items = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget(
            background='k', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot = self.plot_widget.getPlotItem()
        self.plot.showGrid(x=True, y=False, alpha=0.3)
        self.plot.getViewBox().invertY(True)   # first chMap channel on top
        #self.plot.setLabel('bottom', 'Time', units='s')
        #self.plot.setLabel('left', 'Unit')
        self.plot.setMouseEnabled(x=False, y=False)
        layout.addWidget(self.plot_widget)

        self._timeline = None   # synced timeline cursor (driven by pushButton_timeline)
        self._highlight_channel = None   # channel highlighted in the ephys view
        self._highlight_band = None      # horizontal band behind that channel's rows

    # ------------------------------------------------------------------
    # Timeline cursor (mirrors the ephys-plot timeline at the same time x)
    # ------------------------------------------------------------------

    def set_timeline(self, x):
        """Show/move a vertical time cursor at x seconds."""
        if self._timeline is None:
            self._timeline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w'))
            self.plot.addItem(self._timeline)
        self._timeline.setPos(x)
        self._timeline.setVisible(True)

    def clear_timeline(self):
        """Hide the time cursor."""
        if self._timeline is not None:
            self._timeline.setVisible(False)

    def set_highlight(self, channel):
        """Shade the rows of the neurons on `channel` (mirrors the ephys
        channel highlight). Pass None to clear."""
        self._highlight_channel = channel
        if self._highlight_band is None:
            self._highlight_band = pg.LinearRegionItem(
                orientation='horizontal', movable=False,
                brush=pg.mkBrush(255, 255, 255, 40), pen=pg.mkPen(None))
            self._highlight_band.setZValue(-10)   # behind the spikes
            self.plot.addItem(self._highlight_band)

        ids = self._unit_ids if self._unit_ids is not None else []
        unit_channel = getattr(self, '_unit_channel', {})
        rows = [i for i, uid in enumerate(ids) if unit_channel.get(uid) == channel]
        if channel is not None and rows:
            self._highlight_band.setRegion((min(rows) - 0.5, max(rows) + 0.5))
            self._highlight_band.setVisible(True)
        else:
            self._highlight_band.setVisible(False)

    # ------------------------------------------------------------------
    # Load JRCLUST _res.mat
    # ------------------------------------------------------------------

    def load_matlab_files(self, path, sample_rate, channel_region_map, channel_color_map,
                          good_only=True, prm_path=None):
        """
        channel_region_map : {xml_channel_id: region_label} for the current tag.
        channel_color_map  : {xml_channel_id: (r, g, b, a)} matching the ephys colors.
        prm_path : JRCLUST .prm; its `siteMap` maps site index -> channel (1-based,
            so we subtract 1 to match the 0-based ephys XML channel IDs).
        """
        spike_times_raw, spike_clusters, cluster_sites, cluster_notes = self._read_mat(path)

        valid_ids = list(self._valid_unit_ids(spike_clusters, cluster_notes, good_only))
        site_map = [s - 1 for s in self._read_prm_sitemap(prm_path)]  # 1-based -> 0-based

        # channel of every good unit (cluster -> site -> channel); kept so the
        # raster can be re-filtered to another group when the tag changes
        self._unit_channel_all = {
            uid: int(site_map[int(cluster_sites[uid - 1]) - 1]) for uid in valid_ids
        }
        keep = np.isin(spike_clusters, valid_ids)
        self._all_spike_times = spike_times_raw[keep].astype(np.float64) / sample_rate
        self._all_spike_units = spike_clusters[keep]

        self.apply_group(channel_region_map, channel_color_map)

    def apply_group(self, channel_region_map, channel_color_map):
        """Filter/sort/label the loaded units to the current tag's group. Call
        again (with the new tag's maps) whenever the tag/shank changes."""
        # channels in chMap order (channel_region_map key order == chMap order)
        chmap_order = {int(c): i for i, c in enumerate(channel_region_map)}

        kept = [uid for uid, ch in self._unit_channel_all.items() if ch in chmap_order]
        kept.sort(key=lambda u: (chmap_order[self._unit_channel_all[u]], u))  # probe order

        self._unit_channel = {uid: self._unit_channel_all[uid] for uid in kept}
        self._channel_color_map = channel_color_map

        mask = np.isin(self._all_spike_units, kept)
        self._spike_times = self._all_spike_times[mask]
        self._spike_units = self._all_spike_units[mask]
        self._unit_ids    = np.array(kept)

        # channel can host several neurons -> label with both channel and neuron ID
        self._unit_labels = [f'ch{self._unit_channel[uid]} (n{uid})' for uid in kept]
        self._build_y_axis()

        # rows changed -> reposition the highlight band for the current group
        if self._highlight_channel is not None:
            self.set_highlight(self._highlight_channel)

    # ------------------------------------------------------------------
    # Call this every time the time window changes
    # ------------------------------------------------------------------

    def update_view(self, t_start, t_end):
        if self._spike_times is None:
            return

        for item in self._scatter_items:
            self.plot.removeItem(item)
        self._scatter_items.clear()

        mask = (self._spike_times >= t_start) & (self._spike_times <= t_end)
        if not mask.any():
            self.plot.setXRange(t_start, t_end, padding=0)
            return

        t_vis = self._spike_times[mask]
        u_vis = self._spike_units[mask]

        for i, uid in enumerate(self._unit_ids):
            umask = u_vis == uid
            if not umask.any():
                continue
            # same color as the channel's trace in the ephys view
            color = self._channel_color_map.get(self._unit_channel[uid], (200, 200, 200, 255))
            scatter = pg.ScatterPlotItem(
                x=t_vis[umask],
                y=np.full(umask.sum(), i),
                symbol='|',
                size=14,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(*color),
            )
            self.plot.addItem(scatter)
            self._scatter_items.append(scatter)

        self.plot.setXRange(t_start, t_end, padding=0)
        self.plot.setYRange(-0.5, len(self._unit_ids) - 0.5, padding=0)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_y_axis(self):
        ticks = [(i, self._unit_labels[i]) for i in range(len(self._unit_ids))]
        self.plot.getAxis('left').setTicks([ticks])
        self.plot.setYRange(-0.5, len(self._unit_ids) - 0.5, padding=0)

    @staticmethod
    def _is_hdf5(path):
        # MATLAB v7.3 files have a 128-byte text header before HDF5 content,
        # so magic bytes are not at offset 0. Check for '7.3' in the header instead.
        with open(path, 'rb') as f:
            header = f.read(128)
        return b'MATLAB 7.3' in header

    @staticmethod
    def _read_mat(path):
        """Return (spike_times_samples, spike_clusters, cluster_sites, cluster_notes)."""
        if not SpikeRuster._is_hdf5(path):
            res = sio.loadmat(path, squeeze_me=True)
            spike_times    = res['spikeTimes'].flatten()
            spike_clusters = res['spikeClusters'].flatten().astype(int)
            cluster_sites  = res.get('clusterSites', np.array([])).flatten().astype(int)
            notes          = res.get('clusterNotes', np.array([]))
            cluster_notes  = np.array([str(n).strip() for n in np.atleast_1d(notes).flatten()])
            return spike_times, spike_clusters, cluster_sites, cluster_notes

        # v7.3 files are HDF5
        with h5py.File(path, 'r') as f:
            spike_times    = f['spikeTimes'][:].flatten()
            spike_clusters = f['spikeClusters'][:].flatten().astype(int)
            cluster_sites  = f['clusterSites'][:].flatten().astype(int) if 'clusterSites' in f else np.array([])
            if 'clusterNotes' in f:
                refs = f['clusterNotes'][:]
                cluster_notes = np.array([
                    ''.join(chr(c) for c in f[r][:].flatten())
                    for r in refs.flatten()
                ])
            else:
                cluster_notes = np.array([])
        return spike_times, spike_clusters, cluster_sites, cluster_notes

    @staticmethod
    def _read_prm_sitemap(prm_path):
        """Parse the `siteMap` vector from a JRCLUST .prm file.

        Returns a list where site_map[i] is the recording channel for site
        index i+1 (siteMap is 1-indexed in MATLAB). Returns None if the file
        can't be read or siteMap isn't defined inline (e.g. it lives in a
        referenced probe file)."""
        import re
        try:
            with open(prm_path, 'r') as f:
                text = f.read()
        except OSError:
            return None

        text = re.sub(r'%[^\n]*', '', text)  # strip MATLAB comments
        m = re.search(r'\bsiteMap\b\s*=\s*(.+?);', text, re.DOTALL)
        if not m:
            return None
        rhs = m.group(1).strip().strip('[]').strip()

        # MATLAB range syntax: start:stop  or  start:step:stop
        if ':' in rhs:
            try:
                parts = [int(float(p)) for p in rhs.split(':')]
            except ValueError:
                return None
            if len(parts) == 2:
                return list(range(parts[0], parts[1] + 1))
            if len(parts) == 3:
                return list(range(parts[0], parts[2] + 1, parts[1]))
            return None

        nums = re.findall(r'-?\d+', rhs)
        return [int(n) for n in nums] if nums else None

    @staticmethod
    def _valid_unit_ids(spike_clusters, cluster_notes, good_only):
        all_ids = np.unique(spike_clusters[spike_clusters > 0])
        if not good_only or len(cluster_notes) == 0:
            return set(all_ids.tolist())
        valid = set()
        for uid in all_ids:
            idx = uid - 1  # JRCLUST is 1-indexed
            if idx < len(cluster_notes) and cluster_notes[idx].lower() in ('good', ''):
                valid.add(uid)
        return valid if valid else set(all_ids.tolist())
