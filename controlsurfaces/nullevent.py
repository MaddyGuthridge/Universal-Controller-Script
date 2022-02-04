"""
controlsurfaces > nullevent

Contains the definition of the NullEvent, which represents events that should
be ignored entirely.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import NullEventStrategy
from . import ControlSurface

class NullEvent(ControlSurface):
    """
    Represents events that should be ignored entirely by the script.
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
        # Null controls shouldn't be reassigned
        return tuple()
