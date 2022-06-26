"""
common > util > events

Contains useful functions for operating on events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING
import common
import device
from fl_classes import FlMidiMsg, isMidiMsgStandard, isMidiMsgSysex
from common.exceptions import (
    EventEncodeError,
    EventInspectError,
    EventDecodeError,
    EventDispatchError,
)


def getDeviceId() -> str:
    """
    Get the identifier of a device

    ### Returns:
    * `str`: device number of an auxiliary device
    """
    return common.getContext().getDevice().getId()


def getDeviceNum() -> int:
    """
    Determine the number of auxiliary devices that are connected using the
    Universal Event Forwarder

    ### Returns:
    * `int`: device number of an auxiliary device
    """
    return common.getContext().getDevice().getDeviceNumber()


def isEventForwarded(event: FlMidiMsg) -> bool:
    """
    Returns whether an event was forwarded from the Universal Event Forwarder
    script

    Note that the event isn't necessarily directed towards this device

    ### Args:
    * `event` (`FlMidiMsg`): event to check

    ### Returns:
    * `bool`: whether it was forwarded
    """
    # Check if the event is a forwarded one
    # Look for 0xF0 and 0x7D
    if not isMidiMsgSysex(event) \
            or not event.sysex.startswith(bytes([0xF0, 0x7D])):
        return False
    else:
        return True


def getForwardedEventHeader() -> bytes:
    """
    Returns a header for a forwarded event

    ### Returns:
    * `bytes`: event header
    """
    return bytes([
        0xF0,  # Start sysex
        0x7D  # Non-commercial sysex ID
    ]) + getDeviceId().encode() \
       + bytes([0])


def encodeForwardedEvent(event: FlMidiMsg, device_num: int = -1) -> bytes:
    """
    Encode an event such that it can be forwarded to the main script from
    auxiliary scripts or to an auxiliary script from the main script

    ### Args:
    * `event` (`FlMidiMsg`): event to encode
    * `device_num` (`int`, optional): device number to target. Defaults to
      `-1`.

    ### Raises:
    * `ValueError`: no target specified on main script (or forwarding from
    invalid device)

    ### Returns:
    * `bytes`: encoded event data
    """
    if device_num == -1:
        device_num = getDeviceNum()
        if device_num == 1:
            # TODO: Use a custom exception type to improve error checking
            raise EventEncodeError(
                "Either forwarding from an invalid device or target device "
                "number is unspecified"
            )

    sysex = getForwardedEventHeader() + bytes([device_num])

    if isMidiMsgStandard(event):
        return sysex + bytes([0]) + bytes([
            event.data2,
            event.data1,
            event.status,
            0xF7
        ])
    else:
        if TYPE_CHECKING:  # TODO: Find a way to make this unnecessary
            assert isMidiMsgSysex(event)
        return sysex + bytes([1]) + bytes(event.sysex)


def _getForwardedNameEndIdx(event: FlMidiMsg) -> int:
    """
    Returns the index of the null zero of a forwarded event's name

    ### Args:
    * `event` (`FlMidiMsg`): event

    ### Returns:
    * `int`: index of null zero
    """
    assert isMidiMsgSysex(event)
    return event.sysex.index(b'\0')


def getEventForwardedTo(event: FlMidiMsg) -> str:
    """
    Returns the name of the device that this event is targeting

    ### Args:
    * `event` (`FlMidiMsg`): event

    ### Returns:
    * `str`: device name
    """
    assert isMidiMsgSysex(event)
    return event.sysex[2:_getForwardedNameEndIdx(event)].decode()


def isEventForwardedHere(event: FlMidiMsg) -> bool:
    """
    Returns whether an event was forwarded from the Universal Event Forwarder
    script from a controller directed to this particular script

    ### Args:
    * `event` (`FlMidiMsg`): event to check

    ### Returns:
    * `bool`: whether it was forwarded
    """
    if not isEventForwarded(event):
        return False

    if (
        getEventForwardedTo(event)
        != getDeviceId()
    ):
        return False
    return True


def getEventDeviceNum(event: FlMidiMsg) -> int:
    """
    Returns the device number that a forwarded event is targeting or from

    ### Args:
    * `event` (`FlMidiMsg`): event

    ### Returns:
    * `int`: device number
    """
    assert isMidiMsgSysex(event)
    return event.sysex[_getForwardedNameEndIdx(event) + 1]


def isEventForwardedHereFrom(event: FlMidiMsg, device_num: int = -1) -> bool:
    """
    Returns whether an event was forwarded from a particular instance of the
    Universal Event Forwarder script, or is directed to a controller with this
    device number

    ### Args:
    * `event` (`FlMidiMsg`): event to check
    * `device_num` (`int`, optional): device number to match (defaults to the
      device number of this script, must be provided on main script)

    ### Returns:
    * `bool`: whether it was forwarded
    """
    if device_num == -1:
        device_num = getDeviceNum()
        if device_num == 1:
            raise EventInspectError(
                "No target device specified from main script"
            )

    if not isEventForwardedHere(event):
        return False

    if device_num != getEventDeviceNum(event):
        return False

    return True


def decodeForwardedEvent(event: FlMidiMsg, type_idx: int = -1) -> FlMidiMsg:
    """
    Given a forwarded event, decode it and return the original event

    This function assumes that the event is already proven to be forwarded,
    so no additional checks are made.

    ### Args:
    * `event` (`FlMidiMsg`): event to decode
    * `type_idx` (`int`, optional): index of event type flag, if known.
      Defaults to `-1`.

    ### Returns:
    * `FlMidiMsg`: decoded data
    """
    if not isEventForwarded(event):
        raise EventDecodeError(f"Event not forwarded: {eventToString(event)}")
    assert isMidiMsgSysex(event)
    if type_idx == -1:
        type_idx = _getForwardedNameEndIdx(event) + 2

    if event.sysex[type_idx]:
        # Remaining bytes are sysex data
        return FlMidiMsg(list(event.sysex[type_idx + 1:]))
    else:
        # Extract (data2, data1, status)
        return FlMidiMsg(
            event.sysex[type_idx + 3],
            event.sysex[type_idx + 2],
            event.sysex[type_idx + 1]
        )


def forwardEvent(event: FlMidiMsg, device_num: int = -1):
    """
    Encode a forwarded event and send it to all available devices

    ### Args:
    * `event` (`FlMidiMsg`): event to encode and forward
    * `device_num` (`int`, optional): target device number if on main script
    """
    if device_num == -1:
        device_num = getDeviceNum()
        if device_num == 1:
            raise EventEncodeError(
                "No target device specified from main script"
            )
    output = encodeForwardedEvent(event, device_num)
    # Dispatch to all available devices
    if device.dispatchReceiverCount() == 0:
        raise EventDispatchError(
            f"Unable to forward event to/from device {device_num}."
            f" Is the controller configured correctly?"
        )
    for i in range(device.dispatchReceiverCount()):
        device.dispatch(i, 0xF0, output)


def eventToRawData(event: FlMidiMsg) -> 'int | bytes':
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


def bytesToString(bytes_iter: bytes) -> str:
    """
    Convert bytes to a fancy formatted string

    ### Args:
    * `b` (`bytes`): bytes to stringify

    ### Returns:
    * `str`: formatted string
    """
    return f"[{', '.join(f'0x{b:02X}' for b in bytes_iter)}]"


def eventToString(event: FlMidiMsg) -> str:
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
        if not isEventForwarded(event):
            return bytesToString(event.sysex)
        dev = getEventForwardedTo(event)
        num = getEventDeviceNum(event)
        decoded = eventToString(decodeForwardedEvent(event))
        return f"{dev}@{num} => {decoded})"
