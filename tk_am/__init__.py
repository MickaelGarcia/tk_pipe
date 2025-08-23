"""Asset manager module."""

from __future__ import annotations

import json
import os

from enum import Enum
from pathlib import Path

import tk_assert

from tk_am.tk_project import TkProject
from tk_const.am import project_code_str
from tk_error.am import MissingTkProjectError
from tk_error.am import TkProjectAlreadyExistsError


class ReleaseType(str, Enum):
    """Release type values."""

    RELEASE: str = "release"
    WORK: str = "work"


def get_or_create_project(
    project_code: str,
    project_name: str,
    project_root: str,
) -> TkProject:
    """Create new project from given project code, name at given path.

    Args:
        project_code (str): Project code, should be in UPPERCASE.
        project_name (str): Name of project, used for display.
        project_root (str): Root of project path without project code directory.

    Returns:
        TkProject: Project object instance.
    """
    tk_assert.is_str(project_code)
    tk_assert.is_match(project_code, project_code_str)

    tk_assert.is_str(project_name)
    tk_assert.is_str(project_root)

    tk_assert.is_path(project_root)

    project_path = os.path.join(project_root, project_code)

    try:
        project = get_project(project_code)
    except MissingTkProjectError:
        os.mkdir(project_path)
        project = TkProject(project_code, project_name, project_root)
        project.save_project()

    return project


def get_projects_meta() -> dict:
    """Get projects from pipe meta."""
    home = Path.home()
    meta_path = os.path.join(home, ".config", "tk_config", "project.meta")

    old_data = {}
    if os.path.isfile(meta_path):
        with open(meta_path) as f:
            old_data = json.load(f)

    return old_data


def get_project(project_code: str) -> TkProject:
    """Return project in meta from project code."""
    tk_assert.is_str(project_code)
    tk_assert.is_match(project_code, project_code_str)

    data = get_projects_meta()

    project = data.get(project_code)
    if not project:
        raise MissingTkProjectError(f"Project {project_code!r} do not exist.")

    return TkProject.from_dict(project)
