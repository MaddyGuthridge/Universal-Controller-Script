"""
common

Contains common functions and code required to initialize and manage the
script.

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

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

# Import devices and plugins
import devices
import integrations

del devices
del integrations
