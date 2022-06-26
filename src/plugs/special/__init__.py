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
    'transport',
    'final_transport',
    'macro',
    'pressed',
]

from . import transport
from . import final_transport
from . import macro
from . import pressed
