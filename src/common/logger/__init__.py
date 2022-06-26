"""
common > logger

Functions for controlling printouts, so that the console isn't clogged up with
random debugging info. It allows for the user to specify what types of things
should be logged and when.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'log',
    'verbosity',
]

from .logger import log
from . import verbosity
