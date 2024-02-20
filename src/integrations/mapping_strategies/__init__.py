"""
integrations > mapping strategies

Contains strategies to create event mappings for commonly used things, such
as pedals

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'PedalStrategy',
    'WheelStrategy',
    'NoteStrategy',
    'DirectionStrategy',
    'JogStrategy',
    'SimpleFaders',
    'ModXYStrategy',
    'MuteSoloStrategy',
    'GridStrategy',
    'PresetNavigationStrategy',
    'CcForwardStrategy',
]

from .pedal_strategy import PedalStrategy
from .wheel_strategy import WheelStrategy
from .note_strategy import NoteStrategy
from .direction_strategy import DirectionStrategy
from .jog_strategy import JogStrategy
from .simple_faders import SimpleFaders
from .mod_xy import ModXYStrategy
from .mute_solo import MuteSoloStrategy
from .grid_strategy import GridStrategy
from .preset_navigation import PresetNavigationStrategy
from .cc_forward_strategy import CcForwardStrategy
