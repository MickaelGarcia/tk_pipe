"""UI models module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from Qt import QtCore as qtc
from typing_extensions import override


if TYPE_CHECKING:
    from tk_db.dbassettype import DbAssetType
    from tk_db.dbproject import DbProject

ASSET_TYPE_HEADER_TITLES = ["name", "code", "id"]


ProjectRole = qtc.Qt.UserRole + 1
ProjectCodeRole = qtc.Qt.UserRole + 2
AssetTypeRole = qtc.Qt.UserRole + 3


class ProjectListModel(qtc.QAbstractListModel):
    """Project list model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects: list[DbProject] = []

    @override
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._projects)

    @override
    def data(self, index, role=None) -> Any:
        project = self._projects[index.row()]
        if role == qtc.Qt.DisplayRole:
            return f"{project.name} ({project.code})"
        elif role == ProjectRole:
            return project
        elif role == ProjectCodeRole:
            return project.code

        return None

    def set_projects(self, projects: list[DbProject]):
        """Set projects to model."""
        self.beginResetModel()
        self._projects = projects.copy()
        self.endResetModel()

    def add_project(self, project: DbProject):
        """Add project in model."""
        self.beginInsertRows(
            qtc.QModelIndex(),
            len(self._projects),
            len(self._projects) + 1,
        )
        self._projects.append(project)
        self.endInsertRows()


class AssetTypeTableModel(qtc.QAbstractTableModel):
    """Asset type list model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._asset_types: list[DbAssetType] = []

    @override
    def rowCount(self, parent=...):
        return len(self._asset_types)

    @override
    def columnCount(self, parent=...):
        return len(ASSET_TYPE_HEADER_TITLES)

    @override
    def data(self, index, role=...):
        asset_type = self._asset_types[index.row()]
        colum = index.column()
        column_display_role = [
            asset_type.name,
            asset_type.code,
            asset_type.id,
        ]

        if role == qtc.Qt.DisplayRole:
            return column_display_role[colum]
        elif role == AssetTypeRole:
            return asset_type

        return None

    def set_asset_type(self, asset_types: list[DbAssetType]):
        """Set asset type to model."""
        self.beginResetModel()
        self._asset_types = asset_types
        self.endResetModel()

    def add_asset_type(self, asset_type: DbAssetType):
        """Add asset type in model."""
        self.beginInsertRows(
            qtc.QModelIndex(),
            len(self._asset_types),
            len(self._asset_types) + 1,
        )

        self._asset_types.append(asset_type)

        self.endInsertRows()
