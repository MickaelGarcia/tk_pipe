"""Entity object module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tk_am.tk_project import TkProject


class TkEntity:
    """Base class of AM entity.

    Properties:
        code (str); entity code.
        path (str): entity full path.
        project (TkProject): TkProject reference.
    """

    code: str
    _path: str
    project: TkProject


    @property
    def path(self) -> str:
        """Return entity path is file system."""
        return self._path

    @property
    def pattern_path(self):
        """Return project formated path."""
        split_path = self._path.split(self.project.code)[-1].split("\\")
        return f"/{self.project.code}{'/'.join(split_path)}"
