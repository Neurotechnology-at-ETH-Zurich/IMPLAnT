#!/usr/bin/env python3
"""
itksnap_registration.py
=======================

Rigid registration of a MOVING image to a FIXED image, reproducing exactly what
ITK-SNAP's "Registration" panel does when you press "Run Registration".

Why this is faithful
--------------------
ITK-SNAP does not implement registration itself. `GUI/Model/RegistrationModel.cxx`
(`RegistrationModel::RunAutoRegistration`) builds a `GreedyParameters` struct and
calls `GreedyAPI::RunAffine()` from the *greedy* C++ library. This script drives
the very same greedy code through its official Python binding (`picsl_greedy`),
with the parameters set the way ITK-SNAP sets them:

    ITK-SNAP source                                  ->  greedy invocation here
    ------------------------------------------------------------------------
    param.affine_dof   = DOF_RIGID                   ->  -a -dof 6
    param.metric       = NMI (default) | NCC | SSD   ->  -m NMI | -m NCC 4x4x4 | -m SSD
    param.metric_radius = (4,4,4) for NCC            ->  (included above)
    param.iter_per_level: 100 for levels >= finest,  ->  -n 100x100x0x0  (example)
                          0 for finer levels
    param.affine_init_mode = RAS_FILENAME            ->  -ia <matrix>  (identity by default)
    ig.fixed_mask (optional segmentation mask)       ->  -gm <mask>
    everything else                                  ->  greedy defaults (untouched)

All other greedy settings (jitter, smoothing sigmas, NMI bin count, optimiser)
are left at their defaults, which is exactly what ITK-SNAP does.

Requirements
------------
    pip install picsl_greedy SimpleITK numpy

Usage
-----
Edit the CONFIGURATION block below and run `python itksnap_registration.py`,
or import `register_rigid()` from your own code, or use the command line:

    python itksnap_registration.py fixed.nii.gz moving.nii.gz \
        --metric NMI --coarsest 3 --finest 2 -o out/
"""

from __future__ import annotations

import argparse
import contextlib
import math
import os
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np
import SimpleITK as sitk
from picsl_greedy import Greedy3D

# =============================================================================
# CONFIGURATION  --  the three selections exposed as variables
# =============================================================================

# Path to the FIXED (reference / target) image -- ITK-SNAP's "main" image.
FIXED_IMAGE = "fixed.nii.gz"

# Path to the MOVING image -- the layer you select in ITK-SNAP's "Moving layer".
MOVING_IMAGE = "moving.nii.gz"

# ---- 1. Image similarity metric ---------------------------------------------
#   "NMI" -> Normalised Mutual Information   (ITK-SNAP's default)
#   "NCC" -> Normalised Cross-Correlation    (radius 4x4x4, as ITK-SNAP hardcodes)
#   "SSD" -> Sum of Squared Differences
METRIC = "NMI"

# ---- 2. & 3. Multi-resolution schedule --------------------------------------
# Level k corresponds to a shrink factor of 2**k, i.e. the "1x", "2x", "4x",
# "8x" entries of ITK-SNAP's drop-downs:
#     level 0 = "1x" (full resolution), level 1 = "2x", level 2 = "4x", ...
#
# COARSEST_LEVEL is where the optimisation starts, FINEST_LEVEL is where it
# stops. Levels finer than FINEST_LEVEL get 0 iterations (exactly as ITK-SNAP
# builds `param.iter_per_level`).
#
# Set either to None to use ITK-SNAP's automatic heuristic, which derives them
# from the fixed image dimensions (see `itksnap_default_levels`).
COARSEST_LEVEL: Optional[int] = None   # ITK-SNAP: "Coarsest level" drop-down
FINEST_LEVEL: Optional[int] = None     # ITK-SNAP: "Finest level"   drop-down

# ---- Optional extras ---------------------------------------------------------
# Iterations per active pyramid level. ITK-SNAP hardcodes 100.
ITERATIONS_PER_LEVEL = 100

# Optional fixed-image mask, mirroring ITK-SNAP's "Use segmentation as mask"
# checkbox (`ig.fixed_mask` / greedy's -gm). None = no mask.
FIXED_MASK: Optional[str] = None

# Where to write the outputs.
OUTPUT_DIR = "registration_output"

# Print greedy's optimiser log (the numbers ITK-SNAP plots in its progress graph).
VERBOSE = True


# =============================================================================
# ITK-SNAP parameter reproduction
# =============================================================================

#: RAS(greedy) <-> LPS(ITK/NIfTI-in-ITK) flip. Greedy works in RAS physical
#: space; ITK and SimpleITK work in LPS. Conjugating by this diagonal matrix
#: converts between the two.
_RAS_LPS_FLIP = np.diag([-1.0, -1.0, 1.0])


def itksnap_default_levels(fixed_size: Sequence[int]) -> tuple[int, int]:
    """Reproduce ITK-SNAP's automatic pyramid heuristic.

    Verbatim port of `RegistrationModel::ResetOnMainImageChange`:

        coarse_ub_1 = (int) log2(dim_min)
        coarse_ub_2 = (int) log2(dim_max / 32)
        coarsest    = max(0, min(coarse_ub_1, coarse_ub_2))
        finest      = max(0, coarsest - 1)

    Note `dim_max / 32` is integer division in the C++ source, so it is
    reproduced with `//` here.

    Returns
    -------
    (coarsest_level, finest_level)
    """
    dim_min = int(min(fixed_size))
    dim_max = int(max(fixed_size))

    coarse_ub_1 = int(math.log2(dim_min)) if dim_min > 0 else 0
    ratio = dim_max // 32
    coarse_ub_2 = int(math.log2(ratio)) if ratio > 0 else 0

    coarsest = max(0, min(coarse_ub_1, coarse_ub_2))
    finest = max(0, coarsest - 1)
    return coarsest, finest


def itksnap_iterations_per_level(coarsest: int, finest: int,
                                 iterations: int = ITERATIONS_PER_LEVEL) -> list[int]:
    """Reproduce ITK-SNAP's `param.iter_per_level` construction.

        for (k = coarsest; k >= 0; k--)
            iter_per_level.push_back(k >= finest ? 100 : 0);

    The resulting list is ordered coarsest-first, which is what greedy's
    `-n` flag expects.
    """
    if coarsest < 0:
        raise ValueError("coarsest level must be >= 0")
    if not (0 <= finest <= coarsest):
        raise ValueError("finest level must satisfy 0 <= finest <= coarsest")
    return [iterations if k >= finest else 0 for k in range(coarsest, -1, -1)]


def itksnap_metric_flag(metric: str) -> str:
    """Reproduce ITK-SNAP's metric switch, including the hardcoded NCC radius."""
    m = metric.strip().upper()
    if m == "NCC":
        # RegistrationModel.cxx: param.metric_radius = std::vector<int>(3, 4);
        return "-m NCC 4x4x4"
    if m == "NMI":
        return "-m NMI"
    if m == "SSD":
        return "-m SSD"
    raise ValueError(f"Unknown metric {metric!r}; expected one of NMI, NCC, SSD")


# =============================================================================
# Transform conversions
# =============================================================================

def ras_matrix_to_sitk_transform(mat_ras: np.ndarray) -> sitk.AffineTransform:
    """Convert a greedy 4x4 RAS matrix into a SimpleITK (LPS) transform.

    Greedy's affine maps a point in the FIXED image physical space to the
    corresponding point in the MOVING image physical space -- the same direction
    ITK/SimpleITK resampling expects -- so no inversion is needed, only the
    RAS->LPS flip.
    """
    mat_ras = np.asarray(mat_ras, dtype=float)
    A_ras, b_ras = mat_ras[:3, :3], mat_ras[:3, 3]

    A_lps = _RAS_LPS_FLIP @ A_ras @ _RAS_LPS_FLIP
    b_lps = _RAS_LPS_FLIP @ b_ras

    tfm = sitk.AffineTransform(3)
    tfm.SetMatrix(A_lps.flatten(order="C").tolist())
    tfm.SetTranslation(b_lps.tolist())
    return tfm


def sitk_transform_to_ras_matrix(tfm: sitk.Transform) -> np.ndarray:
    """Inverse of :func:`ras_matrix_to_sitk_transform`."""
    aff = sitk.AffineTransform(tfm)
    A_lps = np.array(aff.GetMatrix(), dtype=float).reshape(3, 3)
    b_lps = np.array(aff.GetTranslation(), dtype=float)

    mat = np.eye(4)
    mat[:3, :3] = _RAS_LPS_FLIP @ A_lps @ _RAS_LPS_FLIP
    mat[:3, 3] = _RAS_LPS_FLIP @ b_lps
    return mat


def write_ras_matrix(path: str, mat: np.ndarray) -> None:
    """Write a 4x4 RAS matrix in greedy/ITK-SNAP `.mat` text format."""
    np.savetxt(path, np.asarray(mat, dtype=float), fmt="%.10f")


def read_ras_matrix(path: str) -> np.ndarray:
    return np.loadtxt(path).reshape(4, 4)


# =============================================================================
# Result container
# =============================================================================

@dataclass
class RegistrationResult:
    """Everything ITK-SNAP ends up holding after a registration run."""

    #: 4x4 affine in RAS physical space (greedy / ITK-SNAP ".mat" convention),
    #: mapping fixed-image points to moving-image points.
    matrix_ras: np.ndarray

    #: The same transform as a SimpleITK object, ready for `sitk.Resample`.
    transform: sitk.AffineTransform

    #: Per-level optimiser metric values (what ITK-SNAP plots live). One dict
    #: per pyramid level, with a "TotalPerPixelMetric" array of per-iteration
    #: values.
    metric_log: list = field(default_factory=list)

    #: Pyramid schedule actually used, coarsest level first.
    iterations_per_level: list = field(default_factory=list)

    #: (coarsest, finest) levels used.
    levels: tuple = (0, 0)

    #: The greedy command line that was executed.
    command: str = ""

    @property
    def final_metric_value(self) -> Optional[float]:
        """Last metric value of the last active level, or None."""
        for level in reversed(self.metric_log):
            values = level.get("TotalPerPixelMetric") if isinstance(level, dict) else None
            if values is not None and len(values):
                return float(np.asarray(values).ravel()[-1])
        return None

    def rotation_translation(self) -> tuple[np.ndarray, np.ndarray]:
        """Decompose into rotation matrix (RAS) and translation vector (mm)."""
        return self.matrix_ras[:3, :3].copy(), self.matrix_ras[:3, 3].copy()

    def rotation_angles_deg(self) -> np.ndarray:
        """Euler angles (x, y, z, in degrees) of the rigid rotation, RAS axes."""
        R = self.matrix_ras[:3, :3]
        sy = math.hypot(R[0, 0], R[1, 0])
        if sy > 1e-9:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:  # gimbal lock
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0.0
        return np.degrees([x, y, z])


# =============================================================================
# Core: the registration itself
# =============================================================================

@contextlib.contextmanager
def _stdio_silencer(enabled: bool = True):
    """Silence greedy's optimiser log.

    greedy writes from C++ straight to file descriptors 1/2, so Python-level
    redirection is not enough -- the descriptors themselves are swapped.
    """
    if not enabled:
        yield
        return
    sys.stdout.flush()
    sys.stderr.flush()
    devnull = os.open(os.devnull, os.O_WRONLY)
    saved = (os.dup(1), os.dup(2))
    try:
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        yield
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(saved[0], 1)
        os.dup2(saved[1], 2)
        for fd in (*saved, devnull):
            os.close(fd)


def _as_image(img) -> sitk.Image:
    """Accept a path or a SimpleITK image; always return a float32 image.

    ITK-SNAP casts both layers to float before handing them to greedy
    (`CreateCastToFloatVectorPipeline`), so we do the same.
    """
    if isinstance(img, sitk.Image):
        out = img
    else:
        out = sitk.ReadImage(str(img))
    return sitk.Cast(out, sitk.sitkFloat32)


def register_rigid(
    fixed,
    moving,
    metric: str = METRIC,
    coarsest_level: Optional[int] = COARSEST_LEVEL,
    finest_level: Optional[int] = FINEST_LEVEL,
    iterations_per_level: int = ITERATIONS_PER_LEVEL,
    fixed_mask=None,
    initial_transform: Optional[sitk.Transform] = None,
    verbose: bool = True,
    threads: Optional[int] = None,
    search_iterations: int = 0,
    search_rotation_deg: float = 15.0,
    search_translation_mm: float = 15.0,
    seed: Optional[int] = None,
) -> RegistrationResult:
    """Run ITK-SNAP's automatic *rigid* registration.

    Parameters
    ----------
    fixed, moving
        Paths or SimpleITK images. `fixed` is ITK-SNAP's main image, `moving`
        is the selected moving layer.
    metric
        "NMI" (ITK-SNAP default), "NCC" (radius 4x4x4) or "SSD".
    coarsest_level, finest_level
        Multi-resolution schedule; level k means shrink factor 2**k, so level 0
        is "1x". `None` reproduces ITK-SNAP's automatic choice from the fixed
        image size.
    iterations_per_level
        Iterations at each active level (ITK-SNAP hardcodes 100).
    fixed_mask
        Optional path/image used as greedy's `-gm` fixed mask, mirroring
        ITK-SNAP's "Use segmentation as mask".
    initial_transform
        Optional SimpleITK transform to start from -- the equivalent of having
        moved the layer manually (or run "match by moments") in ITK-SNAP before
        pressing Run. Defaults to identity.
    threads
        Optional cap on concurrent threads.
    search_iterations
        greedy's `-search N <rot> <tran>` random-restart count. greedy always
        applies a random jitter (uniform +/-0.4 per raw coefficient) whenever
        the starting transform is near-identity in voxel space, has no
        best-so-far fallback when its lbfgs line search fails, and reseeds
        its RNG from the system clock by default -- so a single unlucky jitter
        draw can silently corrupt an already-well-aligned pair, non-reproducibly,
        run to run. `-search` mitigates this by drawing `search_iterations`
        random rigid perturbations and keeping only the one that scores better
        than the (already-jittered) baseline before optimization starts.
        0 (default) reproduces ITK-SNAP's own default of not using it.
    search_rotation_deg, search_translation_mm
        Standard deviation of the random restarts' rotation/translation,
        only used when search_iterations > 0.
    seed
        Optional greedy `-seed` value, for reproducible jitter/search draws
        across repeated runs on the same inputs. None leaves greedy's default
        (time-based, different every run).

    Returns
    -------
    RegistrationResult
    """
    fixed_img = _as_image(fixed)
    moving_img = _as_image(moving)

    # --- pyramid schedule ----------------------------------------------------
    auto_coarsest, auto_finest = itksnap_default_levels(fixed_img.GetSize())
    coarsest = auto_coarsest if coarsest_level is None else int(coarsest_level)
    finest = auto_finest if finest_level is None else int(finest_level)

    # ITK-SNAP's drop-downs keep the two consistent (SetCoarsestResolutionLevelValue
    # / SetFinestResolutionLevelValue clamp one against the other).
    if finest > coarsest:
        raise ValueError(
            f"finest level ({finest}) must not be coarser than the coarsest "
            f"level ({coarsest}); level k means a shrink factor of 2**k"
        )

    iters = itksnap_iterations_per_level(coarsest, finest, iterations_per_level)
    n_flag = "x".join(str(i) for i in iters)

    # --- assemble the greedy command ----------------------------------------
    kwargs = {"FIXED_IMAGE": fixed_img, "MOVING_IMAGE": moving_img}

    cmd = ["-d 3", "-a", "-dof 6", itksnap_metric_flag(metric),
           "-i FIXED_IMAGE MOVING_IMAGE", f"-n {n_flag}"]

    if fixed_mask is not None:
        kwargs["GRADIENT_MASK"] = _as_image(fixed_mask)
        cmd.append("-gm GRADIENT_MASK")

    if threads:
        cmd.append(f"-threads {int(threads)}")

    if search_iterations > 0:
        cmd.append(f"-search {int(search_iterations)} {search_rotation_deg} {search_translation_mm}")

    if seed is not None:
        cmd.append(f"-seed {int(seed)}")

    with tempfile.TemporaryDirectory() as tmp:
        out_mat = os.path.join(tmp, "affine.mat")

        # ITK-SNAP always uses affine_init_mode = RAS_FILENAME with the layer's
        # current transform; identity unless the user moved the layer first.
        if initial_transform is not None:
            init_mat = os.path.join(tmp, "init.mat")
            write_ras_matrix(init_mat, sitk_transform_to_ras_matrix(initial_transform))
            cmd.append(f"-ia {init_mat}")
        else:
            # Plain -ia-identity starts EXACTLY at voxel-space identity, which
            # unconditionally triggers greedy's InitializeAffineTransform random
            # jitter (uniform +/-0.4 per raw coefficient, no opt-out flag) --
            # and there's no best-so-far fallback if lbfgs's line search then
            # fails, so the jitter can silently corrupt an already-aligned pair.
            # Nudge deterministically past the trigger's 1e-4 (voxel-space)
            # threshold with a physically-negligible offset instead, so the
            # optimizer gets a clean, unjittered, reproducible start.
            nudge_mat = os.path.join(tmp, "nudge.mat")
            nudge = np.eye(4)
            nudge[0, 3] = 0.5  # mm; anatomically negligible, safely > 1e-4
            write_ras_matrix(nudge_mat, nudge)
            cmd.append(f"-ia {nudge_mat}")

        cmd.append(f"-o {out_mat}")
        command = " ".join(cmd)

        g = Greedy3D()
        with _stdio_silencer(enabled=not verbose):
            g.execute(command, **kwargs)

        matrix_ras = read_ras_matrix(out_mat)
        try:
            metric_log = list(g.metric_log())
        except Exception:
            metric_log = []

    return RegistrationResult(
        matrix_ras=matrix_ras,
        transform=ras_matrix_to_sitk_transform(matrix_ras),
        metric_log=metric_log,
        iterations_per_level=iters,
        levels=(coarsest, finest),
        command=command,
    )


# =============================================================================
# Applying the result
# =============================================================================

def resample_moving(moving, fixed, result: RegistrationResult,
                    interpolator=sitk.sitkLinear,
                    default_value: float = 0.0) -> sitk.Image:
    """Resample the moving image into the fixed image space.

    This is what ITK-SNAP shows you after registration, and what its
    "Save resampled image" produces (linear interpolation).
    """
    moving_img = _as_image(moving)
    fixed_img = _as_image(fixed)
    return sitk.Resample(moving_img, fixed_img, result.transform,
                         interpolator, default_value, moving_img.GetPixelID())


def save_transform(result: RegistrationResult, path: str) -> None:
    """Save the transform.

    `.mat` / `.txt` with 4 rows -> greedy/ITK-SNAP RAS matrix format
    (ITK-SNAP: Registration panel -> save icon -> "Convert3D matrix format").

    Any ITK transform extension (`.tfm`, `.txt` via ITK writer, `.h5`) ->
    ITK format (ITK-SNAP's "ITK transform format").
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".mat":
        write_ras_matrix(path, result.matrix_ras)
    else:
        sitk.WriteTransform(result.transform, path)


# =============================================================================
# Convenience wrapper + CLI
# =============================================================================

def run(fixed_path: str = FIXED_IMAGE,
        moving_path: str = MOVING_IMAGE,
        metric: str = METRIC,
        coarsest_level: Optional[int] = COARSEST_LEVEL,
        finest_level: Optional[int] = FINEST_LEVEL,
        fixed_mask: Optional[str] = FIXED_MASK,
        output_dir: str = OUTPUT_DIR,
        verbose: bool = VERBOSE) -> RegistrationResult:
    """Register, report, and write transform + resampled image to `output_dir`."""
    os.makedirs(output_dir, exist_ok=True)

    result = register_rigid(
        fixed_path, moving_path,
        metric=metric,
        coarsest_level=coarsest_level,
        finest_level=finest_level,
        fixed_mask=fixed_mask,
        verbose=verbose,
    )

    coarsest, finest = result.levels
    print("\n" + "=" * 68)
    print("ITK-SNAP-equivalent rigid registration")
    print("=" * 68)
    print(f"  fixed            : {fixed_path}")
    print(f"  moving           : {moving_path}")
    print(f"  transform model  : Rigid (6 DOF)")
    print(f"  similarity metric: {metric.upper()}")
    print(f"  coarsest level   : {coarsest}  ({2 ** coarsest}x)")
    print(f"  finest level     : {finest}  ({2 ** finest}x)")
    print(f"  iterations/level : {result.iterations_per_level}  (coarsest first)")
    if result.final_metric_value is not None:
        print(f"  final metric     : {result.final_metric_value:.6f}")
    print("\n  RAS transform (fixed -> moving):")
    for row in result.matrix_ras:
        print("   " + "  ".join(f"{v: 10.5f}" for v in row))
    rx, ry, rz = result.rotation_angles_deg()
    tx, ty, tz = result.matrix_ras[:3, 3]
    print(f"\n  rotation (deg): x={rx: .3f}  y={ry: .3f}  z={rz: .3f}")
    print(f"  translation(mm): x={tx: .3f}  y={ty: .3f}  z={tz: .3f}")

    mat_path = os.path.join(output_dir, "transform.mat")
    tfm_path = os.path.join(output_dir, "transform.tfm")
    img_path = os.path.join(output_dir, "moving_registered.nii.gz")

    save_transform(result, mat_path)
    save_transform(result, tfm_path)
    sitk.WriteImage(resample_moving(moving_path, fixed_path, result), img_path)

    print(f"\n  wrote {mat_path}   (load in ITK-SNAP as Convert3D matrix)")
    print(f"  wrote {tfm_path}   (load in ITK-SNAP as ITK transform)")
    print(f"  wrote {img_path}")
    print("=" * 68 + "\n")
    return result


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Rigid registration reproducing ITK-SNAP's automatic registration.")
    p.add_argument("fixed", nargs="?", default=FIXED_IMAGE, help="fixed (main) image")
    p.add_argument("moving", nargs="?", default=MOVING_IMAGE, help="moving image")
    p.add_argument("--metric", default=METRIC, choices=["NMI", "NCC", "SSD"],
                   help="image similarity metric (default: NMI, as in ITK-SNAP)")
    p.add_argument("--coarsest", type=int, default=COARSEST_LEVEL,
                   help="coarsest pyramid level (k -> 2**k shrink); omit for ITK-SNAP's auto choice")
    p.add_argument("--finest", type=int, default=FINEST_LEVEL,
                   help="finest pyramid level; omit for ITK-SNAP's auto choice")
    p.add_argument("--mask", default=FIXED_MASK, help="optional fixed-image mask (-gm)")
    p.add_argument("-o", "--output-dir", default=OUTPUT_DIR)
    p.add_argument("-q", "--quiet", action="store_true", help="suppress greedy's optimiser log")
    a = p.parse_args(argv)

    run(a.fixed, a.moving, a.metric, a.coarsest, a.finest,
        a.mask, a.output_dir, verbose=not a.quiet)


if __name__ == "__main__":
    main()
