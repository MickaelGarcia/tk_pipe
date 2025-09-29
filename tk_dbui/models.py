"""UI models module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from Qt import QtCore as qtc
from typing_extensions import override


if TYPE_CHECKING:
    from tk_db.dbentity import DbEntity
    from tk_db.dbproject import DbProject
    from tk_db.models import Base


PROJECT_HEADER_TITLES = ["Id", "Code", "Name", "Active"]
ASSET_TYPE_HEADER_TITLES = ["Id", "Name", "Code", "Active"]
PUBLISH_TYPE_HEADER_TITLES = ["Id", "Code", "File_type", "Extension", "Active"]

EntityRole = qtc.Qt.UserRole + 1
CodeRole = qtc.Qt.UserRole + 2
ActiveRole = qtc.Qt.UserRole + 3
ProjectRole = qtc.Qt.UserRole + 4
ProjectCodeRole = qtc.Qt.UserRole + 5


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
        elif role == ActiveRole:
            return project.is_active()

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


class EntityTableModel(qtc.QAbstractTableModel):
    """Asset type and task type table model."""

    def __init__(self, entity_type: type[Base], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entity_type = entity_type
        self._entities = []
        self._column_names = self._entity_type.__table__.columns.keys()

    @override
    def rowCount(self, parent=...):
        return len(self._entities)

    @override
    def columnCount(self, parent=...):
        return len(self._column_names)

    @override
    def data(self, index, role=...):
        entity = self._entities[index.row()]
        column = index.column()
        column_name = self._column_names[column]

        if role == qtc.Qt.DisplayRole and column_name != "active":
            return getattr(entity, column_name)
        elif role == EntityRole:
            return entity
        elif role == qtc.Qt.CheckStateRole and column_name == "active":
            return qtc.Qt.Checked if entity.is_active() else qtc.Qt.Unchecked

        return None

    @override
    def setData(self, index, value, role=...):
        asset_type = self._entities[index.row()]
        column = index.column()
        column_name = self._column_names[column]
        if role == qtc.Qt.CheckStateRole and column_name == "active":
            asset_type.set_active(bool(value))
            self.dataChanged.emit(index, index)
            return True

        return False

    @override
    def flags(self, index):
        flags = super().flags(index)
        col = index.column()

        if col == 3:
            flags |= qtc.Qt.ItemIsUserCheckable

        return flags

    @override
    def headerData(self, section, orientation, role=...):
        if role == qtc.Qt.DisplayRole:
            return self._column_names[section].capitalize()

        return None

    def set_entities(self, entities: list[DbEntity]):
        """Set asset type to model."""
        self.beginResetModel()
        self._entities = entities
        self.endResetModel()

    def add_entity(self, entity: DbEntity):
        """Add asset type in model."""
        self.beginInsertRows(
            qtc.QModelIndex(),
            len(self._entities),
            len(self._entities) + 1,
        )

        self._entities.append(entity)

        self.endInsertRows()


class EntityListModel(qtc.QAbstractListModel):
    """Asset type and task type list model."""

    def __init__(self, entity_type: type[Base], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entities: list[DbEntity] = []
        self._entity_type = entity_type
        self._column_names = self._entity_type.__table__.columns.keys()

    @override
    def rowCount(self, parent=...):
        return len(self._entities)

    @override
    def data(self, index, role=...):
        entity = self._entities[index.row()]

        if role == qtc.Qt.DisplayRole:
            return entity.name
        elif role == EntityRole:
            return entity

        return None

    def set_entities(self, entities: list[DbEntity]):
        """Set asset type to model."""
        self.beginResetModel()
        self._entities = entities
        self.endResetModel()

    def add_entity(self, entity: DbEntity):
        """Add asset type in model."""
        self.beginInsertRows(
            qtc.QModelIndex(),
            len(self._entities),
            len(self._entities) + 1,
        )

        self._entities.append(entity)

        self.endInsertRows()
