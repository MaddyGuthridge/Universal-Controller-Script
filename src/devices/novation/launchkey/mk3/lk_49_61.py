"""
devices > novation > launchkey > mk3 > lk_49_61

Device definitions for Launchkey Mk3 49/61/88 controllers

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
from control_surfaces.matchers import (
    BasicControlMatcher,
    NoteMatcher,
    NoteAfterTouchMatcher,
)
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
    LkMk3FaderSet,
    LkMk3ControlSwitchButton,
    LkQuantizeButton,
    LkMk3MetronomeButton,
    LkUndoRedoButton,
    LkMk3CaptureMidiButton,
    Mk3DirectionUp,
    Mk3DirectionDown,
    Mk3DirectionUpSilenced,
    Mk3DirectionDownSilenced,
    Mk3DirectionLeft,
    Mk3DirectionRight,
    LkPauseActive,
)
from .shift import getActivitySwitcherLarge

DEVICE_ID_49 = "Novation.Launchkey.Mk3.49"
DEVICE_ID_61 = "Novation.Launchkey.Mk3.61"
DEVICE_ID_88 = "Novation.Launchkey.Mk3.88"
DEVICE_IDS = (DEVICE_ID_49, DEVICE_ID_61, DEVICE_ID_88)


class LaunchkeyMk3_49_61(Device):
    """
    Novation Launchkey Mk3 25
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # InControl manager
        self._incontrol = InControl(matcher)
        matcher.addSubMatcher(InControlMatcher(self._incontrol))

        # Notes
        matcher.addSubMatcher(NoteMatcher())

        matcher.addSubMatcher(getActivitySwitcherLarge())
        matcher.addSubMatcher(LkKnobSet())
        matcher.addSubMatcher(LkMk3FaderSet())
        matcher.addControl(LkMk3StopButton())
        matcher.addControl(LkMk3PlayButton())
        matcher.addControl(LkMk3LoopButton())
        matcher.addControl(LkMk3RecordButton())
        matcher.addControl(LkMk3ControlSwitchButton())
        matcher.addControl(LkQuantizeButton())
        matcher.addControl(LkMk3MetronomeButton())
        matcher.addControl(LkUndoRedoButton())
        matcher.addControl(LkMk3CaptureMidiButton())
        matcher.addControl(Mk3DirectionUp())
        matcher.addControl(Mk3DirectionDown())
        matcher.addControl(Mk3DirectionUpSilenced())
        matcher.addControl(Mk3DirectionDownSilenced())
        matcher.addControl(Mk3DirectionLeft())
        matcher.addControl(Mk3DirectionRight())
        matcher.addControl(StandardPitchWheel.create())
        matcher.addControl(StandardModWheel.create())
        matcher.addControl(SustainPedal.create())
        matcher.addControl(LkPauseActive())
        # Note after-touch for drum pad
        # TODO: Create custom type for it
        matcher.addSubMatcher(NoteAfterTouchMatcher(...))

        super().__init__(matcher)

    def initialize(self) -> None:
        self._incontrol.enable()

    def deinitialize(self) -> None:
        self._incontrol.enable()

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        return 2, 8

    def getDeviceNumber(self) -> int:
        if (
            'MIDIIN2' in device.getName()
            or 'DAW' in device.getName()
        ):
            return 2
        else:
            return 1

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        if '49' in device.getName():
            return DEVICE_ID_49
        if '61' in device.getName():
            return DEVICE_ID_61
        if '88' in device.getName():
            return DEVICE_ID_88
        return DEVICE_ID_49

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return DEVICE_IDS

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
                (0x36, 0x37, 0x40),  # Family code (documented as 0x7A???)
                0x01,
                0x00,
                0x00,
            ]
        )


# Register devices
ExtensionManager.devices.register(LaunchkeyMk3_49_61)
