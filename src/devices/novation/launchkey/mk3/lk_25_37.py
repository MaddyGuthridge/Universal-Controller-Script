"""
devices > novation > launchkey > mk2 > launchkey

Device definitions for Launchkey Mk2 controllers

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Optional

import device

from control_surfaces.event_patterns import BasicPattern
from common.extension_manager import ExtensionManager
from common.types import EventData
from control_surfaces import (
    StandardModWheel,
    StandardPitchWheel,
)
from devices import BasicControlMatcher, Device
from devices.control_generators import NoteMatcher
from devices.novation.launchkey.incontrol import (
    InControl,
    InControlMatcher,
)
from devices.novation.launchkey.incontrol.controls import (
    LkMk3PlayButton,
    LkMk3StopButton,
    LkMk3LoopButton,
    LkMk3RecordButton,
    LkKnobSet,
    LkMk3DrumPad,
    LkDrumPadMatcher,
    LkDirectionNext,
    LkDirectionPrevious,
    LkMk3ControlSwitchButton,
    LkMk3CaptureMidiButton,
    Mk3DirectionUp,
    Mk3DirectionDown,
    Mk3DirectionLeft,
    Mk3DirectionRight,
)

DEVICE_ID = "Novation.Launchkey.Mk3.25-37"


class LaunchkeyMk3_25_37(Device):
    """
    Novation Launchkey Mk3 25-37
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # InControl manager
        self._incontrol = InControl(matcher)
        matcher.addSubMatcher(InControlMatcher(self._incontrol))

        # Notes
        matcher.addSubMatcher(NoteMatcher())

        matcher.addSubMatcher(LkDrumPadMatcher(LkMk3DrumPad))
        matcher.addSubMatcher(LkKnobSet())
        matcher.addControl(LkMk3StopButton())
        matcher.addControl(LkMk3PlayButton())
        matcher.addControl(LkMk3LoopButton())
        matcher.addControl(LkDirectionNext())
        matcher.addControl(LkDirectionPrevious())
        matcher.addControl(LkMk3RecordButton())
        matcher.addControl(StandardPitchWheel())
        matcher.addControl(StandardModWheel())
        matcher.addControl(LkMk3ControlSwitchButton())
        matcher.addControl(LkMk3CaptureMidiButton())
        matcher.addControl(Mk3DirectionUp())
        matcher.addControl(Mk3DirectionDown())
        matcher.addControl(Mk3DirectionLeft())
        matcher.addControl(Mk3DirectionRight())

        super().__init__(matcher)

    def initialize(self) -> None:
        self._incontrol.enable()

    def deinitialize(self) -> None:
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
                (0x34, 0x35),  # Family code (documented as 0x7A???)
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
ExtensionManager.devices.register(LaunchkeyMk3_25_37)
