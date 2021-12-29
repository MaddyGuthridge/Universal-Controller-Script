"""
common > eventpattern

Contains code for pattern matching with MIDI events, including EventPattern,
a standard way to match events, and IEventPattern, from which custom pattern
matchers can be derived.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import eventData

class IEventPattern:
    """
    Abstract definition for an EventPattern, used to match MIDI events with
    ControlSurfaces.

    This class can be extended if a developer wishes to create their own event
    pattern for a case where the standard EventPattern class doesn't suffice.
    """
    
    def recogniseEvent(self, event: eventData) -> bool:
        """
        Return whether the given event matches the pattern

        This is an abstract method which should be implemented by child classes

        ### Args:
        * `event` (`[type]`): Event to match against

        ### Returns:
        * `bool`: whether the event matches
        """
        return False

class EventPattern(IEventPattern):
    """
    Represents a pattern to match with MIDI events.

    This allows developers to define a complex pattern to match with events,
    so that MIDI events from a controller can be recognised and paired with the
    matching ControlSurface
    """
    
    def __init__(
        self,
        # Status byte or sysex data
        status_sysex:   int|slice|tuple[int]|ellipsis
                 | list[int|slice|tuple[int]|ellipsis]=None,
        data1: Optional[int|slice|tuple[int]|ellipsis]=None,
        data2: Optional[int|slice|tuple[int]|ellipsis]=None
    ) -> None:
        """
        Create an event pattern

        It can be used to identify sysex events and standard events, but it
        should be noted that the two are exclusive for a single event.
        
        Each parameter can be one of multiple types:
        * `int`: A strict value: any value other than this will not match.
        * `slice`: A range of values (eg 2:10): values within the range
          (excluding the upper bound, like in standard slices) will match.
        * `tuple[int]`: Any value included in the tuple will match.
        * `...`: A wildcard: any value will match.
        
        For sysex-type events, a list of objects of that type must be provided.

        ### Args:
        * `status_sysex` (`eventType`, optional): Status byte or sysex data.
          Defaults to `None`.
        * `data1` (`eventType`, optional): data1 byte. Defaults to `None`.
        * `data2` (`eventType`, optional): data2 byte. Defaults to `None`.
        
        ### Example Usage
        
        * `EventPattern(0x7F, 0x03, ...)`: Recognise an event, where the status
          is 127, data1 is 3, and data2 is any value
        
        * `EventPattern((0x90, 0x80), 0x04, slice(10, 20))`: Recognise an event,
          where the status is either 128 or 144, data1 is 4, and data2 is any
          value between 10 and 20
          
        * `EventPattern([0x30, 0x40, slice(0, 20, 2), ...])`: Recognise a 
          sysex event, where the first byte is 48, the second is 64, the third
          is an even number less than 20, and the 4th is any value.
        """
        
        # Ensure that we are given valid data
        
        # Lambda to check if values are none
        isNone = lambda x: x is None
        # Lambda to check if values are of the required type
        typeCheck = lambda x: isinstance(x, (int, slice, ellipsis))\
            or (isinstance(x, tuple) and all(isinstance(y, (int, slice)) for y in x))
        
        # Check for sysex event
        if isinstance(status_sysex, list):
            if not all(typeCheck(x) for x in status_sysex):
                raise TypeError("Incorrect types for sysex data. Refer to "
                                "object documentation.")
            self.sysex_event = True
            self.sysex = status_sysex
            
        # Otherwise check for standard event
        else:
            if any(map(isNone, [status_sysex, data1, data2])):
                raise TypeError("Incorrect number of arguments for a non-sysex "
                                "event type. Refer to object documentation.")
            if not all(map(typeCheck, [status_sysex, data1, data2])):
                raise TypeError("Incorrect types for event data. Refer to "
                                "object docmentation.")
        
            # Store the data
            self.sysex_event = False
            self.status = status_sysex
            self.data1 = data1
            self.data2 = data2

    def recogniseEvent(self, event: eventData) -> bool:
        return False
