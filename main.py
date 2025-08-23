"""Main module."""

from __future__ import annotations

from tk_am import ReleaseType
from tk_am import get_or_create_project
from tk_am import get_project


project = get_or_create_project(
    "TST2",
    "Test_002",
    r"D:\unreal_engine",
)

project = get_project("TST")


for asset in project.get_assets("chr"):
    for task in asset.get_tasks():
        print(f"\t{task}")
        print(f"\t{task.path}")
        print(f"\t{task.pattern_path}")

print(ReleaseType("release"))
