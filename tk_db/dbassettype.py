"""Database asset type module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_db.dbentity import DbEntity
from tk_db.models import AssetType


if TYPE_CHECKING:
    from tk_db.db import Db


class DbAssetType(DbEntity):
    """Database asset type object.

    Args:
        db (Db): Database object instance.
        asset_type (AssetType) AssetType model object.
    """

    def __init__(self, db: Db, asset_type: AssetType):
        super().__init__(asset_type)
        self.db = db

    @property
    def name(self) -> str:
        """Return asset type name."""
        return self._bc_entity.name

    def is_active(self) -> bool:
        """Get if project is active."""
        with self.db.Session() as session:
            project = session.query(AssetType).where(AssetType.id == self.id).first()
            active = project.active

        return active

    def set_active(self, value: bool):
        """Set project active or not."""
        with self.db.Session() as session:
            project = session.query(AssetType).where(AssetType.id == self.id).first()
            project.active = value
            session.commit()
