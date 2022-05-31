"""
common > logger > verbosity

Contains the definitions for all verbosity levels used by the script.
When logging something, these constants should be used.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'Verbosity',
    'MOST_VERBOSE',
    'EVENT',
    'NOTE',
    'INFO',
    'WARNING',
    'SUCCESS',
    'ERROR',
    'CRITICAL',
    'DEFAULT',
]

from typing import NewType

Verbosity = NewType("Verbosity", int)

MOST_VERBOSE = Verbosity(100)

EVENT = Verbosity(15)
NOTE = Verbosity(12)
INFO = Verbosity(10)
WARNING = Verbosity(8)
SUCCESS = Verbosity(5)
ERROR = Verbosity(2)
CRITICAL = Verbosity(1)

DEFAULT = INFO
