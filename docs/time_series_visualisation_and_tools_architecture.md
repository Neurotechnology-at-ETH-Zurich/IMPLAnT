# Time-Series Visualisation & Tools: System Architecture

Technical map of `page_4Ddata0` — the time-series-mode MRI viewer panel and its
"Time-Series Tools" toolset. Standalone companion to
[structural_visualisation_and_tools_architecture.md](structural_visualisation_and_tools_architecture.md),
split out the same way on request. Electrode Localization, Gaussian
analysis, and everything ephys-related get their own separate doc — this
one stops exactly at the handoff point (§5.3).

## 1. Overview

```
FileLoader.initialize_file(path)            (sitk.ReadImage)
       │  is_4d == True
       ▼
page_4Ddata0  ──  3 VTK panels, each showing a DIFFERENT TIMEPOINT
                   of the SAME acquisition (not 3 different views)
       │
       ▼
ButtonsGUI_TimeSeries.buttons_4D
       │
       ├── same ImageLayer/Contrast/Zoom/Minimap/Paintbrush helper
       │   classes as the 3D doc — independently WIRED, not subclassed  (§3-4)
       │
       └── "Time-Series Tools" menu:
             Contrast Adjustments               (§5.1)
             Start MRIDlabels → labeling workflow (§5.2)
                    │
                    ▼  TRANSFORM_InputDialog
             out of scope — Electrode Localization / Ephys doc  (§5.3)
```

**The single structural fact worth internalizing first**: "4D view" here
means **three VTK panels showing three different timepoints of one
acquisition**, not three orthogonal anatomical views the way `page_3D`
does. Everything downstream — contrast, cursor, zoom — is wired per
*timepoint panel* (`data_index`) rather than per *view name*.

## 2. Data model — the same `ImageLayer`, just timestamp-swapped

A 4D file's full time series lives in **`MRIVolume.array_4d`**
(`file_handling/mri_volume.py`, shape `[time, z, y, x]`); `MRIVolume.slices`
is pre-seeded with just **three initial timepoints**
(`timestamp4D = [0,4,7]` or `[0,2,5]` depending on total frame count) —
one per VTK panel. `ImageLayer.timestamp4D_changed(index, image_index,
array_4d)` (`core/image_layer.py:178-182`) does exactly one thing:
`self.volume[image_index] = array_4d[index,:,:,:].copy()`.

**This is the same `ImageLayer` class documented in the 3D doc, reused
completely unmodified** — a 4D "layer" is not a different or extended
data structure, it's a normal `ImageLayer` whose displayed slice gets
swapped out from a larger pre-loaded 4D array on timestamp change. The
entire numpy→VTK render pipeline (`setup_vtk`, `vtkImageReslice`,
`vtkImageActor` + LUT) from the 3D doc applies identically here.

## 3. Viewer controls — shared helpers, duplicated wiring

Worth stating precisely rather than as a blanket "duplicated" claim:
`ButtonsGUI_TimeSeries` **reuses the exact same helper classes** as `ButtonsGUI_Structural`
(`utils.contrast.Contrast`, `utils.zoom.Zoom`, `utils.minimap_handler.Minimap`,
`core.paintbrush.Paintbrush`) — the underlying tools are not duplicated.
What **is** independently written is the *wiring/setup code* around them:

- `initialize_contrast` (`buttons_gui_time_series.py:184-261`): builds a *per-timepoint-panel*
  triple of contrast/brightness sliders — keyed by `data_index`, not view name.
- `initialize_cursor` (`263-293`): same reuse pattern, spinboxes keyed by panel.
- `initialize_zoom_controls` (`310-345`): same `Zoom`/`Minimap` classes, wired
  per `(data_index, image_index)` pair.
- `initialize_paintbrush` (`296-308`): directly instantiates
  `core.paintbrush.Paintbrush` itself
  (`self.MW.Paintbrush = Paintbrush(self.LoadMRI)`) — same underlying tool
  class as the 3D doc's Paintbrush, fully separate wiring code.

`ButtonsGUI_TimeSeries` does **not** subclass `ButtonsGUI_Structural` — confirmed, no
shared base class — but the fragility this creates is narrower than "two
independent implementations of everything": it's specifically that any
future fix to *how a control gets wired up* (not the underlying tool
class) needs to be made in both places.

## 4. The "Time-Series Tools" menu

Wired directly in `buttons_4D` (`buttons_gui_time_series.py:88-92`):
`actionGaussian_Centers`→`get_gaussian_analysis`,
`actionGet_Coordinates`→`electrode_localisation`,
`actionStart_MRIDlabels`→`open_input_dialog`,
`actionContrast_Adjustments`→`contrast_adjustments`,
`actionAddViewImage`→`add_other_view` (loads a second 4D file, rejecting
non-4D input via a `sitk` dimension check).

### 4.1 Contrast Adjustments

`contrast_adjustments` (`buttons_gui_time_series.py:978-989`) is **entirely separate
from the toolbar sliders** in §3's `initialize_contrast` — it opens a
`PopupDialog` (a hide-not-close `QDialog`) wrapping `ManualContrastAdjustments`,
a pre-built advanced-settings widget already in the main UI.

### 4.2 MRID tags labeling workflow — `core/mrid_tags.py` + `utils/mrid_inputdialog.py`

**"MRID tags" is unrelated to `mrid_utils/` (the atlas registry package
from the SAMRI doc)** beyond the shared name — `MRID_tags` only imports
`mrid_utils.heatmap` as a utility module, no shared registry/config. (The
acronym isn't spelled out anywhere in the codebase — treat it as an
app-specific term.)

A fully sequential dialog chain (`open_input_dialog` →
`continue_mridtags`, `buttons_gui_time_series.py:414-589`):

1. **`MRID_InputDialog`** (`utils/mrid_inputdialog.py:9-225`): collects
   named tags (with island counts) and named regions — or loads an
   existing `labels.txt` if one is already on disk.
2. **`ANAT_InputDialog(form_index=0)`** (`229-334`): per-view, locate or
   browse an existing `<file>-anat.nii.gz`, or paint one now.
3. Painting happens via the **shared** `Paintbrush` tool (§3) —
   `MRID_tags.create_labels()` (`mrid_tags.py:55-128`) configures
   *that same tool's* label vocabulary/color table, it does not paint
   anything itself. A **250ms polling `QTimer`**
   (`_update_anat_ok_enabled`, `buttons_gui_time_series.py:570`) keeps "Next"
   disabled until every named region has at least one painted voxel —
   guarding a documented `IndexError` in
   `mrid_utils/heatmap.py::get_relaxation_unsupervised`.
4. `MRID_tags.generate_textfile()` writes
   `<session_path>/anat/labels.txt` (ITK-SNAP-style format) and
   `save_as_niigz()` converts the live label volume to
   `<file>-anat.nii.gz` (or `-segmentation.nii.gz` in the second pass),
   then calls `start_heatmap()`.
5. **`start_heatmap()`/`update_heatmap()`** (`mrid_tags.py:212-593`): calls
   `mrid_utils.heatmap.get_relaxation_*` to compute a per-voxel
   relaxation/similarity map, rendered as a **fourth VTK panel**
   (`vtk_widgets[3]`) with a hand-rolled jet-colormap actor/renderer/LUT —
   **not** built through `ImageLayer` the way the three timepoint panels
   are (§2).
6. **`ANAT_InputDialog(form_index=1)`** (segmentation/islands pass) repeats
   steps 2-5 for `<file>-segmentation.nii.gz`.

On finishing the segmentation pass, a message box offers to continue
straight into Gaussian/electrode-localization work — see §5.3.

### 4.3 The boundary into Electrode Localization / Ephys

**Finishing MRID-tag labeling funnels directly into the Electrode
Localization pipeline inside the same `continue_mridtags` method** — the
two are not cleanly separable at the file level, only at the workflow
step: everything through §4.2 step 6 is pure 4D-labeling with no
ephys/electrode dependency; **`TRANSFORM_InputDialog`**
(`utils/mrid_inputdialog.py:341-482`) is the real bridge — it globs
`<session_path>/anat/*ind_<N>*.txt` (the **same
`transformation-ind_<M>-to-ind_<N>.txt` naming convention** already
documented for the Register tool and Trajectory Planning) and hands
matched files to `get_gaussian_analysis`/`electrode_localisation`
(`buttons_gui_time_series.py:642-975`) — `ElectrodeLoc`
(`core/electrode_localization.py`), `Visualisation3D`
(`ephys/visualisation3D.py`), and barcode plots via `MplWidget`, all
living in this same file but out of scope for this doc. **Draw the
boundary at `TRANSFORM_InputDialog`, not at a file or module boundary.**

## 5. Concurrency & file I/O

No `QThread`/`subprocess`/`multiprocessing`/`moveToThread` anywhere in
`buttons_gui_time_series.py`. Five `BusyOverlay` call sites (lines `485, 499, 652,
706, 815`) — every one the same fake-async, GUI-blocking pattern already
documented for `BusyOverlay` elsewhere this session (SAMRI, Structural Tools,
Trajectory Planning, Intraoperative).

**Files written** (session path = the loaded MRI's session folder):

| File | Written by |
|---|---|
| `anat/labels.txt` (ITK-SNAP format) | `MRID_tags.generate_textfile()` |
| `<file>-anat.nii.gz` | `MRID_tags.save_as_niigz()`, anat pass |
| `<file>-segmentation.nii.gz` | `MRID_tags.save_as_niigz()`, islands pass |
| `analysed/<mrid_tag>/mrid_barcode-detected.pdf`, `-reconstructed.pdf` | electrode-localization barcode plots (`buttons_gui_time_series.py:778-780, 801-802`, matplotlib via `MplWidget`) — out of scope, listed for completeness |

**Files read**: a second 4D file via `add_other_view`; an existing
`labels.txt` if present (`MRID_InputDialog`); existing
`-anat.nii.gz`/`-segmentation.nii.gz` (`ANAT_InputDialog`); existing
`transformation-*.txt` files (`TRANSFORM_InputDialog`).

## 6. Fragile points / cross-references

- **`MRID_InputDialog.browse_file` routes a plain text-file parse
  (`labels.txt`) through `FileLoader.initialize_file(file_name, 1, None,
  0)`** — the general image-loading entry point — which is an unusual
  reuse worth double-checking if `FileLoader`'s contract ever changes;
  it's not loading an image at all here.
- **The viewer-controls duplication (§3) is at the wiring layer, not the
  tool layer** — a fix to `Contrast`/`Zoom`/`Minimap`/`Paintbrush`
  themselves applies to both 3D and 4D automatically; a fix to *how* they
  get wired up (e.g., a new slider, a new keyboard shortcut) needs
  duplicating into both `ButtonsGUI_Structural` and `ButtonsGUI_TimeSeries`.
- **The heatmap panel bypasses `ImageLayer` entirely** (§4.2 step 5) —
  worth knowing before assuming every VTK panel in this app goes through
  the same rendering abstraction; this one is hand-rolled.
- **The MRID-tags → Electrode Localization handoff has no clean seam** —
  it's one Python method (`continue_mridtags`) with a mid-function branch,
  not two subsystems calling into each other through a defined interface.
  Any future split of this file needs to account for that.
