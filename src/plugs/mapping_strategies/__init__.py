"""
plugins > mapping strategies

Contains strategies to create event mappings for commonly used things, such
as pedals
"""

__all__ = [
    'IMappingStrategy',
    'PedalStrategy',
    'WheelStrategy',
    'NoteStrategy',
    'DirectionStrategy',
    'JogStrategy',
    'SimpleFaders',
    'ModXYStrategy',
]

from .mapping_strategy import IMappingStrategy

from .pedal_strategy import PedalStrategy
from .wheel_strategy import WheelStrategy
from .note_strategy import NoteStrategy
from .direction_strategy import DirectionStrategy
from .jog_strategy import JogStrategy
from .simple_faders import SimpleFaders
from .mod_xy import ModXYStrategy
