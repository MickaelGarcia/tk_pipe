"""UI project module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from Qt import QtCore as qtc
from typing_extensions import override


if TYPE_CHECKING:
    from tk_db.dbproject import DbProject


ProjectRole = qtc.Qt.UserRole + 1
ProjectCodeRole = qtc.Qt.UserRole + 2


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
