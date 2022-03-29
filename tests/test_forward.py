"""
tests > test_forward

Tests for forwarded messages, including encoding and decoding

Authors:
* Miguel Guthridge
"""

import pytest

from fl_context import FlContext

from common.types import EventData
from common.util.events import (
    encodeForwardedEvent,
    decodeForwardedEvent,
    isEventForwarded,
    isEventForwardedHere,
    isEventForwardedHereFrom
)


def test_encode_decode():
    """When an event is encoded then decoded, is it still equivalent?"""
    e = EventData(1, 2, 3)
    assert e == decodeForwardedEvent(EventData(encodeForwardedEvent(e, 1)))

    e = EventData([5, 2, 7, 4, 1])
    assert e == decodeForwardedEvent(EventData(encodeForwardedEvent(e, 1)))


def test_invalid_event_forward():
    """Test that forwarding an event without specifying a target fails from
    the main script
    """
    with pytest.raises(ValueError):
        encodeForwardedEvent(EventData(1, 2, 3))


def test_invalid_event_receive():
    """Test that receiving a forwarded event fails on the main script when
    no from index is specified
    """
    with FlContext({"device_name": "MIDIIN2 (My Device)"}):
        e = EventData(encodeForwardedEvent(EventData(1, 2, 3)))
    with pytest.raises(ValueError):
        assert isEventForwardedHereFrom(e)


def test_isEventForwarded():
    """Make sure the forwarded event type checker is working"""
    assert isEventForwarded(
        EventData(encodeForwardedEvent(EventData(1, 2, 3), 1)))

    assert not isEventForwarded(EventData(1, 2, 3))


def test_isEventForwardedHere():
    with FlContext({"device_name": "MIDIIN2 (My Device)"}):
        e = EventData(encodeForwardedEvent(EventData(1, 2, 3)))

    with FlContext({"device_name": "My Device"}):
        assert isEventForwardedHere(e)

    with FlContext({"device_name": "My Other Device"}):
        assert not isEventForwardedHere(e)


def test_isEventForwardedHereFrom():
    with FlContext({"device_name": "MIDIIN2 (My Device)"}):
        e = EventData(encodeForwardedEvent(EventData(1, 2, 3)))

    with FlContext({"device_name": "My Device"}):
        assert isEventForwardedHereFrom(e, 2)

    with FlContext({"device_name": "My Device"}):
        assert not isEventForwardedHereFrom(e, 3)


def test_isEventForwardedHereFrom_target():
    with FlContext({"device_name": "My Device"}):
        e = EventData(encodeForwardedEvent(EventData(1, 2, 3), 2))

    with FlContext({"device_name": "MIDIIN2 (My Device)"}):
        assert isEventForwardedHereFrom(e)


def testForwardChecking():
    """Make sure checks are put into place before we forward an event"""
    with FlContext({"device_name": "MIDIIN2 (My Device)"}):
        # FIXME: Fails because of dispatch receiver count
        # forwardEvent(EventData(7, 8, 9))
        pass
