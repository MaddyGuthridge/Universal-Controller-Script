"""
plugs > special

Contains the definitions for special plugins, which are used to manage global
behaviors such as transport, macros, and fallback processing.
"""

__all__ = [
    'transport',
    'defaults',
    'macro',
    'pressed',
]

from . import transport
from . import defaults
from . import macro
from . import pressed
