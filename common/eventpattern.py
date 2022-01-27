"""
common > eventpattern

Contains code for pattern matching with MIDI events, including EventPattern,
a standard way to match events, and IEventPattern, from which custom pattern
matchers can be derived.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# from __future__ import annotations

from typing import (TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Union,
    Type
)

if TYPE_CHECKING:
    from . import eventData

EllipsisType: Type = type(Ellipsis)

# Variable type for byte match expression
ByteMatch = Union[int, range, tuple[int, ...], 'ellipsis']

class IEventPattern:
    """
    Abstract definition for an EventPattern, used to match MIDI events with
    ControlSurfaces.

    This class can be extended if a developer wishes to create their own event
    pattern for a case where the standard EventPattern class doesn't suffice.
    """
    
    def matchEvent(self, event: 'eventData') -> bool:
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
        status_sysex:  'ByteMatch | list[ByteMatch]',
        data1: Optional[ByteMatch]=None,
        data2: Optional[ByteMatch]=None
    ) -> None:
        """
        Create an event pattern

        It can be used to identify sysex events and standard events, but it
        should be noted that the two are exclusive for a single event.
        
        Each parameter can be one of multiple types:
        * `int`: A strict value: any value other than this will not match.
        * `range`: A range of values (eg 2:10): values within the range
          (excluding the upper bound, like in standard ranges) will match.
        * `tuple[int]`: Any value included in the tuple will match.
        * `...`: A wildcard: any value will match.
        
        For sysex-type events, a list of objects of that type must be provided.

        ### Args:
        * `status_sysex` (`ByteMatch | list[ByteMatch]`): Status byte or sysex data.
        * `data1` (`ByteMatch`, optional): data1 byte. Defaults to `None`.
        * `data2` (`ByteMatch`, optional): data2 byte. Defaults to `None`.
        
        ### Example Usage
        
        * `EventPattern(0x7F, 0x03, ...)`: Recognise an event, where the status
          is 127, data1 is 3, and data2 is any value
        
        * `EventPattern((0x90, 0x80), 0x04, range(10, 20))`: Recognise an event,
          where the status is either 128 or 144, data1 is 4, and data2 is any
          value between 10 and 20
          
        * `EventPattern([0x30, 0x40, range(0, 20, 2), ...])`: Recognise a 
          sysex event, where the first byte is 48, the second is 64, the third
          is an even number less than 20, and the 4th is any value.
        """
        
        # Ensure that we are given valid data
        
        # Lambda to check if values are none
        # isNone = lambda x: x is None
        
        # Lambda to check if values are of the required type
        typeCheck = lambda x: isinstance(x, (int, range, type(...)))\
            or (isinstance(x, tuple) and all(isinstance(y, (int, range)) for y in x))
        
        # Check for sysex event
        if isinstance(status_sysex, list):
            if not all(typeCheck(x) for x in status_sysex):
                raise TypeError("Incorrect types for sysex data. Refer to "
                                "object documentation.")
            self.sysex_event = True
            self.sysex = status_sysex
            
        # Otherwise check for standard event
        else:
            if any(x is None for x in [data1, data2]):
                raise TypeError("Incorrect number of arguments for a non-sysex "
                                "event type. Refer to object documentation.")
            if not all(map(typeCheck, [status_sysex, data1, data2])):
                raise TypeError("Incorrect types for event data. Refer to "
                                "object docmentation.")
        
            # Store the data
            if TYPE_CHECKING:
                assert data1 is not None
                assert data2 is not None
            self.sysex_event = False
            self.status = status_sysex
            self.data1 = data1
            self.data2 = data2

    def matchEvent(self, event: 'eventData') -> bool:
        """
        Returns whether an event matches this pattern.

        ### Args:
        * `event` (`eventData`): Event to attempt to match

        ### Returns:
        * `bool`: whether there is a match
        """
        if self.sysex_event:
            return self._matchSysex(event)
        else:
            return self._matchStandard(event)
    
    @staticmethod
    def _matchByteConst(expected: int, actual: int) -> bool:
        return expected == actual
    
    @staticmethod
    def _matchByteRange(expected: range, actual: int) -> bool:
        return actual in expected
    
    @staticmethod
    def _matchByteTuple(expected: tuple[int], actual: int) -> bool:
        return actual in expected
    
    @staticmethod
    def _matchByteEllipsis(expected: 'ellipsis', actual: int) -> bool:
        return 0 <= actual <= 127

    @staticmethod
    def _matchByte(expected: ByteMatch, actual: int) -> bool:
        """
        Matcher function for a single byte
        """
        # This is type-safe, I promise
        matches: dict[type, Callable[[Any, int], bool]] = {
            int: EventPattern._matchByteConst,
            range: EventPattern._matchByteRange,
            tuple: EventPattern._matchByteTuple,
            type(...): EventPattern._matchByteEllipsis
        }
        return matches[type(expected)](expected, actual)

    def _matchSysex(self, event: 'eventData') -> bool:
        """
        Matcher function for sysex events
        """
        if event.sysex is None:
            return False
        return all(map(self._matchByte, self.sysex, event.sysex))

    def _matchStandard(self, event: 'eventData') -> bool:
        """
        Matcher function for standard events
        """
        if (
            event.status is None
        ):
            return False
        if TYPE_CHECKING:
            assert event.data1 is not None
            assert event.data2 is not None
        return all(self._matchByte(expected, actual) for expected, actual in
                   zip(
                       [self.status, self.data1, self.data2],
                       [event.status, event.data1, event.data2]
                    ))
