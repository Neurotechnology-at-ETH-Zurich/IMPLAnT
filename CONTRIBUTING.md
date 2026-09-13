# Contributing to IMPLAnT

This covers how to work in the codebase day-to-day. For installation and setup, see [README.md](README.md).

## Orient yourself first

Before changing a subsystem, read its architecture doc in [`docs/`](docs/):

- [`trajectory_planning_architecture.md`](docs/trajectory_planning_architecture.md)
- [`intraoperative_architecture.md`](docs/intraoperative_architecture.md)
- [`ephys_architecture.md`](docs/ephys_architecture.md)
- [`samri_atlas_registration_architecture.md`](docs/samri_atlas_registration_architecture.md)
- [`3d_viewer_and_tools_architecture.md`](docs/3d_viewer_and_tools_architecture.md), [`structural_visualisation_and_tools_architecture.md`](docs/structural_visualisation_and_tools_architecture.md), [`time_series_visualisation_and_tools_architecture.md`](docs/time_series_visualisation_and_tools_architecture.md)
- [`surgery_workflow.md`](docs/surgery_workflow.md)

These explain how the pieces connect; the code alone won't make that obvious.

## Editing the UI (`form.ui`)

`form.ui` is the single Qt Designer file backing most of the app and `ui_form.py` is **generated** from it — never hand-edit `ui_form.py`, your changes will be silently overwritten.

1. Open `form.ui` in Qt Designer/Qt Creator (not a text editor) and make your changes there.
2. Regenerate the Python bindings:
   ```
   pyside6-uic form.ui -o ui_form.py
   ```
   (same for `form_tp_3d.ui` → `ui_form_tp_3d.py`).
3. Do not add new widgets to an existing layout at runtime (`addWidget()` in Python) as a substitute for step 1 — it breaks the layout. New widgets belong in Designer.
4. If a widget you need already exists elsewhere in the UI (e.g. a shared stacked widget), reparent/reuse it rather than building a duplicate — several parts of the app wire logic directly to specific widget instances by name.

`form.ui` is large (~17k lines) and any tab you touch may be reviewed as a big XML diff — try to keep unrelated tabs untouched in the same change.

## Adding your own tab/tool to MainWindow

`MainWindow` (`main_window.py`) has a small extension API for attaching a new tab, dock, or menu entry without editing its `__init__`/`add_actions()` or reaching into `self.ui` internals directly. See the "Extension API" comment block in `main_window.py` (just above `register_tab`) for the full picture, caveats included — short version:

- `load_split_ui(ui_class, attach)` — load a Designer form built as its own standalone `.ui` file and attach its top-level widget (e.g. `lambda w: self.register_tab(w, "My Tool")`). Build the form in Designer, not with runtime `addWidget()` calls (see above).
- `register_tab(widget, title, index=None)` — add `widget` as a new page of the main tab strip; returns its index (use `tabWidget.indexOf(widget)` to find it again later, not a hardcoded number).
- `register_menu_action(menu, text, triggered=None, before=None, enabled=True)` — add a `QAction` to an existing menu.
- `register_session_loaded_callback(kind, callback)` — get notified once a `'mri'`/`'ephys'`/`'samri'`/`'trajectory'`/`'surgery'` session finishes loading, instead of hooking `restart_gui`/`do_ephys_heavy`/etc. yourself.
- `register_module(name, module)` — register a controller object (like `SurgeryController`) under `self.<name>` (`name` can be dotted, e.g. `'LoadMRI.TrajPlanning'`, for a module that naturally lives on an attribute other than `self`); if it defines `teardown()`, that's called whenever `restart_gui()` tears down the UI for a full restart.

A brand-new tool typically combines the first two: build its UI as its own `.ui` file, load it with `load_split_ui()`, attach it with `register_tab()`.

The built-in tool tabs (`surgery`, `tab_ephys`, `tab_samri`, plus the earlier popup tabs) are now attached the same way a new tab would be — each was split out of the monolithic `form.ui` into its own standalone `.ui` file and is loaded via `load_split_ui`/`register_tab`, same as above. Only `PostSurgery` (the default Structural/Time-Series Tools view — the primary MRI viewer, not an optional tool) is still defined directly inside `form.ui`, left that way deliberately: it's the app's core view rather than an example of a pluggable tool, and it's far more deeply cross-referenced throughout the codebase than any tool tab, so extracting it carries materially more risk for little of the benefit this API is meant to provide.

When splitting a tab out of `form.ui` into its own file this way, watch for two Designer quirks that have bitten this exact process before: (1) icons set via a relative file path (not a `.qrc` resource) get silently rewritten to be relative to the *new* file's own folder — wrong, since they're resolved against the app's working directory at runtime, not the `.ui` file's location — so re-check every `<iconset>`'s `<normaloff>` path after moving a widget; (2) keep the new form's top-level widget's `objectName` (and ideally its `<class>` tag) exactly what it was in `form.ui`, not Designer's default `Form` — that's what lets `self.ui.<original_name>` keep resolving everywhere else in the codebase without any other code changes.

### Memory management for a registered module

If your module holds onto something worth freeing when it's no longer needed (a large in-memory dataset, VTK actors, a network/file handle), give it a `teardown()` method — `register_module` calls it automatically whenever `restart_gui()` does a full restart. `core/measurement.py`'s `Measurement.teardown()` is the reference example: it resets its own bookkeeping (`measurement_lines = []`); the VTK side needs no separate handling since `core/load_MRI_file.py`'s renderer-wide sweep already tears down every renderer, including whichever ones a module added on its own.

Beyond a full restart, `MainWindow._free_previous_workflow_state` also calls a module's `teardown()` (and frees the heavier ones — `self.Samri`/`self.Ephys`/`self.LoadMRI`, via `_evict_load_mri`) whenever the user switches to a different kind of session (`'ephys'`/`'samri'`/`'surgery'`) — see that method's docstring for exactly which kinds trigger this and why (e.g. never `'trajectory'`, since `LoadMRI` is needed for that). If you register a module this way, remember to pop it back out of `self._registered_modules` when you discard it (`self._registered_modules.pop(name, None)`) — otherwise the registry keeps a live reference to a "freed" object, both misrepresenting what's actually live and keeping it from being garbage-collected.

## Code conventions

There's no linter/formatter config in this repo yet — match the style of the surrounding file. Directories are organized by workflow stage (`trajectory_planning/`, `intraoperative/`, `ephys/`, `core/`, `mrid_utils/`); put new code next to the workflow it belongs to rather than in a shared catch-all.

## Testing

There's a small automated suite under `tests/` (construction/control-flow-level checks for `MainWindow`'s extension API and the dock-closing/memory-eviction logic built on it — see `tests/test_main_window_smoke.py`'s module docstring for exactly what it covers). Install its one dependency and run it with:

```
pip install -r requirements-test.txt
pytest
```

It runs headlessly (`QT_QPA_PLATFORM=offscreen`, set automatically in `tests/conftest.py`) and never loads a real file or renders anything — no display is needed, and none of it touches real VTK rendering (which segfaults offscreen). That means it catches regressions in things like "does `self.ui.<name>` still resolve after a tab extraction," "does `register_module`'s registry stay in sync," "does `teardown()` actually get called" — but **not** anything that needs a real render (a 3D view actually drawing correctly, an icon looking right on screen). For that, and for anything the suite doesn't cover yet, still verify changes by running the app against real data (`python main_window.py`) and exercising the actual workflow your change touches — golden path and edge cases — rather than relying on inspection alone. Add a test alongside any new extension-API behavior you build, the same way `test_main_window_smoke.py` covers what exists today.

## Submodules

`electrode2geometry` and `rippl-AI` are git submodules. If you need to change code inside them, commit and push within the submodule's own repo first, then update the parent repo's pointer:
```
git add electrode2geometry   # or rippl-AI
git commit -m "Bump electrode2geometry to <reason>"
```

## Pull requests

Keep PRs scoped to one workflow/subsystem where possible — this makes both the Python diff and any `form.ui` diff easier to review. Describe *why* the change is needed, not just what changed (the code shows the what).
