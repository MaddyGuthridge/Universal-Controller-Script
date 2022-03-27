"""
common

Contains common functions and code required to initialise and manage the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# Check minimum version
import general
from . import consts
if general.getVersion() < consts.MIN_API_VERSION:
    # raise RuntimeError(
    #     f"Your FL Studio version is out of date: expected API "
    #     f"v{consts.MIN_API_VERSION}, got {general.getVersion()}"
    # )
    pass
del general

from .consts import getVersionString

from .logger import log, verbosity
from .profiler import ProfilerContext, profilerDecoration

from .contextmanager import getContext, resetContext, catchContextResetException, unsafeResetContext

from .eventpattern import BasicPattern, IEventPattern

from . import util

from .types import EventData, Color

from .extensionmanager import ExtensionManager
