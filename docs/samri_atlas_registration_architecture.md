# SAMRI Atlas Registration: System Architecture

Technical map of the pipeline that takes raw Bruker scanner output and turns
it into a subject↔atlas transform IMPLAnT can use everywhere else (electrode
localization, trajectory planning, surgery-day preview). Written for
engineering/security review, not end users — for the user-facing walkthrough
of trajectory planning itself, see [surgery_workflow.md](surgery_workflow.md).

Scope: this covers IMPLAnT's own orchestration code (`samri/samri_main.py`,
`main_window.py`, `mrid_utils/atlas_*.py`, `trajectory_planning/coord_transform.py`).
The vendored `samri/samri/` package (a git-tracked copy of the third-party
[SAMRI](https://samri.readthedocs.io) library, built on `nipype`) is treated
as a dependency and described only at the level IMPLAnT depends on it.

## 1. Pipeline overview

```
Bruker host PC                 IMPLAnT (this app)                          Consumers
┌──────────────┐   SSH/SCP    ┌──────────────────────────────────────┐   ┌─────────────────────┐
│ ParaVision    │─────────────▶│ 1. Fetch raw scan                    │   │ Trajectory planning  │
│ /opt/PV6.0.1/ │  (paramiko)  │    data_fetcher.py                   │   │ (coord_transform.py) │
│ data/mri/     │              ├──────────────────────────────────────┤   ├─────────────────────┤
└──────────────┘              │ 2. bru2bids: Bruker → BIDS NIfTI      │   │ Electrode            │
                               │    samri/samri/pipelines/reposit.py  │   │ localization          │
                               ├──────────────────────────────────────┤   ├─────────────────────┤
                               │ 3. biascorrect_only (optional)        │   │ Surgery-day preview   │
                               │    OR structural(): N4 bias-correct   │   │ (intraoperative/      │
                               │    + ANTs rigid→affine→SyN vs. atlas  │   │  mri_preview.py)      │
                               │    samri/samri/pipelines/preprocess.py│   └─────────────────────┘
                               │    (nipype Workflow, MultiProc)       │            ▲
                               ├──────────────────────────────────────┤            │
                               │ 4. Post-processing:                   │            │
                               │    dense voxel correspondence table,  │            │
                               │    output_Composite.h5 saved,         │────────────┘
                               │    copy sub-<id> into DATA/           │
                               └──────────────────────────────────────┘
```

Everything from step 2 onward runs **on a Qt worker thread** (`SamriWorker`,
`samri/samri_logging.py`) so the GUI stays responsive; step 3's actual heavy
lifting is nipype spawning a **pool of OS subprocesses** that shell out to
ANTs command-line binaries (see §3).

## 2. Stage-by-stage

### 2.1 Credentials & raw data fetch — `samri/data_fetcher.py`, `samri/samri_main.py::SAMRI_InputDialog`

- The SAMRI tab (`SAMRI_InputDialog`) collects `server`, `password`,
  `animal_id`, and a local `raw_base_samri` folder. Server/password default
  from `samri/bruker_info.json` (gitignored, plaintext — see §5) if present.
- `pushButton_fetch` → `MW.fetch_data(samri_input)` → spawns `InitSAMRI`
  (`samri_main.py`) on a `SamriWorker` QThread.
- `InitSAMRI.start_bruker2_bids` connects to the Bruker host over **SSH**
  (`paramiko.SSHClient`, port 22, user `mri`) and pulls files via **SCP**
  from the hardcoded remote path `/opt/PV6.0.1/data/mri/`, matching on
  `animal_id`. Already-fetched sessions are diffed by scan-subfolder number
  so re-fetching only pulls what's missing (`get_data`'s "already exists"
  branch).
- Local target: `raw_base_samri + animal_id` (§5 flags why this is a plain
  string concat, not `os.path.join`).

### 2.2 Bruker → BIDS conversion — `bru2bids` (`samri/samri/pipelines/reposit.py`)

- Runs only if `samri_input['fetch']` is set (re-entering the SAMRI tab
  for an already-fetched animal skips straight past this).
- Before conversion, `_warn_incomplete_scans` (`samri_main.py`) walks every
  `raw_base/<session>/<scan>/pdata/1/2dseq` and flags scans with no
  reconstructed image (empty acquisitions), reading the scan's protocol
  name out of the raw ParaVision `acqp` text file for the log message.
- Any stale nipype cache at `bids_base/bids_work` is wiped
  (`shutil.rmtree`) before each run — conversions are not incremental.
- `bru2bids` itself (vendored SAMRI) parses ParaVision metadata + `2dseq`
  reconstructed images and reorganizes them into a BIDS tree under
  `out_base` (`self.bids_base`), matching structural scan types by
  acquisition protocol name (`structural_match`, the
  `["TurboRARE","UTE","TOF","T1Flash",...]` list also surfaced as
  `comboBox_register_key` choices in the UI).

### 2.3 Bias correction / structural registration — `samri/samri/pipelines/preprocess.py`

Two entry points, both wired from the SAMRI dock (`SAMRI_InputDock`):

- **`biascorrection` (optional, `pushButton_biascorrection`)** → 
  `InitSAMRI.biascorrection` → `biascorrect_only(...)`: N4 bias-field
  correction only, no atlas registration. Useful as a standalone
  preprocessing/QC step before committing to a full registration.
- **`register` (`pushButton_register`)** → `InitSAMRI.start_registration`
  → `structural(...)`: N4 bias-correct, then **ANTs registration**
  (rigid → affine → SyN, via `nipype.interfaces.ants.registration`) of the
  subject's structural scan (`register_key` acquisition, e.g. `TurboRARE`)
  onto the active atlas template (`atlas_folder/atlas_template`, from
  `mrid_utils/atlas_registry.py`'s active entry). `elastic` toggles whether
  the nonlinear SyN stage runs; `presurgery` registers a post-op session to
  a pre-op one instead of straight to the atlas; an optional moving-image
  mask (drawn/segmented by the user, `pushButton_createMovMask`) and/or
  atlas mask constrain what the registration actually optimizes against.
- Both are real **nipype `Workflow`s** executed with
  `plugin="MultiProc", plugin_args={'n_procs': n_jobs}` — nipype forks a
  **pool of OS subprocesses**, sized by `samri_input['num_threads']` (GUI
  spinbox, capped 1–8) threaded down into `n_jobs`, and each pipeline node
  it runs shells out to an **ANTs command-line binary**
  (`antsRegistration`, `N4BiasFieldCorrection`, `antsApplyTransforms`, …).
  On an OOM/crash, `main_window.py`'s `on_registration_failed` detects it
  from the traceback text and offers to retry at half the thread count.
  **The node graph itself is a strict linear chain per scan**, though —
  `structural()`'s only wiring (`preprocess.py:1245-1298`, gated on
  `structural_scan_types.any()`) is
  `get_s_scan → s_biascorrect (N4BiasFieldCorrection) → s_register
  (ants.Registration, i.e. antsRegistration) → s_warp (ants.ApplyTransforms,
  i.e. antsApplyTransforms) → datasink`; there is no parallel functional
  branch wired in at all when `functional_match={}` (IMPLAnT's only usage —
  `real_size_nodes()`'s unused `f_biascorrect` node is created but never
  connected). So for the ordinary case — one scan matching the selected
  `register_key`/`task`/session — these three ANTs steps run strictly
  **sequentially**, one subprocess active at a time; the `MultiProc` pool
  has nothing to actually parallelize. Genuine concurrency only appears if
  the session has **more than one scan** matching the same
  acquisition+task (`get_s_scan.iterables = ("ind_type", struct_ind)` then
  has `len(struct_ind) > 1`) — nipype instantiates one full chain per
  matching scan, and those independent chains' steps can then overlap
  across the thread pool. `biascorrect_only()` is the same story minus the
  last two steps: `get_s_scan → s_biascorrect → datasink`
  (`preprocess.py:1081-1083`), no registration/warp at all.
- **ANTs binary resolution**: `InitSAMRI.__init__` resolves `_paths['ants_bin']`
  (`_resolve_ants_bin`) to an absolute directory — next to the frozen `.exe`
  when packaged (`sys.frozen`), or under the project root otherwise — and
  prepends it to `PATH` plus sets `ANTSPATH`, so nipype's ANTs interfaces
  find the right binaries without a system-wide ANTs install.
- **Monkeypatch**: `samri_main.py` module-load time patches
  `nipype.interfaces.ants.registration.Registration._format_registration`
  to strip `NULL` mask placeholders from the generated `antsRegistration`
  command line (`--masks [ NULL ]` etc.) — a compatibility fix for how
  nipype formats the command when no mask is given, applied globally to
  every `ants.Registration` instance in the process, not just SAMRI's own.

### 2.4 Post-registration bookkeeping — `InitSAMRI.start_registration` (`samri_main.py:198-279`)

After `structural()` returns the warped image path:

1. Looks up that image's row in nipype's own
   `results/generic_work/data_selection.csv` to find the matching
   `output_Composite.h5` transform (`.../s_register/output_Composite.h5`).
2. Loads both images via SimpleITK and **brute-force builds a full
   fixed→moving voxel correspondence table** — a triple nested loop over
   every `(x, y, z)` in the fixed (atlas) image's grid, applying the
   transform and saving both arrays as `fixed_img-indeces.npy` /
   `moving_img_resampled25um-indeces.npy` in the session's `registration/`
   folder. This is `O(voxels)` in the *atlas* grid, not the subject scan,
   and is the slowest pure-Python step in the whole pipeline for a
   full-resolution atlas.
3. Copies `output_Composite.h5` into
   `bids/sub-<id>/ses-<session>/registration/output_Composite.h5` — **this
   file is the single artifact every downstream consumer actually reads**
   (see §2.6).
4. `main_window.py::_on_registration_done` then re-verifies the copy landed
   (exists + non-zero size) before telling the user registration succeeded,
   copies the whole `sub-<id>` tree into `DATA/` (`_copy_sub_to_data`), and
   synchronously (GUI thread) reloads the 3D view via `visualize_results`.

### 2.5 Atlas configuration layer — getting the atlas files

- `mrid_utils/atlas_registry.py`: static registry of every atlas IMPLAnT
  can register against — currently `whs_sd_rat` (source: `"bundle"` — the
  raw WHS SD rat MRI/DTI atlas) and `whs_sd_swc_female_rat` (source:
  `"brainglobe"` — a BrainGlobe microscopy atlas resampled onto WHS's own
  grid). Each entry carries its file names, a `subfolder` (or none), its
  `source`, and per-atlas bregma/lambda voxel coordinates + corpus-callosum
  label id — everything else in the codebase reads these constants rather
  than hardcoding them, so a third atlas is a registry entry, not a code
  change.
- `mrid_utils/atlas_switch.py::switch_active_atlas`: the single entry point
  for making a registry entry the *active* atlas — dispatches to whichever
  of the two fetchers below matches `entry['source']`, then repoints every
  `_paths['atlas_*']` key (`atlas_volume`, `atlas_labels`, `atlas_template`,
  `atlas_mask`, `atlas_bregma_coords`, …) and persists them via
  `save_paths`. `ensure_atlas_available`/`ensure_brainglobe_atlas_available`
  (called from `switch_active_atlas`, and directly by `main_window.py`
  before SAMRI registration, trajectory planning, ephys, and electrode
  localization) are what actually trigger a fetch — both no-op instantly if
  the active atlas's files are already present locally.

**Path A — `mrid_utils/atlas_fetch.py` (bundle source, `whs_sd_rat`).**
Downloads a fixed, pinned tarball (`ATLAS_BUNDLE_URL`, a public GitHub
Release asset, ~1.3GB) over plain `requests.get(..., stream=True)`,
verifies it against a **pinned SHA-256** (`ATLAS_BUNDLE_SHA256`) before
touching it further, and only then extracts it into `atlas_folder` via
`shutil.unpack_archive`. Runs synchronously on the GUI thread (not a
`SamriWorker`), with a `QProgressDialog` driven by manual
`QApplication.processEvents()` calls. On any failure (network error, failed
checksum, cancel) the partial download is discarded and the atlas is left
untouched.

**Path B — `mrid_utils/atlas_fetch_brainglobe.py` (BrainGlobe source,
`whs_sd_swc_female_rat`).** `ensure_brainglobe_atlas_available` delegates
the actual network fetch to the third-party
`brainglobe_atlasapi.BrainGlobeAtlas(entry['brainglobe_name'])` — this
module never makes an HTTP request itself; `bg_atlasapi` downloads and
caches under `~/.brainglobe/` on its own. **No integrity check on IMPLAnT's
side at all** — unlike Path A's pinned SHA-256, whatever `bg_atlasapi`
fetches is trusted as-is; this module only confirms afterward that the
*converted output files exist*, not that the raw download was authentic.
Once fetched, `_convert` reorients the atlas's annotation/template volumes
from its native orientation to a per-atlas `brainglobe_target_orientation`
via `brainglobe_space.AnatomicalSpace.map_stack_to` (this is where the
left-right mirroring quirk noted in `atlas_registry.py` gets corrected),
thresholds `annotation > 0` into a brain mask, and — notably — writes every
volume out using a **hardcoded fixed affine** (`_WHS_AFFINE`: the exact
39.0625µm-isotropic RAS affine of the existing `WHS_SD_rat_atlas_v4.nii.gz`)
rather than the BrainGlobe atlas's own metadata, specifically so its voxel
indices land on the same grid as `whs_sd_rat` and its hardcoded
bregma/lambda coordinates stay valid without atlas-specific overrides. The
five output files then land in `atlas_folder/<subfolder>/` — same shape as
Path A's bundle, so every downstream consumer (`coord_transform.py`,
`registration.py`, `rendering.py`, ephys code) is agnostic to which path
produced them. No subprocess calls; pure Python (`nibabel`/`numpy`); also
runs synchronously on the GUI thread, not wrapped in a `SamriWorker`.

- `paths_config.py`: the one place that loads `paths_config.json`
  (falling back to `paths_config.example.json`), resolves `atlas_folder`
  relative to the executable when unpackaged, and exposes `save_paths()`
  for anything that needs to persist a path/setting back to disk.

### 2.6 Downstream consumers of `output_Composite.h5`

- **`trajectory_planning/coord_transform.py`** (`CoordTransform`): loads
  the fixed atlas image, the raw moving MRI, and the transform via
  `sitk.ReadTransform`; `atlas_to_mri_coordinates` is the one real
  per-point SimpleITK transform lookup (atlas→MRI), used for bregma/lambda
  and other precise landmarks. Everything needing many points fast (mesh
  warping, MRI→atlas — no analytic inverse exists for a SyN transform)
  instead uses a **precomputed dense correspondence lookup**
  (`_build_bregma_lambda_lookup`): a strided grid over the whole atlas,
  forward-transformed once, then queried via a `cKDTree`
  (nearest-neighbour) or `RegularGridInterpolator` (trilinear) — this is a
  second, independent voxel-grid pass distinct from step 2.4's `.npy`
  export (nothing currently reads those `.npy` files back in).
- **`core/electrode_localization.py`**, **`intraoperative/mri_preview.py`**:
  both locate `registration/output_Composite.h5` as a sibling of the
  session's `anat/` folder by convention and treat it strictly as a
  read-only reference — neither regenerates it if missing, they just
  surface a clear error pointing back at the SAMRI tab.

### 2.7 The file-loading layer — a separate concern, not part of this pipeline

Everything above reads atlas/registration files by calling `sitk.ReadImage`
directly on a known path — none of it routes through the app's general file
layer. That layer exists (`file_handling/loader.py`'s `FileLoader`,
`core/load_MRI_file.py`'s `LoadMRI`, `file_handling/resample_data.py`'s
`ResampleData`) and is worth naming precisely so it isn't mistaken for part
of the registration pipeline:

- **`FileLoader`** (`file_handling/loader.py`, instantiated once as
  `main_window.py`'s `self.FileLoader`) is the app-wide "pick a NIfTI file
  and load it" orchestrator — `QFileDialog` + confirmation popup,
  `sitk.ReadImage`, 3D/4D detection, then handing off to `LoadMRI` and the
  VTK rendering stack. It's the generic open-file pathway used by
  Pre-surgery MRI loading, "Add another file", overlays, and session
  restore.
- **`LoadMRI`** (`core/load_MRI_file.py`) is the loaded-volume *state*
  object `FileLoader` populates — VTK renderers, layers, slice indices,
  intensity tables, zoom/contrast — referenced throughout the GUI (~35
  files) as `self.LoadMRI`. `FileLoader` gets bytes off disk into a volume;
  `LoadMRI` owns everything about what's currently loaded and rendered.
- **`ResampleData`** (`file_handling/resample_data.py`) resamples a loaded
  MRI to a display resolution (100µm/25µm) — a viewer utility, unrelated to
  ANTs/SAMRI.
- **`core/registration.py` + `file_handling/itksnap_registration.py`** are
  a **different registration tool entirely** — rigid registration of one
  already-loaded MRI *session* onto another (e.g. post-op onto pre-op),
  via the `picsl_greedy`/ITK-SNAP greedy library, picked from a combo box
  of files already open in the viewer. It shares nothing at runtime with
  SAMRI/ANTs atlas registration beyond both being "register image A to
  image B."

**SAMRI's only touchpoint with any of this** is the very last step:
`InitSAMRI.visualize_results` (`samri_main.py:282-314`) calls
`MW.FileLoader.initialize_file(img_path, ...)` once, purely to display the
already-finished warped registration output as a new layer in the main
viewer. Nothing upstream of that — fetching, converting, bias-correcting,
registering, or reading the atlas itself — goes through `FileLoader` or
`LoadMRI` at all.

## 3. Concurrency & process model

```
GUI (main) thread
  └─ QApplication event loop, all Qt widgets, LogAdapter
       │
       │ SamriWorker(QThread)          ◀── one at a time; main_window.py
       ▼                                    tears down/reconnects .worker
  InitSAMRI.start_bruker2_bids / .biascorrection / .start_registration
       │
       │ nipype Workflow.run(plugin="MultiProc", plugin_args={'n_procs': n})
       ▼
  nipype's own multiprocessing pool (up to n_jobs / num_threads workers)
       │
       │ subprocess.Popen per node
       ▼
  ANTs CLI binaries (antsRegistration, N4BiasFieldCorrection, ...)
       resolved via PATH/ANTSPATH set in InitSAMRI.__init__
```

- Only one `SamriWorker` is expected to be in flight at a time;
  `fetch_data`/`start_registration` both explicitly disconnect/discard the
  previous `self.worker` before starting a new one.
- **The `MultiProc` pool's size is a ceiling, not a guarantee of actual
  concurrency.** As detailed in §2.3, for the ordinary one-scan-per-session
  case, `structural()`'s node graph is a strict sequential chain
  (`N4BiasFieldCorrection → antsRegistration → antsApplyTransforms`) — only
  one ANTs subprocess is ever active at a time regardless of how many
  threads the pool has room for. The pool only does real, simultaneous work
  when a session has multiple scans matching the same acquisition+task,
  each getting its own independent chain.
- `stdout`/`stderr` (and the `logging` root logger) are globally redirected
  into `plainTextEdit_SAMRI` by `LogAdapter` for the duration of a run,
  via a **queued Qt signal** so writes from the worker thread (or nipype's
  subprocess-reading threads) marshal safely onto the GUI thread. It
  detects and stops itself if the target widget was destroyed out from
  under it (e.g. a full `restart_gui` UI rebuild mid-run).
- Actual CPU/RAM load happens in the ANTs subprocesses, not the Qt thread
  or nipype's Python-side coordination — `num_threads` is really "how many
  ANTs processes run concurrently," which is why OOM shows up as an ANTs
  subprocess dying, not a Python exception with a clean message (hence the
  keyword-sniffing in `on_registration_failed`).

## 4. On-disk layout

```
raw_base_samri/<animal_id>/                          # raw Bruker + bru2bids work
├── <session>/<scan#>/{acqp, pdata/1/2dseq, ...}      # raw ParaVision, pre-conversion
├── bids/
│   ├── sub-<animal_id>/
│   │   └── ses-<session>/
│   │       ├── anat/*.nii.gz                         # converted structural scans
│   │       └── registration/output_Composite.h5      # ★ the artifact everything reads
│   └── bids_work/                                    # bru2bids nipype cache (wiped each run)
└── results/
    └── generic_work/
        ├── data_selection.csv                        # index used to look up per-scan output paths
        └── _ind_type_<idx>/{s_register,s_warp}/       # per-scan nipype node outputs

DATA/sub-<animal_id>/                                 # convenience copy of bids/sub-<id>,
                                                        # made after a successful registration
                                                        # (_copy_sub_to_data), data_selection.csv
                                                        # copied alongside it
```

## 5. Threat model / security notes

- **SSH host-key verification is disabled.** `data_fetcher.createSSHClient`
  uses `paramiko.AutoAddPolicy()`, so any host presenting itself as the
  configured server is trusted on first connect with no fingerprint
  check — a MITM on the local network can intercept the connection and
  harvest the plaintext-equivalent SSH session (and the password, since
  paramiko sends it during auth) or serve back attacker-controlled scan
  data.
- **Command injection into the remote shell via `animal_id`.**
  `data_fetcher.find_data` builds `"ls -l /opt/PV6.0.1/data/mri/ | grep " + animal_id`
  and hands it to `client.exec_command` — `animal_id` comes straight from
  a GUI text field with no escaping or allow-list. A value like
  `"x; rm -rf /"` (or any other shell metacharacter payload) runs
  arbitrary commands **on the Bruker host PC** as user `mri`. Same pattern,
  lower severity (filenames come from a prior `ls` rather than direct user
  input) in the "already exists" branch's `exec_command` for missing scans.
- **No path sanitization on `animal_id`/session locally either.**
  `raw_base = samri_input['raw_base_samri'] + self.animal_id` is a plain
  string concatenation (not `os.path.join`, no rejection of `..`/`/`), so a
  crafted animal ID can escape the intended raw-data folder when creating
  directories or resolving `bids_base`. Low severity today (the field is
  operator-entered, not attacker-facing), but worth constraining if
  animal IDs are ever sourced from anything less trusted (e.g. imported
  from a shared spreadsheet).
- **Bruker credentials at rest are plaintext.** `samri/bruker_info.json`
  stores `server`/`password` unencrypted; mitigated somewhat by being
  gitignored (never committed) and explicitly excluded from the PyInstaller
  bundle (see `save_bruker_info`'s docstring in `samri_main.py`), but
  anyone with filesystem read access to the dev/lab machine can read it
  directly. The GUI field is masked (`EchoMode.Password`) but that's
  display-only.
- **Atlas bundle integrity is actually handled well — but only on one of the
  two fetch paths.** `atlas_fetch.py` (bundle source) pins a SHA-256 for
  the downloaded tarball and refuses to use it on mismatch; worth keeping
  as the pattern to replicate elsewhere. `atlas_fetch_brainglobe.py`
  (BrainGlobe source) has **no equivalent check** — it delegates the
  download entirely to the third-party `bg_atlasapi` package, which caches
  under `~/.brainglobe/` with no integrity verification on IMPLAnT's side
  at all. Lower urgency than the SSH/command-injection findings above (the
  BrainGlobe registry itself is the trust boundary here, same as any other
  Python package fetch), but worth knowing it's asymmetric with the bundle
  path if this ever gets audited.
- **`subprocess.call(['rm','-rf', raw_base+'/.DS_Store'])`** uses a list
  argument (not `shell=True`), so it isn't shell-injectable itself, but it
  unconditionally deletes that exact path every fetch regardless of
  whether it's actually a `.DS_Store` file — low risk given the fixed
  suffix, flagged only because `rm -rf` is otherwise worth grepping for.
- **Nipype work directories can be large and are force-cleared.**
  `bids_work` is `shutil.rmtree`'d before every `bru2bids` run with no
  confirmation — intentional (conversions aren't incremental) but means
  any in-progress or crashed run's intermediate state is unrecoverable
  once a new fetch starts.
- **The `_format_registration` monkeypatch is process-global.** It's
  applied at `samri_main` import time to `nipype.interfaces.ants.registration.Registration`
  directly, so it silently affects *any* other code in the same process
  using that nipype interface, not just SAMRI's own calls — fine today
  since SAMRI's registration is the only user, but a landmine if another
  ANTs-registration code path is ever added.

## 6. Notable fragile points (non-security)

- `df.loc[df['path'] == filepath].index[0]` / `df.loc[df['session'] == ...].index[0]`
  (`samri_main.py`, `main_window.py`) assume a unique matching row in
  `data_selection.csv` and raise `IndexError` with no friendly message if
  that assumption ever breaks (e.g. a re-run that appends rather than
  replaces).
- The dense correspondence table in `coord_transform.py` and the `.npy`
  export in `samri_main.py::start_registration` independently recompute
  essentially the same fixed→moving mapping over the whole atlas grid —
  the `.npy` files are never read back in anywhere in the codebase.
