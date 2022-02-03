
from common.eventpattern import BasicEventPattern, fromNibbles
from . import ControlSurface
from . import Data2Strategy

class ModWheel(ControlSurface):
    """
    Represents a modulation wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
    
    def __init__(self) -> None:
        super().__init__(
            BasicEventPattern(0xB0, 0x1, ...),
            Data2Strategy(),
            "transport"
            )

class PitchWheel(ControlSurface):
    """
    Represents a pitch bend wheel
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
