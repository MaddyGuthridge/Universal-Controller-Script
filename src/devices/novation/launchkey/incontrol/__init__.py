"""
devices > novation > launchkey > incontrol

Contains common code for managing devices that use Novation's InControl
protocol.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'colors',
    'InControl',
    'InControlMatcher',
]

from . import colors
from .incontrol import InControl, InControlMatcher
