"""
plugs > special

Contains the definitions for special plugins, which are used to manage global
behaviors such as transport, macros, and fallback processing.
"""

__all__ = [
    'transport',
    'macro',
    'pressed',
]

from . import transport
from . import macro
from . import pressed
