
from common.eventpattern import BasicEventPattern, fromNibbles
from common.types import eventData
from . import ControlSurface
from . import Data2Strategy, IValueStrategy

__all__ = [
    'ModWheel',
    'PitchWheel'
]

class ModWheel(ControlSurface):
    """
    Represents a modulation wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
    
    def __init__(self) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xB, ...), 0x1, ...),
            Data2Strategy(),
            "transport"
            )

class PitchValueStrategy(IValueStrategy):
    """Value strategy for pitch bends
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
    
    def __init__(self) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xE, ...), 0x1, ...),
            PitchValueStrategy(),
            "transport"
            )
