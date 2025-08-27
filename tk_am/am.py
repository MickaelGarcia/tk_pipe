"""Base asset manager module."""

from __future__ import annotations

import json
import os

from pathlib import Path
from typing import TYPE_CHECKING

from typing_extensions import Any

import tk_assert

from tk_am.tk_project import TkProject
from tk_am.tk_publish_type import TkPublishType
from tk_const.am import project_code_str
from tk_error.am import MissingTkProjectError
from tk_error.am import MissingTkPublishTypeError


if TYPE_CHECKING:
    from collections.abc import Iterator


BASE_META = {
    "projects": {},
    "publish_types": {
        "cache_abc": ("cache", ".abc"),
        "image_png": ("img", ".png"),
        "image_sequence_png": ("iseq", ".png"),
        "maya_scene_mb": ("scn", ".mb"),
        "maya_scene_ma": ("scn", ".ma"),
        "scene_fbx": ("cache", ".fbx"),
        "file_json": ("file", ".json"),
    },
    "users": {},
}


class Am:
    """Asset manager object."""

    def __init__(self):
        home = Path.home()
        self._meta_path = os.path.join(home, ".config", "tk_config", "tk_am.meta")
        os.makedirs(os.path.dirname(self._meta_path), exist_ok=True)

        if not os.path.isfile(self._meta_path):
            self._data = BASE_META
            self._save_meta()
            return

        self._data = self._get_meta()

    @property
    def _projects(self) -> dict[str, dict]:
        return self._data["projects"]

    @property
    def publish_types_meta(self):
        """Return publish type meta."""
        return self._data["publish_types"]

    @property
    def _users(self):
        return self._data["users"]

    def _save_meta(self):
        with open(self._meta_path, "w") as f:
            json.dump(self._data, f)

    def _get_meta(self) -> dict[str, Any]:
        with open(self._meta_path) as f:
            data = json.load(f)
        return data

    def update_meta(self, key: str, value: Any):
        """Update metadata from key/value and save meta file."""
        self._data[key].update(value)
        self._save_meta()

    def project(self, code: str) -> TkProject:
        """Get existing project in Am."""
        meta_project = self._projects.get(code)
        if not meta_project:
            raise MissingTkProjectError

        return TkProject.from_dict(meta_project, self)

    def projects(self) -> Iterator:
        """Get all tk project in AM."""
        for project_meta in self._projects.values():
            yield TkProject.from_dict(project_meta, self)

    def get_or_create_project(self, code: str, name: str, path: str) -> TkProject:
        """Create new project from given project code, name at given path.

        Args:
            code (str): Project code, should be in UPPERCASE.
            name (str): Name of project, used for display.
            path (str): Root of project path without project code directory.

        Returns:
            TkProject: Project object instance.
        """
        tk_assert.is_str(code)
        tk_assert.is_match(code, project_code_str)

        tk_assert.is_str(name)
        tk_assert.is_str(path)
        tk_assert.is_path(path)

        project_path = os.path.join(path, code)

        try:
            project = self.project(code)
        except MissingTkProjectError:
            os.makedirs(project_path, exist_ok=True)
            project = TkProject(code, name, path, self)
            self.update_meta("projects", {project.code: project.to_dict()})

        return project

    def publish_type(self, code):
        """Get TkPublishType from meta."""
        meta_pt = self.publish_types_meta.get(code)
        if not meta_pt:
            raise MissingTkPublishTypeError(f"No publish type {code!r} in AM")

        return TkPublishType(code, self)

    def publish_types(self) -> Iterator[TkPublishType]:
        """Get TkPublishType list form meta."""
        for code in  self.publish_types_meta.values():
            yield TkPublishType(code, self)

    def create_publish_type(self, code: str, desc: str, ext: str) -> TkPublishType:
        """Create new publish type."""
        tk_assert.is_str(code)
        tk_assert.is_str(desc)
        tk_assert.is_str(ext)
        tk_assert.is_match(code, r"[a-z]+(?:_[a-z]+)*")
        tk_assert.is_match(desc, r"[a-z]+")
        tk_assert.is_match(ext, r"\.[a-zA-Z0-9]+")

        try:
            tk_publish_type = self.publish_type(code)
        except MissingTkPublishTypeError:
            self.update_meta("publish_type", {code: (desc, ext)})
            tk_publish_type = TkPublishType(code, self)

        return tk_publish_type
