"""
devices > novation > sl > mk3 > device

Device definitions for SL Mk3 controllers

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Optional

import device

from common.eventpattern import BasicPattern
from common.extensionmanager import ExtensionManager
from common.types import EventData
from controlsurfaces import (
    StandardModWheel,
    StandardPitchWheel,
)
from devices import BasicControlMatcher, Device
from devices.controlgenerators import NoteMatcher
from devices.novation.incontrol import (
    InControl,
    InControlMatcher,
)
from .controls.transport import (
    SlPlayButton,
    SlStopButton,
    SlLoopButton,
    SlRecordButton,
    SlDirectionNext,
    SlDirectionPrevious,
    SlRewindButton,
    SlFastForwardButton,
)
from .controls import (
    SlFaderSet,
    SlDrumPadMatcher,
    SlNotifMsg,
)

DEVICE_ID = "Novation.SL.Mk3"


class SlMk3(Device):
    """
    Novation SL Mk3
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # InControl manager
        self._incontrol = InControl(matcher)
        matcher.addSubMatcher(InControlMatcher(self._incontrol))

        matcher.addControl(SlNotifMsg())

        # Notes
        matcher.addSubMatcher(NoteMatcher())

        matcher.addSubMatcher(SlDrumPadMatcher())
        # matcher.addSubMatcher(LkKnobSet())
        matcher.addSubMatcher(SlFaderSet())
        matcher.addControl(SlStopButton())
        matcher.addControl(SlPlayButton())
        matcher.addControl(SlLoopButton())
        matcher.addControl(SlRewindButton())
        matcher.addControl(SlFastForwardButton())
        matcher.addControl(SlDirectionNext())
        matcher.addControl(SlDirectionPrevious())
        matcher.addControl(SlRecordButton())
        matcher.addControl(StandardPitchWheel())
        matcher.addControl(StandardModWheel())

        super().__init__(matcher)

    def initialise(self) -> None:
        self._incontrol.enable()

    def deinitialise(self) -> None:
        self._incontrol.enable()

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 2, 8

    def getDeviceNumber(self) -> int:
        return 2 if'2' in device.getName() else 1

    @classmethod
    def create(cls, event: Optional[EventData]) -> Device:
        return cls()

    @staticmethod
    def getId() -> str:
        return DEVICE_ID

    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicPattern(
            [
                0xF0,  # Sysex start
                0x7E,  # Device response
                ...,  # OS Device ID
                0x06,  # Separator
                0x02,  # Separator
                0x00,  # Manufacturer
                0x20,  # Manufacturer
                0x29,  # Manufacturer
                0x01,  # Family code (documented as 0x7A???)
                0x01,
                0x00,
                0x00,
            ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False


# Register devices
ExtensionManager.registerDevice(SlMk3)
