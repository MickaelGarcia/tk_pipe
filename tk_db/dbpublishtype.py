"""Database publish type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tk_db.db import Db
    from tk_db.models import PublishType


class DbPublishType:
    """Database publish type object.

    Args:
        db (Db): Database object.
        publish_type (PublishType): Publish type model object.
    """

    def __init__(self, db: Db, publish_type: PublishType):
        self.db = db
        self._bc_publish_type = publish_type

    @property
    def id(self):
        """Return publish type id."""
        return self._bc_publish_type.id

    @property
    def code(self):
        """Return publish type description."""
        return self._bc_publish_type.code

    @property
    def file_type(self):
        """Return publish type code."""
        return self._bc_publish_type.file_type

    @property
    def extension(self):
        """Return publish type extension."""
        return self._bc_publish_type.extension

    @property
    def active(self) -> bool:
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
