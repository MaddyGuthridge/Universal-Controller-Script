"""
control_surfaces > controls > note

Contains the definition of the Note class, which represents note events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces.event_patterns import ByteMatch
from ..event_patterns import NotePattern
from . import ControlSurface
from ..value_strategies import NoteStrategy


class Note(ControlSurface):
    """
    Represents a note event, usually linked to a key press on a piano
    """
    def __init__(self, note_num: int, channels: ByteMatch = ...) -> None:
        super().__init__(
            NotePattern(note_num, channels),
            NoteStrategy(),
            (0, note_num)
        )

    @staticmethod
    def isPress(value: float):
        return value != 0

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
