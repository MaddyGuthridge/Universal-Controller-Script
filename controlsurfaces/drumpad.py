"""
controlsurfaces > drumpad

Defines a drum pad control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern.ieventpattern import IEventPattern
from controlsurfaces.valuestrategies.ivaluestrategy import IValueStrategy
from . import ControlSurface

class DrumPad(ControlSurface):
    """
    Defines a drum pad control surface.
    Drum pads are usually used to trigger pads in drum plugins, or keyswitches
    in orchestral plugins.
    
    Coordinates should be: (row, col), where (0, 0) is the top left
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return tuple()

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int]
    ) -> None:
        super().__init__(event_pattern, value_strategy, "drum pads", coordinate)
