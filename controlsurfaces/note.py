"""
controlsurfaces > note

Contains the definition of the Note class, which represents note events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.types.eventdata import EventData, isEventStandard
from common.eventpattern import BasicPattern, fromNibbles
from . import ControlSurface, NoteStrategy


class Note(ControlSurface):
    """
    Represents a note event, usually linked to a key press on a piano
    """
    def __init__(self, note_num: int, channel:int = 0) -> None:
        super().__init__(
            BasicPattern(fromNibbles((8, 9), ...), note_num, ...),
            NoteStrategy(),
            "notes",
            (channel, note_num)
        )

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
