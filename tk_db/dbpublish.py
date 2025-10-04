"""Database publish type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_db.dbentity import DbEntity
from tk_db.dbpublishtype import DbPublishType
from tk_db.models import Publish
from tk_db.models import PublishType


if TYPE_CHECKING:
    from tk_db.dbtask import DbTask


class DbPublish(DbEntity):
    """Database publish object.

    Args:
        task (Task): Database Task object.
        publish (Publish): Publish model object.
    """

    def __init__(self, task: DbTask, publish: Publish):
        super().__init__(publish)
        self.task = task

    @property
    def path(self) -> str:
        """Return publish type code."""
        return self._bc_entity.path

    @property
    def version(self) -> int:
        """Return publish type extension."""
        return self._bc_entity.version

    @property
    def version_name(self) -> str:
        """Return publish version as fancy name."""
        return f"{self.release[0]}{self.version:03d}"

    @property
    def publish_type(self) -> DbPublishType:
        """Return publish type object."""
        with self.task.asset.project.db.Session() as session:
            publish_type = (
                session.query(PublishType)
                .where(PublishType.id == self._bc_entity.publish_type_id)
                .first()
            )
            db_publish_type = DbPublishType(self.task.asset.project.db, publish_type)
        return db_publish_type

    @property
    def release(self) -> str:
        """Return if publish is release or work."""
        return self._bc_entity.release

    @property
    def size(self) -> float:
        """Return size of publish file."""
        return self._bc_entity.size

    @property
    def is_active(self) -> bool:
        """Return if publish is active or not."""
        with  self.task.asset.project.db.Session() as session:
            publish = session.query(Publish).where(Publish.id == self.id).first()
            active = publish.active

        return active

    def set_active(self, value):
        """Set publish active or not."""
        session_obj = self.task.asset.project.db.Session
        with session_obj() as session:
            publish = session.query(Publish).where(Publish.id == self.id).first()
            publish.active = value
            session.commit()
