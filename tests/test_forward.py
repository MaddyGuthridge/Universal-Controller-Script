"""
tests > test_forward

Tests for forwarded messages, including encoding and decoding

Authors:
* Miguel Guthridge
"""

from common.types import EventData
from common.util.events import (
    encodeForwardedEvent,
    decodeForwardedEvent,
    isEventForwarded
)

def test_encode_decode():
    """When an event is encoded then decoded, is it still equivalent?"""
    e = EventData(1, 2, 3)
    assert e == decodeForwardedEvent(EventData(encodeForwardedEvent(e, 1)))
    
    e = EventData([5, 2, 7, 4, 1])
    assert e == decodeForwardedEvent(EventData(encodeForwardedEvent(e, 1)))

def test_isEventForwarded():
    """Make sure the forwarded event type checker is working"""
    assert isEventForwarded(EventData(encodeForwardedEvent(EventData(1, 2, 3), 1)))
