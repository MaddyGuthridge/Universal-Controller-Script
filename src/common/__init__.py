"""
common

Contains common functions and code required to initialise and manage the
script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'getVersionString',
    'exceptions',
    'log',
    'verbosity',
    'ProfilerContext',
    'profilerDecoration',
    'getContext',
    'resetContext',
    'unsafeResetContext',
    'catchContextResetException',
    'ExtensionManager',
]

from .consts import getVersionString

from . import exceptions
from .logger import log, verbosity
from .profiler import ProfilerContext, profilerDecoration

from .contextmanager import (
    getContext,
    resetContext,
    unsafeResetContext,
    catchContextResetException
)

from .extensionmanager import ExtensionManager

# Import devices and plugins
import devices
import plugs
del devices
del plugs
