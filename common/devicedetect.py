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
from common import log, verbosity

from .extensionmanager import ExtensionManager

from .scriptstate import IScriptState

LOG_CAT = "bootstrap.device.type_detect"

class WaitingForDevice(IScriptState):
    """
    State for when we're trying to recognise a device
    """
    def __init__(self) -> None:
        self._init_time = None
    
    def detectFallback(self) -> None:
        """
        Fallback method for device detection, using device name
        """
        name = device.getName()
        try:
            ExtensionManager.getDevice(name)
        except ValueError:
            log(LOG_CAT, f"Failed to recognise device via fallback method", verbosity.WARNING)
            common.getContext().setState(DeviceNotRecognised())
    
    def initialise(self) -> None:
        self._init_time = time.time()
        # If the user specified to skip sending enquiry event
        if common.getContext().settings.get("bootstrap.skip_enquiry"):
            log(
                LOG_CAT,
                f"bootstrap.device.skip_enquiry flag set, using fallback",
                verbosity.INFO
            )
            self.detectFallback()
        else:
            device.midiOutSysex(bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]))
            log(LOG_CAT, "Sent universal device enquiry", verbosity.INFO)
    
    def tick(self) -> None:
        # If it's been too long since we set the time
        if self._init_time is not None:
            if (
                time.time() - self._init_time
              > common.getContext().settings.get("bootstrap.detection_timeout")
            ):
                log(
                    LOG_CAT,
                    f"Device enquiry timeout after {time.time() - self._init_time} seconds",
                    verbosity.INFO
                )
                self.detectFallback()
    
    def processEvent(self, event: eventData) -> None:
        
        # Ignore all events unless they are Sysex
        if event.sysex is not None:
            try:
                device = ExtensionManager.getDevice(event)
                log(LOG_CAT, f"Recognised device via sysex: {device.getName()}", verbosity.INFO)
            except ValueError:
                log(
                    LOG_CAT,
                    f"Failed to recognise device via sysex, using fallback method",
                    verbosity.WARNING
                )
                self.detectFallback()

class DeviceNotRecognised(IScriptState):
    """
    State for when device isn't recognised
    """
    def initialise(self) -> None:
        log(LOG_CAT, "Failed to recognise device", verbosity.ERROR)
        ui.setHintMsg("Failed to recognise device")
    
    def tick(self) -> None:
        ui.setHintMsg("Failed to recognise device")
    
    def processEvent(self, event: eventData) -> None:
        return
