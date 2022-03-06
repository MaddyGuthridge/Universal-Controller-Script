"""
common > eventpattern > notepattern

Contains the definition for the NotePattern class

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

from . import BasicPattern
from .bytematch import fromNibbles

class NotePattern(BasicPattern):
    """
    The note pattern is used as a way to recognise note events
    """
    def __init__(self, note_num: int) -> None:
        """
        Create a NotePattern

        ### Args:
        * `note_num` (`int`): note number to recognise
        """
        super().__init__(fromNibbles((8, 9), ...), note_num, ...)
