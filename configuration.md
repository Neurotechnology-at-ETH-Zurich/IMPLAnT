---
title: Configuration
nav_order: 3
---

# Configuration
{: .no_toc }

1. TOC
{:toc}

## Atlas files

IMPLAnT uses the [Waxholm Space (WHS) rat brain atlas](https://www.nitrc.org/projects/whs-sd-atlas) (5 files, ~1.3GB total).

**Nothing to do here by default.** The first time you open ephys data, start SAMRI registration, or start trajectory planning, IMPLAnT asks to confirm and then downloads + caches these files automatically, into an `atlas/` folder next to `main_window.py` (source) or next to the built executable (standalone) — the same convention as `ants/bin/`. This needs an internet connection *once*; every run after that reuses the cached copy with no network access at all.

If you'd rather set this up yourself — e.g. a machine with no internet access, or to reuse an atlas copy you already have on disk — place the 5 files below into that same `atlas/` folder before first use, and the automatic download is skipped entirely:

| File | Description |
|------|-------------|
| `WHS_SD_rat_atlas_v4.nii.gz` | Atlas volume |
| `WHS_SD_rat_atlas_v4.label` | Region labels |
| `WHS_SD_rat_T2star_v1.01.nii.gz` | Template |
| `WHS_SD_rat_DWI_v1.01.nii.gz` | DWI template |
| `WHS_SD_v2_brainmask_bin.nii.gz` | Brain mask |

If you'd rather keep the atlas elsewhere (e.g. a shared cache used by multiple installs), copy `paths_config.example.json` to `paths_config.json` and set `atlas_folder` to an absolute path instead:

```bash
cp paths_config.example.json paths_config.json
```

```json
{
    "ants_bin": "ants/bin",
    "raw_base": "/path/to/raw/data/",
    "atlas_folder": "/path/to/atlas/folder",
    "atlas_volume": "WHS_SD_rat_atlas_v4.nii.gz",
    "atlas_labels": "WHS_SD_rat_atlas_v4.label",
    "atlas_dwi": "WHS_SD_rat_DWI_v1.01.nii.gz",
    "atlas_template": "WHS_SD_rat_T2star_v1.01.nii.gz",
    "atlas_mask": "WHS_SD_v2_brainmask_bin.nii.gz"
}
```

`raw_base` (root directory for raw Bruker data and BIDS output) still needs an absolute path in `paths_config.json` either way — that data is typically large and kept on its own drive/share, so it isn't defaulted to a folder next to the app.

- **From source**: place `paths_config.json` in the repository root.
- **Standalone app**: place `paths_config.json` in the same folder as the `IMPLAnT` executable.

## Atlas

IMPLAnT can register and plan against either of two atlases:

| Atlas | What it is | Source |
|-------|------------|--------|
| **WHS SD rat (MRI/DTI)** *(default)* | The bundled Waxholm Space atlas described above | Downloaded once, as above |
| **WHS-aligned SWC female rat (microscopy)** | A higher-resolution microscopy atlas, resampled onto the same WHS coordinate grid | Fetched automatically via [BrainGlobe](https://brainglobe.info/) the first time you select it |

Switch between them via **File → Atlas…**, or live from the dropdown on the [Pre-surgical planning](tutorials/pre-surgical-planning) screen itself. The first time you select the microscopy atlas, IMPLAnT downloads and converts it automatically (a one-time step, same idea as the initial WHS atlas download); every switch after that is instant.

## MRID library file

The electrode localisation feature requires `mrid_library.pkl`, a lookup file specific to your experimental setup. Place it in the repository root (next to `main_window.py`) or next to the `IMPLAnT` executable. If no file is found, you'll be prompted to browse for it manually — click **Save** next to the browse field to remember that path in `paths_config.json` (as `mrid_library`) so it's the default on future runs too.

{: .note }
A dummy `mrid_library.pkl` is included in the repository for testing. It contains placeholder entries for all four supported MRID types (`duo`, `trio`, `quad`, `penta`) with uniform geometry values, and can be used to verify the localisation pipeline without real calibration data. Replace it with your own calibrated file before running actual experiments.

## Bruker scanner (optional)

If you are fetching raw data directly from a Bruker MRI scanner, copy `samri/bruker_info.example.json` to `samri/bruker_info.json` and fill in your scanner's hostname and password:

```bash
cp samri/bruker_info.example.json samri/bruker_info.json
```

```json
{
    "server": "your-scanner-hostname",
    "password": "your-password"
}
```

`samri/bruker_info.json` is gitignored, never shared, and explicitly excluded from standalone builds — it never leaves your machine. If you don't use a Bruker scanner, you can skip this entirely; the fields will simply be left blank in the UI.

## Data folder structure

IMPLAnT expects your session data to follow this folder structure. The app derives paths automatically from the file you load, so keeping this layout is important for registration and localisation to work correctly.

```
your-session/
  anat/
    sub-001_T1w_ind_0.nii.gz          ← pre-surgical MRI (main file)
    sub-001_T2w_ind_1.nii.gz          ← post-implant MRI (added via Load Another MRI Image)
    transformation_ind_1-to-ind_0.txt ← registration output (auto-generated)
  registration/                       ← SAMRI registration output (auto-generated)
  analysed/                           ← localisation outputs (auto-generated)
  ephys/
    recording.dat                     ← electrophysiology recording
```

---

Next: follow the [tutorials](tutorials) to walk through a full session.
