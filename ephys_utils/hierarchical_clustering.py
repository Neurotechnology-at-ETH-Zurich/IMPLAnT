# This Python file uses the following encoding: utf-8
import numpy as np
from scipy.stats import zscore
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, optimal_leaf_ordering, leaves_list
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# -----------------------------------------------------------------------
# Activity matrix
# -----------------------------------------------------------------------

def build_activity_matrix(spike_times, spike_clusters, unit_ids, sample_rate, bin_ms=25):
    """
    Bin spike counts per unit into time bins.

    Parameters
    ----------
    spike_times : ndarray (N,) — spike times in samples
    spike_clusters : ndarray (N,) — unit ID per spike
    unit_ids : array-like — which unit IDs to include (in order)
    sample_rate : float — Hz
    bin_ms : float — bin size in milliseconds

    Returns
    -------
    activity : ndarray (n_units, n_bins)
    time_bins : ndarray (n_bins,) — bin centres in seconds
    """
    spike_times_s = spike_times.astype(np.float64) / sample_rate
    duration = spike_times_s.max()
    bin_s = bin_ms / 1000.0
    edges = np.arange(0, duration + bin_s, bin_s)
    time_bins = edges[:-1] + bin_s / 2.0

    activity = np.zeros((len(unit_ids), len(time_bins)), dtype=np.float64)
    for i, uid in enumerate(unit_ids):
        mask = spike_clusters == uid
        activity[i] = np.histogram(spike_times_s[mask], bins=edges)[0]

    return activity, time_bins


# -----------------------------------------------------------------------
# Correlation matrix
# -----------------------------------------------------------------------

def compute_correlation_matrix(activity):
    """
    Z-score each unit's spike-count vector then compute pairwise Pearson correlation.

    Parameters
    ----------
    activity : ndarray (n_units, n_bins)

    Returns
    -------
    corr_matrix : ndarray (n_units, n_units)
    """
    z = zscore(activity, axis=1)
    z = np.nan_to_num(z)  # silent units → zeros
    return np.corrcoef(z)


# -----------------------------------------------------------------------
# Optimal threshold (elbow method)
# -----------------------------------------------------------------------

def find_optimal_threshold_elbow(linkage_matrix):
    distances = linkage_matrix[:, 2]
    deltas = np.diff(distances)
    elbow_idx = np.argmax(deltas)
    return distances[elbow_idx]


# -----------------------------------------------------------------------
# Figure 1: plain correlation matrix heatmap  (Peter's main-script figure)
# -----------------------------------------------------------------------

def plot_correlation_matrix(corr_matrix, labels, colormap=None, clim=(-0.4, 0.4)):
    """
    Heatmap of the raw (unordered) correlation matrix — matches the first
    figure produced before hierarchical clustering in Peter's main script.

    Returns
    -------
    fig : matplotlib Figure
    """
    if colormap is None:
        colormap = plt.cm.RdBu_r

    n = corr_matrix.shape[0]
    plot_corr = corr_matrix - np.diag(np.diag(corr_matrix))

    fig, ax = plt.subplots(figsize=(10, 9))
    im = ax.imshow(plot_corr, aspect='auto', cmap=colormap,
                   vmin=clim[0], vmax=clim[1])
    ax.set_xticks(range(n))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=7)
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_title('Pairwise Neuronal Spike-Count Correlation')
    ax.set_aspect('equal')
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    fig.tight_layout()

    return fig


def plot_dendrogram_and_heatmap(corr_matrix, labels, p=9.5, clim=(-0.3, 0.3)):
    """
    Compute hierarchical clustering order and return the reordered correlation
    matrix as a numpy array (no matplotlib figure — rendering is done by the
    caller via pyqtgraph).

    Returns
    -------
    cluster_labels : list of (label, cluster_id) tuples in dendrogram order
    reordered      : ndarray (n, n) — correlation matrix reordered to match
                     dendrogram leaf order, diagonal zeroed
    """
    labels = list(labels)
    n = corr_matrix.shape[0]

    corr_clean = np.clip(np.nan_to_num(corr_matrix, nan=0.0), -1.0, 1.0)
    dist_matrix = (1.0 - corr_clean) ** p
    dist_matrix = 0.5 * (dist_matrix + dist_matrix.T)
    np.fill_diagonal(dist_matrix, 0.0)
    dist_vector = squareform(dist_matrix, checks=False)

    Z = linkage(dist_vector, method='ward')
    Z_ordered = optimal_leaf_ordering(Z, dist_vector)
    dendr_order = leaves_list(Z_ordered)   # shallow first → ch126 (deepest) at bottom

    optimal_threshold = find_optimal_threshold_elbow(Z)
    cluster_ids = fcluster(Z, optimal_threshold, criterion='distance')

    plot_corr = corr_matrix - np.diag(np.diag(corr_matrix))
    reordered = plot_corr[np.ix_(dendr_order, dendr_order)]

    cluster_labels = [(labels[i], int(cluster_ids[i])) for i in dendr_order]

    return cluster_labels, reordered


# -----------------------------------------------------------------------
# Main entry point: runs both figures
# -----------------------------------------------------------------------

def hierarchical_clustering(corr_matrix, labels, p=9.5, clim_reordered=(-0.3, 0.3)):
    """
    Returns
    -------
    cluster_labels : list of (label, cluster_id) in dendrogram order
    reordered      : ndarray (n, n) — correlation matrix ready for display
    """
    return plot_dendrogram_and_heatmap(corr_matrix, labels, p=p, clim=clim_reordered)


# -----------------------------------------------------------------------
# Convenience: load custom colormap from .mat if available
# -----------------------------------------------------------------------

def load_custom_colormap(mat_path, key='CustomColormap3'):
    """Load a colormap saved from MATLAB as an Nx3 RGB array."""
    try:
        import scipy.io as sio
        data = sio.loadmat(mat_path, squeeze_me=True)
        rgb = data[key]
        return mcolors.ListedColormap(rgb)
    except Exception:
        return None
