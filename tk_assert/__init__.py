"""Assertions module."""

from __future__ import annotations

import os
import re

from typing import Any


def is_str(value):
    """Assert if value is not str type."""
    assert isinstance(value, str), f"{value!r} is type string"


def is_opt_str(value):
    """Assert if value is not str or None type."""
    assert isinstance(value, (str, type(None))), f"{value!r} is not optional type string"


def is_path(value):
    """Assert if value is not an existing directory or file path."""
    assert os.path.isfile(value) or os.path.isdir(value), (
        f"{value!r} is not an existing path."
    )


def is_match(value, pattern: str):
    """Assert if value si not matching given pattern."""
    assert re.match(pattern, value), f"{value!r} do not match pattern {pattern!r}"


def is_inst(value: Any, object_type: type):
    """Assert if value is not type of given object_type."""
    assert isinstance(value, object_type), (
        f"{value!r} is not type {object_type.__name__!r}"
    )


def is_opt_inst(value: Any, object_type: type):
    """Assert if value is not type of given object_type or None."""
    assert isinstance(value, (object_type, type(None))), (
        f"{value!r} is not optional type {object_type!r}"
    )
