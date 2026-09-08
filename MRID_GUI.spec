# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files

datas = []
binaries = []
hiddenimports = []

# Only the specific ANTs CLI binaries samri's nipype pipeline actually
# invokes (see nipype.interfaces.ants.{Registration,ApplyTransforms,
# N4BiasFieldCorrection,AffineInitializer,MeasureImageSimilarity,
# WarpTimeSeriesImageMultiTransform}._cmd) -- bundling the entire ants/bin
# folder would add ~2.2GB to the build for 114 tools nothing here calls;
# these six are ~200MB total. Requires a local ANTs install to build FROM
# (ants/bin next to this .spec, e.g. via `paths_config.json`'s "ants_bin"),
# but the resulting dist/IMPLAnT/ants/bin/ is then self-contained for
# whoever runs the built app -- no separate ANTs download needed. Placed
# at 'ants/bin' in the bundle to match _resolve_ants_bin's first search
# path in samri/samri_main.py (next to the executable).
_ANTS_BIN_DIR = os.path.join('ants', 'bin')
_ANTS_TOOLS = [
    'antsRegistration',
    'antsApplyTransforms',
    'N4BiasFieldCorrection',
    'antsAffineInitializer',
    'MeasureImageSimilarity',
    'WarpTimeSeriesImageMultiTransform',
]
for _tool in _ANTS_TOOLS:
    _tool_path = os.path.join(_ANTS_BIN_DIR, _tool)
    if os.path.isfile(_tool_path):
        binaries.append((_tool_path, _ANTS_BIN_DIR))
    else:
        print(f"WARNING: {_tool_path} not found -- built app will be missing this ANTs tool")

# ephys/videoplayer.py shells out to ffprobe (container-header frame-rate
# probing, not decoding -- Qt's own bundled FFmpeg plugin handles playback
# separately). It's a system binary, not a Python package, so it has to be
# bundled explicitly the same way as the ANTs tools above -- otherwise a
# bare `subprocess.run(["ffprobe", ...])` only ever works by accident, on
# whichever machine happens to have system ffmpeg on PATH. Requires a local
# ffprobe next to this .spec (e.g. via `paths_config.json`'s "ffprobe_bin"),
# but the resulting dist/IMPLAnT/ffmpeg/bin/ is then self-contained for
# whoever runs the built app. Placed at 'ffmpeg/bin' to match
# get_ffprobe_path's exe-relative lookup in paths_config.py.
_FFPROBE_BIN_DIR = os.path.join('ffmpeg', 'bin')
_FFPROBE_PATH = os.path.join(_FFPROBE_BIN_DIR, 'ffprobe')
if os.path.isfile(_FFPROBE_PATH):
    binaries.append((_FFPROBE_PATH, _FFPROBE_BIN_DIR))
else:
    print(f"WARNING: {_FFPROBE_PATH} not found -- built app will be missing ffprobe "
          f"(video frame-rate detection in the Electrophysiology visualisation tab)")

tmp_ret = collect_all('vtk')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PySide6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('SimpleITK')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('qdarkstyle')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
# NOT also collect_all('PySide6.QtSvg') here: QtSvg is a submodule of PySide6,
# so collect_all('PySide6') above already walks its entire .framework bundle.
# The redundant separate call duplicated every file in it into datas/binaries
# -- harmless on Linux, but on macOS a .framework's internal Versions/Current
# symlink is a real filesystem symlink, and COLLECT tries to os.symlink() it
# twice (once per duplicate entry), which crashes with FileExistsError on the
# second attempt. 'PySide6.QtSvg' stays in hiddenimports below so the module
# itself is still forced in, independent of this datas/binaries collection.

# rippl-AI's actual runtime deps (see rippl-AI/aux_fcn.py's imports) --
# tensorflow/xgboost are notorious for incomplete static-import discovery
# under PyInstaller, so collect them explicitly rather than trust the
# --ripple-worker sentinel branch's plain `import run_rippl` in
# main_window.py to pull in everything transitively.
for _pkg in ('tensorflow', 'tf_keras', 'xgboost', 'imblearn', 'matplotlib'):
    tmp_ret = collect_all(_pkg)
    datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# samri/bruker_info.json is a real, gitignored, per-user secret (scanner
# hostname/password -- see README's "Bruker scanner" section), NOT
# something to ever ship in a distributed build. A plain ('samri','samri')
# datas tuple would recursively bundle every file physically present under
# samri/ at build time, credentials included, regardless of .gitignore
# (which only affects git, not the filesystem PyInstaller walks) -- so
# build the samri file list explicitly instead, skipping that one file
# (and __pycache__, which is build noise, not app data) rather than
# trusting whoever runs this build to remember to delete it first.
_SAMRI_EXCLUDE_BASENAMES = {'bruker_info.json'}
_samri_datas = []
for _root, _dirs, _files in os.walk('samri'):
    _dirs[:] = [d for d in _dirs if d != '__pycache__']
    for _fname in _files:
        if _fname in _SAMRI_EXCLUDE_BASENAMES:
            print(f"NOTE: excluding {os.path.join(_root, _fname)} from the build (real per-user secret)")
            continue
        _src = os.path.join(_root, _fname)
        _samri_datas.append((_src, _root))

# rippl-AI submodule: only what --ripple-worker's run_rippl.py actually
# needs at inference time (rippl_AI.py/aux_fcn.py/run_rippl.py + the trained
# model weights in optimized_models/) -- excludes .git (submodule metadata,
# ~29MB), Models_output/figures/examples_explore/notebooks (training/docs
# artifacts never imported by the inference path, ~50MB combined).
_RIPPL_AI_EXCLUDE_DIRNAMES = {'.git', '__pycache__', 'Models_output', 'figures', 'examples_explore'}
_rippl_ai_datas = []
for _root, _dirs, _files in os.walk('rippl-AI'):
    _dirs[:] = [d for d in _dirs if d not in _RIPPL_AI_EXCLUDE_DIRNAMES]
    for _fname in _files:
        if _fname.endswith('.ipynb'):
            continue
        _src = os.path.join(_root, _fname)
        _rippl_ai_datas.append((_src, _root))

# Project data files
datas += _samri_datas + _rippl_ai_datas + [
    ('paths_config.example.json', '.'),
    ('paths_config.py', '.'),
    ('Icons', 'Icons'),
    ('core', 'core'),
    ('ephys', 'ephys'),
    ('ephys_utils', 'ephys_utils'),
    ('file_handling', 'file_handling'),
    ('gui_utils', 'gui_utils'),
    ('mrid_utils', 'mrid_utils'),
    ('trajectory_planning', 'trajectory_planning'),
    ('utils', 'utils'),
    ('segmentation', 'segmentation'),
    ('ui_form.py', '.'),
    ('form.ui', '.'),
    ('mrid_library.pkl', '.'),
]

a = Analysis(
    ['main_window.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + [
        'SimpleITK',
        'qdarkstyle',
        'vtkmodules.all',
        'pkg_resources.py2_warn',
        'PySide6.QtSvg',
        'PySide6.QtXml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# onedir, not onefile: --ripple-worker re-invokes this same exe as a
# subprocess for every single ripple-detection call (see ephys/init_ephys.py)
# -- a onefile build re-unpacks its ENTIRE bundle (tensorflow included) to a
# fresh temp dir on every launch, which would mean paying that full cost on
# every ripple-detection click. onedir sits already-unpacked on disk, so
# re-invoking it is just launching an existing binary.
# UPX-modified Mach-O binaries routinely break macOS's auto-applied ad-hoc
# code signature (Gatekeeper then reports the app as "damaged"), for the
# same marginal size benefit that already isn't worth the risk for the ANTs
# binaries below -- so no UPX at all on darwin, not just excluded by name.
_USE_UPX = sys.platform != 'darwin'

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IMPLAnT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=_USE_UPX,
    # UPX-compressing these large, correctness-critical ANTs binaries risks
    # a corrupted/broken executable for marginal size benefit -- exclude by
    # filename (upx_exclude matches on basename, not full path).
    upx_exclude=_ANTS_TOOLS,
    runtime_tmpdir=None,
    console=True,   # keep True until the app works, then switch to False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Icons/Github/IMPLAnT_quad.png',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=_USE_UPX,
    upx_exclude=_ANTS_TOOLS,
    name='IMPLAnT',
)

if sys.platform == 'darwin':
    # Without this, macOS gets the same COLLECT onedir output as Linux --
    # a plain folder with a Unix executable inside, not a double-clickable,
    # Gatekeeper/Launchpad-recognized .app. Unsigned (codesign_identity=
    # None, matching EXE above): fine for running the build you just made
    # yourself (first launch needs right-click -> Open, or `xattr -cr` if
    # macOS flags it as quarantined/damaged after a transfer); distributing
    # this to other people would need an actual Apple Developer ID
    # certificate to sign and notarize with, which is a cost/process
    # decision for whoever owns the release, not something to assume here.
    app = BUNDLE(
        coll,
        name='IMPLAnT.app',
        icon='Icons/Github/IMPLAnT_quad.png',
        bundle_identifier=None,
    )
