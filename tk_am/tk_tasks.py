"""Tasks object module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tk_assert

from tk_am.tk_entity import TkEntity


if TYPE_CHECKING:
    from tk_am.tk_asset import TkAsset


class TkTask(TkEntity):
    """Task object."""

    def __init__(self, code: str, path: str, asset: TkAsset):
        tk_assert.is_str(code)
        tk_assert.is_str(path)

        self.code = code
        self._path = path
        self.asset = asset
        self.project = self.asset.project

    def __repr__(self):
        return f"TkTask({self.code}) - {self.asset}"
