"""Asset type ui module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from Qt import QtCore as qtc
from Qt import QtGui as qtg
from Qt import QtWidgets as qtw
from typing_extensions import override

from tk_const import c_db
from tk_db.models import AssetType
from tk_db.models import PublishType
from tk_dbui.models import EntityTableModel


if TYPE_CHECKING:
    from tk_dbui.main_window import App


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
        btn_refresh = qtw.QPushButton("Refresh")

        lay_main = qtw.QVBoxLayout(self)
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(btn_add_asset_type)
        lay_btn.addWidget(btn_refresh)

        lay_main.addWidget(self._tbl_asset_type)
        lay_main.addLayout(lay_btn)

        btn_refresh.clicked.connect(self.refresh)
        btn_add_asset_type.clicked.connect(self._on_btn_add_clicked)

        self.refresh()

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
                qtw.QMessageBox.Ok
            )
            return

        entity = self._app.db.get_or_create_asset_type(dlg.code.text(), dlg.name.text())
        self._asset_type_model.add_entity(entity)

    def refresh(self):
        """Refresh ui content."""
        self._asset_type_model.set_entities(list(self._app.db.asset_types()))


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
                qtw.QMessageBox.Ok
            )
            return

        entity = self._app.db.get_or_create_task_type(dlg.code.text(), dlg.name.text())
        self._asset_type_model.add_entity(entity)

    @override
    def refresh(self):
        self._asset_type_model.set_entities(list(self._app.db.task_types()))


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
        self.extension.setText(".")


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
        btn_refresh = qtw.QPushButton("Refresh")

        lay_main = qtw.QVBoxLayout(self)
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(btn_add_publish_type)
        lay_btn.addWidget(btn_refresh)

        lay_main.addWidget(self._tbl_publish_type)
        lay_main.addLayout(lay_btn)

        btn_add_publish_type.clicked.connect(self._on_add_button_clicked)
        btn_refresh.clicked.connect(self.refresh)

        self.refresh()

    def refresh(self):
        """Refresh ui content."""
        self._publish_type_model.set_entities(list(self._app.db.publish_types()))

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
                qtw.QMessageBox.Ok
            )
            return

        entity = self._app.db.get_or_create_publish_type(
            code,
            file_type,
            extension,
        )
        self._publish_type_model.add_entity(entity)
