"""Asset manager constants module."""

from __future__ import annotations

import re

import lucidity


# Uppercase, number after first character.
project_code_str = r"[A-Z](?:[A-Z0-9])*"
project_code_grp = rf"(?P<project_code>{project_code_str})"
project_code_grp_re = re.compile(rf"^{project_code_grp}$")

project_root_path_str = rf".*/{project_code_str}"
project_root_path_grp = rf".*/{project_code_grp}"
project_root_path_grp_re = re.compile(project_root_path_grp)

# lowercase only, three character strict.
asset_type_code_str = r"[a-z][a-z][a-z]"
asset_type_code_grp = rf"(?P<asset_type_code>{asset_type_code_str})"
asset_type_code_grp_re = re.compile(rf"^{asset_type_code_grp}$")

# lower_snake_case, number after first word.
asset_code_str = r"[a-z]+(?:_[a-z0-9]+)+"
asset_code_grp = rf"(?P<asset_code>{asset_code_str})"
asset_code_grp_re = re.compile(rf"^{asset_code_grp}$")

# lower_snake_case only.
task_code_str = r"[a-z]+(?:_[a-z]+)*"
task_code_grp = rf"(?P<task_code>{task_code_str})"
task_code_grp_re = re.compile(rf"^{task_code_grp}$")

# camelCase, number after first word.
publish_code_str = r"[a-z]+(?:[A-Z][a-z0-9]*)*"
publish_code_grp = rf"(?P<publish_code>{publish_code_str})"
publish_code_grp_re = rf"^{publish_code_grp}$"


# lowercase only.
file_desc_str = r"[a-z]+"
file_desc_grp = rf"(?P<file_desc>{file_desc_str})"
file_desc_grp_re = rf"^{file_desc_grp}$"

# file format as `chr_knight_guard_baseAnim_scn_w001.ma`
single_file_str = (
    rf"{asset_type_code_str}_{asset_code_str}_{publish_code_str}_{file_desc_str}_"
    r"[w|r]\d{{3}}\.[a-zA-Z0-9]+"
)

single_file_grp = (
    rf"{asset_type_code_grp}_{asset_code_grp}_{publish_code_grp}_{file_desc_grp}_"
    r"(?P<release>[w|r])(?P<version>\d{3})(?P<extension>\.[a-zA-Z0-9]+)"
)

single_file_re = re.compile(rf"^{single_file_grp}$")

# image sequence format as `chr_knight_guard_metalTexD_iseq.1001.png`
seq_file_str = (
    rf"{asset_type_code_str}_{asset_code_str}_{publish_code_str}_{file_desc_str}"
    r".\d{4}\.[a-zA-Z0-9]+"
)

seq_file_grp = (
    rf"{asset_type_code_grp}_{asset_code_grp}_{publish_code_grp}_{file_desc_grp}"
    r".(?P<frame>\d{4})(?P<extension>\.[a-zA-Z0-9]+)"
)

seq_file_re = re.compile(rf"^{seq_file_grp}$")


project_work_dir_path_str = (
    rf"{project_code_str}/assets/{asset_type_code_str}/{asset_code_str}/"
    rf"{task_code_str}/work"
)

project_work_dir_path_grp = (
    rf"{project_code_grp}/assets/{asset_type_code_grp}/{asset_code_grp}/"
    rf"{task_code_grp}/work"
)

project_work_dir_path_grp_re = re.compile(rf"^{project_work_dir_path_grp}$")

project_release_dir_path_str = (
    rf"{project_root_path_grp}/assets/{asset_type_code_str}/{asset_code_str}/"
    rf"{task_code_str}/release/r(?P<version>\d{{3}})/{publish_code_str}"
)

project_release_dir_path_grp = (
    rf"{project_code_grp}/assets/{asset_type_code_grp}/{asset_code_grp}/"
    rf"{task_code_grp}/release/r(?P<version>\d{{3}})/{publish_code_grp}"
)

project_release_dir_path_grp_re = re.compile(rf"^{project_release_dir_path_grp}$")

work_path_template = lucidity.Template(
    "work",
    rf"/{{project:{project_code_str}}}/assets/"
    f"{{asset_type_code:{asset_type_code_str}}}/"
    f"{{asset_code:{asset_code_str}}}/"
    f"{{task_code:{task_code_str}}}/work/"
    f"{{asset_type_code:{asset_type_code_str}}}_"
    f"{{asset_code:{asset_code_str}}}_"
    f"{{publish_code:{publish_code_str}}}_"
    f"{{file_desc:{file_desc_str}}}_"
    rf"w{{version:\d\d\d}}{{extension:.[a-zA-Z0-p]+}}",
)

release_path_template = lucidity.Template(
    "work",
    rf"/{{project:{project_code_str}}}/assets/"
    f"{{asset_type_code:{asset_type_code_str}}}/"
    f"{{asset_code:{asset_code_str}}}/"
    f"{{task_code:{task_code_str}}}/release/"
    rf"/r{{version:\d\d\d}}/"
    f"{{asset_type_code:{asset_type_code_str}}}_"
    f"{{asset_code:{asset_code_str}}}_"
    f"{{publish_code:{publish_code_str}}}_"
    f"{{file_desc:{file_desc_str}}}_"
    rf"r{{version:\d\d\d}}{{extension:.[a-zA-Z0-p]+}}",
)
