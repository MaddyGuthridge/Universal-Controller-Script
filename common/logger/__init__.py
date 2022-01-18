"""
common > logger

Functions for controlling printouts, so that the console isn't clogged up with
random debugging info. It allows for the user to specify what types of things
should be logged and when.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from .logger import log

from . import verbosity
