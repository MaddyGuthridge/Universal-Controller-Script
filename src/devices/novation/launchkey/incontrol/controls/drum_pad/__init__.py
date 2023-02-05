"""
devices > novation > launchkey > incontrol > controls > drum_pad

Contains common code for managing InControl drum pads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'LkDrumPad',
    'LkDrumPadMatcher',
    'LkMk2DrumPad',
    'LkMk3DrumPad',
    'LkMk3DrumPadMute',
    'LkMk3DrumPadSolo',
    'LkMk3DrumPadActivity',
    'LkMk3MiniDrumPadActivity',
]

from .drum_pad import LkDrumPad, LkDrumPadMatcher
from .mk2 import LkMk2DrumPad
from .mk3 import (
    LkMk3DrumPad,
    LkMk3DrumPadMute,
    LkMk3DrumPadSolo,
    LkMk3DrumPadActivity,
    LkMk3MiniDrumPadActivity,
)
