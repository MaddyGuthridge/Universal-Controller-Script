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
from common import consts

from common.extensionmanager import ExtensionManager

from .scriptstate import IScriptState

LOG_CAT = "bootstrap.device.type_detect"

class WaitingForDevice(IScriptState):
    """
    State for when we're trying to recognise a device
    """
    def __init__(self) -> None:
        self._init_time = None
    
    def nameAssociations(self) -> None:
        """
        Uses the name associations setting to get device mappings

        ### Returns:
        * `bool`: whether we found a match
        """
        name_associations = common.getContext().settings.get("bootstrap.name_associations")
        
        device_name = device.getName()
        for name, id in name_associations:
            if name == device_name:
                try:
                    dev = ExtensionManager.getDeviceById(id)
                    # Assign device (causes StateChangeException)
                except ValueError:
                    log(
                        f"bootstrap.device.type_detect",
                        f"The device mapping '{name}' -> '{id}' didn't match "
                        f"any known devices",
                        verbosity.CRITICAL,
                        "This could be caused by incorrect spelling of the "
                        "device's ID."
                    )
        log(
            f"bootstrap.device.type_detect",
            f"No name associations found for device named '{device_name}'",
            verbosity.INFO
        )
        return
    
    def detectFallback(self) -> None:
        """
        Fallback method for device detection, using device name
        """
        name = device.getName()
        try:
            dev = ExtensionManager.getDevice(name)
        except ValueError:
            log(LOG_CAT, f"Failed to recognise device via fallback method", verbosity.WARNING)
            common.getContext().setState(DeviceNotRecognised())
    
    def initialise(self) -> None:
        self._init_time = time.time()
        # Check if there's an association between the device name and a device
        # If so, a StateChangeException will be raised so this function will
        # return early
        self.nameAssociations()
        
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
                dev = ExtensionManager.getDevice(event)
                log(
                    LOG_CAT,
                    f"Recognised device via sysex: {dev.getId()}",
                    verbosity.INFO,
                    repr(event.sysex)
                )
                event.handled = True
            except ValueError:
                log(
                    LOG_CAT,
                    f"Failed to recognise device via sysex, using fallback method",
                    verbosity.WARNING,
                    repr(event.sysex)
                )
                self.detectFallback()

class DeviceNotRecognised(IScriptState):
    """
    State for when device isn't recognised
    """
    def initialise(self) -> None:
        log(
            LOG_CAT,
            "Failed to recognise device",
            verbosity.ERROR,
            "The device was unable to be recognised. This usually means that "
            "there is no definition available for your device. You could help "
            "by contributing a device definition. Visit the GitHub page for "
            "details: " + consts.WEBSITE)
        ui.setHintMsg("Failed to recognise device")
    
    def tick(self) -> None:
        ui.setHintMsg("Failed to recognise device")
    
    def processEvent(self, event: eventData) -> None:
        return