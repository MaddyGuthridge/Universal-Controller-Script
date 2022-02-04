"""
controlsurfaces > wheel

Contains the definitions for pitch and modulation wheels

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import IEventPattern, BasicEventPattern, fromNibbles
from common.types import eventData
from . import ControlSurface
from . import Data2Strategy, IValueStrategy

__all__ = [
    'ModWheel',
    'PitchWheel',
    'StandardModWheel',
    'StandardPitchWheel',
    'Data2PitchWheel'
]

class ModWheel(ControlSurface):
    """
    Represents a modulation wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()

class StandardModWheel(ModWheel):
    """
    Standard implementation of a mod wheel
    """
    def __init__(self) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xB, ...), 0x1, ...),
            Data2Strategy(),
            "wheels"
        )

class PitchValueStrategy(IValueStrategy):
    """
    Value strategy for standard pitch bends (using 14 bits of information)
    """
    def getValueFromEvent(self, event: eventData) -> int:
        """Returns a 14-bit int (0 - 16384)
        Zero value = 8192
        """
        return event.data1 + (event.data2 << 7)
    
    def getFloatFromValue(self, value: int) -> float:
        return value / 16384
    
    def getValueFromFloat(self, f: float) -> int:
        return int(f * 16384)

class PitchWheel(ControlSurface):
    """
    Represents a pitch bend wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
    
    def __init__(self, event_pattern: IEventPattern, value_strategy: IValueStrategy) -> None:
        super().__init__(event_pattern, value_strategy, "wheels")

class StandardPitchWheel(PitchWheel):
    """
    Standard implementation of a pitch bend wheel (using 14 bits of 
    information)
    """
    def __init__(self) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xE, ...), ..., ...),
            PitchValueStrategy()
        )

class Data2PitchWheel(PitchWheel):
    """
    Implementation of a pitch wheel using data2 values to determine pitch, as
    some manufacturers don't follow the standard of using 14 bits or precision.
    """
    def __init__(self) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xE, ...), 0x0, ...),
            Data2Strategy()
        )
