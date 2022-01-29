"""
common > mainstate

Represents the script in its main state, where the device is recognised and
behaving as expected.
"""

from common.types import eventData
from common.util.events import eventToString
from common import log, verbosity
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
            log(
                "device.event.in",
                f"Failed to recognise event: {eventToString(event)}",
                verbosity.CRITICAL,
                "This usually means that the device hasn't been configured "
                "correctly. Please contact the device's maintainer."
            )
            raise ValueError(f"Couldn't identify event: {eventToString(event)}")
            
        else:
            log("device.event.in", f"Recognised event: {mapping.getControl()}", verbosity.NOTE)
