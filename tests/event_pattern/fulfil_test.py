"""
tests > event_pattern > fulfil_test

Tests to ensure that event patterns are fulfilled

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import pytest
from fl_classes import FlMidiMsg
from tests.helpers.devices import DummyDeviceContext
from control_surfaces.event_patterns import (
    IEventPattern,
    BasicPattern,
    ForwardedPattern,
    ForwardedUnionPattern,
    UnionPattern,
    NullPattern,
    NotePattern,
)


def test_basic():
    assert BasicPattern(1, 2, 3).fulfil() == FlMidiMsg(1, 2, 3)


def test_range():
    r = range(10, 20)
    e = BasicPattern(1, 2, r).fulfil()
    assert e.data2 in r


def test_tuple():
    t = 2, 7, 3, 19, 49
    e = BasicPattern(1, 2, t).fulfil()
    assert e.data2 in t


def test_ellipsis():
    e = BasicPattern(1, 2, ...).fulfil()
    assert e.data2 in range(128)


@pytest.mark.parametrize(
    "pattern", [
        BasicPattern(1, ..., 5),
        ForwardedPattern(2, BasicPattern([1, 2, 3, 4, 5, 6, ...])),
        UnionPattern(BasicPattern([1]), BasicPattern(4, 5, 6)),
        NotePattern(127),
        ForwardedUnionPattern(2, UnionPattern(
            BasicPattern(1, 2, 3),
            BasicPattern(4, 5, 6)
        )),
    ]
)
def test_others(pattern: IEventPattern):
    with DummyDeviceContext():
        assert pattern.matchEvent(pattern.fulfil())


def test_no_fulfillment():
    """Null patterns are impossible to fulfil"""
    with pytest.raises(TypeError):
        NullPattern().fulfil()
