"""Project object module."""

from __future__ import annotations

import json
import os

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import tk_assert

from tk_am.tk_asset import TkAsset
from tk_am.tk_asset_type import TkAssetType
from tk_const import am as c_am
from tk_error.am import MissingTkAssetError
from tk_error.am import MissingTkAssetTypeError
from tk_error.am import TkProjectAlreadyExistsError


if TYPE_CHECKING:
    from collections.abc import Iterator


class TkProject:
    """Object represent a Project."""

    def __init__(self, code: str, name: str, path: str):
        tk_assert.is_str(code)
        tk_assert.is_match(code, c_am.project_code_str)
        tk_assert.is_str(name)
        tk_assert.is_str(path)
        tk_assert.is_path(path)

        self.code = code
        self.name = name
        self._path = path
        self.property = {}

    def __repr__(self):
        return f"TkProject({self.code})"

    @property
    def path(self):
        """Return project root path as .*/PROJ."""
        return os.path.join(self._path, self.code)

    def set_property(self, key: str, value: Any):
        """Set project properties, if key exists, overwrite it.

        Args:
            key (str): Name of property.
            value (Any): Property value.
        """
        self.property[key] = value
        self.save_project(force=True)

    def update_properties(self, data: dict[str, Any]):
        """Update project properties with given data.

        Args:
            data (dict[str, Any]): Dictionary to update current project properties.
        """
        self.property.update(data)
        self.save_project(force=True)

    @classmethod
    def from_dict(cls, data: dict) -> TkProject:
        """Create TkProject from dict.

        Args:
            data (dict): Create TkProject from given data. Related to self.to_dict().
        """
        code = data["code"]
        name = data["name"]
        path = data["path"]
        properties = data.get("properties", {})

        project = cls(code, name, path)
        project.update_properties(properties)
        return project

    def to_dict(self) -> dict:
        """Serialize project as dict format."""
        return {
            "code": self.code,
            "name": self.name,
            "path": self._path,
            "properties": self.property,
        }

    def save_project(self, force: bool = False):
        """Save current project in package configuration.

        Args:
            force (bool): Force to write project as new.

        Raises:
            TkProjectAlreadyExistsError: Raise when force is False and
                                         project already exists.
        """
        from tk_am import get_projects_meta

        home = Path.home()
        meta_path = os.path.join(home, ".config", "tk_config", "project.meta")
        os.makedirs(os.path.dirname(meta_path), exist_ok=True)

        old_data = get_projects_meta()

        if old_data.get(self.code) and not force:
            raise TkProjectAlreadyExistsError(
                f"Project {self.name!r} ({self.code!r}) Already exist."
            )

        old_data[self.code] = self.to_dict()

        with open(meta_path, "w") as f:
            json.dump(old_data, f)

    def get_asset(self, asset_type: str, code: str) -> TkAsset:
        """Get TkAsset object in project.

        Args:
            asset_type (str): Asset type name as chr, prp, lvl ...
            code (str): Asset code.

        Raises:
            MissingTkAssetError
        """
        tk_assert.is_str(asset_type)
        tk_assert.is_str(code)

        for asset in self.get_assets(asset_type):
            if asset.code == code:
                return asset

        raise MissingTkAssetError(f"No asset {code!r} of type {asset_type!r}")

    def get_assets(self, asset_type: str | None = None) -> Iterator[TkAsset]:
        """Yield TkAsset entities.

        Args:
            asset_type (str|None): Filter assets by asset type.

        Raises:
            MissingTkAssetTypeError
        """
        tk_assert.is_opt_str(asset_type)
        if asset_type:
            tk_assert.is_match(asset_type, c_am.asset_type_code_str)

        asset_type_root = os.path.join(self.path, "assets")
        if not os.path.isdir(asset_type_root):
            os.mkdir(asset_type_root)
            if asset_type and not os.path.isdir(
                os.path.join(asset_type_root, asset_type)
            ):
                raise MissingTkAssetTypeError(f"No asset type {asset_type!r}")
            yield from []

        asset_types = [
            TkAssetType(d.name, d.path, self)
            for d in os.scandir(asset_type_root)
            if c_am.asset_type_code_grp_re.match(d.name)
            and (d.name == asset_type if asset_type else True)
        ]

        for asset_type in asset_types:
            asset_dirs = os.scandir(asset_type.path)
            for asset_dir in asset_dirs:
                entity = TkAsset(asset_dir.name, asset_dir.path, asset_type)
                yield entity

    def get_or_create_asset(self, asset_type_code: str, asset_code: str) -> TkAsset:
        """Get existing asset, if asset do not exist, create it.

        Args:
            asset_type_code (str): Type of asset as chr, prp, lvl...
            asset_code (str): Code of asset.

        Returns:
            TkAsset
        """
        tk_assert.is_str(asset_type_code)
        tk_assert.is_match(asset_type_code, c_am.asset_type_code_str)
        tk_assert.is_str(asset_code)
        tk_assert.is_match(asset_code, c_am.asset_code_str)

        assets = []
        asset_type_path = os.path.join(self.path, asset_type_code)
        try:
            assets = self.get_assets(asset_type_code)
        except MissingTkAssetTypeError:
            os.mkdir(asset_type_path)

        for asset in assets:
            if asset_code == asset.code:
                return asset

        asset_type = TkAssetType(asset_type_code, asset_type_path, self)
        asset_path = os.path.join(self.path, asset_type_code, asset_code)
        os.mkdir(os.path.join(self.path, asset_type_code, asset_code))

        return TkAsset(asset_code, asset_path, asset_type)
