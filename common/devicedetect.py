"""
common > devicedetect

Contains the definition for the device detection state of the script, as well
as the device not recognised state of the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import ui

from common.types import eventData

from .scriptstate import IScriptState

class WaitingForDevice(IScriptState):
    """
    State for when we're trying to recognise a device
    """
    def initialise(self) -> None:
        pass
    
    def tick(self) -> None:
        pass
    
    def processEvent(self, event: eventData) -> None:
        pass

class DeviceNotRecognised(IScriptState):
    """
    State machine for when device isn't recognised
    """
    def initialise(self) -> None:
        print("Failed to recognise device")
        ui.setHintMsg("Failed to recognise device")
    
    def tick(self) -> None:
        ui.setHintMsg("Failed to recognise device")
    
    def processEvent(self, event: eventData) -> None:
        return
