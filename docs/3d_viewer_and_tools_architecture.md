# 3D/4D Viewer & Its Tools: System Architecture

Technical map of IMPLAnT's 3D/4D MRI viewer panel and the "Structural Tools" menu
(Register, Resample, Paintbrush, Segmentation, Measurement) that sit on top
of it. Written for engineering review, same treatment as
[samri_atlas_registration_architecture.md](samri_atlas_registration_architecture.md) —
that doc covers what happens *before* a file is loaded and registered; this
one covers what happens *after*, while a scan is open on screen.

**Explicitly out of scope**, confirmed to be real, separate subsystems and
intentionally not folded in here:
- `pgwidget.py` — the ephys time-series plot widget (`pyqtgraph`-based,
  imports from `ephys.visualisationEphys`). Not part of the MRI viewer at
  all despite living at the project root.
- Electrode Localization / Rippl AI / Theta Detection / Spike Sorting (the
  "Time-Series Tools → Electrode Localization" submenu, `core/electrode_localization.py`,
  `ephys/visualisation3D.py`, Gaussian/statistical analysis) — a large,
  separate subsystem `ButtonsGUI_TimeSeries` happens to also wire up. Deserves its
  own doc, not a subsection of this one.
- `stackedWidget_dfx` (electrode/shank geometry) and trajectory planning's
  own 3D view (`stackedWidget_3d_tp`) — different screens entirely.

## 1. Overview

```
FileLoader.initialize_file(path)
       │
       ▼
 is_4d? ──────────────────────────────┬───────────────────────────────
   │ False                            │ True
   ▼                                  ▼
data_4d_3d → page_3D              data_4d_3d → page_4Ddata0
 3 synced 2D slice views            per-timepoint tabs, heatmap,
 + 1 real 3D scene widget           intensity table, own VTK widgets
 (vtkWidget_data_axial/                (ButtonsGUI_TimeSeries — a SEPARATE
  sagittal/coronal/seg3D)                re-implementation, not a
       │                                 subclass of ButtonsGUI_Structural)
       ▼
ButtonsGUI_Structural wires the "Structural Tools" menu on top of this view:
  Register · Resample · Paintbrush · Segmentation · Measurement
```

The single most important structural fact: **"3D view" in this app means
three synced 2D orthogonal slice views (axial/sagittal/coronal) plus one
separate real 3D scene widget** (`vtkWidget_data_seg3D`) — not one
volumetric render of the raw MRI. Everything below (layers, interactor,
minimap) operates per-view across that set.

## 2. Viewer panel structure

- `data_4d_3d` (`ui_form.py:824`) is the top-level `QStackedWidget` that
  decides everything: index 0 = `page_4Ddata0` (4D layout), index 1 =
  `page_3D` (3D layout). The switch happens **once, at load time**:
  `self.ui.data_4d_3d.setCurrentIndex(0 if self.FileLoader.is_4d else 1)`
  (`main_window.py:1253`, also `364, 619, 1070`) — there is no live
  3D↔4D toggle after that; loading a differently-dimensioned file is what
  actually switches pages.
- `page_3D` itself nests a `stackedWidget_3d` (2 pages: Trajectory
  Planning's sidebar, and the plain-3D controls page) plus a separate
  `stackedWidget_dfx` (electrode/DFX geometry — out of scope, see above).
- `page_4Ddata0` has its own parallel set of widgets: `tabWidget_time0`
  (one tab per timepoint), `heatmap_data0`, `tableintensity_data0`, and its
  own per-timepoint VTK widgets — genuinely separate UI, not a reskinned
  3D page.

## 3. Rendering data flow — loaded volume → on-screen VTK actor

```
FileLoader.initialize_file          (sitk.ReadImage — SimpleITK)
       │
       ▼
LoadMRI.volumes[data_index]          MRIVolume: raw numpy array + spacing
       │
       ▼
ButtonsGUI_Structural.buttons_3D / ButtonsGUI_TimeSeries.buttons_4D
       │
       ▼
ImageLayer.__init__ → setup_vtk (per view: axial/coronal/sagittal)
       │
  numpy slice (vol[z,:,:], np.fliplr unless flip=False)
       │
  vtk.util.numpy_support.numpy_to_vtk
       │
  vtkImageData
       │
  vtkImageReslice (cubic or nearest)
       │
       ▼
  vtkImageActor + LUT (Contrast.lut_vtk, for windowing)
```

(`core/image_layer.py:37-98`.) SimpleITK only appears at the very start
(`FileLoader`) and, separately, inside the Register tool's own image I/O
(§5.1) — the routine per-slice render path is pure
numpy → VTK, no SimpleITK in the loop.

**Layers** (`core/image_layer.py`): one `ImageLayer` = one loaded volume's
set of VTK actors across whichever views it's registered for. `update_vtk`
mutates the *existing* `vtkImageData` in place when the cursor moves — no
actor recreation on every frame. Multiple layers stack as independent,
ordered VTK actors in the same renderer; VTK itself composites their
opacity, not app-level alpha-blending logic. `MW.Layers[data_index]` is a
real ordered dict every consumer iterates directly — e.g.
`_show_only_reference_and_warped` (`buttons_gui_structural.py:556-571`) toggles
per-layer visibility to control what's shown after a SAMRI registration
result gets added as a new layer (`InitSAMRI.visualize_results`, already
documented in the SAMRI architecture doc) — that's the same layer
mechanism described here.

## 4. Interaction layer

- **`CustomInteractorStyle`** (`core/interactor_style.py`, a
  `vtkInteractorStyleImage` subclass) is instantiated **per
  `(view_name, image_index)` pair**, not shared globally — e.g. toggling
  Measurement mode swaps in a fresh instance for every view
  (`buttons_gui_structural.py:286-290`). Handles left-click (cursor placement /
  measurement point), mouse-move (crosshair/hover — by far its largest
  handler), mouse-wheel (slice scroll), right-click, middle-click, and
  minimap hit-testing.
- **`Minimap`** (`utils/minimap_handler.py`): one shared instance across
  all views/layers. Builds a small overview render per view, draws/updates
  a viewport-position rectangle on it, and exposes both drag-to-pan
  (`pan_from_minimap`) and the toolbar's up/down/left/right buttons
  (`pan_arrows`, fixed 0.4 step) — both paths move the same underlying
  camera/extent.
- **Contrast** (`utils.contrast.Contrast`): wired by `initialize_contrast`
  (`buttons_gui_structural.py:110-143`); auto-contrast is bound to Ctrl+J.

## 5. The "Structural Tools" toolset

All five are wired directly in `ButtonsGUI_Structural.__init__`
(`buttons_gui_structural.py:97-101`) to the `menuStructural_Tools` ("Structural Tools") menu actions.

### 5.1 Register — `core/registration.py` + `file_handling/itksnap_registration.py`

Rigid (6-DOF Euler) registration of one already-loaded MRI onto another —
**reproduces ITK-SNAP's own "Registration" panel exactly**, per the
module's docstring, by driving the same underlying `greedy` engine
ITK-SNAP itself uses. `picsl_greedy.Greedy3D` is a **compiled pybind11
extension module** — confirmed by directly importing it in both project
venvs and inspecting `picsl_greedy.__file__` — an in-process C++ call,
**not a subprocess or external CLI binary** (unlike SAMRI's ANTs, which
shells out to real binaries via `nipype`). `Registration.__init__`
(`core/registration.py:21-79`) — not a separate `run` method — does the
entire synchronous body of work itself: reads fixed/moving images via
`sitk.ReadImage`, DICOM-orients both to RAS, then
`rigid_transformation()` calls `register_rigid` (`picsl_greedy`) and
writes an ITK `MatrixOffsetTransformBase` `.txt` transform to
`<session>/anat/transformation-ind_<M>-to-ind_<N>.txt`. Because the
constructor *is* the work, whether this blocks the GUI depends entirely
on how the caller wraps it — and there are two real callers that wrap it
very differently:

1. **Structural Tools → Register** menu (`ButtonsGUI_Structural.initialize_registration` →
   `_start_registration`, `buttons_gui_structural.py:412-554`): fixed/moving images
   and metric (NMI/NCC/SSD)/pyramid coarsest-finest levels come from the
   registration popup's combo boxes; runs inside a real `SamriWorker`
   **QThread**, which afterward also imports **ANTsPy**
   (`ants.image_read`/`apply_transforms`/`image_write`) to resample the
   moving image into fixed-image space, writing
   `<moving>-aligned_to_ind_<N>.nii.gz` (`buttons_gui_structural.py:473-504`).
2. **Trajectory Planning's optional second-file comparison**
   (`TrajectoryPlanning.__init__` → `TpRegistration.register_to_main_img`,
   `trajectory_planning/registration.py:19-38`): fires automatically,
   synchronously, whenever the user supplies a second/comparison MRI while
   starting Trajectory Planning — itself only reachable once SAMRI's own
   atlas transform already exists (`main_window.py::initialize_trajectory_planning`,
   lines 990-1012, explicitly checks for `output_Composite.h5` and bounces
   back to the SAMRI tab if it's missing). This call runs inside
   `main_window.py`'s outer `BusyOverlay.run(self.finish_trajectory_work, ...)`
   — the **same fake-async, GUI-thread-blocking pattern as Resample**
   (§5.2/§7), *not* a real thread. `core/registration.py:75-77` documents
   this exact asymmetry in its own comment: *"trajectory_planning/registration.py
   calls Registration() directly without going through
   initialize_registration(), so metric_index may not be set."*

So "Register runs on a `SamriWorker` QThread" is true **only for the
menu-triggered path** — worth stating precisely rather than as one
uniform fact about the tool.

**Register's own transform is still a separate artifact from SAMRI's
`output_Composite.h5`** — neither call site reads or writes it, and
nothing here touches the ANTs/nipype pipeline. But Register is not
functionally isolated from "the SAMRI process" either: Trajectory
Planning, which is gated on SAMRI having already run, is what silently
invokes it when a second comparison file is given. The accurate picture
is a real *sequencing* relationship (SAMRI → Trajectory Planning →
optionally Register) without a shared *data* relationship (no shared
transform file) — see the corrected diagram in the companion blueprint's
sheet 4.

### 5.2 Resample — `file_handling/resample_data.py`

`resampling100um`: resamples **only the z-axis** to 0.1mm spacing (x/y
untouched), linear interpolation via `sitk.Resample`; pads 20 slices at the
far end (repeating the last slice, at its mean intensity) specifically to
avoid black slices appearing post-resample. `resampling25um`: three
**sequential** single-axis passes (z, then y, then x) to reach 25µm
isotropic. Both write a **new sibling file**
(`<orig>_resampled100um.nii.gz` / `<orig>_resampled.nii.gz`) — the
original is never touched. `open_as_new_file` swaps the currently-loaded
MRI for the 100µm result via `MW.restart_gui`.

### 5.3 Paintbrush — `core/paintbrush.py` + `gui_utils/paintbrush_gui.py`

Real-time manual voxel annotation, driven by mouse-move events. One numpy
`uint8` `label_volume` per loaded dataset, brush shapes (square/round)
computed directly in view-plane voxel-index space, displayed as a
semi-transparent (opacity 0.5) `ImageLayer` overlay. **No file I/O
anywhere in either module** — this is a session-only annotation tool, not
a mask-export tool (contrast with Segmentation, next).

### 5.4 Segmentation — `gui_utils/segmentation_gui.py`

The module's own docstring states **"The segmentation is not yet
finished."** — worth carrying that caveat forward rather than treating it
as mature. A 3-step wizard:

1. **Threshold** (`segmentation/segmentation_utils.py`, bounded/lower/upper modes).
2. **Active Bubbles** — the user places circular seed regions (not paint strokes).
3. **Level-Set Evolution** (`segmentation/evolution.py`) — a real
   curve-evolution algorithm (balloon/curvature/advection terms,
   numpy/scipy `ndimage`), stepped via play/pause/step controls.

On finish, `save_mask()` writes **`<original_file>-mask.nii.gz`** next to
the source (`evolution.py:237-246`) — **this is exactly the file SAMRI's
"Create Moving Mask" flow globs for later** (`update_mov_mask_path` in
`samri_main.py`, documented in the SAMRI architecture doc) — closing a
loop only partially traced there. The `samri=True` flag
(`ButtonsGUI_Structural.initialize_segmentation(samri=True)`, used by SAMRI's
"Create Moving Mask" button) only changes what happens *after* finishing —
it jumps back to the SAMRI tab — the segmentation algorithm itself is
identical either way.

### 5.5 Measurement — `core/measurement.py`

Two-click point-to-point distance measurement. First click sets
`start_voxel`, second sets `end_voxel`; converts voxel→physical mm via the
volume's spacing and draws a `vtkLineSource` + billboard distance label
into a **dedicated overlay VTK renderer layer** (on top of the base image
renderer) per view. Results list in `tableWidget_meaurement`; visibility is
**slice-dependent** — a measurement only renders when its recorded slice
matches the currently displayed one. **No persistence to disk** — purely
in-memory VTK actors + table rows, gone when the session ends.

## 6. `ButtonsGUI_TimeSeries` — a separate, duplicated implementation

`ButtonsGUI_TimeSeries` (`gui_utils/buttons_gui_time_series.py`) **does not subclass or
reuse `ButtonsGUI_Structural`** — it independently re-wires its own
contrast/cursor/zoom/paintbrush from scratch for the 4D page. Real code
duplication, not shared logic behind an abstraction — worth treating the
same way as any other "these two should probably share a base class but
don't yet" finding. Its two "Time-Series Tools" menu actions are distinct from the
3D toolset: `actionStart_MRIDlabels` opens a separate MRID-tags labeling
workflow (`core.mrid_tags.MRID_tags`), and `actionContrast_Adjustments`
opens its own contrast dialog. It also pulls in Electrode Localization,
Ephys 3D visualization, and Gaussian/statistical analysis — confirmed to
be a large, genuinely separate subsystem (§ scope note above), not
researched further here.

## 7. Concurrency — three different patterns for basically the same problem

Unlike SAMRI (one consistent `SamriWorker` QThread pattern throughout),
this toolset uses **three distinct concurrency mechanisms**, plus one
outright fake:

| Tool | Mechanism | Real background thread? |
|---|---|---|
| Register — via Structural Tools menu | `SamriWorker` (QThread subclass, reused from SAMRI) | **Yes** |
| Register — via Trajectory Planning's second-file comparison | `BusyOverlay.run()` (same as Resample, below) | **No** — same call, same class, different caller, different (blocking) behavior; see §5.1 |
| Segmentation (evolution step only) | `QObject.moveToThread()` (`EvolutionWorker`) | **Yes** — a different pattern from Register's |
| Resample | `BusyOverlay.run()` | **No** — looks async, actually runs synchronously on the GUI thread (confirmed: `run()` schedules the work via `QTimer.singleShot(50, ...)`, which still fires on the GUI thread) — a large resample blocks the UI, it just shows a spinner first |
| Paintbrush, Measurement, Contrast, Zoom, Minimap, Segmentation's threshold/bubble steps | none | N/A — synchronous by design, meant to feel instant |

This is worth flagging as its own architectural fragility: three
genuinely different ways of doing "run this off the GUI thread" (one real
QThread subclass, one `moveToThread` worker, one that only *looks* async)
coexist in the same toolset, plus SAMRI's own `visualize_results` step
uses the same fake-async `BusyOverlay` pattern as Resample here — worth
checking any other `BusyOverlay.run()` call site in the codebase before
assuming it's actually non-blocking.

## 8. Threat surface

Much smaller surface than SAMRI's (§5 there covers SSH/credentials/atlas
downloads) — everything here is local and in-process:

- **No subprocess or network calls anywhere** in this toolset —
  `picsl_greedy` and `ants.apply_transforms` (Register) are both confirmed
  in-process compiled extensions, not external CLI invocations.
- Files written are all local, predictable, non-overwriting-by-default
  siblings of the source file: `transformation-ind_<M>-to-ind_<N>.txt` and
  `<moving>-aligned_to_ind_<N>.nii.gz` (Register), `<orig>_resampled*.nii.gz`
  (Resample), `<original_file>-mask.nii.gz` (Segmentation). No credentials,
  no remote hosts, no shell strings built from user input.
- The one cross-cutting fragility worth repeating from §7: several
  `BusyOverlay.run()` call sites (here and in SAMRI's own
  `visualize_results`) present as background work but actually block the
  GUI thread — not a security issue, but a real UX/architecture one if a
  future resample/step grows large enough to matter.
