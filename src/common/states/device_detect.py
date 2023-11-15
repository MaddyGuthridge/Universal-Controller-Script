"""
common > device_detect

Contains the definition for the device detection state of the script, as well
as the device not recognized state of the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import time
from typing import Optional
import device

import common
from consts import UNIVERSAL_DEVICE_ENQUIRY
from common.exceptions import DeviceRecognizeError
from common import log, verbosity
from fl_classes import isMidiMsgSysex, FlMidiMsg
from common.util.events import eventToString

from . import IScriptState, ErrorState, DeviceState

LOG_CAT = "bootstrap.device.type_detect"


class WaitingForDevice(IScriptState):
    """
    State for when we're trying to recognize a device
    """
    def __init__(self, switch_to: type[DeviceState]) -> None:
        """
        Create the WaitingForDevice state

        ### Args:
        * `switch_to` (`IScriptState`): state to switch to when the device is
          recognized
        """
        self._init_time: Optional[float] = None
        self._sent_enquiry = False
        self._to = switch_to

    def nameAssociations(self) -> None:
        """
        Uses the name associations setting to get device mappings

        ### Returns:
        * `bool`: whether we found a match
        """
        name_associations = common.getContext().settings.get(
            "bootstrap.name_associations"
        )

        device_name = device.getName()
        for name, id in name_associations:
            if name == device_name:
                try:
                    dev = common.ExtensionManager.devices.getById(id)
                    log(
                        LOG_CAT,
                        f"Recognized device via device name associations: "
                        f"{dev.getId()}",
                        verbosity.INFO
                    )
                    common.getContext().setState(self._to.create(dev))
                except DeviceRecognizeError:
                    log(
                        "bootstrap.device.type_detect",
                        f"The device mapping '{name}' -> '{id}' didn't match "
                        f"any known devices",
                        verbosity.CRITICAL,
                        "This could be caused by incorrect spelling of the "
                        "device's ID."
                    )
        log(
            "bootstrap.device.type_detect",
            f"No name associations found for device named '{device_name}'",
            verbosity.INFO
        )
        return

    def detectFallback(self) -> None:
        """
        Fallback method for device detection, using device name
        """
        name = device.getName()
        dev = common.ExtensionManager.devices.get(name)
        log(
            LOG_CAT,
            f"Recognized device via fallback: {dev.getId()}",
            verbosity.INFO
        )
        common.getContext().setState(self._to.create(dev))

    def sendEnquiry(self) -> None:
        self._sent_enquiry = True
        # If the user specified to skip sending enquiry event
        if common.getContext().settings.get("bootstrap.skip_enquiry"):
            log(
                LOG_CAT,
                "bootstrap.device.skip_enquiry flag set, using fallback",
                verbosity.INFO
            )
            self.detectFallback()
        else:
            device.midiOutSysex(UNIVERSAL_DEVICE_ENQUIRY)
            log(LOG_CAT, "Sent universal device enquiry", verbosity.INFO)

    def initialize(self) -> None:
        self._init_time = time.time()
        # Check if there's an association between the device name and a device
        # If so, a StateChangeException will be raised so this function will
        # return early
        self.nameAssociations()
        log(
            LOG_CAT,
            f"Device is assigned: {bool(device.isAssigned())}",
            verbosity.INFO
        )
        if not common.getContext().settings.get("bootstrap.delay_enquiry"):
            self.sendEnquiry()

    def deinitialize(self) -> None:
        pass

    def tick(self) -> None:
        # If it's been too long since we set the time
        if self._sent_enquiry:
            assert self._init_time is not None
            if (
                time.time() - self._init_time
                > common.getContext().settings.get(
                    "bootstrap.detection_timeout"
                )
            ):
                log(
                    LOG_CAT,
                    f"Device enquiry timeout after "
                    f"{(time.time() - self._init_time):.2f} seconds",
                    verbosity.INFO
                )
                self.detectFallback()
        else:
            self.sendEnquiry()

    def processEvent(self, event: FlMidiMsg) -> None:
        # Always handle all events
        event.handled = True
        # Ignore all events unless they are Sysex
        if self._sent_enquiry and isMidiMsgSysex(event):
            try:
                dev = common.ExtensionManager.devices.get(event)
                log(
                    LOG_CAT,
                    f"Recognized device via sysex: {dev.getId()}",
                    verbosity.INFO,
                    eventToString(event)
                )
                common.getContext().setState(self._to.create(dev))
            except DeviceRecognizeError as e:
                log(
                    LOG_CAT,
                    f"Failed to recognize device via sysex, using fallback "
                    f"method {eventToString(event)}",
                    verbosity.INFO,
                )
                try:
                    self.detectFallback()
                except DeviceRecognizeError:
                    common.getContext().setState(ErrorState(e))
