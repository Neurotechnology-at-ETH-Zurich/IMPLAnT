![IMPLAnT](Icons/Github/logo_Final.png)
# IMPLAnT - Integrated Multimodal Planning, Localisation, Analysis Toolbox


Intracranial electrode implantation involves three distinct workflows: surgical planning, post-implant electrode localisation, and electrophysiological analysis. Currently, these steps are carried out through disconnected tools and custom scripts.
IMPLAnT is an open-source graphical user interface (GUI) that unifies all three stages into one single, cohesive platform improving both reproducibility and efficiency.

Currently, the GUI contains the following functions:

- **Pre-surgical planning** - register subject MRI data to the WHS brain atlas, letting you plan and visualise electrode trajectories before surgery
- **Post-implant localisation** - uses semi-supervised pipeline for MR identification tags to localise electrodes after implantation and automatically assign atlas-defined region labels to each channel to facilitate a more accurate analysis 
- **Electrophysiology data visualisation** - visualises and curates signal data channel-by-channel, directly linked to the anatomical labels from previous steps

Electrophysiology data preprocessing and analysis is planned to be implemented in the next few weeks.
As far as we are aware, IMPLAnT is the first open-source tool to bridge this entire pipeline in one interface. It is released fully open-source and designed to adapt to a range of experimental protocols.


## Screenshots

**Pre-surgical trajectory planning** — plan and visualise electrode trajectories across axial, sagittal, and coronal views of the WHS rat brain atlas, with individual shanks labelled directly in 3D.

![Trajectory Planning](Icons/Github/Trajectory_Planning.png)

**Electrophysiology visualisation** — view raw signal traces colour-coded by atlas region alongside a 3D rendering of the implanted electrodes, with per-channel anatomical labels and coordinates.

![Ephys](Icons/Github/Ephys.png)



## Requirements

- **OS**: Linux (tested on Ubuntu 24)
- **Python**: 3.10 (from source only)
- **ANTs**: required by all users (see [Dependencies](#dependencies))

## Release

Pre-built standalone executables for **Linux** are available on the [Releases page](../../releases). No Python installation is required — download the executable, install ANTs, and configure `paths_config.json` as described in [Configuration](#configuration).

## Installation

Choose one of two options:
- **Download the release** from the [Releases page](../../releases) — no Python installation needed
- **Run from source** — requires Python 3.10 and all dependencies

Regardless of which option you choose, **ANTs must be installed separately** (see [Dependencies](#dependencies)).

### Dependencies
IMPLAnT requires **ANTs** (Advanced Normalization Tools) for MRI registration. ANTs is not a Python package and must be installed separately by all users.

1. Download ANTs from the [ANTs releases page](https://github.com/ANTsX/ANTs/releases)
2. Place the ANTs binaries so that the folder structure looks like this:

   **From source:**
   ```
   IMPLAnT/
     ants/
       bin/
         antsRegistration
         antsApplyTransforms
         ...
   ```

   **Standalone application:**
   ```
   IMPLAnT  (executable)
   ants/
     bin/
       antsRegistration
       antsApplyTransforms
       ...
   ```

### From source
1. Clone the repository
   ```
   git clone git@github.com:Neurotechnology-at-ETH-Zurich/IMPLAnT.git
   ```
2. Install dependencies
   ```
   cd IMPLAnT
   pip install -r requirements.txt
   ```
3. Install ANTs as described above

4. Run the app
   ```
   python main_window.py
   ```
   Alternatively, in Qt Creator: open the project and press Ctrl+R

### Standalone application

1. Install ANTs as described above
2. Build the executable
   ```
   pyinstaller MRID_GUI.spec
   ```
3. The app is created at `dist/IMPLAnT`
4. Place the `ants/bin/` folder next to the executable as described in [Dependencies](#dependencies)

## Configuration

### Atlas files

IMPLAnT uses the [Waxholm Space (WHS) rat brain atlas](https://www.nitrc.org/projects/whs-sd-atlas). Download the following files and place them in a folder of your choice:

| File | Description |
|------|-------------|
| `WHS_SD_rat_atlas_v4.nii.gz` | Atlas volume |
| `WHS_SD_rat_atlas_v4.label` | Region labels |
| `WHS_SD_rat_T2star_v1.01.nii.gz` | Template |
| `WHS_SD_rat_DWI_v1.01.nii.gz` | DWI template |
| `WHS_SD_v2_brainmask_bin.nii.gz` | Brain mask |

Copy `paths_config.example.json` to `paths_config.json` and edit it to match your local setup:

```bash
cp paths_config.example.json paths_config.json
```

- `atlas_folder`: path to the folder where you saved the atlas files
- `raw_base`: root directory where raw Bruker data is stored and BIDS output will be written

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

- **From source**: place `paths_config.json` in the repository root
- **Standalone app**: place `paths_config.json` in the same folder as the `IMPLAnT` executable

### MRID library file

The electrode localization feature requires `mrid_library.pkl`, a lookup file specific to your experimental setup. Place it in the repository root (next to `main_window.py`) or next to the `IMPLAnT` executable. If no file is found, you will be prompted to browse for it manually. A dummy version for testing is included with the app.

### Bruker scanner (optional)

If you are fetching raw data directly from a Bruker MRI scanner, create a file `samri/bruker_info.json` with your scanner's hostname and password:
```json
{
    "server": "your-scanner-hostname",
    "password": "your-password"
}
```
This file is gitignored and never shared. If you don't use a Bruker scanner, you can skip this — the fields will simply be left blank in the UI.

## Usage
TODO - not yet finished
IMPLAnT follows a three-stage workflow:

**1. Pre-surgical planning**
Register the subject MRI to the WHS atlas via the *SAMRI* panel. Then load the atlas via *File → Open* and use the *3D Tools* panel to plan electrode trajectories. Position shanks in the axial, sagittal, and coronal views until the target regions are reached.

**2. Post-implant localisation**
After surgery, load the post-implant MRI via *File → Open* and register it to the pre-surgical image. Optionally resample to 50 μm/voxel for higher resolution. Paint anatomical brain regions and electrode traces on the post-surgical image to generate heatmaps. Combined with the WHS atlas files and the implanted shank's `.pkl` file, IMPLAnT automatically localises each channel to its atlas-defined brain region.

**3. Electrophysiology visualisation**
Load your electrophysiology data via *File → Open*. Channels are displayed with their anatomical labels from the previous step, allowing direct comparison of signal traces across brain regions.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

