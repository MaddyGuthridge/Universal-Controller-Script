"""
devices > novation > launchkey > mk2 > launchkey

Device definitions for Launchkey Mk2 controllers

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
from devices.novation.incontrol.controls import (
    LkMk2DrumPad,
    LkDrumPadMatcher,
    LkMk2ControlSwitchButton,
    LkMk2MetronomeButton,
    LkKnobSet,
    LkMk2StopButton,
    LkPlayButton,
    LkDirectionNext,
    LkDirectionPrevious,
    LkFastForwardButton,
    LkRewindButton,
    LkRecordButton,
    LkMk2LoopButton,
    LkFaderSet,
)

ID_PREFIX = "Novation.Launchkey.Mk2"


class LaunchkeyMk2(Device):
    """
    Novation Launchkey Mk2 series controllers
    """

    def __init__(self, matcher: BasicControlMatcher) -> None:
        # InControl manager
        self._incontrol = InControl(matcher)
        matcher.addSubMatcher(InControlMatcher(self._incontrol))

        # Notes
        matcher.addSubMatcher(NoteMatcher())

        matcher.addSubMatcher(LkDrumPadMatcher(LkMk2DrumPad))
        matcher.addControl(LkMk2ControlSwitchButton())
        matcher.addControl(LkMk2MetronomeButton())
        matcher.addSubMatcher(LkKnobSet())

        # Transport
        matcher.addControl(LkMk2StopButton())
        matcher.addControl(LkPlayButton())
        matcher.addControl(LkMk2LoopButton())
        matcher.addControl(LkRecordButton())
        matcher.addControl(LkDirectionNext())
        matcher.addControl(LkDirectionPrevious())
        matcher.addControl(LkRewindButton())
        matcher.addControl(LkFastForwardButton())
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
        name = device.getName()
        if "MIDIIN2" in name:
            return 2
        elif "MIDI" in name:
            return 1
        elif "InCo" in name:
            return 2
        else:
            return 1


class LaunchkeyMk2_49_61(LaunchkeyMk2):
    """
    Standard controls with added faders
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        matcher.addSubMatcher(LkFaderSet())
        super().__init__(matcher)

    @classmethod
    def create(cls, event: Optional[EventData]) -> Device:
        return cls()

    @staticmethod
    def getId() -> str:
        if "49" in device.getName():
            num = 49
        else:
            num = 61
        return f"{ID_PREFIX}.{num}"

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
                (0x7C, 0x7D)  # Family code (documented as 0x7A???)
            ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False


class LaunchkeyMk2_25(LaunchkeyMk2):
    """
    Standard controls with no faders
    """

    def __init__(self) -> None:
        super().__init__(BasicControlMatcher())

    @classmethod
    def create(cls, event: Optional[EventData]) -> Device:
        return cls()

    @staticmethod
    def getId() -> str:
        return f"{ID_PREFIX}.25"

    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicPattern(
            [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0x7B]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False


# Register devices
ExtensionManager.registerDevice(LaunchkeyMk2_49_61)
ExtensionManager.registerDevice(LaunchkeyMk2_25)
