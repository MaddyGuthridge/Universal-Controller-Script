"""
control_surfaces > event_patterns > event_pattern

Contains the definition for IEventPattern, the interface that all event
patterns must inherit from.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from fl_classes import FlMidiMsg
from abc import abstractmethod
from common.util.abstract_method_error import AbstractMethodError


class IEventPattern:
    """
    Abstract definition for an EventPattern, used to match MIDI events with
    ControlSurfaces.

    This class can be extended if a developer wishes to create their own event
    pattern for a case where the standard BasicPattern class doesn't suffice.
    """

    @abstractmethod
    def matchEvent(self, event: FlMidiMsg) -> bool:
        """
        Return whether the given event matches the pattern

        This is an abstract method which should be implemented by child
        classes.

        ### Args:
        * `event` (`FlMidiMsg`): Event to match against

        ### Returns:
        * `bool`: whether the event matches
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def fulfil(self) -> FlMidiMsg:
        """
        Create and return an FlMidiMsg object which will match with this
        pattern. The return value should be randomly generated.

        ## Raises:
        * `TypeError`: unable to fulfil a pattern

        ### Returns:
        * `FlMidiMsg`: event that matches the strategy
        """
        raise AbstractMethodError(self)
