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
    """
    Defines a mapping to a control surface, which has the property that
    different instances of a mapping to the same control have the same hash.
    """
    def __init__(self, mapping: 'ControlSurface') -> None:
        self.__mapping = mapping
    
    def __hash__(self) -> int:
        return hash(self.__mapping)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ControlMapping):
            return self.__mapping == __o.__mapping
        else:
            return False
    
    def getControl(self) -> 'ControlSurface':
        return self.__mapping
