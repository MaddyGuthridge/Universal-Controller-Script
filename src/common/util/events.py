"""
common > util > events

Contains useful functions for operating on events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg, isMidiMsgStandard, isMidiMsgSysex
from .forwarded_events import (
    is_event_forwarded,
    get_forwarded_origin_device,
    get_forwarded_target_device,
    decode_forwarded_event,
)


def event_to_raw_data(event: FlMidiMsg) -> 'int | bytes':
    """
    Convert event to raw data.

    For standard events data is presented as little-endian, meaning that the
    status byte has the lowest component value in the integer.

    ### Returns:
    * `int | bytes`: data
    """
    if isMidiMsgStandard(event):
        return (event.status) + (event.data1 << 8) + (event.data2 << 16)
    else:
        assert isMidiMsgSysex(event)
        return event.sysex


def bytes_to_string(bytes_iter: bytes) -> str:
    """
    Convert bytes to a fancy formatted string

    ### Args:
    * `b` (`bytes`): bytes to stringify

    ### Returns:
    * `str`: formatted string
    """
    return f"[{', '.join(f'0x{b:02X}' for b in bytes_iter)}]"


def event_to_string(event: FlMidiMsg) -> str:
    """
    Convert event to string

    ### Args:
    * `event` (`FlMidiMsg`): event

    ### Returns:
    * `str`: stringified
    """
    if isMidiMsgStandard(event):
        return (
            f"(0x{event.status:02X}, 0x{event.data1:02X}, 0x{event.data2:02X})"
        )
    else:
        assert isMidiMsgSysex(event)
        if not is_event_forwarded(event):
            return bytes_to_string(event.sysex)
        origin = get_forwarded_origin_device(event)
        target = get_forwarded_target_device(event)
        decoded = event_to_string(decode_forwarded_event(event))
        return f"{origin}->{target} | {decoded})"
