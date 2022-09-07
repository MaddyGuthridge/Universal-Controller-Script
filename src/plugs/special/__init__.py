"""
plugs > special

Contains the definitions for special plugins, which are used to manage global
behaviors such as transport, macros, and fallback processing.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'final_transport',
    'macro',
    'manual_mapper',
    'pressed',
    'transport',
]

from . import final_transport
from . import macro
from . import manual_mapper
from . import pressed
from . import transport
