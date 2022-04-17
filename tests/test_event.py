"""
tests > test_event

Tests for events

Authors:
* Miguel Guthridge
"""

from common.types.eventdata import (
    EventData,
    isEventStandard,
    isEventSysex
)


def test_event_filter_standard():
    assert isEventStandard(EventData(1, 2, 3))
    assert not isEventSysex(EventData(4, 5, 6))


def test_event_filter_sysex():
    assert isEventSysex(EventData([1, 2, 3]))
    assert not isEventStandard(EventData([4, 5, 6]))
