# Trajectory Planning: System Architecture

Technical map of Trajectory Planning — the screen where shanks get placed
on a subject's MRI before surgery, downstream of SAMRI's atlas
registration. Same treatment as
[samri_atlas_registration_architecture.md](samri_atlas_registration_architecture.md)
and [3d_viewer_and_tools_architecture.md](3d_viewer_and_tools_architecture.md).
For the user-facing walkthrough, see
[surgery_workflow.md](surgery_workflow.md) — this doc covers the code
underneath it, and corrects one detail that doc got wrong (§6.2).

## 1. Overview

```
main_window.py::initialize_trajectory_planning()
  requires output_Composite.h5 (SAMRI) to already exist
       │
       ▼
FileInput dialog → (main_file, second_file, spacing_mm)
       │
       ▼
finish_trajectory_work(data, transformPath)
  resample main_file (reusing SAMRI's own 25µm convention if spacing==25µm)
  load it into the main viewer (FileLoader/LoadMRI — same layer as the
  3D/4D viewer doc)
       │
       ▼
TrajectoryPlanningMri(MW, ui, data, transformPath)   ← the class that ACTUALLY runs
  (see §2 — NOT the base TrajectoryPlanning class a naive read would expect)
       │
       ├── shank placement, electrode geometry, DFX bending      (§3)
       ├── in-panel 3D (Visualisation3D) + dockable 3D window    (§4)
       ├── optional forbidden-area painting → warp_red_areas,
       │   a REAL direct consumer of output_Composite.h5         (§5)
       └── Save Trajectory Report → PDF + embedded JSON          (§6)
                                          │
                                          ▼
                              Intraoperative reads it back
```

## 2. The real live class hierarchy — MRI-space overrides

**The single most important architectural fact here**: reading
`trajectory_planning/trajectory_planning.py` in isolation describes code
that **never runs**. `main_window.py:1101` constructs
`TrajectoryPlanningMri`, not `TrajectoryPlanning` — confirmed by grepping
the entire repo for bare `TrajectoryPlanning(` calls: there are none.

```
trajectory_planning_mri.py :  TrajectoryPlanningMri(RenderingMri, TpRegistrationMri,
                                                     ElecGeometryMri, ShankRenderingMri,
                                                     TrajectoryPlanning)
registration_mri.py        :  TpRegistrationMri(TpRegistration)
rendering_mri.py           :  RenderingMri(Rendering)
electrode_mri.py           :  ElecGeometryMri(ElecGeometry)
shank_mri.py               :  ShankRenderingMri(ShankRendering)
visualisation3D_mri.py     :  VisualisationMri(Visualisation3D)
```

The `*Mri` mixins are placed **before** `TrajectoryPlanning` in the base
list specifically so Python's C3 MRO resolves every overridden method to
its MRI-space version while everything `TrajectoryPlanning` defines
directly (or inherits unmodified from `CoordTransform`/`DfxGeometry`)
still resolves normally — `trajectory_planning_mri.py`'s own module
docstring documents this reasoning explicitly, down to citing where the
design was decided (`~/.claude/plans/wise-popping-nest.md`).

**What the rewrite is for**: keep the subject's own MRI as the displayed
volume for the *entire* workflow, instead of swapping to the atlas the way
the base classes do — atlas region labels are instead scattered onto the
MRI's own voxel grid as a colored overlay
(`registration_mri.py::build_mri_label_overlay`, using
`mri_label_overlay.py`'s cached correspondence table). Each `*Mri` class
overrides **only** the methods that depend on which volume is on screen:

| Base method | Base behavior | `*Mri` override behavior |
|---|---|---|
| `do_get_shank_line` | swaps display to atlas via `restart_gui` | stays on the MRI; calls `build_mri_label_overlay` instead |
| `warp_red_areas` | `ants.apply_transforms` via `output_Composite.h5` (§5.2) | no-op passthrough — mask is already MRI-space; `transform_path` param accepted-and-ignored to keep the same call signature |
| `draw_atlas_reference_points`, `reload_atlas_view`, `_atlas_plane_normal_and_point`, `compute_shank_reference_angle`, `draw_electrode_line`, `create_edge_mask` | operate in atlas voxel space | operate in MRI voxel space directly |
| `VisualisationMri.load_atlas` | n/a | still builds the background mesh from the **atlas's own grid** (a ready-made brain outline with real region indices as cell data), then reprojects only its *vertex positions* into true MRI space via `atlas_points_to_mri_indices` — the mesh's cell data (which region each cell belongs to) is untouched, since moving a point doesn't change which cell owns it |

Everything else — `register_to_main_img`, `get_shank_line`,
`init_page30_mirror`, `sync_page30_display`, `ask_paint_forbidden_areas`,
`paint_red_areas` — is inherited **unchanged** from the base classes.

**`RenderingMri` also adds genuinely new functionality**, not just
overrides — confirmed by its method inventory (`rendering_mri.py`) having
entries with no counterpart at all in `rendering.py`: a **misalignment
correction** control (`setup_misalignment_controls`, wiring
`dial_missalignment`/`doubleSpinBox_missalignment` — UI elements that
"only exist in this MRI-space rewrite," per `trajectory_planning_mri.py`'s
own comment) and **oblique coronal/sagittal view** support
(`setup_oblique_coronal_view`/`setup_oblique_sagittal_view`,
`oblique_click_to_voxel`) — both MRI-space-only features with no atlas-space
equivalent.

## 3. Coordinate system & shank/electrode geometry

- **Bregma/lambda & atlas correspondence**: handled by `CoordTransform`
  (`trajectory_planning/coord_transform.py`) — already fully documented in
  the SAMRI doc's downstream-consumers section. `TrajectoryPlanning.__init__`
  calls `get_atlas_coords` immediately to populate the bregma/lambda
  spinboxes.
- **Shank management** (`ShankRendering`/`ShankRenderingMri`,
  `trajectory_planning/shank.py`): `add_shank`/`remove_shank`/`select_shank`
  manage per-shank VTK actors across three combo boxes kept in lockstep.
  `remove_shank` explicitly re-numbers remaining shank IDs to keep
  `id == combo position` — a documented, deliberate guard against an
  `IndexError`/`KeyError` class of bug. `compute_shank_regions` samples the
  atlas along the *entire* deep→insertion line at ~1-voxel resolution
  (not just at sparse electrode contacts) specifically so thin
  regions with no contact inside them still show up in the sidebar.
- **Electrode geometry** (`ElecGeometry`/`ElecGeometryMri`,
  `trajectory_planning/electrode.py`): computes per-shank contact
  positions along the deep→insert axis, either from DXF-bent depths
  (§3.4) or uniform spacing. `check_region_to_avoid`/
  `check_shank_intersections` warn (via `QMessageBox`) on forbidden-region
  crossings or shank-to-shank proximity (closest-segment-distance
  geometry, 0.05mm touch threshold). `check_CA1_or_2` uses the atlas's DWI
  volume, when present, to find the CA1 pyramidal-layer-darkest-voxel
  channel. A dedicated **insertion-point refinement page** (page_31) swaps
  to the subject's own resampled MRI and lets the user click along a
  shank's fixed guide line to correct its auto-guessed insertion point in
  native MRI voxel space (`pick_insertion_point_from_click`, wired through
  `core/interactor_style.py`'s left-click handler while
  `LoadMRI.picking_insertion_point` is set).
- **DFX geometry** (`DfxGeometry`, `trajectory_planning/dfx_geometry.py`):
  a real dependency on the `electrode2geometry` git submodule
  (`from electrode2geometry.python.geometry_core import
  bend_dxf_probe_geometry, read_electrode_centroids, parse_neuroscope_xml,
  write_kilosort_json, parse_channel_text`). Reads a user-selected `.dxf`
  (probe bend geometry) and optional Neuroscope `.xml`; writes a
  Kilosort-style `probe_geometry.json` at a user-chosen path. Pure
  numpy/pandas, no subprocess. Uses `pyqtgraph` for its 2D bend-preview
  plots — a different plotting stack from the VTK/PyVista views elsewhere.
  **`widget_dfx`/`stackedWidget_dfx` is a single shared widget instance**
  reparented back and forth between Trajectory Planning's `DfxGeometry`
  and the separate "4D electrode localisation" subsystem
  (`core/dfx_geometry_4d.py::Dfx4DGeometry`, out of scope for this doc) via
  `reclaim_dfx_widget` — both subsystems re-wire the *same* widget's
  signals depending on who currently owns it, rather than each having its
  own copy.

## 4. 3D visualization — two independent PyVista scenes

Both use **PyVista** (`pyvistaqt.QtInteractor`) — a different rendering
stack from the main MRI viewer's raw VTK (`core/image_layer.py`, per the
3D/4D viewer doc). They do not import each other; both read shank/coordinate
state off the same live `TrajectoryPlanningMri` instance
(`self.MW.LoadMRI.TrajPlanning`).

- **`Visualisation3D`** (`trajectory_planning/visualisation3D.py`,
  overridden by `VisualisationMri` per §2): three separate `QtInteractor`
  plotters (`plotter_co`/`plotter_sa`/`plotter_ax`), each with a **clipping
  plane** (`render_clipped`) making a true 3D scene look like a 2D
  orthogonal slice, plus hover/click picking and region desaturation
  (`_bg_colors_for_shank` — the same HSV-desaturation convention as
  `ephys/visualisation3D.py`, a real cross-reference worth knowing before
  the Ephys doc). `load_atlas` uses a real `ThreadPoolExecutor(max_workers=3)`
  for **intra-call parallel file loading** — genuinely faster, but the
  call still blocks its caller until all three loads finish; not
  background/async relative to the GUI thread. `TpRegistration.reload_atlas_view`
  **re-instantiates this whole class** when the active atlas changes —
  confirms it isn't a session-wide singleton.
- **`TrajectoryPlanning3DWindow`** (`trajectory_planning_3d/window.py`): a
  **`QDockWidget`** (not modal, not a separate process —
  `WA_DeleteOnClose=False`, so closing it just hides it), opened on demand
  via `open_3d_window` and reused afterward. Builds atlas-shaped meshes
  (`_build_background_mesh`, `_build_mask_mesh`) warped into true MRI
  space via the same `atlas_points_to_mri_indices` technique
  `VisualisationMri.load_atlas` uses. Supports genuine **live interactive
  shank nudging** (`_nudge_shank`, with `_queue_nudge`/`_apply_pending_nudge`
  coalescing rapid clicks via a `QTimer`) — real editing, not just display.
  `_rebuild_background_mesh` wraps the mesh rebuild in `BusyOverlay.run()`
  (§7).

## 5. Registration touchpoints — two mechanisms, only one touches SAMRI's transform

- **`register_to_main_img`** (`TpRegistration`, inherited unchanged by
  `TrajectoryPlanningMri`): the separate rigid-registration tool
  (`core.registration.Registration`, fully documented in the 3D/4D viewer
  doc) — fires automatically in `TrajectoryPlanning.__init__` when a
  second/comparison file was supplied. Writes its own
  `transformation-ind_<M>-to-ind_<N>.txt`; **never reads or writes
  `output_Composite.h5`**.
- **`warp_red_areas(transform_path)`** (`TpRegistration`, base/atlas-space
  version only — `TpRegistrationMri`'s override is a no-op, see §2's
  table): after the user optionally paints forbidden areas (reusing the
  Structural Tools' own Paintbrush directly —
  `self.MW.ButtonsGUI_Structural.initialize_paintbrush(red_only=True)`, a
  previously-undocumented `red_only` mode), this method **genuinely
  applies SAMRI's own `output_Composite.h5`** via `ants.apply_transforms`
  (in-process ANTsPy, nearest-neighbor interpolation) to warp the painted
  mask from MRI space into atlas space. This is a real, direct data
  dependency on SAMRI's transform — distinct from, and easy to confuse
  with, the unrelated Register tool above.

## 6. PDF report generation & the Intraoperative handoff

- **`FileOutput`** (`trajectory_planning/file_input_output.py:149`):
  builds the report as a sequence of **PIL `Image` pages**, then
  `pages[0].save(path, save_all=True, append_images=pages[1:])` — Pillow
  does the PDF assembly (not reportlab/fpdf). `capture_pages` = cover page
  + one page per shank + a summary page.
- **A genuine hybrid rendering pipeline, not one uniform approach**: the
  atlas-space panels on each shank's page are **literal screenshots of the
  live, already-on-screen `Visualisation3D` plotters**
  (`self._screenshot_plotter(vis.plotter_co)`, where `vis` is the
  session's own live instance — these panels cannot drift from what's on
  screen). The **MRI-space panels are a separate, fresh off-screen render**
  (`pv.Plotter(off_screen=True, ...)`, driven by dedicated
  `_render_clipped_mri`/`_draw_electrode_lines_mri`/
  `_draw_mri_reference_plane_and_angle` methods) — genuinely different
  drawing code from the live viewer, built just for the report. The
  **cover page reuses `intraoperative/buttons_gui_surgery.py::build_skull_reference_scene`
  directly** — a real, pre-existing architectural link to Intraoperative
  beyond the JSON handoff below, not a re-derivation.
- **The JSON attachment mechanism** (write side): `_attach_reload_data`
  reopens the just-written PDF (`PdfReader`), builds a `PdfWriter`,
  `writer.append(reader)`, then
  `writer.add_attachment("trajectory_planning_data.json", data)` where
  `data = json.dumps(summary, indent=2).encode("utf-8")` and `summary`
  comes from `compute(tp)` (including a `summary['raw']` sub-key with the
  exact bregma/lambda/per-shank voxel/mm values needed to reconstruct the
  plan). **Read side, confirmed by grep, two real call sites**:
  `main_window.py:437` (session-restore) and
  `intraoperative/load_surgery_plan.py:67` (the primary Intraoperative load
  path) — both read `reader.attachments["trajectory_planning_data.json"][0]`.
  `load_surgery_plan.py`'s own comment explicitly cites
  `FileOutput._attach_reload_data` as the write side — the two ends of
  this handoff are cross-referenced in the code itself, not just by
  convention. **The PDF is physically written twice per save**: once by
  Pillow (the visual pages), once more by `pypdf` to inject the
  attachment.
- **Correction to the existing user-facing doc**: `docs/surgery_workflow.md`
  paraphrases the output filename as `trajectory_planning-sub-X-ind_2.pdf`.
  The actual pattern (`file_input_output.py:210`) is
  **`<short_id>-trajectory_planning.pdf`**, where `short_id` comes from
  `re.search(r'(sub-.+?)(?=_[A-Za-z]+-|$)', mri_filename)` (falling back to
  the full filename stem if no `sub-` match). The "saved alongside the MRI
  scan" claim is accurate — `os.path.dirname(mri_file_path)` is the
  default save directory.

## 7. Concurrency & file I/O

No `QThread`/`subprocess`/`multiprocessing`/`moveToThread` anywhere across
`trajectory_planning/*.py` or `trajectory_planning_3d/window.py`. Every
"async-looking" operation uses the same **`BusyOverlay.run()`
fake-async, GUI-thread-blocking pattern** already documented in the 3D/4D
viewer doc:

- `main_window.py:1020` (`initialize_trajectory_planning`)
- `electrode.py` (entering/leaving the insertion-refinement page, twice)
- `registration.py` (`get_shank_line`'s `proceed()`, wrapping either
  `warp_red_areas` or `do_get_shank_line`)
- `trajectory_planning_3d/window.py` (`_rebuild_background_mesh`)
- `file_input_output.py` (`_generate_and_save`) — its own comment
  acknowledges PDF generation "can take a real, noticeable few seconds"
  and needs the overlay purely for feedback, not real backgrounding.

The one recurring timer is `init_page30_mirror`'s 200ms polling `QTimer`,
which mirrors cursor position/intensity values onto page_30's duplicate
widgets — a UI-sync poll, not a concurrency mechanism.

**Files read/written in this subsystem** (SAMRI's atlas volume and
`output_Composite.h5` already covered elsewhere, not re-listed):

| File | Direction | Written/read by |
|---|---|---|
| `<mri>_resampled.nii.gz` (exactly SAMRI's 25µm convention) or `<mri>_resampled<N>um.nii.gz` | write | `finish_trajectory_work`, reusing `ResampleData.resampling25um`/`resampling50um_trajectoryPlanning` |
| `transformation-ind_<M>-to-ind_<N>.txt`, `<moving>-aligned_to_ind_<N>.nii.gz` | write | `register_to_main_img` → `core.registration.Registration` (unrelated to SAMRI) |
| user's `.dxf` | read | `dfx_geometry.py::browse_dfx_file` |
| user's Neuroscope `.xml` | read | `dfx_geometry.py::browse_dfx_xml`, `shank_setup_dialog.py` |
| `probe_geometry.json` | write | `dfx_geometry.py::export_dfx_json` |
| `<short_id>-trajectory_planning.pdf` | write (twice, see §6) | `file_input_output.py::FileOutput` |

## 8. Fragile points worth knowing

- **The MRI-space rewrite is a parallel class hierarchy, not a
  parameter.** Reading `trajectory_planning.py`/`registration.py`/
  `rendering.py`/`electrode.py`/`shank.py` alone describes a code path
  that never executes in the live app — any future change to shared
  logic needs to be checked against both the base class *and* its `*Mri`
  override, since Python's MRO silently picks whichever one is more
  specific.
- **`remove_shank`'s manual re-numbering** (§3) is a real, documented
  landmine class (`id == combo position` invariant) — any new code path
  that removes shanks without going through this exact method risks
  breaking every other shank's identity.
- **Two visually similar but functionally unrelated "registration" steps**
  can appear back-to-back in one Trajectory Planning session: the rigid
  `register_to_main_img` (a second comparison file, no SAMRI involvement)
  and `warp_red_areas` (genuinely uses `output_Composite.h5`). Worth
  naming precisely in any future work rather than treating "registration"
  as one concept here.
