"""
common

Contains common functions and code required to initialise and manage the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from . import consts

from .contextmanager import getContext, resetContext, catchContextResetException

from . import util

from .util import eventData
