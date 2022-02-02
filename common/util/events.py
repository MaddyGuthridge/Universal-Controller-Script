"""
common > util > events

Contains useful functions for operating on events.
"""

from common.types import eventData

from typing import TYPE_CHECKING

def eventFromForwarded(event: eventData, type_idx:int=-1) -> eventData:
    """
    Given a forwarded event, decode it and return the original event

    This function assumes that the event is already proven to be forwarded,
    so no additional checks are made.

    ### Args:
    * `event` (`eventData`): event to decode
    * `type_idx` (`int`, optional): index of event type flag, if known. 
      Defaults to `-1`.

    ### Returns:
    * `eventData`: decoded data
    """
    assert event.sysex is not None
    if type_idx == -1:
        type_idx = event.sysex.index(b'\0')
    
    if event.sysex[type_idx]:
        # Remaining bytes are sysex data
        return eventData(list(event.sysex[type_idx+1:]))
    else:
        # Extract (data2, data1, status)
        return eventData(
            event.sysex[type_idx+3],
            event.sysex[type_idx+2],
            event.sysex[type_idx+1]
        )

def eventToRawData(event: eventData) -> 'int | bytes':
    """
    Convert event to raw data.

    For standard events data is presented as little-endian, meaning that the
    status byte has the lowest component value in the integer.

    ### Returns:
    * `int | bytes`: data
    """
    if event.sysex is None:
        if TYPE_CHECKING:
            assert event.status is not None
            assert event.data1 is not None
            assert event.data2 is not None
        return (event.status) + (event.data1 << 8) + (event.data2 << 16)
    else:
        return event.sysex

def bytesToString(bytes_iter: bytes) -> str:
    """
    Convert bytes to a fancy formatted string

    ### Args:
    * `b` (`bytes`): bytes to stringify

    ### Returns:
    * `str`: formatted string
    """
    return f"[{', '.join(f'0x{b:02X}' for b in bytes_iter)}]"

def eventToString(event: eventData) -> str:
    """
    Convert event to string

    ### Args:
    * `event` (`eventData`): event

    ### Returns:
    * `str`: stringified
    """
    if event.sysex is None:
        if TYPE_CHECKING:
            assert event.status is not None
            assert event.data1 is not None
            assert event.data2 is not None
        return f"(0x{event.status:02X}, 0x{event.data1:02X}, 0x{event.data2:02X})"
    else:
        return bytesToString(event.sysex)
