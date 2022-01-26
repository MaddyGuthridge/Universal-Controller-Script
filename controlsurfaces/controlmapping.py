"""
controlsurfaces > controlmapping

Defines a mapping to a control surface.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import ControlSurface

class ControlMapping:
    
    def __init__(self, mapping: 'ControlSurface') -> None:
        self.__mapping = mapping
    
    def getControl(self) -> 'ControlSurface':
        return self.__mapping
