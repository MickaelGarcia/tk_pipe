"""Main window module."""

from __future__ import annotations

import functools
import sys

from Qt import QtCore as qtc
from Qt import QtWidgets as qtw

from tk_db.db import Db
from tk_dbui.models import AssetTypeTableModel
from tk_dbui.models import ProjectListModel


class App:
    """Application object."""

    def __init__(self):
        self.db = Db()


class DbTableWidget(qtw.QWidget):
    """Database button widget."""

    ButtonPressed = qtc.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lay_main = qtw.QVBoxLayout(self)

        self._btn_types = {
            qtw.QPushButton("Projects"): "projects",
            qtw.QPushButton("Asset types"): "asset_types",
            qtw.QPushButton("Task types"): "task_types",
            qtw.QPushButton("Publish types"): "publish_types",
        }

        for btn in self._btn_types:
            btn.setCheckable(True)
            btn.clicked.connect(functools.partial(self._on_button_pressed, btn))
            lay_main.addWidget(btn)

        lay_main.addStretch()

    def _on_button_pressed(self, button):
        for btn, name in self._btn_types.items():
            if btn == button:
                self.ButtonPressed.emit(name)
                continue
            btn.setChecked(False)


class MainWindow(qtw.QMainWindow):
    """Database main window."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setWindowTitle("Asset Manager")

        wgt_main = MainWidget(self.app)
        self.setCentralWidget(wgt_main)


class MainWidget(qtw.QWidget):
    """Central widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        # Widgets
        self._cbx_project = qtw.QComboBox(self)
        self._project_model = ProjectListModel()
        self._project_model.set_projects(list(self.app.db.projects()))
        self._cbx_project.setModel(self._project_model)

        self._btn_db = qtw.QPushButton("Db")
        self._btn_db.setCheckable(True)

        self._btn_asset = qtw.QPushButton("Asset")
        self._btn_asset.setCheckable(True)

        self._lsv_asset_type = qtw.QListView(self)
        self._asset_type_model = AssetTypeTableModel()
        self._lsv_asset_type.setModel(self._asset_type_model)
        self._lsv_asset_type.hide()

        self._db_buttons = DbTableWidget(self)
        self._db_buttons.hide()

        # Layouts
        lay_master = qtw.QHBoxLayout(self)
        lay_base_content = qtw.QVBoxLayout()
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(self._btn_db)
        lay_btn.addWidget(self._btn_asset)

        lay_base_content.addWidget(self._cbx_project)
        lay_base_content.addLayout(lay_btn)
        lay_base_content.addWidget(self._lsv_asset_type)
        lay_base_content.addWidget(self._db_buttons)

        lay_master.addLayout(lay_base_content)

        # Connections
        self._btn_asset.clicked.connect(self._on_btn_asset_clicked)
        self._btn_db.clicked.connect(self._on_btn_db_clicked)
        self._db_buttons.ButtonPressed.connect(print)

        # Initialisation

        self._asset_type_model.set_asset_type(list(self.app.db.asset_types()))

    def _on_btn_asset_clicked(self):
        is_checked = self._btn_asset.isChecked()
        if is_checked:
            self._btn_db.setChecked(False)
            self._lsv_asset_type.show()
            self._db_buttons.hide()

    def _on_btn_db_clicked(self):
        is_checked = self._btn_db.isChecked()
        if is_checked:
            self._btn_asset.setChecked(False)
            self._db_buttons.show()
            self._lsv_asset_type.hide()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    tk_app = App()
    widget = MainWindow(tk_app)
    widget.show()
    app.exec_()
