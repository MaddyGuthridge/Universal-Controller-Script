"""
controlsurfaces > note

Contains the definition of the Note class, which represents note events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.types.eventdata import eventData, isEventStandard
from common.eventpattern import BasicPattern, fromNibbles
from . import ControlSurface, IValueStrategy

class NoteValueStrategy(IValueStrategy):
    """
    The strategy to get data values from note events
    """
    def getValueFromEvent(self, event: eventData) -> int:
        assert isEventStandard(event)
        if 0x80 <= event.status < 0x90:
            return 0
        else:
            return event.data2
    
    def getFloatFromValue(self, value: int) -> float:
        return value / 127
    
    def getValueFromFloat(self, f: float) -> int:
        return int(f * 127)

class Note(ControlSurface):
    """
    Represents a note event, usually linked to a key press on a piano
    """
    def __init__(self, note_num: int, channel:int = 0) -> None:
        super().__init__(
            BasicPattern(fromNibbles((8, 9), channel), note_num, ...),
            NoteValueStrategy(),
            "notes",
            (channel, note_num)
        )

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
