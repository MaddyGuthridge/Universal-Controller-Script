"""
common > util > forwarded_events

Contains code for forwarding events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import device
from typing import TYPE_CHECKING, Optional, Union
from fl_classes import FlMidiMsg, isMidiMsgStandard, isMidiMsgSysex
from common.exceptions import EventDispatchError


EVENT_HEADER = bytes([
    0xF0,  # Start sysex
    0x7D  # Non-commercial sysex ID
])
TARGET_INDEX = 2
ORIGIN_INDEX = 3
IS_SYSEX_INDEX = 4


def is_event_forwarded(event: FlMidiMsg) -> bool:
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
            or not event.sysex.startswith(EVENT_HEADER):
        return False
    else:
        return True


def forward_event_to_main(event: FlMidiMsg, origin: int) -> None:
    sysex = EVENT_HEADER + bytes([0, origin])
    if isMidiMsgStandard(event):
        encoded = sysex + bytes([0]) + bytes([
            event.data2,
            event.data1,
            event.status,
            0xF7
        ])
    else:
        if TYPE_CHECKING:  # TODO: Find a way to make this unnecessary
            assert isMidiMsgSysex(event)
        encoded = sysex + bytes([1]) + bytes(event.sysex)
    # Dispatch to all available devices
    if device.dispatchReceiverCount() == 0:
        raise EventDispatchError(
            "Unable to forward event to main device."
            " Is the controller configured correctly?"
        )
    # Send it to all devices, and make sure they
    for i in range(device.dispatchReceiverCount()):
        encoded.dispatch(i, 0xF0, encoded)


def forward_event_to_external(event: FlMidiMsg, target: int) -> None:
    sysex = EVENT_HEADER + bytes([target, 0])
    if isMidiMsgStandard(event):
        encoded = sysex + bytes([0]) + bytes([
            event.data2,
            event.data1,
            event.status,
            0xF7
        ])
    else:
        # We need this check, because there is no better way to do it sadly
        # https://stackoverflow.com/a/71252167/6335363
        if TYPE_CHECKING:
            assert isMidiMsgSysex(event)
        encoded = sysex + bytes([1]) + bytes(event.sysex)
    # Dispatch to all available devices
    if device.dispatchReceiverCount() == 0:
        raise EventDispatchError(
            f"Unable to forward event to device {target}."
            f" Is the controller configured correctly?"
        )
    # Send it to all devices, and make sure they
    for i in range(device.dispatchReceiverCount()):
        encoded.dispatch(i, 0xF0, encoded)


def receive_event_from_origin(
    event: FlMidiMsg,
    device_num: int,
) -> Optional[FlMidiMsg]:
    if not is_event_forwarded(event):
        return None
    assert isMidiMsgSysex(event)

    if event.sysex[TARGET_INDEX] != device_num:
        return None

    if event.sysex[IS_SYSEX_INDEX] == 1:
        # Remaining bytes are sysex data
        return FlMidiMsg(list(event.sysex[IS_SYSEX_INDEX + 1:]))
    else:
        # Extract (data2, data1, status)
        return FlMidiMsg(
            event.sysex[IS_SYSEX_INDEX + 3],
            event.sysex[IS_SYSEX_INDEX + 2],
            event.sysex[IS_SYSEX_INDEX + 1]
        )


def receive_event_from_external(
    event: FlMidiMsg,
) -> Optional[Union[FlMidiMsg, int]]:
    if not is_event_forwarded(event):
        return None
    assert isMidiMsgSysex(event)

    # If it isn't targeting the main script
    if event.sysex[TARGET_INDEX] != 0:
        return None

    origin = event.sysex[ORIGIN_INDEX]

    if event.sysex[IS_SYSEX_INDEX] == 1:
        # Remaining bytes are sysex data
        return FlMidiMsg(list(event.sysex[IS_SYSEX_INDEX + 1:])), origin
    else:
        # Extract (data2, data1, status)
        return FlMidiMsg(
            event.sysex[IS_SYSEX_INDEX + 3],
            event.sysex[IS_SYSEX_INDEX + 2],
            event.sysex[IS_SYSEX_INDEX + 1]
        ), origin
