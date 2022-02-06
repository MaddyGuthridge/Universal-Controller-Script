"""
controlsurfaces > navigation

Defines jog wheel control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import ControlSurface
from . import NavigationControl, DirectionNext, DirectionPrevious

class JogWheel(NavigationControl):
    """
    Jog wheels (rotary encoders) are an endless rotating knob that is used for
    navigation. Compared to endless knobs, they should be mapped to navigation
    controls, rather than standard parameters.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()

class JogForwards(JogWheel):
    """
    Represents a jog wheel event where the jog wheel is moved forwards
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return (DirectionNext,)

class JogBackards(JogWheel):
    """
    Represents a jog wheel event where the jog wheel is moved backwards
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return (DirectionPrevious,)
