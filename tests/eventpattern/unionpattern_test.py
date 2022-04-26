"""
tests > eventpattern > test_unionpattern

Tests for union pattern matching
"""

import pytest

from common.eventpattern import BasicPattern, UnionPattern
from common.types import EventData


def test_create_not_enough():
    with pytest.raises(ValueError):
        UnionPattern()
    with pytest.raises(ValueError):
        UnionPattern(BasicPattern(1, 2, 3))


def test_union():
    p = UnionPattern(
        BasicPattern(1, 2, 3),
        BasicPattern(4, 5, 6),
        BasicPattern(7, 8, 9)
    )

    # Make sure it matches
    assert p.matchEvent(EventData(1, 2, 3))
    assert p.matchEvent(EventData(4, 5, 6))
    assert p.matchEvent(EventData(7, 8, 9))

    # And make sure it doesn't match anything else
    assert not p.matchEvent(EventData([1, 2, 3]))
    assert not p.matchEvent(EventData(2, 3, 4))


def test_union_sysex():
    p = UnionPattern(
        BasicPattern(1, 2, 3),
        BasicPattern([1, 2, 3])
    )

    # Make sure it matches
    assert p.matchEvent(EventData(1, 2, 3))
    assert p.matchEvent(EventData([1, 2, 3]))

    # And make sure it doesn't match anything else
    assert not p.matchEvent(EventData(4, 5, 6))
