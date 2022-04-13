"""
plugs > special

Contains the definitions for special plugins, which are used to manage global
behaviours such as transport, macros, and fallback processing.
"""

__all__ = [
    'transport',
    'fallback',
    'macro'
]

from . import transport
from . import fallback
from . import macro
