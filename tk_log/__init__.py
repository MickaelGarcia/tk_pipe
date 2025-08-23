"""Logging package."""

from __future__ import annotations

import logging
import sys

from tk_log._core import _tk_package_names


###############################################################################
# Forward levels to make tk_log easier to use.
###############################################################################
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

###############################################################################
# Globals.
###############################################################################
_disabled = False  # Store whether the loggers were disabled
_loggers = {}  # Session logger cache.

_padding = max(len(n) for n in _tk_package_names())

_fmt_str = f"%(asctime)s|%(name)-{_padding}s|%(levelname)-8s|%(message)s"
# _fmt_str += "|[%(filename)s:%(lineno)s - %(funcName)s()]"

_formatter = logging.Formatter(_fmt_str)


def get(mod_name: str) -> logging.Logger:
    """Return logger from the place the logger is called.

    Args:
        mod_name (str): Module name (dmnmaya, dmnnuke, etc.).

    Returns:
        logging.Logger:
    """
    # Get or create logger.
    global _loggers

    try:
        return _loggers[mod_name]
    except KeyError:
        logger = logging.getLogger(mod_name)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_formatter)
        logger.addHandler(handler)

        _loggers[mod_name] = logger

        if _disabled:
            logger.disabled = True

        return logger


def set_level(lvl: int | str):
    """Set given level to every Tk logger.

    Args:
        lvl (int): Level to set to every Tk logger.
    """
    if isinstance(lvl, str):
        lvl = logging.getLevelName(lvl.upper())
    for logger in _loggers.values():
        logger.setLevel(lvl)


def disable():
    """Disable every Tk loggers."""
    global _disabled
    _disabled = True

    for logger in _loggers.values():
        logger.disabled = True
