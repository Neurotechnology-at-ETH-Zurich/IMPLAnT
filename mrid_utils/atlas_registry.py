# This Python file uses the following encoding: utf-8
"""Per-atlas constants and fetch metadata for every atlas IMPLAnT can use as
the active reference atlas (see mrid_utils/atlas_switch.py). Adding a new
atlas means adding one entry here -- everything else (coord_transform.py's
bregma/lambda/CC lookups, ephys/visualisation3D.py's CA1 region lookups,
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
        "cc_label": 67,
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
        # Resampled into WHS's own coordinate grid at matching 39um resolution,
        # so bregma/lambda land on the same voxel indices as WHS -- verified
        # against the fetched volume's shape in atlas_fetch_brainglobe.py.
        "bregma_coords": [245, 652, 439],
        "lambda_coords": [243, 441, 463],
        # Corpus-callosum label id and the CA1 region's exact name string in
        # this atlas's own structures list, looked up once against the
        # fetched BrainGlobeAtlas (see mrid_utils/atlas_fetch_brainglobe.py).
        "cc_label": 118,
        "ca1_region_name": "Field CA1",
    },
}

DEFAULT_ATLAS = "whs_sd_rat"


def get_active_atlas_id(paths):
    return paths.get("active_atlas", DEFAULT_ATLAS)


def get_active_atlas(paths):
    return ATLASES[get_active_atlas_id(paths)]
