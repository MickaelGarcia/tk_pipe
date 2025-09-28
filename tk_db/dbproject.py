"""Database project object module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from tk_db.dbasset import DbAsset
from tk_db.dbassettype import DbAssetType
from tk_db.errors import DbAssetAlreadyExistError
from tk_db.errors import MissingDbAssetError
from tk_db.models import Asset
from tk_db.models import AssetType
from tk_db.models import Project


if TYPE_CHECKING:

    from tk_db.db import Db


class DbProject:
    """Database project object.

    Args:
        db (Db): Instance of Database object.
        project (Project): Database project model.
    """

    def __init__(self, db: Db, project: Project):
        self.db = db
        self._bc_project = project

    def __repr__(self):
        return f"DbProject({self.code} - {self.id})"

    @property
    def id(self) -> int:
        """Return project id."""
        return self._bc_project.id

    @property
    def code(self) -> str:
        """Return project code."""
        return self._bc_project.code

    @property
    def name(self) -> str:
        """Return project name."""
        return self._bc_project.name

    @property
    def metadata(self) -> dict:
        """Return project metadata."""
        with self.db.Session() as session:
            project_q = session.query(Project).where(Project.code == self.code).first()

        return eval(project_q.metadata_)

    @metadata.setter
    def metadata(self, value: dict[str, Any]):
        """Set metadata to project.

        Args:
            value (dict[str, Any]): Project metadata like environment, root path ect.
        """
        assert isinstance(value, dict)
        with self.db.Session() as session:
            session.query(Project).where(Project.code == self.code).update(
                {"metadata_": str(value)}
            )
            session.commit()

    def metadata_update(self, value: dict):
        """Update project metadata.

        Args:
            value (dict[str, Any]): Project metadata like environment, root path ect.
        """
        assert isinstance(value, dict)
        updated = self.metadata.update(value)
        self.metadata = updated

    def asset(self, asset_type: DbAssetType, asset_code: str) -> DbAsset:
        """Get specific asset in project with given asset type and code.

        Args:
            asset_type (DbAssetType): Asset type of looking asset.
            asset_code (str): Asset code of looking asset.

        Raises:
            MissingDbAssetError: No asset with given asset type and code in project.

        Returns:
            DbAsset
        """
        with self.db.Session() as session:
            asset_query = session.query(Asset).join(Project).join(AssetType)
            found_asset = asset_query.filter(
                Project.id == self.id, AssetType.id == asset_type.id
            ).where(Asset.code == asset_code)
            found_asset = found_asset.first()

        if found_asset is None:
            raise MissingDbAssetError

        return DbAsset(found_asset, asset_type, self)

    def assets(self) -> list[DbAsset]:
        """Return assets in project."""
        assets = []
        with self.db.Session() as session:
            assets_query = session.query(Asset).join(Project)

            for asset in assets_query:
                asset_type_query = (
                    session.query(AssetType)
                    .where(AssetType.id == asset.asset_type_id)
                    .first()
                )
                asset_type = DbAssetType(self.db, asset_type_query)
                assets.append(DbAsset(asset, asset_type, self))

        return assets

    def get_or_create_asset(
        self,
        asset_code: str,
        asset_type: DbAssetType,
    ) -> DbAsset:
        """Create new asset in database related to given project.

        Args:
            asset_code (str): Asset code.
            asset_type (DbAssetType): Asset type of asset.

        Raises:
            DbAssetAlreadyExistError

        Returns:
            DbAsset
        """
        try:
            self.asset(asset_type, asset_code)
        except MissingDbAssetError:
            with self.db.Session() as session:
                asset_obj = Asset(
                    code=asset_code,
                    asset_type_id=asset_type.id,
                    project_id=self.id,
                )
                session.add(asset_obj)
                session.commit()
        else:
            raise DbAssetAlreadyExistError(
                f"Asset '{asset_type.code}_{asset_code}' "
                f"already exists in project {self.code!r}."
            )

        return self.asset(asset_type, asset_code)
