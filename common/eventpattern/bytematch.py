"""
common > eventpattern > bytematch

Contains the definition for the byte-match type expression, as well as helper
functions for creating event patterns.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import TYPE_CHECKING, Type, Union
if TYPE_CHECKING:
    from collections.abc import Iterable

EllipsisType: Type = type(Ellipsis)

# Variable type for byte match expression
ByteMatch = Union[int, range, tuple[int, ...], 'ellipsis']

def fromNibbles(upper: ByteMatch, lower: ByteMatch) -> tuple:
    """
    Returns a ByteMatch expression from two nibble ByteMatches

    ### Args:
    * `upper` (`ByteMatch`): upper nibble
    * `lower` (`ByteMatch`): lower nibble

    ### Returns:
    * `tuple`: combined ByteMatch
    """
    def toIter(b: ByteMatch) -> 'Iterable[int]':
        """
        Convert a bytematch to an iterable
        """
        if isinstance(b, int):
            return [b]
        elif b is ...:
            return [i for i in range(16)]
        else:
            if TYPE_CHECKING:
                assert not isinstance(b, ellipsis)
            return b
    u = toIter(upper)
    l = toIter(lower)
    ret = []
    for i in u:
        for j in l:
            ret.append((i << 4) + j)
    return (*ret,)
