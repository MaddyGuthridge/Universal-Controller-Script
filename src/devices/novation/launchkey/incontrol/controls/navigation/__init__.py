"""
devices > novation > launchkey > incontrol > controls > navigation

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'LkMk2DirectionNext',
    'LkMk2DirectionPrevious',
    'Mk3DirectionLeft',
    'Mk3DirectionRight',
    'MiniMk3DirectionUp',
    'MiniMk3DirectionDown',
    'Mk3DirectionUp',
    'Mk3DirectionDown',
    'Mk3DirectionUpSilenced',
    'Mk3DirectionDownSilenced',
]

from .mk2 import (
    LkMk2DirectionNext,
    LkMk2DirectionPrevious,
)
from .mk3 import (
    Mk3DirectionLeft,
    Mk3DirectionRight,
    MiniMk3DirectionUp,
    MiniMk3DirectionDown,
    Mk3DirectionUp,
    Mk3DirectionDown,
    Mk3DirectionUpSilenced,
    Mk3DirectionDownSilenced,
)
