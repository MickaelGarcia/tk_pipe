"""Assertions module."""

from __future__ import annotations

import os
import re

from typing import Any

from tk_error import TkAssertionError


def is_str(value):
    """Assert if value is not str type."""
    if not  isinstance(value, str):
        raise TkAssertionError(f"{value!r} is type string")


def is_opt_str(value):
    """Assert if value is not str or None type."""
    if not isinstance(value, (str, type(None))):
        raise TkAssertionError(f"{value!r} is not optional type string")


def is_int(value):
    """Assert if value is not int  type."""
    if not isinstance(value, int):
        raise TkAssertionError(f"{value!r} is not type int")


def is_path(value):
    """Assert if value is not an existing directory or file path."""
    if not (os.path.isfile(value) or os.path.isdir(value)):
        raise TkAssertionError(f"{value!r} is not an existing path.")


def is_match(value, pattern: str):
    """Assert if value si not matching given pattern."""
    if not re.match(pattern, value):
        raise TkAssertionError(f"{value!r} do not match pattern {pattern!r}")


def is_inst(value: Any, object_type: type):
    """Assert if value is not type of given object_type."""
    if not isinstance(value, object_type):
        raise TkAssertionError(f"{value!r} is not type {object_type.__name__!r}")


def is_opt_inst(value: Any, object_type: type):
    """Assert if value is not type of given object_type or None."""
    if not isinstance(value, (object_type, type(None))):
        raise TkAssertionError(f"{value!r} is not optional type {object_type!r}")
