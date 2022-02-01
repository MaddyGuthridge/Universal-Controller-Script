"""
common

Contains common functions and code required to initialise and manage the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import consts

from .logger import log, verbosity

from .eventpattern import BasicEventPattern, IEventPattern

from .contextmanager import getContext, resetContext, catchContextResetException

from . import util

from .types import eventData, Color

from .extensionmanager import ExtensionManager
