"""
common > util > forwarded_events

Contains code for forwarding events.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import device
from typing import TYPE_CHECKING, Optional
from fl_classes import FlMidiMsg, isMidiMsgStandard, isMidiMsgSysex
from . import events
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


def get_forwarded_origin_device(event: FlMidiMsg) -> int:
    """
    Returns the origin device of a forwarded event

    ### Args
    * `event` (`FlMidiMsg`): message to parse

    ### Returns
    * `int`: origin device number
    """
    return event.sysex[ORIGIN_INDEX]


def get_forwarded_target_device(event: FlMidiMsg) -> int:
    """
    Returns the target device of a forwarded event

    ### Args
    * `event` (`FlMidiMsg`): message to parse

    ### Returns
    * `int`: target device number
    """
    return event.sysex[TARGET_INDEX]


def encode_forwarded_event(event: FlMidiMsg, origin: int):
    """
    Encode an event to prepare it to be forwarded to secondary ports

    ### Args
    * `event` (`FlMidiMsg`): event to encode

    * `origin` (`int`): device number from which the event originates

    ### Returns
    * `bytes`: encoded sysex event
    """
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
    return encoded


def forward_event_to_main(event: FlMidiMsg, origin: int) -> None:
    """
    Given an event from an origin device, forward it to the main device

    ### Args
    * `event` (`FlMidiMsg`): message to encode and forward

    * `origin` (`int`): origin device number
    """
    encoded = encode_forwarded_event(event, origin)
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
    """
    Given an event from an origin device, forward it to the main device

    ### Args
    * `event` (`FlMidiMsg`): message to encode and forward

    * `origin` (`int`): origin device number
    """
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


def decode_forwarded_event(event: FlMidiMsg) -> FlMidiMsg:
    """
    Given a forwarded event, decode it and return the result

    ### Args
    * `event` (`FlMidiMsg`): event to decode

    ### Returns
    * `FlMidiMsg`: decoded event
    """
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


def receive_event_from_main(
    event: FlMidiMsg,
    device_num: int,
) -> Optional[FlMidiMsg]:
    """
    Attempt to receive an event forwarded from the main script

    ### Args
    * `event` (`FlMidiMsg`): event to receive

    * `device_num` (`int`): device number that is receiving the event

    ### Returns
    * `Optional[FlMidiMsg]`: decoded message, if it was forwarded from the main
      script, otherwise, `None`.
    """
    if not is_event_forwarded(event):
        return None
    assert isMidiMsgSysex(event)

    if get_forwarded_target_device(event) != device_num:
        return None
    return decode_forwarded_event(event)


def receive_event_from_external(
    event: FlMidiMsg,
) -> Optional[tuple[FlMidiMsg, int]]:
    """
    Attempt to receive an event from an external controller, and return the
    decoded event and the origin device number it was sent from.

    ### Args
    * `event` (`FlMidiMsg`): event to attempt to receive

    ### Returns
    * `Optional[Union[FlMidiMsg, int]]`: decoded event and origin device number
      if event was forwarded, else `None`.
    """
    if not is_event_forwarded(event):
        return None
    assert isMidiMsgSysex(event)

    # If it isn't targeting the main script
    if get_forwarded_target_device(event) != 0:
        return None

    origin = get_forwarded_origin_device(event)
    return decode_forwarded_event(event), origin


def handle_event_on_external(
    device_num: int,
    event: FlMidiMsg,
) -> None:
    """
    Handle incoming MIDI messages on secondary port

    For events that are forwarded here, output them to this port, and for
    events that originated from this port, forward them to the main script.

    ### Args
    * `device_num` (`int`): device number to handle events for

    * `event` (`FlMidiMsg`): event to handle
    """
    if is_event_forwarded(event):
        decoded = receive_event_from_main(event, device_num)
        if decoded is not None:
            if isMidiMsgSysex(decoded):
                device.midiOutSysex(decoded.sysex)
            else:
                assert isMidiMsgStandard(decoded)
                device.midiOutMsg(events.event_to_raw_data(decoded))
    else:
        forward_event_to_main(event, device_num)
