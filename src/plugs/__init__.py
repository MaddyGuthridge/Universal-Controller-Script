"""
plugins

Contains definitions for plugins, allowing the script to interface with them
"""

__all__ = [
    'IMappingStrategy',
    'NoteStrategy',
    'PedalStrategy',
    'WheelStrategy',
    'Plugin',
    'SpecialPlugin',
    'StandardPlugin',
    'WindowPlugin',
]

from .mappingstrategies import (
    IMappingStrategy,
    NoteStrategy,
    PedalStrategy,
    WheelStrategy,
)

from .plugin import Plugin, SpecialPlugin, StandardPlugin, WindowPlugin

# Register plugins
from . import (
    special,
    windows,
    standard
)
del (
    special,
    windows,
    standard
)
