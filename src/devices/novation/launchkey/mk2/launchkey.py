"""
devices > novation > launchkey > mk2 > launchkey

Device definitions for Launchkey Mk2 controllers

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional
import device

from control_surfaces.event_patterns import BasicPattern
from common.extension_manager import ExtensionManager
from fl_classes import FlMidiMsg
from control_surfaces import (
    StandardModWheel,
    StandardPitchWheel,
    SustainPedal,
)
from devices import Device
from control_surfaces.matchers import BasicControlMatcher, NoteMatcher

from devices.novation.launchkey.incontrol import (
    InControl,
    InControlMatcher,
)
from devices.novation.launchkey.incontrol.controls import (
    LkMk2DrumPad,
    LkDrumPadMatcher,
    LkMk2ControlSwitchButton,
    LkMk2MetronomeButton,
    LkKnobSet,
    LkMk2StopButton,
    LkMk2PlayButton,
    LkMk2DirectionNext,
    LkMk2DirectionPrevious,
    LkFastForwardButton,
    LkRewindButton,
    LkMk2RecordButton,
    LkMk2LoopButton,
    LkMk2FaderSet,
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
        matcher.addControl(LkMk2PlayButton())
        matcher.addControl(LkMk2LoopButton())
        matcher.addControl(LkMk2RecordButton())
        matcher.addControl(LkMk2DirectionNext())
        matcher.addControl(LkMk2DirectionPrevious())
        matcher.addControl(LkRewindButton())
        matcher.addControl(LkFastForwardButton())
        matcher.addControl(StandardPitchWheel.create())
        matcher.addControl(StandardModWheel.create())
        matcher.addControl(SustainPedal.create())

        super().__init__(matcher)

    def initialize(self) -> None:
        self._incontrol.enable()

    def deinitialize(self) -> None:
        self._incontrol.enable()

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
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
        matcher.addSubMatcher(LkMk2FaderSet())
        super().__init__(matcher)

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        if "49" in device.getName():
            num = 49
        else:
            num = 61
        return f"{ID_PREFIX}.{num}"

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return (f"{ID_PREFIX}.49", f"{ID_PREFIX}.61")

    @classmethod
    def getUniversalEnquiryResponsePattern(cls):
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


class LaunchkeyMk2_25(LaunchkeyMk2):
    """
    Standard controls with no faders
    """

    def __init__(self) -> None:
        # FIXME: This has a master fader, investigate it further
        super().__init__(BasicControlMatcher())

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        return f"{ID_PREFIX}.25"

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return (f"{ID_PREFIX}.25",)

    @classmethod
    def getUniversalEnquiryResponsePattern(cls):
        return BasicPattern(
            [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0x7B]
        )


# Register devices
ExtensionManager.devices.register(LaunchkeyMk2_49_61)
ExtensionManager.devices.register(LaunchkeyMk2_25)
