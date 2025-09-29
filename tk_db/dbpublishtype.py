"""Database publish type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_db.dbentity import DbEntity
from tk_db.models import PublishType


if TYPE_CHECKING:
    from tk_db.db import Db


class DbPublishType(DbEntity):
    """Database publish type object.

    Args:
        db (Db): Database object.
        publish_type (PublishType): Publish type model object.
    """

    def __init__(self, db: Db, publish_type: PublishType):
        super().__init__(publish_type)
        self.db = db

    @property
    def file_type(self):
        """Return publish type code."""
        return self._bc_entity.file_type

    @property
    def extension(self):
        """Return publish type extension."""
        return self._bc_entity.extension

    def is_active(self) -> bool:
        """Return if publish is active or not."""
        with  self.db.Session() as session:
            publish = session.query(PublishType).where(PublishType.id == self.id).first()
            active = publish.active

        return active

    def set_active(self, value):
        """Set publish active or not."""
        with self.db.Session as session:
            publish = session.query(PublishType).where(PublishType.id == self.id).first()
            publish.active = value
            session.commit()
