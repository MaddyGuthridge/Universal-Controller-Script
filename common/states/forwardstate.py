"""
common > forwardstate

Represents the forwarder script in its main state, where the device is
recognised and behaving as expected. Events are forwarded to the main script.
"""

from typing import TYPE_CHECKING

import device

import common
from common.logger import log
from common.types import EventData
from common.types.eventdata import isEventStandard, isEventSysex
from common.util.events import (
    decodeForwardedEvent,
    eventToString,
    forwardEvent,
    isEventForwarded,
    isEventForwardedHereFrom
)
from .devstate import DeviceState

if TYPE_CHECKING:
    from devices import Device


def outputForwarded(event: EventData):
    """
    Output a received event to this device

    This handles events forwarded from the main script

    ### Args:
    * `event` (`EventData`): event
    """
    event = decodeForwardedEvent(event)
    if isEventSysex(event):
        device.midiOutSysex(event.sysex)
    else:
        if TYPE_CHECKING:
            assert isEventStandard(event)
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
    recognised and forwarding events.
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

    def initialise(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def processEvent(self, event: EventData) -> None:
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
