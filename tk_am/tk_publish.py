"""Publish object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tk_am.tk_entity import TkEntity



if TYPE_CHECKING:
    from tk_am.tk_tasks import TkTask
    from tk_am.tk_publish_type import TkPublishType
    from tk_const.am import ReleaseType


class TkPublish(TkEntity):
    """Publish object."""

    def __init__(
        self,
        code: str,
        path: str,
        publish_type: TkPublishType,
        task: TkTask,
        release: ReleaseType,
        version: int,
    ):
        self.code = code
        self._path = path
        self.publish_type = publish_type
        self.task = task
        self.project = task.project
        self.release = release
        self._version = version

    def __repr__(self):
        return (
            f"TkPublish({self.code}_{self.version_code}"
            f"_{self.publish_type.code}) - {self.task}"
        )

    @property
    def version_number(self) -> int:
        """Return version number."""
        return self._version

    @property
    def version_code(self) -> str:
        """Return version code."""
        return f"{self.release.value[0]}{self._version:03d}"
