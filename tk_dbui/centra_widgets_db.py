"""Asset type ui module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from Qt import QtCore as qtc
from Qt import QtGui as qtg
from Qt import QtWidgets as qtw
from typing_extensions import override

from tk_const import c_db
from tk_dbui.models import AssetTaskTypeTableModel
from tk_dbui.models import CheckBoxDelegate
from tk_dbui.models import PublishTypeTableModel


if TYPE_CHECKING:
    from tk_dbui.main_window import App


class AssetTypeTable(qtw.QWidget):
    """Asset type table widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app

        self._tbl_asset_type = qtw.QTableView(self)
        self._tbl_asset_type.setItemDelegateForColumn(
            3, CheckBoxDelegate(self._tbl_asset_type)
        )
        self._tbl_asset_type.setEditTriggers(
            qtw.QAbstractItemView.EditTrigger.DoubleClicked
            | qtw.QAbstractItemView.EditTrigger.SelectedClicked
        )

        self._tbl_asset_type.verticalHeader().hide()
        self._asset_type_model = AssetTaskTypeTableModel()
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
        if not dlg.exec():
            return

        code = dlg.code.text()
        name = dlg.name.text()
        if not code or not name:
            return
        self._app.db.get_or_create_asset_type(dlg.code.text(), dlg.name.text())
        self.refresh()

    def refresh(self):
        """Refresh ui content."""
        self._asset_type_model.set_asset_type(list(self._app.db.asset_types()))


class TaskTypeTable(AssetTypeTable):
    """Task type table."""

    def _on_btn_add_clicked(self):
        dlg = AddAssetTaskTypeDialog(self)
        if not dlg.exec():
            return

        code = dlg.code.text()
        name = dlg.name.text()
        if not code or not name:
            return
        self._app.db.get_or_create_task_type(dlg.code.text(), dlg.name.text())
        self.refresh()

    @override
    def refresh(self):
        self._asset_type_model.set_asset_type(list(self._app.db.task_types()))


class AddAssetTaskTypeDialog(qtw.QDialog):
    """Dialog to add asset type."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Add asset type")

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


class PublishTypeTable(qtw.QWidget):
    """Publish type table widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app

        self._tbl_publish_type = qtw.QTableView(self)
        self._tbl_publish_type.verticalHeader().hide()
        self._publish_type_model = PublishTypeTableModel()
        self._tbl_publish_type.setModel(self._publish_type_model)

        btn_add_publish_type = qtw.QPushButton("Add")
        btn_refresh = qtw.QPushButton("Refresh")

        lay_main = qtw.QVBoxLayout(self)
        lay_btn = qtw.QHBoxLayout()

        lay_btn.addWidget(btn_add_publish_type)
        lay_btn.addWidget(btn_refresh)

        lay_main.addWidget(self._tbl_publish_type)
        lay_main.addLayout(lay_btn)

        btn_refresh.clicked.connect(self.refresh)

        self.refresh()

    def refresh(self):
        """Refresh ui content."""
        self._publish_type_model.set_publish_types(list(self._app.db.publish_types()))
