"""
common > forward_state

Represents the forwarder script in its main state, where the device is
recognized and behaving as expected. Events are forwarded to the main script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING

import device

import common
from common.logger import log
from fl_classes import FlMidiMsg
from fl_classes import isMidiMsgStandard, isMidiMsgSysex
from common.util.events import (
    decodeForwardedEvent,
    eventToString,
    forwardEvent,
    isEventForwarded,
    isEventForwardedHereFrom
)
from .dev_state import DeviceState

if TYPE_CHECKING:
    from devices import Device


def outputForwarded(event: FlMidiMsg):
    """
    Output a received event to this device

    This handles events forwarded from the main script

    ### Args:
    * `event` (`FlMidiMsg`): event
    """
    event = decodeForwardedEvent(event)
    if isMidiMsgSysex(event):
        device.midiOutSysex(event.sysex)
    else:
        if TYPE_CHECKING:
            assert isMidiMsgStandard(event)
        device.midiOutMsg(
            event.status + (event.data1 << 8) + (event.data2 << 16)
        )
    log(
        "device.forward.in",
        "Output event to device: " + eventToString(event)
    )


class ForwardState(DeviceState):
    """
    Represents the main state of the forwarder script, where the device is
    recognized and forwarding events.
    """

    def __init__(self, device: 'Device') -> None:
        if device.getDeviceNumber() == 1:
            raise ValueError(
                "The main device should be configured to use the main "
                "'Universal Controller' script, rather than the 'Universal "
                "Event Forwarder' script"
            )
        self._device = device
        common.getContext().registerDevice(device)

    @classmethod
    def create(cls, device: 'Device') -> 'DeviceState':
        return cls(device)

    def initialize(self) -> None:
        pass

    def deinitialize(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def processEvent(self, event: FlMidiMsg) -> None:
        if isEventForwarded(event):
            if isEventForwardedHereFrom(event):
                outputForwarded(event)
        else:
            forwardEvent(event)
            log(
                "device.forward.out",
                "Dispatched event to main script: " + eventToString(event)
            )
        event.handled = True
