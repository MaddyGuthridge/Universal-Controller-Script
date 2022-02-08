"""
common > eventpattern > forwardedpattern

Contains the definition for the ForwardedPattern class

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

import device
from typing import TYPE_CHECKING

from common.util.events import eventFromForwarded, isEventForwardedHereFrom, eventToString
from . import IEventPattern

from common.types import eventData

class ForwardedPattern(IEventPattern):
    """
    The forwarded pattern is used to parse data from events which were forwarded
    from the Universal Event Forwarded device script.

    This allows events to all be processed on the same script, which massively
    simplifies things. Refer to device_eventforward.py for a reference on
    how the event is stored.
    """
    def __init__(self, device_num: int, pattern: IEventPattern) -> None:
        """
        Create a ForwardedPattern recogniser

        ### Args:
        * `device_num` (`int`): device number to accept events from
        * `pattern` (`IEventPattern`): pattern to detect from
        """
        super().__init__()
        self._device_num = device_num
        self._pattern = pattern
    
    def matchEvent(self, event: 'eventData') -> bool:
        # Check if the event was forwarded here
        if not isEventForwardedHereFrom(event, self._device_num):
            return False
        
        # Extract the event and determine if it matches with the
        # underlying pattern
        # print(eventToString(eventFromForwarded(event, null+2)))
        return self._pattern.matchEvent(eventFromForwarded(event))
