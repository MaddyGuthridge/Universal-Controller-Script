"""
common > eventpattern > forwardedpattern

Contains the definition for the ForwardedPattern class

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

from common.util.events import decodeForwardedEvent, isEventForwardedHereFrom
from . import IEventPattern, UnionPattern

from common.types import EventData

class ForwardedPattern(IEventPattern):
    """
    The forwarded pattern is used to parse data from events which were forwarded
    from the Universal Event Forwarded device script.

    This decodes the forwarded event, then checks it against another provided
    pattern.

    This allows events to all be processed on the same script, which massively
    simplifies things. Refer to device_eventforward.py for a reference on
    how the event is stored.
    """
    def __init__(self, device_num: int, pattern: IEventPattern) -> None:
        """
        Create a ForwardedPattern recogniser. This is used to pattern match with
        events that were forwarded from the Universal Event Forwarder.

        ### Args:
        * `device_num` (`int`): device number to accept events from
        * `pattern` (`IEventPattern`): pattern to detect from
        """
        super().__init__()
        self._device_num = device_num
        self._pattern = pattern

    def matchEvent(self, event: 'EventData') -> bool:
        # Check if the event was forwarded here
        if not isEventForwardedHereFrom(event, self._device_num):
            return False

        # Extract the event and determine if it matches with the
        # underlying pattern
        # print(eventToString(eventFromForwarded(event, null+2)))
        return self._pattern.matchEvent(decodeForwardedEvent(event))

class ForwardedUnionPattern(IEventPattern):
    """
    Represents an event that can either be forwarded or direct.
    """

    def __init__(self, device_num: int, pattern: IEventPattern) -> None:
        """
        Create a ForwardedUnionPattern recogniser

        ### Args:
        * `device_num` (`int`): device number to recognise
        * `pattern` (`IEventPattern`): pattern to match
        """
        self._pattern = UnionPattern(pattern, ForwardedPattern(device_num, pattern))

    def matchEvent(self, event: 'EventData') -> bool:
        return self._pattern.matchEvent(event)
