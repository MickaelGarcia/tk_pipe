"""Logging core module."""

from __future__ import annotations

import os.path
import sys

from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterator


def _tk_package_names() -> Iterator[str]:
    """Iterate over tk_pipe package names.

    Yields:
        str: tk_pipe package names.
    """
    module_file_path = Path(__file__).parent.parent
    yield from (
        entry.name for entry in module_file_path.iterdir() if entry.name.startswith("tk_")
    )


def _module_name(path: str) -> str:
    """Return tk_pipe module name for the given file path.

    Args:
        path (str): Python path calling the logger.
    """
    path = Path(path)

    cur_path = path

    # The ugly part is here: We try to find the package name, from the file
    # path, moving from bottom to top.
    while True:
        if (
            cur_path.name.startswith("tk_")
            and cur_path.parent.name == "tk_"
            and cur_path.parent.parent.name == "tk_pipe"
        ):
            return cur_path.name

        cur_path = cur_path.parent

        # We reached the top of the path without finding anything.
        if cur_path.parent == cur_path:
            break

    # Try to provide a module name from current application.
    if sys.executable is not None:
        # /path/to/maya.exe -> maya.exe
        exec_name = os.path.basename(sys.executable)
        name, _ = os.path.splitext(exec_name)
        return name

    return path.name
