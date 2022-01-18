"""
common > devicedetect

Contains the definition for the device detection state of the script, as well
as the device not recognised state of the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import time
import ui
import device

import common
from common.types import eventData

from .scriptstate import IScriptState

class WaitingForDevice(IScriptState):
    """
    State for when we're trying to recognise a device
    """
    def __init__(self) -> None:
        self._init_time = None
    
    def initialise(self) -> None:
        self._init_time = time.time()
        device.midiOutSysex(bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]))
    
    def tick(self) -> None:
        # If it's been too long since we set the time
        if self._init_time is not None:
            if (
                time.time() - self._init_time
              > common.getContext().settings.get("device.detection_timeout")
            ):
                common.getContext().setState(DeviceNotRecognised())
    
    def processEvent(self, event: eventData) -> None:
        
        # Ignore all events unless they are Sysex
        print(event.sysex)

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
