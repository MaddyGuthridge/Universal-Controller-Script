
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import NullEventStrategy
from . import ControlSurface

class NullEvent(ControlSurface):
    """
    Represents control surfaces that should be ignored entirely
    """
    
    def __init__(self, event_pattern: IEventPattern) -> None:
        super().__init__(event_pattern, NullEventStrategy(), "null")

    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Knob controls should be assigned to faders if knobs aren't available
        return tuple()
