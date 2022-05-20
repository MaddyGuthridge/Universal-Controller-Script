"""
tests > event_pattern > fulfil_test

Tests to ensure that event patterns are fulfilled
"""
import pytest
from common.types import EventData
from tests.helpers.devices import DummyDeviceContext
from control_surfaces.event_patterns import (
    fulfil,
    IEventPattern,
    BasicPattern,
    ForwardedPattern,
    ForwardedUnionPattern,
    UnionPattern,
    NullPattern,
    NotePattern,
)


def test_basic():
    assert fulfil(BasicPattern(1, 2, 3)) == EventData(1, 2, 3)


def test_range():
    r = range(10, 20)
    e = fulfil(BasicPattern(1, 2, r))
    assert e.data2 in r


def test_tuple():
    t = 2, 7, 3, 19, 49
    e = fulfil(BasicPattern(1, 2, t))
    assert e.data2 in t


def test_ellipsis():
    e = fulfil(BasicPattern(1, 2, ...))
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
        assert pattern.matchEvent(fulfil(pattern))


def test_no_fulfillment():
    """Null patterns are impossible to fulfil"""
    with pytest.raises(TypeError):
        fulfil(NullPattern())
