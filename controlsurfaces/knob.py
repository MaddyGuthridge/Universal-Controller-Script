"""
controlsurfaces > knob

Defines a knob control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import IValueStrategy
from . import ControlSurface

class Knob(ControlSurface):
    """
    Knobs are limited rotating controls, which usually yield a value relative to
    the rotational position of the knob. They should be assigned to non-linear
    parameters such as pans, or mix levels.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Knob controls should be assigned to faders if knobs aren't available
        return (Fader, )
    
    def __init__(self, event_pattern: IEventPattern, value_strategy: IValueStrategy, coordinate: tuple[int, int], group: str = "knobs") -> None:
        super().__init__(event_pattern, value_strategy, "knobs", coordinate)

from .fader import Fader
