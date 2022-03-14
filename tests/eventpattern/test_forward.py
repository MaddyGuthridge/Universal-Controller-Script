"""
tests > eventpattern > test_forward

Tests for forwarded event pattern matching
"""

from fl_context import FlContext

from common.eventpattern import (
    BasicPattern,
    ForwardedPattern,
    ForwardedUnionPattern,
)
from common.types import EventData
from common.util.events import encodeForwardedEvent

def test_forwarded():
    p = ForwardedPattern(2, BasicPattern(1, 2, 3))
    e = EventData(encodeForwardedEvent(EventData(1, 2, 3), 2))
    assert p.matchEvent(e)
    assert not p.matchEvent(EventData(1, 2, 3))

def test_union():
    p = ForwardedUnionPattern(2, BasicPattern(1, 2, 3))
    e = EventData(encodeForwardedEvent(EventData(1, 2, 3), 2))
    assert p.matchEvent(e)
    assert p.matchEvent(EventData(1, 2, 3))
    e = EventData(encodeForwardedEvent(EventData(1, 2, 3), 3))
    assert not p.matchEvent(e)
