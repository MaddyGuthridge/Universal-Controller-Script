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
    DirectionNext,
    DirectionPrevious,
    Fader,
    FastForwardButton,
    GenericFaderButton,
    MasterGenericFaderButton,
    Knob,
    LoopButton,
    MasterFader,
    PlayButton,
    RecordButton,
    RewindButton,
    StandardModWheel,
    StandardPitchWheel,
    StopButton,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    Data2Strategy,
    ForwardedStrategy,
)
from devices import BasicControlMatcher, Device
from devices.controlgenerators import NoteMatcher

from .drumpad import LaunchkeyDrumpad
from .incontrol import InControl, InControlMatcher

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

        # Drum pads (high priority because they just use note on events)
        for r in range(self.getDrumPadSize()[0]):
            for c in range(self.getDrumPadSize()[1]):
                matcher.addControl(LaunchkeyDrumpad((r, c)), 10)

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
        matcher.addControl(StopButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x72, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(PlayButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(LoopButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        ))
        matcher.addControl(RecordButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(DirectionNext(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(DirectionPrevious(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        ))
        matcher.addControl(RewindButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x70, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        ))
        matcher.addControl(FastForwardButton(
            ForwardedPattern(2, BasicPattern(0xBF, 0x71, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
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

        # Create faders
        for i in range(8):
            matcher.addControl(
                Fader(
                    ForwardedPattern(2, BasicPattern(0xBF, 0x29 + i, ...)),
                    ForwardedStrategy(Data2Strategy()),
                    (0, i)
                )
            )
        # Master fader
        matcher.addControl(
            MasterFader(
                ForwardedPattern(2, BasicPattern(0xBF, 0x07, ...)),
                ForwardedStrategy(Data2Strategy())
            )
        )

        # Fader buttons
        for i in range(8):
            matcher.addControl(
                GenericFaderButton(
                    ForwardedPattern(2, BasicPattern(0xBF, 0x33 + i, ...)),
                    ForwardedStrategy(Data2Strategy()),
                    (0, i)
                )
            )

        matcher.addControl(
            MasterGenericFaderButton(
                ForwardedPattern(2, BasicPattern(0xBF, 0x3B, ...)),
                ForwardedStrategy(Data2Strategy())
            )
        )

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
