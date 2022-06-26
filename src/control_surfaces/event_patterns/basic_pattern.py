"""
control_surfaces > event_patterns > basic_pattern

Contains a basic pattern for recognizing MIDI events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING, Any, Callable, Optional

from fl_classes import FlMidiMsg, isMidiMsgStandard, isMidiMsgSysex
from . import ByteMatch, IEventPattern, fulfilByte


class BasicPattern(IEventPattern):
    """
    Represents a pattern to match with MIDI events.

    This allows developers to define a complex pattern to match with events,
    so that MIDI events from a controller can be recognized and paired with the
    matching ControlSurface.
    """

    def __init__(
        self,
        # Status byte or sysex data
        status_sysex:  'ByteMatch | list[ByteMatch]',
        data1: Optional[ByteMatch] = None,
        data2: Optional[ByteMatch] = None
    ) -> None:
        """
        Create a basic event pattern.

        It can be used to identify sysex events and standard events, but it
        should be noted that the two are exclusive for a single event. If you
        need to match both, use a UnionPattern

        Each parameter can be one of multiple types:
        * `int`: A strict value: any value other than this will not match.
        * `range`: A range of values (eg 2:10): values within the range
          (excluding the upper bound, like in standard ranges) will match.
        * `tuple[int]`: Any value included in the tuple will match.
        * `...`: A wildcard: any value will match.

        For sysex-type events, a list of objects of that type must be provided.
        If given sysex messages are longer than the pattern, then any extra
        data will be ignored, and assumed to match with any data.

        ### Args:
        * `status_sysex` (`ByteMatch | list[ByteMatch]`): Status byte or sysex
          data.
        * `data1` (`ByteMatch`, optional): data1 byte. Defaults to `None`.
        * `data2` (`ByteMatch`, optional): data2 byte. Defaults to `None`.

        ### Example Usage

        * `EventPattern(0x7F, 0x03, ...)`: Recognize an event, where the status
          is 127, data1 is 3, and data2 is any value

        * `EventPattern((0x90, 0x80), 0x04, range(10, 20))`: Recognize an
          event, where the status is either 128 or 144, data1 is 4, and data2
          is any value between 10 and 20

        * `EventPattern([0x30, 0x40, range(0, 20, 2), ...])`: Recognize a
          sysex event, where the first byte is 48, the second is 64, the third
          is an even number less than 20, and the 4th is any value.
        """

        # Ensure that we are given valid data

        # Lambda to check if values are none
        # isNone = lambda x: x is None

        # Function to check if values are of the required type
        def typeCheck(x):
            if isinstance(x, (int, range, type(...))):
                return True
            else:
                return (
                    isinstance(x, tuple)
                    and all(isinstance(y, (int, range)) for y in x)
                )

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
                raise TypeError(
                    "Incorrect number of arguments for a non-sysex event "
                    "type. Refer to object documentation."
                )
            if not all(map(typeCheck, [status_sysex, data1, data2])):
                raise TypeError(
                    "Incorrect types for event data. Refer to object "
                    "documentation."
                )

            # Store the data
            if TYPE_CHECKING:
                assert data1 is not None
                assert data2 is not None
            self.sysex_event = False
            self.status = status_sysex
            self.data1 = data1
            self.data2 = data2

    def fulfil(self) -> FlMidiMsg:
        if self.sysex_event:
            return FlMidiMsg(bytes([fulfilByte(b) for b in self.sysex]))
        else:
            return FlMidiMsg(
                fulfilByte(self.status),
                fulfilByte(self.data1),
                fulfilByte(self.data2),
            )

    def matchEvent(self, event: FlMidiMsg) -> bool:
        """
        Returns whether an event matches this pattern.

        ### Args:
        * `event` (`FlMidiMsg`): Event to attempt to match

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
    def _matchByteEllipsis(
        expected: 'ellipsis',  # noqa: F821
        actual: int
    ) -> bool:
        return 0 <= actual <= 127

    @staticmethod
    def _matchByte(expected: ByteMatch, actual: int) -> bool:
        """
        Matcher function for a single byte
        """
        # This is type-safe, I promise
        matches: dict[type, Callable[[Any, int], bool]] = {
            int: BasicPattern._matchByteConst,
            range: BasicPattern._matchByteRange,
            tuple: BasicPattern._matchByteTuple,
            type(...): BasicPattern._matchByteEllipsis
        }
        return matches[type(expected)](expected, actual)

    def _matchSysex(self, event: FlMidiMsg) -> bool:
        """
        Matcher function for sysex events
        """
        if not isMidiMsgSysex(event):
            return False
        # If we have more sysex data than them, it can't possibly be a match
        if len(self.sysex) > len(event.sysex):
            return False
        return all(map(self._matchByte, self.sysex, event.sysex))

    def _matchStandard(self, event: FlMidiMsg) -> bool:
        """
        Matcher function for standard events
        """
        if not isMidiMsgStandard(event):
            return False
        return all(self._matchByte(expected, actual) for expected, actual in
                   zip(
                       [self.status, self.data1, self.data2],
                       [event.status, event.data1, event.data2]
        ))
