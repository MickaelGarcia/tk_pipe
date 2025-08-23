"""Asset type object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tk_assert

from tk_am.tk_entity import TkEntity


if TYPE_CHECKING:
    from tk_am import TkProject


class TkAssetType(TkEntity):
    """Asset type object."""

    def __init__(self, code: str, path: str, project: TkProject):
        tk_assert.is_str(code)
        tk_assert.is_str(path)

        self.code = code
        self._path = path
        self.project = project

    def __repr__(self):
        return f"TkAssetType({self.code}) - {self.project}"
