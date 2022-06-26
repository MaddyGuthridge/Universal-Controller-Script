"""
tests > event_pattern > forward_test

Tests for forwarded event pattern matching

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import (
    BasicPattern,
    ForwardedPattern,
    ForwardedUnionPattern,
)
from fl_classes import FlMidiMsg
from common.util.events import encodeForwardedEvent

from tests.helpers.devices import DummyDeviceContext


def test_forwarded():
    with DummyDeviceContext():
        p = ForwardedPattern(2, BasicPattern(1, 2, 3))
        e = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(1, 2, 3), 2))
        assert p.matchEvent(e)
        assert not p.matchEvent(FlMidiMsg(1, 2, 3))


def test_union():
    with DummyDeviceContext():
        p = ForwardedUnionPattern(2, BasicPattern(1, 2, 3))
        e = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(1, 2, 3), 2))
        assert p.matchEvent(e)
        assert p.matchEvent(FlMidiMsg(1, 2, 3))
        e = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(1, 2, 3), 3))
        assert not p.matchEvent(e)
