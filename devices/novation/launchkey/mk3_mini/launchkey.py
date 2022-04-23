"""
devices > novation > launchkey > mk2 > launchkey

Device definitions for Launchkey Mk2 controllers

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Optional

import device

from common.eventpattern import BasicPattern, ForwardedPattern
from common.extensionmanager import ExtensionManager
from common.types import EventData
from controlsurfaces import (
    Knob,
    PlayButton,
    RecordButton,
    StandardModWheel,
    StandardPitchWheel,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    Data2Strategy,
    ForwardedStrategy,
)
from devices import BasicControlMatcher, Device
from devices.controlgenerators import NoteMatcher

from .drumpad import LkDrumPad
from .incontrol import InControl, InControlMatcher

DEVICE_ID = "Novation.Launchkey.Mk3.Mini"


class LaunchkeyMiniMk3(Device):
    """
    Novation Launchkey Mk3 Mini
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # InControl manager
        self._incontrol = InControl(matcher)
        matcher.addSubMatcher(InControlMatcher(self._incontrol))

        # Notes
        matcher.addSubMatcher(NoteMatcher())

        # Drum pads (high priority because they just use note on events)
        for r in range(self.getDrumPadSize()[0]):
            for c in range(self.getDrumPadSize()[1]):
                matcher.addControl(LkDrumPad((r, c)), 10)

        # Control switch and metronome buttons
        # matcher.addControl(LkControlSwitchButton())
        # matcher.addControl(LkMetronomeButton())

        # Create knobs
        for i in range(8):
            matcher.addControl(
                Knob(
                    ForwardedPattern(2, BasicPattern(0xBF, 0x15 + i, ...)),
                    ForwardedStrategy(Data2Strategy()),
                    (0, i)
                )
            )

        # Transport
        matcher.addControl(PlayButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RecordButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
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
                0x02,  # Family code (documented as 0x7A???)
                0x01,
                0x00,
            ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False


# Register devices
ExtensionManager.registerDevice(LaunchkeyMiniMk3)
