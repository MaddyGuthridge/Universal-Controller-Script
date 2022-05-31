"""
tests > test_event

Tests for events

Authors:
* Miguel Guthridge

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.types.event_data import (
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
