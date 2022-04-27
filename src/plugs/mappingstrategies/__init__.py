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
]

from .mappingstrategy import IMappingStrategy

from .pedalstrategy import PedalStrategy
from .wheelstrategy import WheelStrategy
from .notestrategy import NoteStrategy
