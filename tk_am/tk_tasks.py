"""Tasks object module."""

from __future__ import annotations

import os
import re

from typing import TYPE_CHECKING

import tk_assert

from tk_am.tk_entity import TkEntity
from tk_am.tk_publish import TkPublish
from tk_am.tk_publish_type import TkPublishType
from tk_am.tk_publish_type import publish_code_by_desc_ext
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

    def _get_work_publishes(self) -> Iterator[TkPublish]:
        publish_code_dirs = os.scandir(self.path)

        # /base
        for publish_code_dir in publish_code_dirs:
            if not c_am.publish_code_grp_re.match(publish_code_dir.name):
                continue

            # /base/work
            for releases_dir in os.scandir(publish_code_dir.path):
                if releases_dir.name != "work":
                    continue

                # /base/work/chr_agile_scout_base_snc_w001.mb
                for work_dir in os.scandir(releases_dir.path):
                    work_match = c_am.single_file_re.match(work_dir.name)
                    if not work_match:
                        continue

                    work_publish_code = work_match.group("publish_code")
                    work_version = int(work_match.group("version"))
                    work_pt_desc_ext = (
                        work_match.group("file_desc"),
                        work_match.group("extension"),
                    )
                    publish_type_code = publish_code_by_desc_ext.get(work_pt_desc_ext)

                    work_publish_type = TkPublishType(publish_type_code, self.project.am)
                    work_pb = TkPublish(
                        work_publish_code,
                        work_dir.path,
                        work_publish_type,
                        self,
                        c_am.ReleaseType.WORK,
                        work_version,
                    )

                    yield work_pb

    def _get_release_publishes(self):
        publish_code_dirs = os.scandir(self.path)
        # /base
        for publish_code_dir in publish_code_dirs:
            if not c_am.publish_code_grp_re.match(publish_code_dir.name):
                continue

            # /base/release
            for releases_dir in os.scandir(publish_code_dir.path):
                if releases_dir.name != "release":
                    continue

                release_version_dir = os.scandir(releases_dir.path)

                # /base/release/r001
                for version_dir in release_version_dir:
                    if not re.match(r"r\d{3}", version_dir.name):
                        continue

                    # /base/release/r001/chr_agile_scout_base_scn_r001.mb
                    for release_dir in os.scandir(version_dir.path):
                        release_match = c_am.single_file_re.match(release_dir.name)
                        if not release_match:
                            continue

                        release_pt_desc_ext = (
                            release_match.group("file_desc"),
                            release_match.group("extension"),
                        )
                        publish_type_code = publish_code_by_desc_ext.get(
                            release_pt_desc_ext
                        )

                        release_publish_code = release_match.group("publish_code")
                        release_version = int(release_match.group("version"))
                        release_publish_type = TkPublishType(
                            publish_type_code, self.project.am
                        )

                        release_publish = TkPublish(
                            release_publish_code,
                            release_dir.path,
                            release_publish_type,
                            self,
                            c_am.ReleaseType.RELEASE,
                            release_version,
                        )

                        yield release_publish

    def publishes(
        self,
        code: str | None = None,
        publish_type: TkPublishType | None = None,
        release: c_am.ReleaseType = c_am.ReleaseType.RELEASE,
    ) -> Iterator[TkPublish]:
        """Yield all publishes of task."""
        tk_assert.is_opt_str(code)
        tk_assert.is_opt_inst(release, c_am.ReleaseType)

        if release == c_am.ReleaseType.WORK:
            yield from (
                pb
                for pb in self._get_work_publishes()
                if (code is None or pb.code == code)
                and (publish_type is None or pb.publish_type == publish_type)
            )
        else:
            yield from (
                pb
                for pb in self._get_release_publishes()
                if (code is None or pb.code == code)
                and (publish_type is None or pb.publish_type == publish_type)
            )

                        if (
                            publish_type and publish_type_code == publish_type.code
                        ) or publish_type is None:
                            work_publish_type = TkPublishType(
                                publish_type_code, self.project.am
                            )
                            work_pb = TkPublish(
                                work_publish_code,
                                work_dir.path,
                                work_publish_type,
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

                            release_pt_desc_ext = (
                                release_match.group("file_desc"),
                                release_match.group("extension"),
                            )
                            publish_type_code = publish_code_by_desc_ext.get(
                                release_pt_desc_ext
                            )
                            if (
                                publish_type and publish_type_code == publish_type.code
                            ) or publish_type is None:
                                release_publish_code = release_match.group("publish_code")
                                release_version = int(release_match.group("version"))
                                release_publish_type = TkPublishType(
                                    publish_type_code, self.project.am
                                )

                                release_publish = TkPublish(
                                    release_publish_code,
                                    release_dir.path,
                                    release_publish_type,
                                    self,
                                    c_am.ReleaseType.RELEASE,
                                    release_version,
                                )

                                yield release_publish
