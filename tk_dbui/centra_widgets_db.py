"""Asset type ui module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from Qt import QtWidgets as qtw
from typing_extensions import override

from tk_dbui.models import AssetTaskTypeTableModel
from tk_dbui.models import PublishTypeTableModel


if TYPE_CHECKING:
    from tk_dbui.main_window import App


class AssetTypeTable(qtw.QWidget):
    """Asset type table widget."""

    def __init__(self, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app

        self._tbl_asset_type = qtw.QTableView(self)
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

        self.refresh()

    def _on_btn_add_clicked(self):
        print("Add asset type")

    def refresh(self):
        """Refresh ui content."""
        self._asset_type_model.set_asset_type(list(self._app.db.asset_types()))


class TaskTypeTable(AssetTypeTable):
    """Task type table."""

    @override
    def refresh(self):
        self._asset_type_model.set_asset_type(list(self._app.db.task_types()))


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

    def _on_btn_add_clicked(self):
        print("Add asset type")

    def refresh(self):
        """Refresh ui content."""
        self._publish_type_model.set_publish_types(list(self._app.db.publish_types()))
