"""
controlsurfaces > note

Contains the definition of the Note class, which represents note events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from ..eventpatterns import NotePattern
from . import ControlSurface
from ..valuestrategies import NoteStrategy


class Note(ControlSurface):
    """
    Represents a note event, usually linked to a key press on a piano
    """
    def __init__(self, note_num: int, channel: int = 0) -> None:
        super().__init__(
            NotePattern(note_num),
            NoteStrategy(),
            (channel, note_num)
        )

    @staticmethod
    def isPress(value: float):
        return value != 0

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
