"""
tests > test_eventpattern

Tests for event pattern matching
"""

from common.eventpattern import EventPattern
from common.types import eventData

def test_basic_pattern():
    p = EventPattern(10, 10, 10)
    assert p.matchEvent(eventData(10, 10, 10))
    assert not p.matchEvent(eventData(11, 10, 10))

def test_range_pattern():
    p = EventPattern(range(10, 20), 4, 5)
    assert p.matchEvent(eventData(13, 4, 5))
    assert not p.matchEvent(eventData(20, 4, 5))
    
def test_tuple_pattern():
    p = EventPattern((5, 12, 20), 4, 5)
    assert p.matchEvent(eventData(12, 4, 5))
    assert not p.matchEvent(eventData(13, 4, 5))
    
def test_ellipsis_pattern():
    p = EventPattern(..., 4, 5)
    assert p.matchEvent(eventData(12, 4, 5))
    assert not p.matchEvent(eventData(128, 4, 5))

def test_sysex_pattern():
    p = EventPattern([1, 3, 5, 7])
    assert p.matchEvent(eventData([1, 3, 5, 7]))
    assert not p.matchEvent(eventData(1, 3, 5))
    
    p2 = EventPattern(10, 10, 10)
    assert not p2.matchEvent(eventData([1, 3, 5, 7]))
    
