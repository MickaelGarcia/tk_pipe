"""Database object module."""

from __future__ import annotations

import os

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tk_db.dbassettype import DbAssetType
from tk_db.dbproject import DbProject
from tk_db.dbtasktype import DbTaskType
from tk_db.errors import DbAssetTypeAlreadyExistsError
from tk_db.errors import DbProjectAlreadyExistsError
from tk_db.errors import DbTaskTypeAlreadyExistError
from tk_db.errors import MissingDbAssetTypeError
from tk_db.errors import MissingDbProjectError
from tk_db.errors import MissingDbTaskTypeError
from tk_db.models import AssetType
from tk_db.models import Base
from tk_db.models import Project
from tk_db.models import TaskType


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class Db:
    """Database object."""

    _db_path = f"sqlite:///{os.path.dirname(__file__)}/test_alchemy.db"

    def __init__(self):
        engine = create_engine(self._db_path)
        Base.metadata.create_all(bind=engine)

    def __repr__(self):
        return f"Db({self._db_path})"

    def session(self) -> Session:
        """Return database session."""
        engine = create_engine(self._db_path)
        session = sessionmaker(bind=engine)()
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
        session = self.session()
        project_query = session.query(Project).where(Project.code == code)
        found_project = project_query.first()

        if found_project is None:
            raise MissingDbProjectError(f"Unable to found project with code: {code!r}")

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
        session = self.session()
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

        return self.project(code)

    def asset_type(self, code: str) -> DbAssetType:
        """Get database asset type from his code.

        Args:
            code (str): Asset type code

        Returns:
            DbAssetType: Instance of database asset type.

        Raises:
            MissingDbAssetTypeError: Given asset type code not found in database.
        """
        session = self.session()
        asset_type_query = session.query(AssetType).where(AssetType.code == code)
        found_asset_type = asset_type_query.first()

        if found_asset_type is None:
            raise MissingDbAssetTypeError(
                f"Unable to found asset type with code {code!r}"
            )

        return DbAssetType(self, found_asset_type)

    def get_or_create_asset_type(self, code: str, name: str) -> DbAssetType:
        """Create new asset type in database asset_type table.

        If given code:name already exist in database, return it.

        Args:
            code (str): Asset type code.
            name (str): Asset type name.

        Returns:
            DbAssetType
        """
        session = self.session()
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

        return self.asset_type(code)

    def task_type(self, code: str) -> DbTaskType:
        """Get task type object.

        Args:
            code (str): Task type code.

        Returns:
            DbTaskType: Instance of database asset type.

        Raises:
            MissingDbTaskTypeError: Given task type code not found in database.
        """
        session = self.session()
        task_type_query = session.query(TaskType).where(TaskType.code == code)
        found_task_type = task_type_query.first()

        if found_task_type is None:
            raise MissingDbTaskTypeError(f"Unable to found task type with code {code!r}")

        return DbTaskType(self, found_task_type)

    def task_types(self):
        """Return all task types table."""
        session = self.session()
        tasks_query = session.query(TaskType)
        for task in tasks_query:
            yield DbTaskType(self, task)

    def get_or_create_task_type(self, code: str, name: str) -> DbTaskType:
        """Create new task type in database.

        Args:
            code (str): Task type code.
            name (str): Task type name.

        Raises:
            DbTaskTypeAlreadyExistError

        Returns:
            DbTaskType
        """
        session = self.session()
        try:
            self.task_type(code)
        except MissingDbTaskTypeError:
            task_type_obj = TaskType(code=code, name=name)
            session.add(task_type_obj)
            session.commit()

        else:
            raise DbTaskTypeAlreadyExistError(
                f"Task type {code!r} - {name!r} already exists."
            )

        return self.task_type(code)
