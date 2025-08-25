"""Tasks object module."""

from __future__ import annotations

import os
import re

from typing import TYPE_CHECKING

import tk_assert

from tk_am.tk_entity import TkEntity
from tk_am.tk_publish import TkPublish
from tk_const import am as c_am


if TYPE_CHECKING:
    from collections.abc import Iterator

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

    def get_publishes(
        self,
        code: str | None = None,
        release: c_am.ReleaseType | None = None,
    ) -> Iterator[TkPublish]:
        """Yield all publishes of task."""
        tk_assert.is_opt_str(code)
        tk_assert.is_opt_inst(release, c_am.ReleaseType)

        publish_code_dirs = os.scandir(self.path)
        for publish_code_dir in publish_code_dirs:
            if code and publish_code_dir.name != code:
                continue

            if not c_am.publish_code_grp_re.match(publish_code_dir.name):
                continue

            for releases_dir in os.scandir(publish_code_dir.path):
                if releases_dir.name not in ["work", "release"]:
                    continue

                # Manage works
                if (
                    not release or release == c_am.ReleaseType.WORK
                ) and releases_dir.name == "work":
                    for work_dir in os.scandir(releases_dir.path):
                        work_match = c_am.single_file_re.match(work_dir.name)
                        if not work_match:
                            continue

                        work_publish_code = work_match.group("publish_code")
                        work_version = int(work_match.group("version"))
                        work_pb = TkPublish(
                            work_publish_code,
                            work_dir.path,
                            self,
                            c_am.ReleaseType.WORK,
                            work_version,
                        )

                        yield work_pb

                # Manage release
                elif (
                    release is None or release == c_am.ReleaseType.RELEASE
                ) and releases_dir.name == "release":
                    release_version_dir = os.scandir(releases_dir.path)

                    for version_dir in release_version_dir:
                        if not re.match(r"r\d{3}", version_dir.name):
                            continue

                        for release_dir in os.scandir(version_dir.path):
                            release_match = c_am.single_file_re.match(release_dir.name)
                            if not release_match:
                                continue

                            release_publish_code = release_match.group("publish_code")
                            release_version = int(release_match.group("version"))
                            release_publish = TkPublish(
                                release_publish_code,
                                release_dir.path,
                                self,
                                c_am.ReleaseType.RELEASE,
                                release_version,
                            )

                            yield release_publish
