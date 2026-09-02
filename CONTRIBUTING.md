# Contributing to IMPLAnT

This covers how to work in the codebase day-to-day. For installation and setup, see [README.md](README.md).

## Orient yourself first

Before changing a subsystem, read its architecture doc in [`docs/`](docs/):

- [`trajectory_planning_architecture.md`](docs/trajectory_planning_architecture.md)
- [`intraoperative_architecture.md`](docs/intraoperative_architecture.md)
- [`ephys_architecture.md`](docs/ephys_architecture.md)
- [`samri_atlas_registration_architecture.md`](docs/samri_atlas_registration_architecture.md)
- [`3d_viewer_and_tools_architecture.md`](docs/3d_viewer_and_tools_architecture.md), [`3d_visualisation_and_tools_architecture.md`](docs/3d_visualisation_and_tools_architecture.md), [`4d_visualisation_and_tools_architecture.md`](docs/4d_visualisation_and_tools_architecture.md)
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

## Code conventions

There's no linter/formatter config in this repo yet — match the style of the surrounding file. Directories are organized by workflow stage (`trajectory_planning/`, `intraoperative/`, `ephys/`, `core/`, `mrid_utils/`); put new code next to the workflow it belongs to rather than in a shared catch-all.

## Testing

There's no automated test suite yet. Verify changes by running the app against real data (`python main_window.py`) and exercising the actual workflow your change touches — golden path and edge cases — rather than relying on inspection alone.

## Submodules

`electrode2geometry` and `rippl-AI` are git submodules. If you need to change code inside them, commit and push within the submodule's own repo first, then update the parent repo's pointer:
```
git add electrode2geometry   # or rippl-AI
git commit -m "Bump electrode2geometry to <reason>"
```

## Pull requests

Keep PRs scoped to one workflow/subsystem where possible — this makes both the Python diff and any `form.ui` diff easier to review. Describe *why* the change is needed, not just what changed (the code shows the what).
