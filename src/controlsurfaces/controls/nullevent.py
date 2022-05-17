"""
controlsurfaces > nullevent

Contains the definition of the NullEvent, which represents events that should
be ignored entirely.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from typing import Optional

from .eventpattern import IEventPattern
from controlsurfaces.valuestrategies import NullEventStrategy, IValueStrategy
from . import ControlSurface


class NullEvent(ControlSurface):
    """
    Represents events that should be ignored entirely by the script.
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: Optional[IValueStrategy] = None,
    ) -> None:
        """
        Create a NullEvent

        This is used for events which should be ignored

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to match
        """
        if value_strategy is None:
            value_strategy = NullEventStrategy()
        super().__init__(event_pattern, value_strategy)

    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Null controls shouldn't be reassigned
        return tuple()
