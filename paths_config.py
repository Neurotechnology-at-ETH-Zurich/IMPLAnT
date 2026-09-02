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
import sys

_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir

_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = json.load(_f)

# atlas_folder is a fixed, shared reference dataset (unlike raw_base/
# raw_base_samri, which point at large, user-specific, often-elsewhere
# scan data, and so stay absolute/user-provided) -- safe to default to a
# folder next to the executable, same convention samri_main.py's own
# _resolve_ants_bin already uses for ants_bin, so a build's atlas files
# just need to land in <exe_dir>/atlas/ instead of editing the JSON.
if not os.path.isabs(_paths['atlas_folder']):
    _paths['atlas_folder'] = os.path.join(_exe_dir, _paths['atlas_folder'])

_user_config_path = os.path.join(_exe_dir, 'paths_config.json')


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
