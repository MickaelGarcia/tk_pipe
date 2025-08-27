"""Am error module."""

from __future__ import annotations


class TkProjectAlreadyExistsError(Exception):
    """Raised when project already exist."""

class MissingTkProjectError(Exception):
    """Raised when project do not exist."""

class MissingTkAssetTypeError(Exception):
    """Raised when asset type do not exist."""

class MissingTkAssetError(Exception):
    """Raised when asset do not exist."""

class MissingTkTaskError(Exception):
    """Raised when task do not exist."""

class MissingTkPublishTypeError(Exception):
    """Raise when publish type is not managed."""

class MissingTkPublishError(Exception):
    """Raise when publish do not exist."""

class TkPublishAlreadyExistsError(Exception):
    """Raise when publish already exist."""
