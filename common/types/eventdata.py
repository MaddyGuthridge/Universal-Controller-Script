"""
common > types > eventdata

Contains a shadow of the FL Studio MIDI Event Data type, to use with type
annotations so that we can get those sweet, sweet autocompletions.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# from __future__ import annotations

__all__ = [
    'eventData'
]

from typing import Optional, TypeVar, Generic, TYPE_CHECKING

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

# StatusSysex = TypeVar('StatusSysex', int, list[int])

# Define substitute type if we're type-checking
# if TYPE_CHECKING:
# Nope nevermind, turns out that it's impossible to access that class during
# runtime unless you have a reference object for it.
class eventData:
    """
    A simple reproduction of the eventData object used by FL Studio.
    
    Yes, I know the capitalisation is inconsistent, blame FL Studio devs, not me
    
    Read-only types are marked as such
    """
    def __init__(
        self,
        status_sysex: 'int | list[int]',
        data1: Optional[int]=None,
        data2:Optional[int]=None
    ) -> None:
        self.handled = False
        self.timestamp = ReadOnly(0.0)
        self.status = 0 if isinstance(status_sysex, list) else status_sysex
        self.data1 = data1 if data1 is not None else 0
        self.data2 = data2 if data2 is not None else 0
        self.port = ReadOnly(0)
        self.note = 0
        self.velocity = 0
        self.pressure = 0
        self.progNum = ReadOnly(0)
        self.controlNum = ReadOnly(0)
        self.controlVal = ReadOnly(0)
        self.pitchBend = ReadOnly(0)
        self.sysex = bytes(status_sysex) if isinstance(status_sysex, list) else None
        self.isIncrement = False
        self.res = 0.0
        self.inEv = 0
        self.outEv = 0
        self.midiId = 0
        self.midiChan = 0
        self.midiChanEx = 0
        self.pmeflags = ReadOnly(0)
# Otherwise, define it as the build-in type flmidimsg
# else:
#     for k in __builtins__:
#         print(f"{k}")
#     eventData = globals()["__builtins__"]["flmidimsg"]
