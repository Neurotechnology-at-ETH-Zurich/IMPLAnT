# Intraoperative: System Architecture

Technical map of the Intraoperative tab — where a previously-saved trajectory
plan gets corrected against real, measured bregma/lambda on the day of
surgery. Same treatment as
[trajectory_planning_architecture.md](trajectory_planning_architecture.md).
For the user-facing walkthrough, see
[surgery_workflow.md](surgery_workflow.md) — this covers the code
underneath it.

**The single governing design constraint, stated explicitly in the code's
own docstrings**: the surgeon's measured bregma/lambda are mm offsets from
an arbitrary stereotaxic-manipulator **null point**, in the manipulator's
own physical frame — a frame with **no defined mapping back into image
space** (no fiducial ties "the null point" to a location in any scan).
Every design choice here follows from that one fact: what can be corrected
live (a 2D numeric table, a 2D photo marker) and what fundamentally cannot
(the 3D MRI view, which always shows the original plan).

## 1. Overview

```
main_window.py::initialize_surgery()
       │
       ▼
LoadSurgeryPlan dialog — pick a saved Trajectory Report PDF
       │
  PdfReader(path).attachments["trajectory_planning_data.json"][0]
  (same JSON FileOutput._attach_reload_data embeds — see the
  Trajectory Planning doc's §6.2)
       │
       ▼  BusyOverlay.run(...)
SurgeryController.load_plan(data, pdf_path)
       │
       ├── axial_view.load(data)      — skull-photo markers (§5.1)
       ├── on_bregma_lambda_changed() — summary table (§4)
       └── mri_preview.render(...)    — 3D reference, if MRI findable (§5.2)
```

`SurgeryController` is instantiated **once**, in `MainWindow.__init__`
(`main_window.py:96`), and lives for the app's entire session — unlike
`TrajectoryPlanningMri`, which only exists while a plan is actively being
edited. It is **entirely independent of `TrajectoryPlanningMri`/`LoadMRI`**:
correcting bregma/lambda only needs the per-shank `ap_mm`/`rl_mm` (plus
`roll_deg`/`pitch_deg`/`depth_mm`, carried over unchanged) a saved plan's
PDF already carries — never a loaded MRI, registration, or rendering
context. The surgeon only ever picks a PDF.

## 2. The PDF → JSON handoff

`LoadSurgeryPlan.load_and_accept` (`intraoperative/load_surgery_plan.py`):
reads `trajectory_planning_data.json` from the picked PDF's attachments,
`json.loads`s it, then **closes the dialog before calling `load_plan`**
rather than blocking the picker on a potentially slow load (locating the
MRI, building the 3D preview) — a `BusyOverlay` over the main window gives
feedback instead. Same error handling for both known failure modes: no
attachment at all (`KeyError`/`IndexError`/`FileNotFoundError` → "no
trajectory data found") and an unreadable PDF (generic exception →
"could not read PDF"). `main_window.py:451` — the app's own session-restore
path — funnels into the exact same `SurgeryController.load_plan` call.

## 3. Controller lifecycle — surviving `restart_gui`

`SurgeryController.ui` is a **live property**, not cached at construction:
`MainWindow.restart_gui` replaces `self.MW.ui` with a brand-new
`Ui_MainWindow()` instance while the controller itself is *not* recreated
— caching the old `.ui` would silently keep talking to torn-down widgets.
`.mri_preview` and `.axial_view` follow the same pattern one level
further: each is a **lazy property, rebuilt whenever its container widget's
identity changes** (`self._mri_preview_container is not self.ui.widget`),
since a `QtInteractor` embedded in a widget that no longer exists would
otherwise silently keep rendering into nothing.

## 4. Intraoperative reprojection math — `intraoperative/reprojection.py`

A deliberately standalone module (not a mixin, unlike
`trajectory_planning/`'s composition pattern) — it only ever needs a `tp`
object passed in explicitly, and `SurgeryController` is a documented
**drop-in stand-in** for that parameter, exposing just `.ui` and
`.surgery_shank_offsets` (the module was originally written against a real
`TrajectoryPlanning` instance).

- **`reproject_target_to_null`**: the exact 2D reduction of
  `FileOutput.compute()`'s own 3D bregma-lambda-axis math (Trajectory
  Planning doc §6) — exact, not approximate, specifically *because* there
  is no intraoperative DV/vertical measurement any more to re-level with
  (those "ax" spinboxes were removed), which makes the drop-to-2D
  mathematically clean rather than a simplification. Critically, it
  applies a **scale correction**: `scale = measured_bregma_lambda_distance
  / planned_bregma_lambda_distance` — the surgeon's real, measured
  bregma-lambda separation on the rig rarely matches the MRI-planned one
  exactly (probe placement, scan distortion, calibration drift), and this
  ratio keeps each shank's *target position* accurate, not just its
  direction. `roll_deg` is loaded but has no correction path at all — it's
  carried over from the plan unchanged and intentionally not shown in the
  summary table (pitch alone is what the surgeon dials in).
- **`null_point_ap_rl`**: the exact inverse — where the manipulator's own
  dial-(0,0) lands in the plan's bregma-relative anatomical frame, used
  only to draw a marker on the skull photo (§5.1). Being a pure
  rig-calibration artifact unrelated to anatomy, it often lands well
  outside the photo entirely (handled explicitly, not treated as an
  error).
- **`refresh_surgery_summary`**: populates the 5-column summary table
  (Shank / AP mm / RL mm / angle-to-AP-RL-plane / depth) live, on every
  bregma/lambda spinbox edit (`main_window.py`'s `add_actions` wires all
  four spinboxes' `valueChanged` directly to
  `self.surgery.on_bregma_lambda_changed`).

## 5. Two independent reference views

### 5.1 Skull-photo view — `intraoperative/buttons_gui_surgery.py`

**Replaced a previous design** that reused the app's real
`LoadMRI`/`ImageLayer` pipeline to reslice the subject's own MRI — now
a **fixed, generic dorsal rat-skull photo** (Paxinos & Watson's published
bregma/lambda reference) with hand-calibrated pixel positions for bregma
and lambda, entirely independent of whatever plan is loaded. Each shank's
planned insertion point is placed via `_mri_to_photo_affine` — a
**similarity transform only** (uniform scale + rotation/reflection, no
independent x/y scale or shear — deliberately, since only two point
correspondences, bregma and lambda, are available, which is exactly enough
degrees of freedom for a similarity transform and not enough for a full
affine), scaled per-animal by *this plan's own real* bregma-lambda
distance rather than a generic figure. The transform's determinant is
**−1 (a reflection, not a pure rotation)** — the code's own comment notes
an earlier "no mirroring needed" assumption here was empirically confirmed
backwards against the app's existing 3D trajectory-planning view, and was
fixed to match that real reference rather than re-derived from first
principles.

**`build_skull_reference_scene` is shared, verbatim, with Trajectory
Planning's PDF cover page** (`file_input_output.py::_cover_page`, per the
Trajectory Planning doc §6) — both the live Intraoperative tab and the saved
report's cover page render from the *exact same drawing code*, not two
independent implementations that happen to look similar.

### 5.2 3D MRI preview — `intraoperative/mri_preview.py` — a SECOND real `output_Composite.h5` consumer

A static, read-only reference view — never regenerates missing files, only
locates them (`locate_resampled_mri` reconstructs the same resampled-file
naming convention `finish_trajectory_work` uses, without needing any of
that function's setup; `_locate_registration_transform` looks for
`output_Composite.h5` as a sibling of the anat folder). **This is a
second, independent, genuine consumer of SAMRI's registration
transform** — alongside Trajectory Planning's `warp_red_areas` (see that
doc's §5) — worth knowing both exist rather than assuming there's only
one:

- **If the registration transform is available**
  (`_build_atlas_warped_shell`): builds the brain-shell *shape* from the
  **atlas's own** clean, hand-curated brain mask (exactly
  `TrajectoryPlanning3DWindow._build_background_mesh`'s MRI-mode
  construction), then warps every vertex through the real SimpleITK
  transform into this subject's true MRI space — shape from the atlas,
  *color* from the subject's own real MRI intensity, sampled at those
  already-correctly-positioned vertices.
- **If it isn't** (`_build_otsu_shell`): falls back to segmenting the raw
  MRI directly — Otsu thresholding, hole-filling, largest-connected-component
  — a less anatomically faithful shell, but the best available without a
  real registration to warp the atlas mask through.

Either way, `render()` also draws each shank's **original**
`mri_insert`/`mri_deep` line segment (exact voxel indices already stored
in the saved plan — no atlas/registration lookup needed for those) plus
bregma/lambda spheres, all as a translucent static reference. If no MRI
can be located at all, `clear()` empties the view — **non-fatal**, since
the numeric table and skull-photo markers are what the tab is actually
for.

## 6. What can — and fundamentally cannot — be corrected live

| Corrected live from measured bregma/lambda? | View |
|---|---|
| Yes | Summary table (`refresh_surgery_summary`) |
| Yes | Skull-photo null-point marker (`update_null_point`) |
| **No — always shows the original plan** | 3D MRI preview (`SurgeryMRIPreview.render`) |

The 3D view's docstring states the reason plainly: the manipulator's null
point lives in a physical frame with no fiducial or calibration tying it
to a location in the scan, so the intraoperative correction simply has
nowhere to go in image space. This isn't a missing feature — it's a
real, stated boundary of what the correction math can express, and the
one-time step popup (`show_step_popup`) tells the surgeon this directly
("The 3D view shows the ORIGINAL planned positions only... it does not
update with the correction above").

## 7. Concurrency & file I/O

Only one async-looking call in this subsystem:
`load_surgery_plan.py`'s `BusyOverlay.run(self.MW.surgery.load_plan, ...)`
— the same fake-async, GUI-thread-blocking pattern documented everywhere
else in the app (3D/4D viewer doc §7, Trajectory Planning doc §7). No
`QThread`/`subprocess`/`multiprocessing` anywhere in
`intraoperative/*.py`.

**Files read** (all read-only — nothing in this subsystem writes a new
file): the picked report PDF and its embedded JSON attachment; the
resampled MRI, if locatable by naming convention; SAMRI's
`output_Composite.h5`, if present as a sibling of the anat folder; the
fixed skull-photo asset
(`Icons/csm_SBIR_rat_skull_overhead_01_93d6774e3d.jpg.webp`).

## 8. Fragile points / cross-references worth knowing

- **Two separate, real consumers of `output_Composite.h5` now exist app-wide**
  — Trajectory Planning's `warp_red_areas` and this doc's
  `SurgeryMRIPreview._build_atlas_warped_shell`. Both are optional/read-only,
  but any future change to what that file means or how it's produced needs
  checking against both.
- **`axial_view.load()` must run before `on_bregma_lambda_changed()`** in
  `load_plan` — the former stashes the plan's bregma/lambda calibration
  that the latter's null-point marker update depends on. The ordering
  dependency is documented in the code but not enforced by any type system
  — a future refactor that reorders these two calls would silently break
  the null-point marker without an obvious error.
- **Two placeholder widget names still carry TODOs** (`tp.ui.label`,
  `tp.ui.tableWidget` — auto-generated Designer names never renamed) —
  cosmetic today, but worth fixing before this UI grows further, per the
  code's own TODO comments.
