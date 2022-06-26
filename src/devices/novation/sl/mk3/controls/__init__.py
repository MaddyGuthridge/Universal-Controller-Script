"""
devices > novation > sl > mk3 > controls

Controls used by Novation SL Mk3 controllers

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'SlColorSurface',
    'SlDrumPadMatcher',
    'SlFaderSet',
    'SlNotifMsg',
]

from .sl_color_surface import SlColorSurface
from .drum_pad import SlDrumPadMatcher
from .fader import SlFaderSet
from .notif_msg import SlNotifMsg
