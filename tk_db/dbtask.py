"""Database task object module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tk_db.dbasset import DbAsset
    from tk_db.dbtasktype import DbTaskType
    from tk_db.models import Task


class DbTask:
    """Database task object."""

    def __init__(self, task: Task, task_type: DbTaskType, asset: DbAsset):
        self.asset = asset
        self.task_type = task_type
        self._bc_task = task

    def __repr__(self):
        return f"DbTask({self.asset.code} - {self.name} - {self.id})"

    @property
    def id(self):
        """Return task id."""
        return self._bc_task.id

    @property
    def code(self):
        """Return task type code."""
        return self.task_type.code

    @property
    def name(self):
        """Return task type name."""
        return self.task_type.name
