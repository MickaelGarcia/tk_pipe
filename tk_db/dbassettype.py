"""Database asset type module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tk_db.db import Db
    from tk_db.models import AssetType


class DbAssetType:
    """Database asset type object.

    Args:
        db (Db): Database object instance.
        asset_type (AssetType) AssetType model object.
    """

    def __init__(self, db: Db, asset_type: AssetType):
        self.db = db
        self._bc_asset_type = asset_type

    def __repr__(self):
        return f"DbAssetType({self.code} - {self.id})"

    @property
    def id(self) -> int:
        """Return asset type id."""
        return self._bc_asset_type.id

    @property
    def code(self) -> str:
        """Return asset type code."""
        return self._bc_asset_type.code

    @property
    def name(self) -> str:
        """Return asset type name."""
        return self._bc_asset_type.name

    def is_active(self) -> bool:
        """Get if project is active."""
        with self.db.Session() as session:
            project = session.query(AssetType).where(AssetType.id == self.id).first()
            active =  project.active

        return active

    def set_active(self, value: bool):
        """Set project active or not."""
        with self.db.Session() as session:
            project = session.query(AssetType).where(AssetType.id == self.id).first()
            project.active = value
            session.commit()
