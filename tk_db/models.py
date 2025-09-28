"""Db models module."""

from __future__ import annotations

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Project(Base):
    """Project table."""

    __tablename__ = "project"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, unique=False, nullable=False)
    metadata_ = Column(String)
    active = Column(Boolean, default=True)

    asset = relationship("Asset", back_populates="project")


class AssetType(Base):
    """Asset type table."""

    __tablename__ = "asset_type"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)

    asset = relationship("Asset", back_populates="asset_type")


class Asset(Base):
    """Asset table."""

    __tablename__ = "asset"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    asset_type_id = Column(Integer, ForeignKey("asset_type.id"))
    project_id = Column(Integer, ForeignKey("project.id"))

    project = relationship("Project", back_populates="asset")
    asset_type = relationship("AssetType", back_populates="asset")
    task = relationship("Task", back_populates="asset")


class TaskType(Base):
    """Task type table."""

    __tablename__ = "task_type"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)

    task = relationship("Task", back_populates="task_type")


class Task(Base):
    """Task table."""

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    task_type_id = Column(Integer, ForeignKey("task_type.id"))
    active = Column(Boolean, default=True)

    asset = relationship("Asset", back_populates="task")
    task_type = relationship("TaskType", back_populates="task")
    publish = relationship("Publish", back_populates="task")


class PublishType(Base):
    """Publish type table."""

    __tablename__ = "publish_type"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, nullable=False, unique=True)
    file_type = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    publish = relationship("Publish", back_populates="publish_type")


class Publish(Base):
    """Publish table."""

    __tablename__ = "publish"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, nullable=False)
    path = Column(String, nullable=False, unique=True)
    version = Column(Integer, nullable=False)
    release = Column(String, nullable=False)
    size = Column(Integer)
    active = Column(Boolean, default=True)

    publish_type_id = Column(Integer, ForeignKey("publish_type.id"))
    task_id = Column(Integer, ForeignKey("task.id"))

    publish_type = relationship("PublishType", back_populates="publish")
    task = relationship("Task", back_populates="publish")
