"""Database object module."""

from __future__ import annotations

import os

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tk_db.dbassettype import DbAssetType
from tk_db.dbproject import DbProject
from tk_db.errors import DbAssetTypeAlreadyExistsError
from tk_db.errors import DbProjectAlreadyExistsError
from tk_db.errors import MissingDbAssetTypeError
from tk_db.errors import MissingDbProjectError
from tk_db.models import AssetType
from tk_db.models import Project


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class Db:
    """Database object."""

    _db_path = f"sqlite:///{os.path.dirname(__file__)}/test_alchemy.db"

    def __init__(self):
        self._engine = create_engine(self._db_path)

    def __repr__(self):
        return f"Db({self._db_path})"

    def session(self) -> Session:
        """Return database session."""
        session = sessionmaker(bind=self._engine)()
        return session

    def project(self, code: str) -> DbProject:
        """Get Database project from his code.

        Args:
            code (str): Project code.

        Returns:
            Project: Instance of database project.

        Raises:
            MissingDbProjectError: Given project code not found in database.
        """
        session = sessionmaker(bind=self._engine)()
        project_query = session.query(Project).where(Project.code == code)
        found_project = project_query.first()

        if found_project is None:
            raise MissingDbProjectError

        return DbProject(self, found_project)

    def create_project(self, code: str, name: str) -> DbProject:
        """Create new project in database project table.

        If given code:name already exist in database, return it.

        Args:
            code (str): Project code.
            name (str): Project name.

        Raises:
            DbProjectAlreadyExistsError

        Returns:
            DbProject
        """
        session = sessionmaker(bind=self._engine)()
        try:
            self.project(code)
        except MissingDbProjectError:
            project_obj = Project(code=code, name=name)

            session.add(project_obj)
            session.commit()
        else:
            raise DbProjectAlreadyExistsError(
                f"Project {code!r} - {name!r} already exist."
            )

        return DbProject(self, project_obj)

    def asset_type(self, code: str) -> DbAssetType:
        """Get database asset type from his code.

        Args:
            code (str): Asset type code

        Returns:
            DbAssetType: Instance of database asset type.

        Raises:
            MissingDbAssetTypeError: Given asset type code not found in database.
        """
        session = sessionmaker(bind=self._engine)()
        asset_type_query = session.query(AssetType).where(AssetType.code == code)
        found_asset_type = asset_type_query.first()

        if found_asset_type is None:
            raise MissingDbAssetTypeError

        return DbAssetType(self, found_asset_type)

    def create_asset_type(self, code: str, name: str) -> DbAssetType:
        """Create new asset type in database asset_type table.

        If given code:name already exist in database, return it.

        Args:
            code (str): Asset type code.
            name (str): Asset type name.

        Returns:
            DbAssetType
        """
        session = sessionmaker(bind=self._engine)()
        try:
            self.asset_type(code)
        except MissingDbAssetTypeError:
            asset_type_obj = AssetType(code=code, name=name)
            session.add(asset_type_obj)
            session.commit()

        else:
            raise DbAssetTypeAlreadyExistsError(
                f"Asset type {code!r} - {name!r} already exists."
            )


        return asset_type_obj
