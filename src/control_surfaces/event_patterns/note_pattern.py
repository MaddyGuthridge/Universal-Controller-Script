"""
control_surfaces > event_patterns > note_pattern

Contains the definition for the NotePattern class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
