# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCompleter, QDialog, QDialogButtonBox, QLabel, QLineEdit, QMessageBox, QVBoxLayout
)


class AddRegionDialog(QDialog):
    """Same idea as Change_AnatRegion (ephys/change_anatRegion.py), but a free-typed
    QLineEdit with autocomplete instead of an editable combobox -- picking one atlas
    region name out of a couple hundred is faster to type-and-filter than to scroll."""

    def __init__(self, region_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Show Another Region")
        self.region_names = sorted(region_names)
        self._chosen = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Type or search for an anatomical region:"))

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Start typing a region name...")
        completer = QCompleter(self.region_names, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.line_edit.setCompleter(completer)
        layout.addWidget(self.line_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_accept(self):
        text = self.line_edit.text().strip()
        if text not in self.region_names:
            matches = [n for n in self.region_names if n.lower() == text.lower()]
            if not matches:
                QMessageBox.warning(self, "Unknown region", f'"{text}" is not a known atlas region.')
                return
            text = matches[0]
        self._chosen = text
        self.accept()

    def selected_region_name(self):
        return self._chosen
