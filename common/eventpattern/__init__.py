"""
common > eventpattern

Contains code for pattern matching with MIDI events, including IEventPattern,
a simple way to match events, and IEventPattern, and interface from which
custom pattern matchers can be derived.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'ByteMatch',
    'fromNibbles',
    'IEventPattern',
    'UnionPattern',
    'BasicPattern',
    'ForwardedPattern',
    'ForwardedUnionPattern',
    'NullPattern',
    'NotePattern'
]

from .bytematch import ByteMatch, fromNibbles
from .ieventpattern import IEventPattern
from .unionpattern import UnionPattern
from .basicpattern import BasicPattern
from .forwardedpattern import ForwardedPattern, ForwardedUnionPattern
from .nullpattern import NullPattern
from .notepattern import NotePattern
