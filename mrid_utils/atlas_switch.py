# This Python file uses the following encoding: utf-8
"""Single entry point for making a different registry atlas
(mrid_utils/atlas_registry.py) the active one -- ensures its files exist
(fetching/converting if needed), then repoints every _paths['atlas_*'] key
every existing consumer already reads. Used both by AtlasSelectorDialog below
(the non-live surface, reachable via File -> Atlas... whenever the user
isn't already inside trajectory planning) and by trajectory planning's live
in-view switcher (trajectory_planning/registration.py's
TpRegistration.reload_atlas_view)."""
import os

from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QLabel, QVBoxLayout

from paths_config import _paths, save_paths
from mrid_utils import atlas_fetch, atlas_fetch_brainglobe
from mrid_utils.atlas_registry import ATLASES, get_active_atlas_id


def _file_path(entry, key):
    """entry['files'][key], prefixed with entry['subfolder'] when the atlas
    keeps its converted files under a subfolder of atlas_folder rather than
    directly in it (see mrid_utils/atlas_registry.py)."""
    filename = entry['files'][key]
    return os.path.join(entry['subfolder'], filename) if entry['subfolder'] else filename


def switch_active_atlas(atlas_id, parent_widget):
    """Returns True once atlas_id's files are available and _paths has been
    repointed + persisted to it. Returns False (leaving the previously
    active atlas untouched in _paths) if the user cancels or the fetch
    fails."""
    entry = ATLASES[atlas_id]

    if entry['source'] == 'bundle':
        available = atlas_fetch.ensure_atlas_available(parent_widget)
    elif entry['source'] == 'brainglobe':
        available = atlas_fetch_brainglobe.ensure_brainglobe_atlas_available(parent_widget, atlas_id)
    else:
        raise ValueError(f"Unknown atlas source: {entry['source']!r}")

    if not available:
        return False

    save_paths(
        active_atlas=atlas_id,
        atlas_volume=_file_path(entry, 'atlas_volume'),
        atlas_labels=_file_path(entry, 'atlas_labels'),
        atlas_template=_file_path(entry, 'atlas_template'),
        atlas_mask=_file_path(entry, 'atlas_mask'),
        atlas_dwi=_file_path(entry, 'atlas_dwi') if entry['has_dwi'] else None,
        atlas_bregma_coords=entry['bregma_coords'],
        atlas_lambda_coords=entry['lambda_coords'],
        atlas_cc_label=entry['cc_label'],
        atlas_ca1_region_name=entry['ca1_region_name'],
    )
    return True


class AtlasSelectorDialog(QDialog):
    """Reachable via File -> Atlas... (main_window.py) or wherever else
    ensure_atlas_available-style checks fire (ephys, electrode
    localization). Not needed inside trajectory planning itself, which gets
    its own live in-view combo (see TpRegistration.reload_atlas_view) --
    this is for choosing the active atlas before entering one of the
    screens that don't."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Atlas")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Active atlas:"))

        self.combo = QComboBox()
        self._ids = list(ATLASES.keys())
        for atlas_id in self._ids:
            self.combo.addItem(ATLASES[atlas_id]['display_name'])
        current_id = get_active_atlas_id(_paths)
        if current_id in self._ids:
            self.combo.setCurrentIndex(self._ids.index(current_id))
        layout.addWidget(self.combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def chosen_atlas_id(self):
        return self._ids[self.combo.currentIndex()]


def show_atlas_selector(parent_widget):
    """Opens AtlasSelectorDialog; switches to whichever atlas the user
    picked (fetching/converting it first if needed). No-op if cancelled or
    the user re-picks the atlas that's already active."""
    dlg = AtlasSelectorDialog(parent_widget)
    if dlg.exec() != QDialog.DialogCode.Accepted:
        return
    atlas_id = dlg.chosen_atlas_id()
    if atlas_id == get_active_atlas_id(_paths):
        return
    switch_active_atlas(atlas_id, parent_widget)
