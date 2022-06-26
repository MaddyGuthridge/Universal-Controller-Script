"""
tests > event_pattern > basic_pattern_test

Tests for basic event pattern matching

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern
from fl_classes import FlMidiMsg


def test_basic_pattern():
    p = BasicPattern(10, 10, 10)
    assert p.matchEvent(FlMidiMsg(10, 10, 10))
    assert not p.matchEvent(FlMidiMsg(11, 10, 10))


def test_range_pattern():
    p = BasicPattern(range(10, 20), 4, 5)
    assert p.matchEvent(FlMidiMsg(13, 4, 5))
    assert not p.matchEvent(FlMidiMsg(20, 4, 5))


def test_tuple_pattern():
    p = BasicPattern((5, 12, 20), 4, 5)
    assert p.matchEvent(FlMidiMsg(12, 4, 5))
    assert not p.matchEvent(FlMidiMsg(13, 4, 5))


def test_ellipsis_pattern():
    p = BasicPattern(..., 4, 5)
    assert p.matchEvent(FlMidiMsg(12, 4, 5))
    assert not p.matchEvent(FlMidiMsg(128, 4, 5))


def test_sysex_pattern():
    p = BasicPattern([1, 3, 5, 7])
    assert p.matchEvent(FlMidiMsg([1, 3, 5, 7]))
    assert not p.matchEvent(FlMidiMsg(1, 3, 5))

    p2 = BasicPattern(10, 10, 10)
    assert not p2.matchEvent(FlMidiMsg([1, 3, 5, 7]))
