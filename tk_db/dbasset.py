"""Database asset object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_db.dbtask import DbTask
from tk_db.errors import MissingDbTaskError
from tk_db.models import Asset
from tk_db.models import Task
from tk_db.models import TaskType


if TYPE_CHECKING:
    from tk_db.dbassettype import DbAssetType
    from tk_db.dbproject import DbProject
    from tk_db.dbtasktype import DbTaskType


class DbAsset:
    """Database asset object.

    Args:
        asset (Asset): Database asset model.
        project (DbProject): DbProject object.
        asset_type (DbAssetType): Asset type of asset.
    """

    def __init__(
        self,
        asset: Asset,
        asset_type: DbAssetType,
        project: DbProject,
    ):
        self.project = project
        self.asset_type = asset_type
        self._bc_asset = asset

    def __repr__(self):
        return f"DbAsset({self.code} - {self.id})"

    @property
    def id(self) -> int:
        """Return asset id."""
        return self._bc_asset.id

    @property
    def code(self) -> str:
        """Return asset code."""
        return self._bc_asset.code

    def task(
        self, task_type: DbTaskType | None = None, code: str | None = None
    ) -> DbTask:
        """Get asset task type or code.

        Args:
            task_type (DbTaskType|None): Optional task type to found asset task.
            code (str|None): Optional task code to found asset task.

        Returns:
            DbTask

        Raises:
            ValueError: No task_type and code given
            MissingDbTaskError: No task found on asset with given code or type.
        """
        with self.project.db.Session() as session:
            if task_type is None and code is not None:
                task_type = (
                    session.query(TaskType)
                    .where(TaskType.code == code)
                    .first()
                )

            if task_type is None:
                raise ValueError("No code found from given task_type of code.")

            task_qr = session.query(Task).join(TaskType).join(Asset)
            task_filter = task_qr.filter(
                TaskType.id == task_type.id,
                Asset.id == self.id,
            )
            found_task = task_filter.first()

        if found_task is None:
            raise MissingDbTaskError(f"Unable to found task {code!r}")

        return DbTask(found_task, task_type, self)

    def tasks(self) -> list[DbTask]:
        """Get all tasks of asset.

        Returns:
            list[DbTask]
        """
        tasks = []
        with self.project.db.Session() as session:
            task_query = session.query(Task).where(Task.asset_id == self.id)
            for task in task_query:
                task_type = (
                    session.query(TaskType)
                    .where(TaskType.id == task.task_type_id)
                    .first()
                )
                tasks.append(DbTask(task, task_type, self))

        return tasks

    def get_or_create_task(
        self,
        task_type: DbTaskType | None = None,
        code: str | None = None,
    ) -> DbTask:
        """Create new task.

        Args:
            task_type (DbTaskType): Type of task to create.
            code (str): Task code of task to create.

        Returns:
            DbTask: Instance of database task.

        Raises:
            MissingDbTaskTypeError: Raised if given task type is missing.
        """
        if task_type is None and code is not None:
            task_type = self.project.db.task_type(code)

        try:
            self.task(task_type)
        except MissingDbTaskError:
            with self.project.db.Session() as session:
                task_obj = Task(
                    asset_id=self.id,
                    task_type_id=task_type.id,
                )
                session.add(task_obj)
                session.commit()

        return self.task(task_type)
