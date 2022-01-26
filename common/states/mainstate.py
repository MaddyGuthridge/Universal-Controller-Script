"""
common > mainstate

Represents the script in its main state, where the device is recognised and
behaving as expected.
"""

from common.types import eventData
from common.util.events import eventToString
from devices import Device
from .scriptstate import IScriptState

class MainState(IScriptState):
    """
    Represents the main state of the script, where the device is recognised and
    behaving as expected.
    """
    
    def __init__(self, device: Device) -> None:
        self._device = device
    
    def initialise(self) -> None:
        pass
    
    def tick(self) -> None:
        self._device.tick()

    def processEvent(self, event: eventData) -> None:
        mapping = self._device.matchEvent(event)
        if mapping is None:
            raise ValueError(f"Couldn't identify event: {eventToString(event)}")
