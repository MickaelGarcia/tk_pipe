"""Db Error module."""

from __future__ import annotations


class MissingDbProjectError(Exception):
    """Raised when project do not exist in database."""

class MissingDbAssetTypeError(Exception):
    """Raised when asset type do not exist in database."""

class MissingDbAssetError(Exception):
    """Raised when asset do not exist in project."""


class DbProjectAlreadyExistsError(Exception):
    """Raised when trying to create project that already exist."""

class DbAssetTypeAlreadyExistsError(Exception):
    """Raised when trying to create asset type that already exist."""

class DbAssetAlreadyExistError(Exception):
    """Raised when trying to create asset that already exist."""
