# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files

datas = []
binaries = []
hiddenimports = []

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

# Project data files
datas += [
    ('paths_config.example.json', '.'),
    ('Icons', 'Icons'),
    ('samri', 'samri'),
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='IMPLAnT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,   # keep True until the app works, then switch to False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Icons/Github/IMPLAnT_logo.png',
)
