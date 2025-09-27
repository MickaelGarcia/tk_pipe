"""Database publish type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_db.models import Publish


if TYPE_CHECKING:
    from tk_db.dbtask import DbTask


class DbPublish:
    """Database publish object.

    Args:
        task (Task): Database Task object.
        publish (Publish): Publish model object.
    """

    def __init__(self, task: DbTask, publish: Publish):
        self.task = task
        self._bc_publish = publish

    @property
    def id(self):
        """Return publish type id."""
        return self._bc_publish.id

    @property
    def code(self):
        """Return publish type description."""
        return self._bc_publish.code

    @property
    def path(self):
        """Return publish type code."""
        return self._bc_publish.path

    @property
    def version(self):
        """Return publish type extension."""
        return self._bc_publish.version

    @property
    def release(self):
        """Return if publish is release or work."""
        return self._bc_publish.release

    @property
    def size(self):
        """Return size of publish file."""
        return self._bc_publish.size

    @property
    def active(self):
        """Return if publish is active or not."""
        session_obj = self.task.asset.project.db.Session
        with session_obj() as session:
            publish = session.query(Publish).where(Publish.id == self.id).first()
            return publish.active

    def set_active(self, value):
        """Set publish active or not."""
        session_obj = self.task.asset.project.db.Session
        with session_obj() as session:
            publish = session.query(Publish).where(Publish.id == self.id).first()
            publish.active = value
            session.commit()
