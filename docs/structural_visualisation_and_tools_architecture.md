# Structural Visualisation & Tools: System Architecture

Technical map of `page_3D` — the structural-mode MRI viewer panel and its
"Structural Tools" toolset (Register, Resample, Paintbrush, Segmentation,
Measurement). This supersedes the structural half of the earlier combined
[3d_viewer_and_tools_architecture.md](3d_viewer_and_tools_architecture.md)
doc, split out on request into a fully standalone package. The time-series
counterpart (`page_4Ddata0`, `ButtonsGUI_TimeSeries`) gets its own separate doc —
mentioned here only where it's directly relevant (§7).

## 1. Overview

```
FileLoader.initialize_file(path)            (sitk.ReadImage)
       │  is_4d == False
       ▼
page_3D  ──  3 synced 2D slice views (axial/sagittal/coronal)
              + 1 real 3D scene widget (vtkWidget_data_seg3D)
       │
       ▼
ButtonsGUI_Structural.buttons_3D
       │
       ├── ImageLayer.setup_vtk (per view) → VTK actor pipeline   (§3)
       ├── CustomInteractorStyle, Minimap, Contrast                (§4)
       └── "Structural Tools" menu: Register · Resample · Paintbrush ·
                             Segmentation · Measurement             (§5)
```

**The single structural fact worth internalizing first**: "3D view" in
this app means **three synced 2D orthogonal slice views plus one separate
real 3D scene widget** — confirmed by the actual render-widget names
(`vtkWidget_data_axial`/`_sagittal`/`_coronal`/`_seg3D`,
`main_window.py:634-637`) — not a single volumetric render of the raw MRI.

## 2. The 3D viewer panel

`page_3D` (`ui_form.py:1422`) is one of two pages inside the top-level
`data_4d_3d` `QStackedWidget` — the switch to it happens **once, at load
time**, decided by `FileLoader.is_4d`
(`self.ui.data_4d_3d.setCurrentIndex(0 if self.FileLoader.is_4d else 1)`,
`main_window.py:1253`, also `364, 619, 1070`) — there's no live 3D↔4D
toggle afterward. `page_3D` itself nests a `stackedWidget_3d` (2 pages:
Trajectory Planning's sidebar, and the plain-3D controls page) plus a
separate `stackedWidget_dfx` (electrode/DFX geometry — a different
subsystem, see the Trajectory Planning doc).

## 3. Rendering pipeline — loaded volume → on-screen VTK actor

```
FileLoader.initialize_file          (sitk.ReadImage — SimpleITK)
       │
LoadMRI.volumes[data_index]          MRIVolume: raw numpy array + spacing
       │
ButtonsGUI_Structural.buttons_3D
       │
ImageLayer.__init__ → setup_vtk (per view: axial/coronal/sagittal)
       │
  numpy slice (vol[z,:,:], np.fliplr unless flip=False)
       │
  vtk.util.numpy_support.numpy_to_vtk
       │
  vtkImageData → vtkImageReslice (cubic or nearest)
       │
  vtkImageActor + LUT (Contrast.lut_vtk, for windowing)
```

(`core/image_layer.py:37-98`.) SimpleITK only appears at the very start
(`FileLoader`) and, separately, inside the Register tool's own image I/O
(§5.1) — the routine per-slice render path is pure numpy → VTK.

**Layers**: one `ImageLayer` = one loaded volume's set of VTK actors
across whichever views it's registered for. `update_vtk` mutates the
*existing* `vtkImageData` in place when the cursor moves — no actor
recreation per frame. Multiple layers stack as independent, ordered VTK
actors in the same renderer; VTK itself composites their opacity, not
app-level blending logic. `MW.Layers[data_index]` is a real ordered dict
every consumer iterates directly — e.g. `_show_only_reference_and_warped`
(`buttons_gui_structural.py:556-571`) toggles per-layer visibility after a SAMRI
registration result gets added as a new layer
(`InitSAMRI.visualize_results`, per the SAMRI doc).

## 4. Interaction layer

- **`CustomInteractorStyle`** (`core/interactor_style.py`, a
  `vtkInteractorStyleImage` subclass): instantiated **per
  `(view_name, image_index)` pair**, not shared globally — toggling
  Measurement mode, for instance, swaps in a fresh instance for every view
  (`buttons_gui_structural.py:286-290`). Handles left-click (cursor placement /
  measurement point), mouse-move (crosshair/hover — its largest handler),
  mouse-wheel (slice scroll), right-click, middle-click, and minimap
  hit-testing.
- **`Minimap`** (`utils/minimap_handler.py`): one shared instance across
  all views/layers. Builds a small overview render per view, draws/updates
  a viewport-position rectangle, and exposes both drag-to-pan
  (`pan_from_minimap`) and the toolbar's arrow buttons (`pan_arrows`,
  fixed 0.4 step).
- **Contrast** (`utils.contrast.Contrast`): wired by `initialize_contrast`
  (`buttons_gui_structural.py:110-143`); Ctrl+J triggers auto-contrast.

## 5. The "Structural Tools" toolset

All five are wired directly in `ButtonsGUI_Structural.__init__`
(`buttons_gui_structural.py:97-101`) to the `menuStructural_Tools` ("Structural Tools") menu actions.

### 5.1 Register — `core/registration.py` + `file_handling/itksnap_registration.py`

Rigid (6-DOF Euler) registration reproducing ITK-SNAP's own "Registration"
panel exactly, via `picsl_greedy.Greedy3D` — a **compiled pybind11
extension** (confirmed by direct import in both project venvs), i.e.
in-process C++, **not a subprocess** (unlike SAMRI's ANTs CLI binaries).
`Registration.__init__` — not a separate `run` method — does the entire
synchronous body of work itself; whether this blocks the GUI depends
entirely on the caller, and there are **two real callers with two
different behaviors**:

1. **Structural Tools → Register menu** (`ButtonsGUI_Structural._start_registration`,
   `buttons_gui_structural.py:412-554`): images/metric/pyramid levels come from the
   registration popup; runs inside a real `SamriWorker` **QThread**, which
   afterward also uses ANTsPy (`ants.image_read`/`apply_transforms`/
   `image_write`, also in-process) to resample the moving image into
   fixed-image space, writing `<moving>-aligned_to_ind_<N>.nii.gz`.
2. **Trajectory Planning's optional second-file comparison**
   (`TpRegistration.register_to_main_img`, inherited unchanged by the live
   `TrajectoryPlanningMri` — see that doc's §5): fires automatically,
   **synchronously**, inside `main_window.py`'s outer `BusyOverlay.run()`
   — the same fake-async, GUI-blocking pattern as Resample (§6),
   *not* a real thread. `core/registration.py:75-77`'s own comment
   documents this exact asymmetry.

Output either way: `transformation-ind_<M>-to-ind_<N>.txt`
(`registration.py:136-154`). **Confirmed entirely separate from SAMRI/ANTs
atlas registration** — no reference to `output_Composite.h5`, no shared
code path; it only reuses `SamriWorker` as a generic QThread-wrapper
utility class, by name, not by pipeline.

### 5.2 Resample — `file_handling/resample_data.py`

`resampling100um`: resamples **only the z-axis** to 0.1mm spacing (x/y
untouched), linear interpolation via `sitk.Resample`; pads 20 slices at
the far end (repeating the last slice, at its mean intensity) to avoid
black slices post-resample. `resampling25um`: three **sequential**
single-axis passes (z, then y, then x) to reach 25µm isotropic — this
exact convention is what SAMRI's atlas-correspondence build and Trajectory
Planning's MRI-space label overlay both depend on matching byte-for-byte
(see those docs). Both write a **new sibling file**
(`<orig>_resampled100um.nii.gz` / `<orig>_resampled.nii.gz`) — the
original is never touched.

### 5.3 Paintbrush — `core/paintbrush.py` + `gui_utils/paintbrush_gui.py`

Real-time manual voxel annotation via mouse-move events. One numpy
`uint8` `label_volume` per loaded dataset, brush shapes computed directly
in view-plane voxel-index space, displayed as a semi-transparent
(opacity 0.5) `ImageLayer` overlay. **No file I/O anywhere** — session-only,
not a mask-export tool (contrast with Segmentation, next). Supports a
previously-undocumented **`red_only` mode**
(`self.MW.ButtonsGUI_Structural.initialize_paintbrush(red_only=True)`), reused
directly by Trajectory Planning's forbidden-area painting
(`TpRegistration.ask_paint_forbidden_areas`) rather than that subsystem
having its own paint tool.

### 5.4 Segmentation — `gui_utils/segmentation_gui.py`

The module's own docstring states **"The segmentation is not yet
finished."** A 3-step wizard: **Threshold**
(`segmentation/segmentation_utils.py`) → **Active Bubbles** (circular seed
regions, not paint strokes) → **Level-Set Evolution**
(`segmentation/evolution.py`, a real curve-evolution algorithm —
balloon/curvature/advection terms, numpy/scipy `ndimage`), stepped via
play/pause/step controls. On finish, `save_mask()` writes
**`<original_file>-mask.nii.gz`** next to the source — **exactly the file
SAMRI's "Create Moving Mask" flow globs for later**
(`update_mov_mask_path`, per the SAMRI doc). The `samri=True` flag
(`ButtonsGUI_Structural.initialize_segmentation(samri=True)`) only changes what
happens *after* finishing (jump back to the SAMRI tab) — the algorithm is
identical either way.

### 5.5 Measurement — `core/measurement.py`

Two-click point-to-point distance measurement. Converts voxel→physical mm
via the volume's spacing and draws a `vtkLineSource` + billboard distance
label into a **dedicated overlay VTK renderer layer** per view. Results
list in `tableWidget_meaurement`; visibility is **slice-dependent** — a
measurement only renders when its recorded slice matches the current one.
**No persistence to disk** — in-memory VTK actors + table rows only.

## 6. Concurrency — three real patterns, one fake

| Mechanism | Used by | Real background thread? |
|---|---|---|
| `SamriWorker` (QThread subclass) | Register — Structural Tools menu path only | **Yes** |
| `QObject.moveToThread()` (`EvolutionWorker`) | Segmentation's evolution step only | **Yes** — a different pattern from Register's |
| `BusyOverlay.run()` | Resample; Register — Trajectory Planning's call path | **No** — looks async, actually runs synchronously on the GUI thread (`run()` schedules work via `QTimer.singleShot(50, ...)`, which still fires on the GUI thread) |
| none | Paintbrush, Measurement, Contrast, Zoom, Minimap, Segmentation's threshold/bubble steps | N/A — synchronous by design, meant to feel instant |

Worth flagging as its own architectural fragility: three genuinely
different "run this off the GUI thread" mechanisms coexist in one
toolset, and **the same tool (Register) uses two of them depending on
which screen calls it** — not obvious from reading either call site in
isolation.

## 7. Cross-subsystem handoffs

- **Segmentation → SAMRI**: real, direct — `save_mask()`'s
  `-mask.nii.gz` is exactly what SAMRI's moving-mask picker looks for.
- **Register → Trajectory Planning**: real, but *only* a call-site
  relationship (§5.1) — no shared transform file, no shared threading
  behavior.
- **Register vs. SAMRI's `output_Composite.h5`**: explicitly **not
  connected** — a completely separate transform, easy to confuse by name
  alone.
- **`ButtonsGUI_TimeSeries` is a separate, duplicated implementation** — it does
  **not** subclass or reuse `ButtonsGUI_Structural`; it independently re-wires its
  own contrast/cursor/zoom/paintbrush for the 4D page. Out of scope for
  this doc (see the forthcoming 4D Visualisation & Tools doc), but worth
  knowing before assuming any change here automatically applies there.

## 8. Threat surface

Much smaller than SAMRI's — everything here is local and in-process:

- **No subprocess or network calls anywhere** in this toolset —
  `picsl_greedy` and `ants.apply_transforms` are both confirmed in-process
  compiled extensions.
- Files written are local, predictable, non-overwriting-by-default
  siblings of the source file: `transformation-ind_<M>-to-ind_<N>.txt` and
  `<moving>-aligned_to_ind_<N>.nii.gz` (Register), `<orig>_resampled*.nii.gz`
  (Resample), `<original_file>-mask.nii.gz` (Segmentation).
- The one cross-cutting fragility worth repeating from §6: several
  `BusyOverlay.run()` call sites across the app (here, in SAMRI's own
  `visualize_results`, and in Trajectory Planning) present as background
  work but actually block the GUI thread — worth checking any given call
  site's real behavior before assuming it's non-blocking.
