"""Database task type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tk_db.db import Db
    from tk_db.models import TaskType


class DbTaskType:
    """Database task type object.

    Args:
        db (Db): Database object.
        task (TaskType): Task type model object.
    """

    def __init__(self, db: Db, task: TaskType):
        self.db = db
        self._bc_task = task

    def __repr__(self):
        return f"TaskType({self.code} - {self.id})"

    @property
    def id(self):
        """Return task id."""
        return self._bc_task.id

    @property
    def code(self):
        """Return task code."""
        return self._bc_task.code

    @property
    def name(self):
        """Return task name."""
        return self._bc_task.name
