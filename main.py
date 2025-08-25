"""Main module."""

from __future__ import annotations

from tk_am import get_or_create_project
from tk_am import get_project
from tk_const.am import ReleaseType


project = get_or_create_project(
    "TST2",
    "Test_002",
    r"D:\unreal_engine",
)

project = get_project("TST")


for asset in project.get_assets("chr"):
    for task in asset.get_tasks():
        # for work_publish in task.get_publishes():
        #     print(work_publish)
            # print(work_publish.path)
        print()
        for release_publish in task.get_publishes(release=ReleaseType.RELEASE):
            print(type(release_publish))
            print(release_publish)
            # print(release_publish.path)
