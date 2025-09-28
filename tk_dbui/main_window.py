"""Main window module."""

from __future__ import annotations

import functools
import sys

from Qt import QtCore as qtc
from Qt import QtWidgets as qtw

from tk_db.db import Db
from tk_dbui.centra_widgets_db import AssetTypeTable
from tk_dbui.centra_widgets_db import PublishTypeTable
from tk_dbui.centra_widgets_db import TaskTypeTable
from tk_dbui.models import AssetTaskTypeListModel
from tk_dbui.models import AssetTaskTypeTableModel
from tk_dbui.models import ProjectListModel


class App:
    """Application object."""

    def __init__(self):
        self.db = Db()


class DbButtonsWidget(qtw.QWidget):
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
                continue
            btn.setChecked(False)

    def add_buttons(self, button_name, index: int = -1, *args, **kwargs):
        """Add button to the ui."""
        btn = qtw.QPushButton(*args, **kwargs)
        btn.setCheckable(True)
        btn.clicked.connect(functools.partial(self._on_button_pressed, button_name))
        if index == -1:
            index  = len(self._btn_types) + 1
        self._lay_main.insertWidget(index, btn)

        self._btn_types[btn] = button_name



class DbTableWidget(qtw.QWidget):
    """Database table widget."""

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        self._btn_widget = DbButtonsWidget(self)
        self._btn_widget.add_buttons("projects", 0, "Projects")
        self._btn_widget.add_buttons("asset_types", 1, "Asset Types")
        self._btn_widget.add_buttons("task_types", 2, "Task Types")
        self._btn_widget.add_buttons("publish_types", 3, "Publish Types")

        self._tbl_asset_type = AssetTypeTable(self.app, self)
        self._tbl_asset_type.hide()

        self._tbl_task_type = TaskTypeTable(self.app, self)
        self._tbl_task_type.hide()

        self._tbl_publish_type = PublishTypeTable(self.app, self)
        self._tbl_publish_type.hide()

        self._central_widget_by_name: dict[str, qtw.QWidget] = {
            "asset_types": self._tbl_asset_type,
            "task_types": self._tbl_task_type,
            "publish_types": self._tbl_publish_type,
        }

        lay_main = qtw.QHBoxLayout(self)
        lay_main.addWidget(self._btn_widget)
        lay_main.addWidget(self._tbl_asset_type)
        lay_main.addWidget(self._tbl_task_type)
        lay_main.addWidget(self._tbl_publish_type)

        self._btn_widget.ButtonPressed.connect(self._on_db_button_clicked)

    def _on_db_button_clicked(self, widget_name):
        for name, db_widget in self._central_widget_by_name.items():
            if widget_name == name:
                db_widget.show()
                continue
            db_widget.hide()


class DbEntityTabWidget(qtw.QWidget):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        self._cbx_project = qtw.QComboBox(self)
        self._project_model = ProjectListModel()
        self._project_model.set_projects(list(self.app.db.projects()))
        self._cbx_project.setModel(self._project_model)

        self._btn_asset = qtw.QPushButton("Asset")
        self._btn_asset.setCheckable(True)

        self._lsv_asset_type = qtw.QListView(self)
        self._asset_type_model = AssetTaskTypeListModel()
        self._lsv_asset_type.setModel(self._asset_type_model)
        self._lsv_asset_type.hide()

        # Layouts
        lay_master = qtw.QHBoxLayout(self)
        lay_base_content = qtw.QVBoxLayout()
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(self._btn_asset)

        lay_base_content.addWidget(self._cbx_project)
        lay_base_content.addLayout(lay_btn)
        lay_base_content.addWidget(self._lsv_asset_type)

        lay_master.addLayout(lay_base_content)

        # Connections
        self._btn_asset.clicked.connect(self._on_btn_asset_clicked)

        # Initialisation

        self._asset_type_model.set_asset_type(list(self.app.db.asset_types()))

        self._btn_asset.setChecked(True)
        self._on_btn_asset_clicked()

    def _on_btn_asset_clicked(self):
        is_checked = self._btn_asset.isChecked()
        if not is_checked:
            self._lsv_asset_type.hide()
            return

        self._lsv_asset_type.show()
        self._asset_type_model.set_asset_type(list(self.app.db.asset_types()))

class MainWindow(qtw.QMainWindow):
    """Database main window."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setWindowTitle("Asset Manager")
        self.setMinimumSize(800, 800)

        wgt_main = MainWidget(self.app)
        self.setCentralWidget(wgt_main)


class MainWidget(qtw.QWidget):
    """Central widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        # Widgets
        self._db_widget = DbTableWidget(self.app, self)
        self._entity_widget = DbEntityTabWidget(self.app, self )

        self._tab_widget = qtw.QTabWidget(self)
        self._tab_widget.addTab(self._entity_widget, "Entity")
        self._tab_widget.addTab(self._db_widget, "Db")

        lay_main = qtw.QVBoxLayout(self)
        lay_main.addWidget(self._tab_widget)


if __name__ == "__main__":
    qt_app = qtw.QApplication(sys.argv)
    tk_app = App()
    widget = MainWindow(tk_app)
    widget.show()
    qt_app.exec_()
