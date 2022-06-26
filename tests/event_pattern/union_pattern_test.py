"""
tests > event_pattern > union_pattern_test

Tests for union pattern matching

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import pytest

from control_surfaces.event_patterns import BasicPattern, UnionPattern
from fl_classes import FlMidiMsg


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
    assert p.matchEvent(FlMidiMsg(1, 2, 3))
    assert p.matchEvent(FlMidiMsg(4, 5, 6))
    assert p.matchEvent(FlMidiMsg(7, 8, 9))

    # And make sure it doesn't match anything else
    assert not p.matchEvent(FlMidiMsg([1, 2, 3]))
    assert not p.matchEvent(FlMidiMsg(2, 3, 4))


def test_union_sysex():
    p = UnionPattern(
        BasicPattern(1, 2, 3),
        BasicPattern([1, 2, 3])
    )

    # Make sure it matches
    assert p.matchEvent(FlMidiMsg(1, 2, 3))
    assert p.matchEvent(FlMidiMsg([1, 2, 3]))

    # And make sure it doesn't match anything else
    assert not p.matchEvent(FlMidiMsg(4, 5, 6))
