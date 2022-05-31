"""
common > types > event_data

Contains a shadow of the FL Studio MIDI Event Data type, to use with type
annotations so that we can get those sweet, sweet auto-completions, and a bit
of type safety.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

# from __future__ import annotations

__all__ = [
    'EventData'
]

from typing import Optional, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import TypeGuard

PropType = TypeVar("PropType")


class ReadOnly(Generic[PropType]):
    """
    Simple wrapper class to make an object read only
    """

    def __init__(self, value: PropType) -> None:
        self._value = value

    def __get__(self, instance, owner) -> PropType:
        return self._value

    def __set__(self, value) -> None:
        raise AttributeError("This value is read-only")


class WriteIgnored(Generic[PropType]):
    """
    Simple wrapper class to warn that writes to a parameter will be ignored
    """

    def __init__(self, value: PropType) -> None:
        self._value = value

    def __get__(self, instance, owner) -> PropType:
        return self._value

    def __set__(self, value) -> None:
        raise AttributeError("This value is read-only")

# StatusSysex = TypeVar('StatusSysex', int, list[int])

# Define substitute type if we're type-checking
# if TYPE_CHECKING:
# Nope never mind, turns out that it's impossible to access that class during
# runtime unless you have a reference object for it.


class EventData:
    """
    A simple reproduction of the eventData object used by FL Studio.

    NOTE: The `status`, `data1` and `data2` are set to `None` if the event is a
    sysex event in the interest of error prevention. In FL Studio, they are set
    to `0`.

    Read-only types are marked as such.
    """

    def __init__(
        self,
        status_sysex: 'int | list[int] | bytes',
        data1: Optional[int] = None,
        data2: Optional[int] = None
    ) -> None:
        self.handled = False
        self.timestamp = ReadOnly(0.0)
        self.status = status_sysex if isinstance(status_sysex, int) else None
        self.data1 = data1  # if data1 is not None else 0
        self.data2 = data2  # if data2 is not None else 0
        self.port = ReadOnly(0)
        self.note = 0
        self.velocity = 0
        self.pressure = 0
        self.progNum = ReadOnly(0)
        self.controlNum = ReadOnly(0)
        self.controlVal = ReadOnly(0)
        self.pitchBend = ReadOnly(0)
        self.sysex = bytes(status_sysex) if not isinstance(
            status_sysex, int) else None
        self.isIncrement = False
        self.res = 0.0
        self.inEv = 0
        self.outEv = 0
        self.midiId = 0
        self.midiChan = 0
        self.midiChanEx = 0
        self.pmeflags = ReadOnly(0)

    def __eq__(self, o: object) -> bool:

        if isinstance(o, EventData):
            if isEventStandard(self) and isEventStandard(o):
                return (
                    self.status == o.status
                    and self.data1 == o.data1
                    and self.data2 == o.data2
                )
            elif isEventSysex(self) and isEventSysex(o):
                return self.sysex == o.sysex
            else:
                return False
        else:
            return NotImplemented

    def __repr__(self) -> str:
        from common.util.events import eventToString
        return eventToString(self)


class _StandardEventData(EventData):
    """
    A type narrowed event data object

    Don't type hint as this, it is only to facilitate type narrowing
    """
    status: int
    data1: int
    data2: int
    sysex: None

    def __init__(self, status: int, data1: int, data2: int) -> None:
        super().__init__(status, data1, data2)


class _SysexEventData(EventData):
    """
    A type narrowed event data object

    Don't type hint as this, it is only to facilitate type narrowing
    """
    status: None
    data1: None
    data2: None
    sysex: bytes

    def __init__(self, sysex: list[int]) -> None:
        super().__init__(sysex)


def isEventSysex(event: EventData) -> 'TypeGuard[_SysexEventData]':
    """
    Returns whether an event is a sysex event

    ### Args:
    * `event` (`eventData`): event to check

    ### Returns:
    * `TypeGuard[SysexEventData]`: type guarded event
    """
    return event.sysex is not None


def isEventStandard(event: EventData) -> 'TypeGuard[_StandardEventData]':
    """
    Returns whether an event is a standard event

    ### Args:
    * `event` (`eventData`): event to check

    ### Returns:
    * `TypeGuard[SysexEventData]`: type guarded event
    """
    return not isEventSysex(event)
