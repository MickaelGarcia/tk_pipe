"""Main window module."""

from __future__ import annotations

import sys

from Qt import QtWidgets as qtw

from tk_db.db import Db
from tk_dbui.project_ui import ProjectListModel


class App:
    """Application object."""

    def __init__(self):
        self.db = Db()


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

        self._btn_asset = qtw.QPushButton("Asset")
        self._btn_asset.setCheckable(True)

        self._btn_db = qtw.QPushButton("Db")
        self._btn_db.setCheckable(True)

        # Layouts
        lay_master = qtw.QHBoxLayout(self)
        lay_base_content = qtw.QVBoxLayout()
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(self._btn_asset)
        lay_btn.addWidget(self._btn_db)

        lay_base_content.addWidget(self._cbx_project)
        lay_base_content.addLayout(lay_btn)

        lay_master.addLayout(lay_base_content)

        # Connections
        self._btn_asset.clicked.connect(self._on_btn_asset_clicked)
        self._btn_db.clicked.connect(self._on_btn_db_clicked)

    def _on_btn_asset_clicked(self):
        is_checked = self._btn_asset.isChecked()
        if is_checked:
            self._btn_db.setChecked(False)

    def _on_btn_db_clicked(self):
        is_checked = self._btn_db.isChecked()
        if is_checked:
            self._btn_asset.setChecked(False)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    tk_app = App()
    widget = MainWindow(tk_app)
    widget.show()
    app.exec()
