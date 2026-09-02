# -*- mode: python ; coding: utf-8 -*-
import os
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

tmp_ret = collect_all('vtk')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PySide6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('SimpleITK')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('qdarkstyle')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PySide6.QtSvg')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

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
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IMPLAnT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    upx=True,
    upx_exclude=_ANTS_TOOLS,
    name='IMPLAnT',
)
