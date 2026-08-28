# This Python file uses the following encoding: utf-8
"""Auto-fetch the ~1.3GB raw WHS SD rat atlas files (atlas_volume,
atlas_labels, atlas_dwi, atlas_template, atlas_mask -- see
paths_config.example.json) into _paths['atlas_folder'] the first time
they're needed, so there's no manual download/placement step whether the
app is run from source or as the frozen .exe -- paths_config.py already
resolves atlas_folder to <exe_dir>/atlas either way, this just needs to
make sure something is actually there.

Does NOT touch the separately-built/verified BrainGlobeAtlas package
(whs_sd_rat_full_39um) -- none of the app's own code (coord_transform.py,
registration.py, visualisation3D.py, rendering.py) consumes that, they all
read these 5 raw files directly by path.
"""
import hashlib
import os
import shutil
import tempfile

import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QProgressDialog, QPushButton, QVBoxLayout,
)

from paths_config import _paths, save_paths
from mrid_utils.atlas_registry import ATLASES

# Published as a GitHub Release asset on Neurotechnology-at-ETH-Zurich/IMPLAnT
# (public repo, so a plain URL works -- no token needs to ship inside the
# .exe). See mrid_utils/build_atlas_bundle.py for how the bundle itself is
# produced and published; re-run that + update these two if the bundle
# ever needs to change.
ATLAS_BUNDLE_URL = "https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT/releases/download/atlas-v1/whs_sd_rat_raw_atlas.tar.gz"
ATLAS_BUNDLE_SHA256 = "195a66ae093f9431cefe1099c284811e315ffe7239d4ab3216e0b79b3358f892"

_ATLAS_FILE_KEYS = ('atlas_volume', 'atlas_labels', 'atlas_dwi', 'atlas_template', 'atlas_mask')

_DOWNLOAD_CHUNK_BYTES = 1024 * 1024  # 1MB


def _atlas_files_present():
    """Whether the WHS bundle's own known files (fixed filenames, from the
    atlas registry) are present under atlas_folder -- deliberately checked
    against ATLASES['whs_sd_rat']['files'] rather than _paths[key], since
    _paths reflects whichever atlas is CURRENTLY active (see
    mrid_utils/atlas_registry.py) and can point at a completely different
    atlas' files, or have _paths['atlas_dwi'] set to None (for an active
    atlas with no DWI, e.g. the brainglobe microscopy atlas) -- neither of
    which says anything about whether the WHS bundle itself is present.
    This function's only job is gating/driving the WHS-bundle download
    below, regardless of which atlas happens to be active right now (e.g.
    mid-switch, via atlas_switch.py's switch_active_atlas, called before
    _paths gets repointed to whs_sd_rat)."""
    files = ATLASES['whs_sd_rat']['files']
    return all(
        os.path.exists(os.path.join(_paths['atlas_folder'], files[key]))
        for key in _ATLAS_FILE_KEYS
    )


def _sha256_of(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(_DOWNLOAD_CHUNK_BYTES), b''):
            digest.update(chunk)
    return digest.hexdigest()


class _AtlasFolderDialog(QDialog):
    """Lets the user confirm (or change) where the atlas gets downloaded
    to, rather than silently always using _paths['atlas_folder']'s current
    default -- e.g. to put it on a shared/faster/larger drive instead of
    next to the executable. Mirrors the SAMRI dock's existing browse+save
    pattern for atlas_folder (samri_main.py's pushButton_browseAtlas /
    save_all_paths), just as a standalone dialog since this can fire from
    several different entry points (ephys, trajectory planning, SAMRI
    registration, electrode localization) rather than only from that dock."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Atlas Files")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(
            "The reference atlas files (~1.3GB) aren't present yet and are "
            "needed for this step. This only happens once -- they're cached "
            "afterward.\n\nSave them to:"))

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit(_paths['atlas_folder'])
        browse_button = QPushButton("Browse…")
        browse_button.clicked.connect(self._browse)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_button)
        layout.addLayout(path_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Download")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Atlas Folder", self.path_edit.text())
        if folder:
            self.path_edit.setText(folder)

    def chosen_folder(self):
        return self.path_edit.text().strip()


def _choose_atlas_folder(parent_widget):
    """Shows _AtlasFolderDialog; returns the confirmed folder path, or
    None if the user cancelled. Persists a changed path into
    paths_config.json (via save_paths, which also updates the shared
    _paths dict in place) so it's remembered as the default next time."""
    dlg = _AtlasFolderDialog(parent_widget)
    if dlg.exec() != QDialog.DialogCode.Accepted:
        return None
    folder = dlg.chosen_folder()
    if not folder:
        QMessageBox.warning(parent_widget, "Download Atlas Files", "Please choose a folder.")
        return None
    if folder != _paths['atlas_folder']:
        save_paths(atlas_folder=folder)
    return folder


def ensure_atlas_available(parent_widget):
    """Returns True once _paths['atlas_folder'] actually has all 5 atlas
    files -- either because they were already there (no network touched
    at all), or because this just downloaded+verified+extracted them.
    Returns False if the user declines, the download/checksum fails, or
    is cancelled -- callers should abort whatever needed the atlas."""
    if _atlas_files_present():
        return True

    if not ATLAS_BUNDLE_URL:
        QMessageBox.critical(
            parent_widget, "Atlas files missing",
            "The atlas files aren't present, and no download URL is configured "
            "yet (mrid_utils/atlas_fetch.py's ATLAS_BUNDLE_URL is empty).\n\n"
            f"Expected them under: {_paths['atlas_folder']}")
        return False

    if _choose_atlas_folder(parent_widget) is None:
        return False

    tmp_path = None
    dlg = None
    try:
        response = requests.get(ATLAS_BUNDLE_URL, stream=True, timeout=30)
        response.raise_for_status()
        total_bytes = int(response.headers.get('Content-Length', 0))

        # setWindowTitle matters here -- an untitled top-level Qt window
        # falls back to showing QApplication.applicationName() ("IMPLAnT",
        # set in main_window.py's __main__) as its title bar text instead
        # of staying blank, which is confusing on an otherwise-plain
        # progress dialog.
        dlg = QProgressDialog("Downloading atlas files…", "Cancel", 0, 100, parent_widget)
        dlg.setWindowTitle("Downloading Atlas Files")
        dlg.setWindowModality(Qt.WindowModal)
        dlg.setMinimumDuration(0)
        dlg.setValue(0)

        fd, tmp_path = tempfile.mkstemp(suffix='.tar.gz')
        received = 0
        with os.fdopen(fd, 'wb') as f:
            for chunk in response.iter_content(chunk_size=_DOWNLOAD_CHUNK_BYTES):
                if not chunk:
                    continue
                f.write(chunk)
                received += len(chunk)
                if total_bytes:
                    dlg.setValue(int(received / total_bytes * 100))
                QApplication.processEvents()
                if dlg.wasCanceled():
                    raise KeyboardInterrupt("Atlas download cancelled")
        dlg.setValue(100)

        digest = _sha256_of(tmp_path)
        if digest != ATLAS_BUNDLE_SHA256:
            QMessageBox.critical(
                parent_widget, "Atlas download failed",
                "The downloaded atlas bundle failed checksum verification "
                "and was discarded. Please try again.\n\n"
                f"Expected: {ATLAS_BUNDLE_SHA256}\nGot: {digest}")
            return False

        os.makedirs(_paths['atlas_folder'], exist_ok=True)
        shutil.unpack_archive(tmp_path, _paths['atlas_folder'])

    except KeyboardInterrupt:
        return False
    except Exception as exc:
        QMessageBox.critical(
            parent_widget, "Atlas download failed",
            f"Could not download the atlas files:\n{exc}")
        return False
    finally:
        # Explicit close rather than relying on QProgressDialog's implicit
        # autoClose-at-100% -- it's driven by manual processEvents() calls
        # here rather than a normal event loop, and any exception raised
        # before the loop reaches 100% would otherwise leave it orphaned
        # on screen behind whatever error dialog follows.
        if dlg is not None:
            dlg.close()
        if tmp_path is not None and os.path.exists(tmp_path):
            os.remove(tmp_path)

    if not _atlas_files_present():
        QMessageBox.critical(
            parent_widget, "Atlas download failed",
            "The atlas bundle was downloaded and extracted, but the expected "
            f"files still aren't all present under {_paths['atlas_folder']}.\n"
            "The bundle's internal layout may not match what's expected.")
        return False

    return True
