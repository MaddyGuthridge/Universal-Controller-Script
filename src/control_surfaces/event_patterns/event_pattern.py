"""
control_surfaces > event_patterns > event_pattern

Contains the definition for IEventPattern, the interface that all event
patterns must inherit from.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# from __future__ import annotations

from typing import TYPE_CHECKING
from abc import abstractmethod
from common.util.abstract_method_error import AbstractMethodError

if TYPE_CHECKING:
    from common.types import EventData


class IEventPattern:
    """
    Abstract definition for an EventPattern, used to match MIDI events with
    ControlSurfaces.

    This class can be extended if a developer wishes to create their own event
    pattern for a case where the standard BasicPattern class doesn't suffice.
    """

    @abstractmethod
    def matchEvent(self, event: 'EventData') -> bool:
        """
        Return whether the given event matches the pattern

        This is an abstract method which should be implemented by child
        classes.

        ### Args:
        * `event` (`eventData`): Event to match against

        ### Returns:
        * `bool`: whether the event matches
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def fulfil(self) -> 'EventData':
        """
        Create and return an EventData object which will match with this
        pattern. The return value should be randomly generated.

        ## Raises:
        * `TypeError`: unable to fulfil a pattern

        ### Returns:
        * `EventData`: event that matches the strategy
        """
        raise AbstractMethodError(self)
