"""Asset type ui module."""

from __future__ import annotations

import json

from typing import TYPE_CHECKING

from Qt import QtCore as qtc
from Qt import QtGui as qtg
from Qt import QtWidgets as qtw

from tk_const import c_db
from tk_db.models import AssetType
from tk_db.models import Project
from tk_db.models import PublishType
from tk_dbui.models import EntityListModel
from tk_dbui.models import EntityRole
from tk_dbui.models import EntityTableModel


if TYPE_CHECKING:
    from tk_db.dbassettype import DbAssetType
    from tk_db.dbproject import DbProject
    from tk_db.dbpublishtype import DbPublishType
    from tk_db.dbtasktype import DbTaskType
    from tk_dbui.main_window import App


class ProjectEditableWidget(qtw.QWidget):
    """Project based widget to view project list and edit metadata."""

    ProjectEdited = qtc.Signal()

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app

        # Widgets
        self._lst_projects = qtw.QListView(self)
        self._project_model = EntityListModel(Project)
        self._lst_projects.setModel(self._project_model)
        btn_add_project = qtw.QPushButton("Add")

        self._btn_locked = qtw.QPushButton("Locked")
        self._btn_locked.setCheckable(True)
        self._btn_locked.setChecked(True)

        self._cbx_active = qtw.QCheckBox(self)
        self._cbx_active.setEnabled(False)

        self._lne_project_code = qtw.QLineEdit(self)
        self._lne_project_code.setEnabled(False)

        self._lne_project_name = qtw.QLineEdit(self)
        self._lne_project_name.setEnabled(False)

        self._txt_metadata = qtw.QTextEdit(self)
        self._txt_metadata.setEnabled(False)

        self._btn_save = qtw.QPushButton("Save")
        self._btn_save.setEnabled(False)

        self._btn_undo = qtw.QPushButton("Cancel edit")
        self._btn_undo.setEnabled(False)

        # Layout
        lay_main = qtw.QHBoxLayout(self)

        lay_projects_list = qtw.QVBoxLayout()

        lay_property = qtw.QVBoxLayout()
        lay_lines_prop = qtw.QFormLayout()
        lay_btn_prop = qtw.QHBoxLayout()

        lay_projects_list.addWidget(self._lst_projects)
        lay_projects_list.addWidget(btn_add_project)

        lay_lines_prop.addRow("Active:", self._cbx_active)
        lay_lines_prop.addRow("Code:", self._lne_project_code)
        lay_lines_prop.addRow("Display Name:", self._lne_project_name)

        lay_btn_prop.addWidget(self._btn_save)
        lay_btn_prop.addWidget(self._btn_undo)

        lay_main.addLayout(lay_projects_list)

        lay_property.addWidget(self._btn_locked)
        lay_property.addLayout(lay_lines_prop)
        lay_property.addWidget(self._txt_metadata)
        lay_property.addLayout(lay_btn_prop)

        lay_main.addLayout(lay_projects_list)
        lay_main.addLayout(lay_property)

        # Connections
        self._btn_locked.clicked.connect(self._on_btn_locked_clicked)
        self._lst_projects.clicked.connect(self._on_project_selected)
        self._btn_undo.clicked.connect(self._on_btn_cancel_clicked)
        self._btn_save.clicked.connect(self._on_btn_save_clicked)
        btn_add_project.clicked.connect(self._on_btn_add_clicked)

        # Initialisation

    def set_projects(self, projects: list[DbProject]):
        """Set projects list to model."""
        current_index = self._lst_projects.currentIndex()

        self._project_model.set_entities(projects)

        if current_index.isValid():
            self._lst_projects.setCurrentIndex(current_index)

    def _on_btn_locked_clicked(self):
        current_index = self._lst_projects.currentIndex()
        if not current_index.isValid():
            self._btn_locked.setChecked(True)
            return

        value = not self._btn_locked.isChecked()
        self._cbx_active.setEnabled(value)
        self._lne_project_code.setEnabled(value)
        self._lne_project_name.setEnabled(value)
        self._txt_metadata.setEnabled(value)
        self._btn_save.setEnabled(value)
        self._btn_undo.setEnabled(value)
        if not value:
            self._on_btn_cancel_clicked()

    def _on_project_selected(self, index: qtc.QModelIndex):
        if not index.isValid():
            return
        project: DbProject = self._lst_projects.model().data(index, role=EntityRole)
        self._cbx_active.setChecked(project.is_active())
        self._lne_project_code.setText(project.code)
        self._lne_project_name.setText(project.name)
        metadata = project.metadata.copy()
        self._txt_metadata.setText(json.dumps(metadata, indent=4))

        if self._btn_locked.isChecked():
            return

        self._btn_locked.setChecked(True)
        self._cbx_active.setEnabled(False)
        self._lne_project_code.setEnabled(False)
        self._lne_project_name.setEnabled(False)
        self._txt_metadata.setEnabled(False)
        self._btn_save.setEnabled(False)
        self._btn_undo.setEnabled(False)

    def _on_btn_cancel_clicked(self):
        index = self._lst_projects.currentIndex()
        self._on_project_selected(index)

    def _on_btn_save_clicked(self):
        code = self._lne_project_code.text()
        name = self._lne_project_name.text()
        metadata_text = self._txt_metadata.toPlainText()
        if not metadata_text:
            return

        metadata = eval(metadata_text)

        project = self._lst_projects.model().data(
            self._lst_projects.currentIndex(), role=EntityRole
        )
        project.metadata = metadata
        project.code = code
        project.name = name
        self.ProjectEdited.emit()

    def _on_btn_add_clicked(self):
        dlg = AddProjectDialog()

        if not dlg.exec():
            return

        code = dlg.code.text()
        name = dlg.name.text()
        if not code or not name:
            return

        if self._project_model.get_entity(code):
            qtw.QMessageBox.critical(
                self,
                "Project already exists",
                f"Project {code!r} already exists in database.",
                qtw.QMessageBox.Ok,
            )
            return

        project = self._app.db.create_project(code, name)
        self._project_model.add_project(project)


class AssetTypeTable(qtw.QWidget):
    """Asset type table widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app

        self._tbl_asset_type = qtw.QTableView(self)
        self._tbl_asset_type.verticalHeader().hide()
        self._asset_type_model = EntityTableModel(AssetType)
        self._tbl_asset_type.setModel(self._asset_type_model)

        btn_add_asset_type = qtw.QPushButton("Add")

        lay_main = qtw.QVBoxLayout(self)
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(btn_add_asset_type)

        lay_main.addWidget(self._tbl_asset_type)
        lay_main.addLayout(lay_btn)

        btn_add_asset_type.clicked.connect(self._on_btn_add_clicked)

    def set_asset_types(self, asset_types: list[DbAssetType]):
        """Set asset types in model."""
        self._asset_type_model.set_entities(asset_types)

    def _on_btn_add_clicked(self):
        dlg = AddAssetTaskTypeDialog(self)
        dlg.setWindowTitle("Add asset type")

        if not dlg.exec():
            return

        code = dlg.code.text()
        name = dlg.name.text()
        if not code or not name:
            return

        if self._asset_type_model.get_entity(code):
            qtw.QMessageBox.critical(
                self,
                "Asset type already exists",
                f"Asset type {code!r} already exists in database.",
                qtw.QMessageBox.Ok,
            )
            return

        entity = self._app.db.get_or_create_asset_type(dlg.code.text(), dlg.name.text())
        self._asset_type_model.add_entity(entity)


class TaskTypeTable(AssetTypeTable):
    """Task type table."""

    def _on_btn_add_clicked(self):
        dlg = AddAssetTaskTypeDialog(self)
        dlg.setWindowTitle("Add task type")

        if not dlg.exec():
            return

        code = dlg.code.text()
        name = dlg.name.text()
        if not code or not name:
            return

        if self._asset_type_model.get_entity(code):
            qtw.QMessageBox.critical(
                self,
                "Task type already exists",
                f"Task type {code!r} already exists in database.",
                qtw.QMessageBox.Ok,
            )
            return

        entity = self._app.db.get_or_create_task_type(dlg.code.text(), dlg.name.text())
        self._asset_type_model.add_entity(entity)

    def set_task_type(self, task_type: list[DbTaskType]):
        """Set asset types in model."""
        self._asset_type_model.set_entities(task_type)


class PublishTypeTable(qtw.QWidget):
    """Publish type table widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app

        self._tbl_publish_type = qtw.QTableView(self)
        self._tbl_publish_type.verticalHeader().hide()
        self._publish_type_model = EntityTableModel(PublishType)
        self._tbl_publish_type.setModel(self._publish_type_model)

        btn_add_publish_type = qtw.QPushButton("Add")

        lay_main = qtw.QVBoxLayout(self)
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(btn_add_publish_type)

        lay_main.addWidget(self._tbl_publish_type)
        lay_main.addLayout(lay_btn)

        btn_add_publish_type.clicked.connect(self._on_add_button_clicked)

    def set_publish_types(self, publish_types: list[DbPublishType]):
        """Set publish types in model."""
        self._publish_type_model.set_entities(publish_types)

    def _on_add_button_clicked(self):
        dlg = AddPublishTypeDialog(self)
        dlg.setWindowTitle("Add publish type")

        if not dlg.exec():
            return

        code = dlg.code.text()
        file_type = dlg.file_type.text()
        extension = dlg.extension.text()
        if not code or not file_type or not extension:
            return

        if self._publish_type_model.get_entity(code):
            qtw.QMessageBox.critical(
                self,
                "Publish type already exists",
                f"Publish type {code!r} already exists in database.",
                qtw.QMessageBox.Ok,
            )
            return

        entity = self._app.db.get_or_create_publish_type(
            code,
            file_type,
            extension,
        )
        self._publish_type_model.add_entity(entity)


class AddProjectDialog(qtw.QDialog):
    """Dialog to add project."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Add Project")

        # Widgets
        self.code = qtw.QLineEdit()
        project_code_re = qtc.QRegExp(c_db.project_code_str)
        code_validator = qtg.QRegExpValidator(project_code_re)
        self.code.setValidator(code_validator)

        self.name = qtw.QLineEdit()
        project_name_re = qtc.QRegExp("[a-zA-Z].+")
        name_validator = qtg.QRegExpValidator(project_name_re)
        self.name.setValidator(name_validator)

        btn_ok = qtw.QPushButton("Ok")
        btn_cancel = qtw.QPushButton("Cancel")

        # Layout
        lay_main = qtw.QVBoxLayout(self)
        lay_lines = qtw.QFormLayout()

        lay_lines.addRow("Code:", self.code)
        lay_lines.addRow("Name:", self.name)

        lay_btn = qtw.QHBoxLayout()
        lay_btn.addStretch()
        lay_btn.addWidget(btn_ok)
        lay_btn.addWidget(btn_cancel)

        lay_main.addLayout(lay_lines)
        lay_main.addLayout(lay_btn)

        # Connections
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)


class AddAssetTaskTypeDialog(qtw.QDialog):
    """Dialog to add asset type."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Widgets
        self.code = qtw.QLineEdit()
        asset_type_code_re = qtc.QRegExp(c_db.asset_type_code_str)
        code_validator = qtg.QRegExpValidator(asset_type_code_re)
        self.code.setValidator(code_validator)

        self.name = qtw.QLineEdit()
        asset_type_name_re = qtc.QRegExp("[a-z]+")
        name_validator = qtg.QRegExpValidator(asset_type_name_re)
        self.name.setValidator(name_validator)

        btn_ok = qtw.QPushButton("Ok")
        btn_cancel = qtw.QPushButton("Cancel")

        # Layout
        lay_main = qtw.QVBoxLayout(self)
        lay_lines = qtw.QFormLayout()

        lay_lines.addRow("Code:", self.code)
        lay_lines.addRow("Name:", self.name)

        lay_btn = qtw.QHBoxLayout()
        lay_btn.addStretch()
        lay_btn.addWidget(btn_ok)
        lay_btn.addWidget(btn_cancel)

        lay_main.addLayout(lay_lines)
        lay_main.addLayout(lay_btn)

        # Connections
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)


class AddPublishTypeDialog(qtw.QDialog):
    """Dialog to add publish type."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Add Publish type")

        # Widgets
        self.code = qtw.QLineEdit()
        publish_type_code_re = qtc.QRegExp(r"[a-z]+(?:_[a-z]+)*")
        publish_type_code_validator = qtg.QRegExpValidator(publish_type_code_re)
        self.code.setValidator(publish_type_code_validator)

        self.file_type = qtw.QLineEdit()
        file_desc_re = qtc.QRegExp(c_db.file_desc_grp)
        file_desc_validator = qtg.QRegExpValidator(file_desc_re)
        self.file_type.setValidator(file_desc_validator)

        self.extension = qtw.QLineEdit()
        extension_re = qtc.QRegExp(r"\.\w+")
        extension_validator = qtg.QRegExpValidator(extension_re)
        self.extension.setValidator(extension_validator)

        btn_ok = qtw.QPushButton("Ok")
        btn_cancel = qtw.QPushButton("Cancel")

        # Layout
        lay_main = qtw.QVBoxLayout(self)
        lay_lines = qtw.QFormLayout()

        lay_lines.addRow("Code:", self.code)
        lay_lines.addRow("File type:", self.file_type)
        lay_lines.addRow("Extension:", self.extension)

        lay_btn = qtw.QHBoxLayout()
        lay_btn.addStretch()
        lay_btn.addWidget(btn_ok)
        lay_btn.addWidget(btn_cancel)

        lay_main.addLayout(lay_lines)
        lay_main.addLayout(lay_btn)

        # Connections
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
