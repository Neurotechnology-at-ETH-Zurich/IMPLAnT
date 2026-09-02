# This Python file uses the following encoding: utf-8
"""Per-atlas constants and fetch metadata for every atlas IMPLAnT can use as
the active reference atlas (see mrid_utils/atlas_switch.py). Adding a new
atlas means adding one entry here -- everything else (coord_transform.py's
bregma/lambda lookups, ephys/visualisation3D.py's CA1 region lookups,
atlas_fetch.py/atlas_fetch_brainglobe.py's file presence checks) reads its
constants from whichever entry is active via paths_config._paths, rather
than from hardcoded literals.
"""

ATLASES = {
    "whs_sd_rat": {
        "display_name": "WHS SD rat (MRI/DTI)",
        "source": "bundle",  # mrid_utils/atlas_fetch.py's existing GitHub-release bundle
        "subfolder": None,   # files sit directly in atlas_folder (back-compat with existing installs)
        "files": {
            "atlas_volume": "WHS_SD_rat_atlas_v4.nii.gz",
            "atlas_labels": "WHS_SD_rat_atlas_v4.label",
            "atlas_dwi": "WHS_SD_rat_DWI_v1.01.nii.gz",
            "atlas_template": "WHS_SD_rat_T2star_v1.01.nii.gz",
            "atlas_mask": "WHS_SD_v2_brainmask_bin.nii.gz",
        },
        "has_dwi": True,
        "label_format": "whs_legacy",
        "bregma_coords": [245, 652, 439],
        "lambda_coords": [243, 441, 463],
        "ca1_region_name": "Cornu ammonis 1",
    },
    "whs_sd_swc_female_rat": {
        "display_name": "WHS-aligned SWC female rat (microscopy)",
        "source": "brainglobe",
        "brainglobe_name": "whs_sd_swc_female_rat_39um",
        "subfolder": "whs_sd_swc_female_rat",  # converted files land in atlas_folder/<subfolder>/
        "files": {
            "atlas_volume": "annotation.nii.gz",
            "atlas_labels": "structures.label",
            "atlas_template": "reference.nii.gz",
            "atlas_mask": "mask.nii.gz",
        },
        "has_dwi": False,
        "label_format": "itk_snap",
        # BrainGlobeAtlas('whs_sd_swc_female_rat_39um').orientation reports
        # "asr", same as BrainGlobeAtlas('whs_sd_rat_39um') -- but its
        # annotation array is left-right MIRRORED relative to that plain WHS
        # atlas despite the identical reported orientation (confirmed by
        # comparing both atlases' native foreground masks directly: IoU is
        # 0.706 unflipped vs 0.880 flipped along the native "r" axis, and by
        # an exact voxel-for-voxel corpus-callosum-centroid match, to 8
        # significant figures, between IMPLAnT's existing raw
        # WHS_SD_rat_atlas_v4.nii.gz and this atlas once so flipped -- vs.
        # only a coarse/approximate match without it). This looks like a
        # packaging inconsistency specific to this one BrainGlobe atlas
        # (whs_sd_rat_39um needs no such extra flip to match the same raw
        # file exactly). atlas_fetch_brainglobe.py must map this atlas's
        # annotation/reference to orientation "rpi" (not "lpi", which is
        # what its own stated "asr" would naively imply) via
        # brainglobe_space.AnatomicalSpace to land in IMPLAnT's existing
        # voxel-index convention. Re-verify this if BrainGlobe ever
        # re-publishes a corrected version of this atlas.
        "brainglobe_target_orientation": "rpi",
        # Resampled into WHS's own coordinate grid at matching 39um
        # resolution (once correctly un-mirrored, see above), so bregma/
        # lambda land on the same voxel indices as WHS.
        "bregma_coords": [245, 652, 439],
        "lambda_coords": [243, 441, 463],
        # Verified directly against this atlas's own structures list: its
        # terminology reuses WHS's own id for this region (id 98 = "Cornu
        # ammonis 1") -- identical to the plain WHS atlas already used, so
        # no atlas-specific override was actually needed here.
        "ca1_region_name": "Cornu ammonis 1",
    },
}

DEFAULT_ATLAS = "whs_sd_rat"


def get_active_atlas_id(paths):
    return paths.get("active_atlas", DEFAULT_ATLAS)


def get_active_atlas(paths):
    return ATLASES[get_active_atlas_id(paths)]
