# This Python file uses the following encoding: utf-8
"""Pre-flight free-RAM check for launching a SAMRI registration -- doesn't
touch anything inside samri/ (registration parameters, atlas resolution,
num_threads, ...); it only decides whether to let the existing call happen
at all. Exists because antsRegistration's peak memory for a full-resolution
SyN stage scales with the FIXED image's voxel count (confirmed empirically:
a 512x1024x512 WHS rat atlas peaked at ~37.9GB anon-rss, i.e. ~150 bytes per
voxel), and a run that starts without enough headroom can take the whole
desktop down hours later via the kernel OOM killer rather than failing fast.

Estimating from the fixed image's own header (via nibabel) rather than a
hardcoded number is what makes this portable across machines: a lab desktop
with 16GB RAM and a smaller/lower-res atlas, and a workstation with 128GB and
the full WHS atlas, each get a threshold scaled to their own atlas file and
their own available RAM, instead of a number tuned for one machine.
"""
import nibabel as nib
import psutil

# Empirically calibrated from the 2026-09-01 OOM: a 512x1024x512 fixed image
# (268,435,456 voxels) drove antsRegistration to ~37.9GB anon-rss during the
# full-resolution SyN stage, i.e. ~148 bytes/voxel. This is a single data
# point, not an analytic model (real usage also depends on which stages/
# metrics run), so it's rounded up with some margin rather than treated as
# exact -- but not padded so far past the measured value that the estimate
# stops being useful (e.g. 220 pushed that same atlas to ~63GB required).
BYTES_PER_FIXED_IMAGE_VOXEL = 150
# Registration also needs room for the moving image, OS, and everything else
# already resident -- on top of the fixed-image estimate above.
BASELINE_OVERHEAD_GB = 4


def estimate_required_gb(fixed_image_path):
    """Rough peak-memory estimate (GB) for registering against fixed_image_path,
    based only on its own voxel count -- so it scales automatically with
    whatever atlas/template a given machine is actually configured to use."""
    img = nib.load(fixed_image_path)
    voxel_count = 1
    for dim in img.shape[:3]:
        voxel_count *= dim
    return (voxel_count * BYTES_PER_FIXED_IMAGE_VOXEL) / 1e9 + BASELINE_OVERHEAD_GB


def available_gb():
    """Free-to-use RAM (GB) right now, per the OS's own accounting (psutil's
    'available', not raw 'free' -- this already counts reclaimable cache as
    usable, matching what the kernel itself would offer a new allocation)."""
    return psutil.virtual_memory().available / 1e9


def check(fixed_image_path):
    """Returns (ok, required_gb, available_gb). ok is False when available
    memory doesn't cover the estimated requirement -- caller decides what to
    do with that (e.g. warn and let the user proceed anyway, or block)."""
    required = estimate_required_gb(fixed_image_path)
    available = available_gb()
    return available >= required, required, available
