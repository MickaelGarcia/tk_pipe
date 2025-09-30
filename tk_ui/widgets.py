"""Custom widget module."""

from __future__ import annotations

import functools

from Qt import QtCore as qtc
from Qt import QtWidgets as qtw


class RadioButtonsWidget(qtw.QWidget):
    """Database button widget."""

    ButtonPressed = qtc.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._lay_main = qtw.QVBoxLayout(self)
        self.selected_button = None

        self._btn_types = {}

        self._lay_main.addStretch()

    def _on_button_pressed(self, button_name):
        for btn, name in self._btn_types.items():
            if name == button_name:
                self.selected_button = name
                self.ButtonPressed.emit(name)
                btn.setChecked(True)
                continue
            btn.setChecked(False)

    def add_buttons(self, button_name, index: int = -1, *args, **kwargs):
        """Add button to the ui."""
        btn = qtw.QPushButton(*args, **kwargs)
        btn.setCheckable(True)
        btn.clicked.connect(functools.partial(self._on_button_pressed, button_name))
        if index == -1:
            index = len(self._btn_types) + 1
        self._lay_main.insertWidget(index, btn)

        self._btn_types[btn] = button_name
