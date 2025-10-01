"""Main window module."""

from __future__ import annotations

import sys

from Qt import QtWidgets as qtw

from tk_db.db import Db
from tk_db.models import AssetType
from tk_dbui.centra_widgets_db import AssetTypeTable
from tk_dbui.centra_widgets_db import ProjectEditableWidget
from tk_dbui.centra_widgets_db import PublishTypeTable
from tk_dbui.centra_widgets_db import TaskTypeTable
from tk_dbui.models import EntityListModel
from tk_dbui.models import ProjectListModel
from tk_ui.widgets import RadioButtonsWidget


class App:
    """Application object."""

    def __init__(self):
        self.db = Db()


class DbTableWidget(qtw.QWidget):
    """Database table widget."""

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        self._btn_widget = RadioButtonsWidget(self)
        self._btn_widget.add_buttons("projects", 0, "Projects")
        self._btn_widget.add_buttons("asset_types", 1, "Asset Types")
        self._btn_widget.add_buttons("task_types", 2, "Task Types")
        self._btn_widget.add_buttons("publish_types", 3, "Publish Types")

        self._project_widget = ProjectEditableWidget(self.app, self)
        self._project_widget.set_projects(self.app.db.projects())
        self._project_widget.hide()

        self._tbl_asset_type = AssetTypeTable(self.app, self)
        self._tbl_asset_type.set_asset_types(self.app.db.asset_types())
        self._tbl_asset_type.hide()

        self._tbl_task_type = TaskTypeTable(self.app, self)
        self._tbl_task_type.set_task_type(self.app.db.task_types())
        self._tbl_task_type.hide()

        self._tbl_publish_type = PublishTypeTable(self.app, self)
        self._tbl_publish_type.set_publish_types(self.app.db.publish_types())
        self._tbl_publish_type.hide()

        self._central_widget_by_name: dict[str, qtw.QWidget] = {
            "projects": self._project_widget,
            "asset_types": self._tbl_asset_type,
            "task_types": self._tbl_task_type,
            "publish_types": self._tbl_publish_type,
        }

        lay_main = qtw.QHBoxLayout(self)
        lay_main.addWidget(self._btn_widget)
        lay_main.addWidget(self._project_widget)
        lay_main.addWidget(self._tbl_asset_type)
        lay_main.addWidget(self._tbl_task_type)
        lay_main.addWidget(self._tbl_publish_type)

        # Connections
        self._btn_widget.ButtonPressed.connect(self._on_db_button_clicked)
        self._project_widget.ProjectEdited.connect(self._on_project_edited)

    def _on_db_button_clicked(self, widget_name):
        for name, db_widget in self._central_widget_by_name.items():
            if widget_name == name:
                db_widget.show()
                continue
            db_widget.hide()

    def _on_project_edited(self):
        self._project_widget.set_projects(self.app.db.projects())


class DbEntityTabWidget(qtw.QWidget):
    """Entity tab widget."""

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        self._cbx_project = qtw.QComboBox(self)
        self._project_model = ProjectListModel()
        self._project_model.set_projects(list(self.app.db.projects()))
        self._cbx_project.setModel(self._project_model)

        self._btn_asset = qtw.QPushButton("Asset")

        self._lsv_asset_type = qtw.QListView(self)
        self._asset_type_model = EntityListModel(AssetType)
        self._lsv_asset_type.setModel(self._asset_type_model)

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
        self._asset_type_model.set_entities(list(self.app.db.asset_types()))

    def _on_btn_asset_clicked(self):
        self._asset_type_model.set_entities(list(self.app.db.asset_types()))


class MainWindow(qtw.QMainWindow):
    """Database main window."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setWindowTitle("Asset Manager")
        self.setMinimumSize(800, 800)


        # Widgets
        self._db_widget = DbTableWidget(self.app, self)
        self._entity_widget = DbEntityTabWidget(self.app, self)

        self._tab_widget = qtw.QTabWidget(self)
        self._tab_widget.addTab(self._entity_widget, "Entity")
        self._tab_widget.addTab(self._db_widget, "Db")

        lay_main = qtw.QVBoxLayout(self)
        lay_main.addWidget(self._tab_widget)

        wgt_main = qtw.QWidget()
        self.setCentralWidget(wgt_main)
        wgt_main.setLayout(lay_main)


if __name__ == "__main__":
    qt_app = qtw.QApplication(sys.argv)
    tk_app = App()
    widget = MainWindow(tk_app)
    widget.show()
    qt_app.exec_()
