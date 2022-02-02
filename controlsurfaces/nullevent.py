
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import NullEventStrategy
from . import ControlSurface

class NullEvent(ControlSurface):
    """
    Represents control surfaces that should be ignored entirely
    """
    
    def __init__(self, event_pattern: IEventPattern) -> None:
        """
        Create a NullEvent

        This is used for events which should be ignored

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to match
        """
        super().__init__(event_pattern, NullEventStrategy(), "null")

    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Null controls should be reassigned
        return tuple()
