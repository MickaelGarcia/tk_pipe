"""Database task object module."""

from __future__ import annotations

import os

from typing import TYPE_CHECKING

from tk_db.dbentity import DbEntity
from tk_db.dbpublish import DbPublish
from tk_db.errors import MissingDbPublishError
from tk_db.models import Publish
from tk_db.models import PublishType
from tk_db.models import Task


if TYPE_CHECKING:
    from collections.abc import Iterable

    from tk_db.dbasset import DbAsset
    from tk_db.dbpublishtype import DbPublishType
    from tk_db.dbtasktype import DbTaskType


class DbTask(DbEntity):
    """Database task object."""

    def __init__(self, task: Task, task_type: DbTaskType, asset: DbAsset):
        super().__init__(task)
        self.asset = asset
        self.task_type = task_type

    @property
    def id(self):
        """Return task id."""
        return self._bc_entity.id

    @property
    def code(self):
        """Return task type code."""
        return self.task_type.code

    @property
    def name(self):
        """Return task type name."""
        return self.task_type.name

    @property
    def is_active(self) -> bool:
        """Return if publish is active or not."""
        with self.asset.project.db.Session() as session:
            publish = session.query(Task).where(Task.id == self.id).first()
            active = publish.active

        return active

    def set_active(self, value):
        """Set publish active or not."""
        with self.asset.project.db.Session as session:
            publish = session.query(Task).where(Task.id == self.id).first()
            publish.active = value
            session.commit()

    def publish(
        self,
        code: str,
        publish_type: DbPublishType,
        release: str,
        version: int,
    ) -> DbPublish:
        """Get specific publish form task.

        Args:
            code (str): Publish code.
            publish_type (DbPublishType): Type of publish.
            release (str): Is release or work.
            version (int): Publish version.

        Returns:
            DbPublish

        Raises:
            MissingDbPublishError: Raised when publish is missing in database.
        """
        with self.asset.project.db.Session() as session:
            publish_query = (
                session.query(Publish)
                .join(Task)
                .join(PublishType)
                .filter(
                    PublishType.id == publish_type.id,
                    Task.id == self.id,
                    Publish.code == code,
                    Publish.release == release,
                    Publish.version == version,
                )
                .first()
            )

        if not publish_query:
            raise MissingDbPublishError(
                f"Unable to found publish {release} {code!r} type "
                f"{publish_type.code!r} version {version!r} in database."
            )

        return DbPublish(self, publish_query)

    def publishes(
        self,
        code: str | None = None,
        publish_type: DbPublishType | None = None,
        release: str | None = None,
    ) -> Iterable[DbPublish]:
        """Get list of publishes with given params."""
        publishes = []
        with self.asset.project.db.Session() as session:
            publish_query = session.query(Publish).where(Publish.task_id == self.id)
            if code:
                publish_query = publish_query.filter(Publish.code == code)
            if publish_type:
                publish_query = publish_query.filter(
                    Publish.publish_type_id == publish_type.id
                )
            if release:
                publish_query = publish_query.filter(Publish.release == release)

            publishes = [DbPublish(self, publish) for publish in publish_query]

        return publishes

    def last_active_publish(self, code: str, publish_type: DbPublishType, release: str):
        """Get the last active publish of given publish code/type."""
        publishes = self.publishes(code, publish_type, release)
        if not publishes:
            raise MissingDbPublishError

        return max(publishes, key=lambda x: x.version)

    def create_next_publish(
        self, code: str, publish_type: DbPublishType, release: str
    ) -> DbPublish:
        """Create publish at next versions."""
        try:
            last_publish = self.last_active_publish(code, publish_type, release)
            version = last_publish.version + 1
        except MissingDbPublishError:
            version = 1
        with self.asset.project.db.Session() as session:
            publish = Publish(
                code=code,
                path=self._publish_path(code, publish_type, release, version),
                version=version,
                release=release,
                size=0,
                active=False,
                publish_type_id=publish_type.id,
                task_id=self.id,
            )

            session.add(publish)
            session.commit()

        return self.publish(code, publish_type, release, version)

    def _publish_path(
        self,
        code: str,
        publish_type: DbPublishType,
        release: str,
        version: int,
    ) -> str:
        environ = self.asset.project.metadata.get("env")
        root_path = environ["TK_PROJECT_PATH"]

        if not root_path:
            raise ValueError("Missing project root path")

        publish_name = (
            f"{self.asset.asset_type.code}_{self.asset.code}_{code}_"
            f"{publish_type.file_type}_{release[0]}"
            f"{version:03d}{publish_type.extension}"
        )
        if release == "release":
            publish_path = os.path.join(
                root_path,
                "assets",
                self.asset.asset_type.code,
                self.asset.code,
                self.name,
                code,
                release,
                f"{release[0]}{version:03d}",
                publish_name,
            )
            return str(publish_path)

        publish_path = os.path.join(
            root_path,
            "assets",
            self.asset.asset_type.code,
            self.asset.code,
            self.name,
            code,
            release,
            publish_name,
        )
        return str(publish_path)
