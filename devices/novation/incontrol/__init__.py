"""
devices > novation > launchkey > incontrol

Contains common code for managing devices that use Novation's InControl
protocol.
"""

__all__ = [
    'colors',
    'InControl',
    'InControlMatcher',
]

from . import colors
from .incontrol import InControl, InControlMatcher
