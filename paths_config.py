# This Python file uses the following encoding: utf-8
"""Single source of truth for loading paths_config.json (falling back to
paths_config.example.json) -- every module used to duplicate this exact
block (compute _base_dir/_exe_dir, pick the config file, json.load it)
independently, which meant any fix to it (e.g. resolving atlas_folder
relative to the executable, below) had to be copy-pasted into every one
of them. Import _paths (and _base_dir/_exe_dir, if a module also derives
other exe-relative paths of its own) from here instead."""
import json
import os
import shutil
import sys

_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir

_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = json.load(_f)

# Whichever atlas a previous session ended up on (e.g. the microscopic
# whs_sd_swc_female_rat, picked via one of the live in-view atlas switchers
# -- see mrid_utils/atlas_switch.py) is only ever a same-session override,
# never a lasting default: every fresh process start forces the active
# atlas back to the registry's own DEFAULT_ATLAS (WHS) in memory, regardless
# of what got persisted to paths_config.json by the last switch. Users can
# still switch away for that session; it just never sticks past a restart.
from mrid_utils.atlas_registry import ATLASES, DEFAULT_ATLAS

_default_atlas_entry = ATLASES[DEFAULT_ATLAS]
_paths['active_atlas'] = DEFAULT_ATLAS
for _key in ('atlas_volume', 'atlas_labels', 'atlas_template', 'atlas_mask'):
    _filename = _default_atlas_entry['files'][_key]
    _paths[_key] = (
        os.path.join(_default_atlas_entry['subfolder'], _filename)
        if _default_atlas_entry['subfolder'] else _filename
    )
_paths['atlas_dwi'] = _default_atlas_entry['files']['atlas_dwi'] if _default_atlas_entry['has_dwi'] else None
_paths['atlas_bregma_coords'] = _default_atlas_entry['bregma_coords']
_paths['atlas_lambda_coords'] = _default_atlas_entry['lambda_coords']
_paths['atlas_ca1_region_name'] = _default_atlas_entry['ca1_region_name']
del _default_atlas_entry, _key, _filename

# atlas_folder is a fixed, shared reference dataset (unlike raw_base/
# raw_base_samri, which point at large, user-specific, often-elsewhere
# scan data, and so stay absolute/user-provided) -- safe to default to a
# folder next to the executable, same convention samri_main.py's own
# _resolve_ants_bin already uses for ants_bin, so a build's atlas files
# just need to land in <exe_dir>/atlas/ instead of editing the JSON.
if not os.path.isabs(_paths['atlas_folder']):
    _paths['atlas_folder'] = os.path.join(_exe_dir, _paths['atlas_folder'])

# Unlike atlas_folder (a user manually places files next to the executable,
# so _exe_dir is correct there), ffprobe is bundled BY PyInstaller itself
# (MRID_GUI.spec's `binaries` list) -- in a onedir build PyInstaller's own
# COLLECT step puts bundled binaries/datas under _internal/ (its default
# --contents-directory), not next to the exe. _base_dir (sys._MEIPASS when
# frozen) is what actually points there; _exe_dir would silently resolve to
# a directory that doesn't exist.
if not os.path.isabs(_paths['ffprobe_bin']):
    _paths['ffprobe_bin'] = os.path.join(_base_dir, _paths['ffprobe_bin'])

_user_config_path = os.path.join(_exe_dir, 'paths_config.json')


def get_ffprobe_path():
    """Absolute path to the bundled ffprobe binary if a standalone build
    shipped one (see MRID_GUI.spec), otherwise the bare command name so
    subprocess resolves it via PATH -- the normal case when running from
    source with a system ffmpeg install (see README's Dependencies section)."""
    bundled = os.path.join(_paths['ffprobe_bin'], 'ffprobe')
    return bundled if os.path.isfile(bundled) else 'ffprobe'


def ffprobe_available():
    """Whether get_ffprobe_path() actually resolves to something runnable --
    checked up front (e.g. when the video tab is opened) so a missing ffprobe
    is reported as one clear message there, instead of only surfacing as a
    subprocess error the first time a video's frame rate is read."""
    path = get_ffprobe_path()
    return os.path.isfile(path) or shutil.which(path) is not None


def save_paths(**updates):
    """Persist the given key/value pairs into paths_config.json, creating
    it (seeded from whatever's already on disk, or from paths_config.
    example.json if there's no user config yet) if it doesn't exist --
    e.g. from a "Save settings" button that writes back whatever the user
    just typed/browsed to in the GUI (raw_base_samri, atlas_folder, ...),
    so it survives past this session instead of only ever living in the
    in-memory _paths dict.

    Reads the base config FRESH from disk rather than reusing the already-
    loaded _paths dict, since _paths['atlas_folder'] above may have been
    resolved to an absolute exe-relative path -- writing THAT back out
    would permanently bake in one machine's exact folder layout the first
    time anything gets saved, destroying the relative-path convention for
    every key not actually part of this particular save."""
    if os.path.exists(_user_config_path):
        with open(_user_config_path) as f:
            base = json.load(f)
    else:
        with open(os.path.join(_base_dir, 'paths_config.example.json')) as f:
            base = json.load(f)
    base.update(updates)
    with open(_user_config_path, 'w') as f:
        json.dump(base, f, indent=4)
    _paths.update(updates)


def get_raw_base(parent_widget=None):
    """_paths['raw_base'], resolved to a directory that actually exists, to
    hand a QFileDialog as its starting folder. raw_base has no dedicated
    settings field anywhere in the GUI (unlike mrid_library/raw_base_samri/
    the atlas bundle, which all check-and-prompt already) -- it's only ever
    used as an "open file" dialog's default location, so a wrong/placeholder
    value (e.g. straight from paths_config.example.json) isn't a blocker,
    just an unhelpful starting folder. Prompt once for the real folder and
    persist it via save_paths, same pattern as those others. Falls back to
    the home directory if there's no parent_widget to prompt with, or the
    user cancels, so callers always get a real, existing directory."""
    if os.path.isdir(_paths['raw_base']):
        return _paths['raw_base']
    if parent_widget is not None:
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        QMessageBox.information(
            parent_widget, "Raw data folder",
            "Where's your raw data folder? Pick it once and IMPLAnT will remember it."
        )
        chosen = QFileDialog.getExistingDirectory(parent_widget, "Select raw data folder")
        if chosen:
            save_paths(raw_base=chosen)
            return chosen
    return os.path.expanduser('~')
