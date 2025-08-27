"""Asset object module."""

from __future__ import annotations

import os

from typing import TYPE_CHECKING

import tk_assert

from tk_am.tk_entity import TkEntity
from tk_am.tk_tasks import TkTask
from tk_const import am as c_am
from tk_error.am import MissingTkTaskError


if TYPE_CHECKING:
    from collections.abc import Iterator

    from tk_am.tk_asset_type import TkAssetType


class TkAsset(TkEntity):
    """Asset object."""

    def __init__(self, code: str, path: str, asset_type: TkAssetType):
        tk_assert.is_str(code)
        tk_assert.is_str(path)

        self.code = code
        self._path = path
        self.asset_type = asset_type
        self.project = self.asset_type.project

    def __repr__(self):
        return f"TkAsset({self.full_code}) - {self.asset_type}"

    @property
    def full_code(self):
        """Return asset full code."""
        return f"{self.asset_type.code}_{self.code}"

    def tasks(self) -> Iterator[TkTask]:
        """Yield asset tasks."""
        return (
            TkTask(d.name, d.path, self)
            for d in os.scandir(self.path)
            if c_am.task_code_grp_re.match(d.name)
        )

    def task(self, code:str):
        """Return TkTask with given code.

        Args:
            code (str): task code.

        Raises:
            MissingTkTaskError
        """
        for task in self.tasks():
            if task.code == code:
                return task

        raise MissingTkTaskError(f"No task found with given code {code!r}")

    def get_or_create_task(self, code: str) -> TkTask:
        """Get existing task, if task do not exist, create it.

        Args:
            code (str): Task code.
        """
        tk_assert.is_str(code)
        tk_assert.is_match(code, c_am.task_code_str)

        try:
            task = self.task(code)
        except MissingTkTaskError:
            task_path = os.path.join(self.path, code)
            os.mkdir(task_path)
            task = TkTask(code, task_path, self)

        return task
