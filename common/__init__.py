"""
common

Contains common functions and code required to initialise and manage the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import consts
from .consts import getVersionString

from .logger import log, verbosity

from .contextmanager import getContext, resetContext, catchContextResetException

from .eventpattern import BasicPattern, IEventPattern

from . import util

from .types import eventData, Color

from .extensionmanager import ExtensionManager
