# Ephys: System Architecture

Technical map of the Ephys subsystem — recording load, LFP/theta/ripple/spike
analysis, 3D/2D visualization, and Electrode Localization. The largest and
most internally cross-connected package in this series; same treatment as
the other docs, but with more emphasis on **where data actually crosses
subsystem boundaries**, since that turned out to be the defining structural
fact here.

## 1. Overview

```
main_window.py  ──"Open Ephys Data"──▶  InitEphys(MW, file_name)   (§2)
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
         EphysRecording / DigitalInFile   Visualisation3D      VisualisationEphys
         / MRIDInfo            (§3)       (ephys 3D)  (§6.1)   (2D trace view) (§6.2)
                    │
                    ▼
         LFPCreationDialog (§4, one-time, fixed pipeline)
                    │
      ┌─────────────┼──────────────┬───────────────────┐
      ▼              ▼              ▼                    ▼
Theta Detection  Ripple/Rippl-AI  Spike Sorting        CSD (§5.4)
  (§5.1, in-      (§5.2, ONLY      (§5.3, JRCLUST        (kCSD, shares
  process)         cross-venv       .mat/.prm)            depth ordering
                   subprocess                             with wavelet view)
                   in the app)

Electrode Localization (core/electrode_localization.py, §7) is a SEPARATE
entry point (from the 4D subsystem's TRANSFORM_InputDialog, per that doc) —
it writes analysed/<tag>/gaussian_centers_3D.npy + channel_atlas_
coordinates.xlsx, which InitEphys/MRIDInfo (§3) READS BACK to identify
which shank a recording belongs to. This is the one real closed loop
spanning three separate docs in this series (4D → Electrode Localization
→ Ephys session load).
```

## 2. Entry point & session controller

`InitEphys` (`ephys/init_ephys.py:73`) is constructed **exactly once**, at
`main_window.py:504` (`self.Ephys = InitEphys(self, file_name)`). Its
`__init__` loads `MRIDInfo.from_file()` and `EphysRecording.from_file()`
(§3), builds `Visualisation3D` and `VisualisationEphys` (§6), prompts
`LFPCreationDialog` (§4) if no `.lfp` exists yet, embeds a `SpikeRuster`
and an `LFPSpectrogram`, and wires/enables the three "Ephys Analysis" menu
actions (§5). Other structurally significant methods: `change_xml_file`/
`open_dat`/`open_dat_newly` (a recording can have multiple anatomical
channel groups in one `.xml`, switchable without reloading); `changeRegion`
(opens `Change_AnatRegion`, §6.3); `change_mridTAG`/`change_mridTAG_combobox`
(switching which MRID tag's data is shown, ties into `MRIDInfo`); `add_video`
(§6.4).

## 3. Recording data model

- **`EphysRecording`** (`ephys/ephysrecording.py`, dataclass): reads the
  `.dat` via `neo.io.NeuroScopeIO` (lazy); parses the companion `.xml`,
  scoped specifically to `anatomicalDescription/channelGroups/group` —
  **deliberately distinct from the `spikeDetection` channel groups in the
  same XML**, a documented gotcha; memory-maps an existing `.lfp` if
  present; optionally loads the fixed-filename Intan sidecar
  `digitalin.dat` (not derived from the recording's own name — standard
  RHD2000 convention, same family as `auxiliary.dat`/`time.dat`).
- **`DigitalInFile`** (`ephys/digitalin.py`): reads that TTL file — one
  uint16 word per sample, bit 0 = camera shutter, bit 1 = LED on/off,
  memory-mapped (files run tens of millions of samples).
- **`MRIDInfo`** (`ephys/mrid_info.py`) — **confirmed genuinely different
  from `core/mrid_tags.py`** (the 4D-labeling `MRID_tags` class), despite
  the shared name, and a **real, load-bearing cross-subsystem
  dependency**: `MRIDInfo.get_mrid_tag()` reads
  `<session_path>/analysed/<mrid_tag>/gaussian_centers_3D.npy` and
  `channel_atlas_coordinates.xlsx` for every tag subfolder — **exactly the
  outputs Electrode Localization's Gaussian-fit step (§7) writes**. Tags
  are sorted by their Gaussian-center RAS x-coordinate (anatomical
  left-right ordering) to identify which physical shank a given recording
  channel-group corresponds to. **The real chain**: 4D MRID labeling →
  Electrode Localization's Gaussian analysis writes
  `analysed/<tag>/gaussian_centers_3D.npy` + `.xlsx` → ephys session load
  reads them back to identify "which shank is this."

## 4. LFP creation — one fixed pipeline

`LFPCreationDialog` (`ephys_utils/lfp_creation_dialog.py`) confirms/lets
the user correct XML-parsed parameters, then calls
`downsample_filter_LFP` (`ephys_utils/downsample_filter_LFP.py`) with a
genuinely **fixed** pipeline: **10× downsample** (`_DS_FACTOR = 10`,
e.g. 20kHz → 2kHz, not configurable), a **600-order FIR lowpass** (passband
250Hz, stopband 450Hz — filter order is user-adjustable, everything else
isn't), writing `<stem>.lfp`. Every downstream consumer (theta detection,
ripple detection, the 2D trace view) reads int16 samples from this file
and scales by the same fixed **0.195 → µV** factor.

## 5. Analysis tools — four genuinely different execution models

### 5.1 Theta Detection — in-process, MATLAB-faithful

`detect_theta` (`init_ephys.py:763-908`) → `theta_detection.detect_theta`
(`ephys_utils/theta_detection.py`) — a direct **in-process** Python call
(`BusyOverlay` only, no thread/subprocess), confirmed to run on the `.lfp`
file, not raw. The module's own docstring states it's a faithful port of
a MATLAB pipeline; **no `MATLAB_Peter` reference implementation exists in
the current codebase** (only mentioned in this file's comments — the
directory itself is gone). Three rate-agnostic stages, confirmed by
direct read: **`get_theta_states`** (spectrogram at 100 log-spaced
frequencies via a hand-written DFT-at-arbitrary-frequencies routine
matching MATLAB's `spectrogram()` semantics exactly — Hamming window, no
detrending, magnitude not power — → theta/delta ratio → candidate
windows, with an optional multi-channel `consensus` flag), **`get_theta_phase`**
(order-40 Butterworth bandpass + Hilbert transform for instantaneous
phase), **`postprocess_theta_segments`** (reject/split on peak phase,
amplitude, cycle period, duration). Output: `<lfp_stem>_theta.npy` plus
JSON sidecars for the detection info and settings used.

### 5.2 Ripple Detection — subprocesses out to rippl-AI

`detect_ripples` (`init_ephys.py:487-621`) → `_run_ripple_detection`:
selects a pyramidal channel ± up to 7 neighbors (8 channels total), then
runs **`subprocess.run([sys.executable, 'rippl-AI/run_rippl.py', ...])`**.
There is only ever one venv — `.venv10` in this maintainer's own checkout
is simply their local name for the main app environment (Python 3.10,
same tensorflow/keras/xgboost pins as `requirements.txt`), not a separate
ML-only environment. The call previously hardcoded the literal path
`.venv10/bin/python3` instead of using `sys.executable`, which broke for
anyone naming their venv anything else (including the `.venv` name the
README itself instructs); this has been fixed to use `sys.executable`,
and a check now shows a clean error dialog if the `rippl-AI` submodule
script is missing rather than raising an unhandled `FileNotFoundError`.
This is a genuinely **blocking subprocess call** wrapped in `BusyOverlay`
(real GUI-blocking for the whole external-process duration — not the
fake-async pattern used almost everywhere else in this app). I/O is
entirely file-based: the LFP channel slice is written to a temp `.npy`,
the subprocess reads it and writes an events `.npy` back. Inside
`run_rippl.py`: calls **`rippl_AI.predict(lfp, sf=lfp_rate, arch=arch,
model_number=1, channels=np.arange(8))`** → a per-sample
ripple-probability trace, then **`rippl_AI.get_intervals(prob,
threshold=..., sf=1250)`** → an `(n_events, 2)` array of ripple
start/end times. Settings persist to `<lfp_stem>_ripples_settings.json`;
events to `<lfp_stem>_ripples.npy`.

**Still broken in the packaged build.** `MRID_GUI.spec` (PyInstaller)
bundles `ants/bin`, `samri/`, `ephys/`, etc., but never bundles the
`rippl-AI` submodule's `.py` sources, and a frozen `dist/IMPLAnT`
executable has no live `.py` interpreter to shell out to at all — using
`sys.executable` fixes the dev/source-checkout case but doesn't make this
work in a release build. Fixing that would mean bundling `rippl-AI` as
data and shipping a full companion Python runtime that gets shelled out
to exactly as today.

**In-process import is not viable — confirmed by a hard crash, not just
theory.** Calling `rippl_AI.predict()`/`get_intervals()` directly instead
of subprocessing (tried once, then reverted) segfaults the whole GUI
process inside TensorFlow's `tf_keras` `predict()` call (`Fatal Python
error: Segmentation fault`, deep in
`tensorflow/python/ops/gen_dataset_ops.py:make_iterator`) — almost
certainly a native-library conflict between TensorFlow and the
VTK/PySide6 stack already loaded in the same process. The subprocess
boundary here is load-bearing for stability, not just a defensive
nicety — any packaging fix must keep ripple detection in its own OS
process.

### 5.3 Spike Sorting — JRCLUST, not Kilosort/Phy

`load_spike_sorting` (`init_ephys.py:1121-1163`) loads a **JRCLUST**
result — `<dat_stem>_res.mat` plus a companion `.prm` file, auto-detected
next to the loaded `.dat`. Hands off to
`SpikeRuster.load_matlab_files(path, sample_rate, region_map, color_map,
prm_path=...)` (`ephys_utils/spiking_ruster.py`) to render the raster
(one row per cluster/unit). Automatically triggers
`run_hierarchical_clustering()` afterward (clusters spike-sorted units by
cross-correlation, renders a heatmap) — synchronous, `BusyOverlay` only.

### 5.4 Current Source Density (CSD)

`_csd_inputs` (`ephys/visualisationEphys.py:199`) derives a 1D depth
ordering for the displayed channels via SVD projection onto the shank's
principal axis (oriented so the surface-entry channel has the smallest
depth) — this ordering is **shared between the CSD map and the
per-channel wavelet spectrogram** so a feature lands on the same row in
both, and depends directly on `Visualisation3D`'s own
`coords_list`/`chMap` state (a real cross-file coupling within Ephys).
`export_csd` solves kernel CSD (`ephys_utils/run_kCSD.py`/`csd_widget.py`)
over the **whole recording**, streamed to a raw float32 `.bin` + JSON
sidecar via a manual `QProgressDialog` + `processEvents()` poll loop — not
a real thread, just event-pumped synchronous work. **Contains a real bug**:
`visualisationEphys.py:307` references an undefined name `dat_path` (not
a local, not a `self.` attribute anywhere in the class) — this code path
would raise `NameError` if reached.

## 6. Visualization

### 6.1 Ephys 3D — `ephys/visualisation3D.py` — two operating modes, one shared convention

**A different class from `trajectory_planning/visualisation3D.py`** — same
name, unrelated files. Two modes, set by an `electrode_localisation`
constructor flag: **standalone Electrode Localization tab**
(`electrode_localisation=True`, embeds in `vtkWidget_vis3D`, tag-switching
calls back into `ButtonsGUI_TimeSeries.activate_fill_table_and_plots` — control
flows back to the 4D subsystem) vs. **live per-recording ephys view**
(`electrode_localisation=False`, embeds in `vtkWidget_ephys`, tag-switching
calls `Ephys.change_mridTAG` instead — a separate, per-recording notion of
"current tag"). **Same word "mrid tag" means two unrelated things across
this app** (a 4D-labeling tag vs. a physical-shank identifier read from an
Excel sheet) — both loaded from files under `analysed/`, worth not
conflating.

Renders a whole-brain atlas background plus a **derived, electrode-specific
atlas subset**: `create_atlas_region_file` zeroes every atlas voxel whose
label isn't one of this shank's own recorded regions and **writes**
`analysed/atlas-regions.nii.gz` — a real write-back into session output.
Electrode point cloud/trajectory comes from
`analysed/<mrid>/channel_atlas_coordinates.xlsx`. A fallback pyramidal-layer
finder (`_compute_pyl_from_lfp`) computes ripple-band (100-250Hz) Welch-PSD
power over a 60s LFP chunk when no Excel-marked row exists.

**Confirmed shared convention, both sides cited exactly**: this file's
`desaturate`/`_rebuild_colormap` (HSV saturation ×0.25 for non-focused
regions) and `trajectory_planning/visualisation3D.py`'s `_desaturate` use
the *same factor*, independently implemented, with an explicit
cross-referencing comment on the Trajectory Planning side.

### 6.2 2D scrolling trace viewer — `visualisationEphys.py` + `pgwidget.py`

pyqtgraph-based (`ClickablePlotWidget(pg.PlotWidget)`). `EVENT_STYLES`:
ripples (gold, 0.025s half-width) and theta (green, 0.25s half-width) as
`pg.LinearRegionItem` overlays, editable via right-click. Right-drag =
time-scroll; left-drag = zoom/measure/timeline depending on the active
toolbar mode; double-click a trace jumps the 3D view focus to that
channel. `prewarm_tabs()` deliberately force-computes the spectrogram/CSD/
wavelet tabs right after load so the first click on any of them is
instant. **A real behavioral bug**: `ClickablePlotWidget`'s right-drag
time-scroll calls the raw-data loader directly, **bypassing**
`VisualisationEphys.visualize_data`'s LFP-vs-broadband mode check entirely
— dragging to scroll always reloads raw broadband data even while viewing
LFP mode, inconsistent with the spinbox/slider navigation path.

### 6.3 Region reassignment — `Change_AnatRegion`

Lets the user manually reassign which atlas region an electrode channel
belongs to. **Reuses the exact widget-reparenting technique already
documented for `widget_dfx`** (Trajectory Planning doc) — a genuinely
repeated codebase pattern, not a one-off: `groupBox_ChangeanatRegion` is
reparented into this dialog at construction and returned to its original
parent on close. Lists every atlas region within a fixed ~4.37mm radius of
the channel's 3D coordinate, sorted by distance. No independent data
model — reads/writes `Visualisation3D`'s live state directly.

### 6.4 Video playback — the app's only `ffprobe` dependency

`VideoPlayer` (`ephys/videoplayer.py`) plays a behavioral `.avi` via
`QMediaPlayer`. `get_frame_rate` runs a genuine external
**`subprocess.run(["ffprobe", ...])`** — a real binary dependency, distinct
from every other subprocess pattern in this app. **`synchronize_frames` is
incomplete** — it loads a `.mat` sidecar with camera-frame-to-sample
timestamps but the method ends after a debug print with no actual sync
logic implemented; only `seek_frame`/`play_pause` are functional.

## 7. Electrode Localization — `core/electrode_localization.py` — the app's only real multiprocessing

Entry point is external to this doc's subsystem (the 4D doc's
`TRANSFORM_InputDialog` → `get_gaussian_analysis`/`electrode_localisation`
in `buttons_gui_time_series.py`). `ElectrodeLoc` does two things:

- **`get_gaussian_centers`**: reads `transformation-ind_<M>-to-ind_<N>.txt`
  (single view, direct `sitk.ReadTransform`) or chains several via
  `mrid_utils.warper.create_composite_transform` (multi-view). Warps each
  tag's per-voxel heatmap (`<file>-<roi>-heatmap.nii.gz`, written earlier
  by `MRID_tags.start_heatmap`, per the 4D doc) into atlas space, then
  Gaussian-fits per-channel centers via `mrid_utils.gauss_aux.run_gaussian_analysis`.
- **`getCoordinates`** → `ChannelVariablesInput` dialog → `chmap.main`: the
  real channel-to-region mapping algorithm lives in `mrid_utils.chmap`
  (out of scope). Critically, **the dialog's default file paths are
  `<session_path>/registration/fixed_img-indeces.npy` and
  `moving_img_resampled25um-indeces.npy`** — **the exact same precomputed
  atlas↔MRI voxel-correspondence arrays SAMRI's own `InitSAMRI.start_registration`
  writes** (per the SAMRI doc). This is a **second, independent, real
  cross-subsystem data dependency on SAMRI's output** — separate from (and
  in addition to) the `transformation-*.txt` read above.

**Genuine multiprocessing — confirmed as the only real one in the app this
session**: `getCoordinates`'s continuation uses a real
`concurrent.futures.ProcessPoolExecutor` — one OS subprocess per ROI tag,
each running `chmap.main` — actual CPU parallelism across real processes
(unlike `SamriWorker` QThread, `QObject.moveToThread`, or any
`BusyOverlay` elsewhere in this app). **The `as_completed()` wait loop
itself still runs synchronously on the GUI thread**, though — no `QThread`
wraps the wait — so the GUI still blocks for the full duration; work is at
least genuinely parallelized across cores, unlike every other
"concurrency" pattern documented in this series.

Visualization here (`add_point`/`show_warped_volume`) draws electrode
centers as raw `vtkSphereSource` actors directly, bypassing `ImageLayer`
entirely — same hand-rolled-VTK pattern as `MRID_tags.start_heatmap`'s 4th
panel (4D doc). `show_warped_volume` swaps `LoadMRI.volumes[idx]` in-place
for a resampled warped volume with extensive manual actor/cursor/LUT
rebookkeeping.

## 8. DFX geometry for Electrode Localization — `Dfx4DGeometry`

Shares the literal `stackedWidget_dfx` widget with Trajectory Planning's
`DfxGeometry` (confirmed from both sides now — see that doc) via the same
reparent-and-`reclaim_dfx_widget` pattern. **Persistence differs, though**:
`Dfx4DGeometry` keeps geometry purely **in memory**
(`self.tag_geometry`, per-tag `{"geometry": Nx2 array, "result": dict}`) —
it does **not** write a `probe_geometry.json` the way Trajectory Planning's
`DfxGeometry` does. Both share the same underlying
`electrode2geometry.python.geometry_core.bend_dxf_probe_geometry` function
and the same widget instance, but not the output format.

## 9. Concurrency — the most diverse mix in this series

| Mechanism | Used by | Real parallelism? |
|---|---|---|
| `subprocess.run` to a **different venv's Python** | Ripple detection (rippl-AI) | Yes — genuinely leaves the process, but blocks the GUI thread for its duration |
| `ProcessPoolExecutor` | Electrode Localization's `getCoordinates` | Yes — real multi-core work, but the wait itself still blocks the GUI thread |
| `subprocess.run` to an external binary (`ffprobe`) | Video playback frame-rate query | Yes, trivial/fast |
| In-process direct call, `BusyOverlay` only | Theta detection, spike-sorting load, hierarchical clustering, LFP creation, CSD export | No — same fake-async pattern as everywhere else in the app |
| `ThreadPoolExecutor` (intra-call) | `Visualisation3D.load_atlas` (both this file and Trajectory Planning's) | Faster loading, but still blocks the caller |

**No `QThread`/`moveToThread` exists anywhere in the entire Ephys
subsystem** — a notable contrast with SAMRI (`SamriWorker`) and
Segmentation (`EvolutionWorker`) elsewhere in the app.

## 10. Fragile points

- **`visualisationEphys.py:307`**: undefined `dat_path` in `export_csd` —
  a real `NameError` waiting to happen if that code path is exercised.
- **`videoplayer.py`'s `synchronize_frames`** is incomplete — loads the
  sync sidecar but never actually applies it.
- **Right-drag time-scroll bypasses LFP/broadband mode** (`pgwidget.py`)
  — a real, user-visible inconsistency between two navigation paths.
- **"MRID tag" and "mrid tag" mean different things** depending on which
  file you're reading (4D-labeling tag vs. physical-shank identifier) —
  worth being precise about in any future work here.
- **Two independent, real dependencies on SAMRI's registration output**
  exist in Electrode Localization alone (`transformation-*.txt` and the
  `fixed_img-indeces.npy`/`moving_img_resampled25um-indeces.npy`
  correspondence arrays) — a change to either format needs checking
  against this file specifically, not just the SAMRI/Trajectory Planning
  consumers already documented.
