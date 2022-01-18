"""
common > logger > verbosity

Contains the definitions for all verbosity levels used by the script.
When logging something, these constants should be used.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'Verbosity',
    'MOST_VERBOSE',
    'NOTE',
    'INFO',
    "WARNING",
    'ERROR',
    'CRITICAL',
    'DEFAULT'
]

from typing import NewType

Verbosity = NewType("Verbosity", int)

MOST_VERBOSE = Verbosity(100)

NOTE = Verbosity(5)
INFO = Verbosity(4)
WARNING = Verbosity(3)
ERROR = Verbosity(2)
CRITICAL = Verbosity(1)

DEFAULT = INFO
