"""
common

Contains common functions and code required to initialize and manage the
script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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


from . import exceptions
from .logger import log, verbosity
from .profiler import ProfilerContext, profilerDecoration

from .context_manager import (
    getContext,
    resetContext,
    unsafeResetContext,
    catchContextResetException
)

from .extension_manager import ExtensionManager

# Import devices and plugins
import devices
import integrations

del devices
del integrations
