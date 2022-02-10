"""
controlsurfaces > fader

Defines a fader control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern.ieventpattern import IEventPattern
from controlsurfaces.valuestrategies.ivaluestrategy import IValueStrategy
from . import ControlSurface

class Fader(ControlSurface):
    """
    Defines a fader (slider) control surface.
    Faders are generally mapped to linear parameters, such as volumes or effect
    levels.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Fader controls should be assigned to knobs if faders aren't available
        return (Knob, )
    
    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int],
        group: str = "faders"
    ) -> None:
        super().__init__(event_pattern, value_strategy, group, coordinate)

from .knob import Knob
