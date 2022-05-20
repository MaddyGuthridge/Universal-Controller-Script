"""
common > event_pattern > note_pattern

Contains the definition for the NotePattern class

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

from . import BasicPattern
from .byte_match import fromNibbles, ByteMatch


class NotePattern(BasicPattern):
    """
    The note pattern is used as a way to recognize note events
    """

    def __init__(self, note_num: int, channel_match: ByteMatch = ...) -> None:
        """
        Create a NotePattern, in order to recognize note events.

        ### Args:
        * `note_num` (`int`): note number to recognize
        """
        super().__init__(fromNibbles((8, 9), channel_match), note_num, ...)
