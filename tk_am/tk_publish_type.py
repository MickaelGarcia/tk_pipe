"""Publish type module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tk_assert

from tk_error.am import MissingTkPublishTypeError


if TYPE_CHECKING:
    from tk_am.am import Am

publish_desc_ext_by_code = {
    "cache_abc": ("cache", ".abc"),
    "image_png": ("img", ".png"),
    "image_sequence_png": ("iseq", ".png"),
    "maya_scene_mb": ("scn", ".mb"),
    "maya_scene_ma": ("scn", ".ma"),
    "scene_fbx": ("cache", ".fbx"),
    "file_json": ("file", ".json"),
}

publish_code_by_desc_ext = {
    value: key for key, value in publish_desc_ext_by_code.items()
}


class TkPublishType:
    """PublishType object."""

    def __init__(self, code: str, am: Am):
        tk_assert.is_str(code)
        tk_assert.is_match(code, r"^[a-z]+(?:_[a-z]+)*$")

        self.code = code
        self.am = am

        publish_type_info = self.am.publish_types_meta.get(code)

        if not publish_type_info:
            raise MissingTkPublishTypeError(f"File type {code!r} is not managed.")
        self.desc, self.ext = publish_type_info
