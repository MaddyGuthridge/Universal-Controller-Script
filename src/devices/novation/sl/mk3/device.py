"""
devices > novation > sl > mk3 > device

Device definitions for SL Mk3 controllers

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
    ChannelAfterTouch,
    ActivitySwitcher,
)
from devices import Device
from control_surfaces.matchers import (
    BasicControlMatcher,
    NoteMatcher,
    ShiftMatcher,
    ShiftView,
)
from .controls.transport import (
    SlPlayButton,
    SlStopButton,
    SlLoopButton,
    SlRecordButton,
    SlDirectionRight,
    SlDirectionLeft,
    SlDirectionDown,
    SlDirectionUp,
    SlDirectionNext,
    SlDirectionPrevious,
    SlRewindButton,
    SlFastForwardButton,
    SlControlSwitchButton,
    SlActivitySwitchButton,
)
from .controls import (
    SlFaderSet,
    SlEncoderSet,
    SlToolSelectorSet,
    SlMuteSet,
    SlDrumPadMatcher,
    SlNotifMsg,
    SlAmbientKeys,
)

DEVICE_ID = "Novation.SL.Mk3"


def getDrumPads():
    """
    Create drum pad definition
    """
    main = SlDrumPadMatcher()
    activity = SlDrumPadMatcher(ActivitySwitcher)
    return ShiftMatcher(
        main,
        [ShiftView(SlActivitySwitchButton(), activity, latch=True)]
    )


class SlMk3(Device):
    """
    Novation SL Mk3
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()

        matcher.addControl(SlNotifMsg())

        # Notes
        matcher.addSubMatcher(NoteMatcher())
        matcher.addControl(ChannelAfterTouch.fromChannel(...))

        matcher.addSubMatcher(getDrumPads())
        matcher.addSubMatcher(SlEncoderSet())
        matcher.addSubMatcher(SlMuteSet())
        matcher.addSubMatcher(SlToolSelectorSet())
        matcher.addSubMatcher(SlFaderSet())
        matcher.addControl(SlStopButton())
        matcher.addControl(SlPlayButton())
        matcher.addControl(SlLoopButton())
        matcher.addControl(SlRewindButton())
        matcher.addControl(SlFastForwardButton())
        matcher.addControl(SlDirectionRight())
        matcher.addControl(SlDirectionLeft())
        matcher.addControl(SlDirectionDown())
        matcher.addControl(SlDirectionUp())
        matcher.addControl(SlDirectionPrevious())
        matcher.addControl(SlDirectionNext())
        matcher.addControl(SlRecordButton())
        matcher.addControl(SlControlSwitchButton())
        matcher.addControl(StandardPitchWheel.create())
        matcher.addControl(StandardModWheel.create())
        matcher.addControl(SustainPedal.create())
        matcher.addControl(SlAmbientKeys())

        super().__init__(matcher)

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        return 2, 8

    def getDeviceNumber(self) -> int:
        return 2 if '2' in device.getName() else 1

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        return DEVICE_ID

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return (DEVICE_ID,)

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
                0x01,  # Family code (documented as 0x7A???)
                0x01,
                0x00,
                0x00,
            ]
        )


# Register devices
ExtensionManager.devices.register(SlMk3)
