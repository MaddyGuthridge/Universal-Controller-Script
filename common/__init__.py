"""
common

Contains common functions and code required to initialise and manage the
script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'getVersionString',
    'log',
    'verbosity',
    'ProfilerContext',
    'profilerDecoration',
    'getContext',
    'resetContext',
    'catchContextResetException',
    'ExtensionManager'
]

from .consts import getVersionString

from .logger import log, verbosity
from .profiler import ProfilerContext, profilerDecoration

from .contextmanager import (
    getContext,
    resetContext,
    catchContextResetException
)

from .extensionmanager import ExtensionManager
