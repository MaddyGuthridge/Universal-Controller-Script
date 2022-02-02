"""
common > eventpattern > forwardedpattern

Contains the definition for the ForwardedPattern class

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

import device
from typing import TYPE_CHECKING
from . import IEventPattern

from common.types import eventData

class ForwardedEventPattern(IEventPattern):
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
        # Check if the event is a forwarded one
        # Look for 0xF0 and 0x7D
        if event.sysex is None \
            or not event.sysex.startswith(bytes([0xF0, 0x7D])):
                return False
        
        # Check if it matches this device's name
        null = event.sysex[2:].find(bytes(0))
        if event.sysex[2:null].decode() != device.getName():
            return False
        
        # Check if it matches the expected device number
        if self._device_num != event.sysex[null+1]:
            return False
        
        # If we reach this point, it's a forwarded event that matches this
        # device. Extract the event to determine if it matches with the
        # underlying pattern
        
        # First check if it's a sysex event
        if event.sysex[null+2]:
            # Remaining bytes are sysex data
            decoded = eventData(list(event.sysex[null+3:]))
        else:
            # Extract (data2, data1, status)
            decoded = eventData(
                event.sysex[null+5],
                event.sysex[null+4],
                event.sysex[null+3]
            )
        
        return super().matchEvent(decoded)
