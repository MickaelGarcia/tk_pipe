"""Database asset object module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tk_db.dbassettype import DbAssetType
    from tk_db.dbproject import DbProject
    from tk_db.models import Asset


class DbAsset:
    """Database asset object.

    Args:
        asset (Asset): Database asset model.
        project (DbProject): DbProject object.
        asset_type (DbAssetType): Asset type of asset.
    """

    def __init__(self, asset: Asset, asset_type: DbAssetType, project: DbProject):
        self.project = project
        self.asset_type = asset_type
        self._bc_asset = asset

    def __repr__(self):
        return f"DbAsset({self.code} - {self.id})"

    @property
    def id(self):
        """Return asset id."""
        return self._bc_asset.id

    @property
    def code(self):
        """Return asset code."""
        return self._bc_asset.code
