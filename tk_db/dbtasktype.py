"""Database task type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_db.dbentity import DbEntity
from tk_db.models import TaskType


if TYPE_CHECKING:
    from tk_db.db import Db


class DbTaskType(DbEntity):
    """Database task type object.

    Args:
        db (Db): Database object.
        task (TaskType): Task type model object.
    """

    def __init__(self, db: Db, task: TaskType):
        super().__init__(task)
        self.db = db

    @property
    def name(self):
        """Return task name."""
        return self._bc_entity.name

    def is_active(self) -> bool:
        """Return if publish is active or not."""
        with  self.db.Session() as session:
            publish = session.query(TaskType).where(TaskType.id == self.id).first()
            active = publish.active

        return active

    def set_active(self, value):
        """Set publish active or not."""
        with self.db.Session as session:
            publish = session.query(TaskType).where(TaskType.id == self.id).first()
            publish.active = value
            session.commit()
