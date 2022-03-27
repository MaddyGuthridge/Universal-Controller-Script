"""
common > forwardstate

Represents the forwarder script in its main state, where the device is
recognised and behaving as expected. Events are forwarded to the main script.
"""

import plugins
from typing import TYPE_CHECKING, Optional

import common
from common import ProfilerContext, profilerDecoration
from common import log, verbosity
from common.types import EventData
from common.util.events import eventToString
from .devstate import DeviceState

if TYPE_CHECKING:
    from devices import Device

class ForwardState(DeviceState):
    """
    Represents the main state of the forwarder script, where the device is
    recognised and forwarding events.
    """

    def __init__(self, device: 'Device') -> None:
        self._device = device

    @classmethod
    def create(cls, device: Device) -> 'DeviceState':
        return cls(device)

    def initialise(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def processEvent(self, event: EventData) -> None:
        pass
