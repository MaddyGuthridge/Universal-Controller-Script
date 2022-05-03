"""
devices > korg > nanokontrol > mk1 > nanokontrol

Definition for the Korg NanoKontrol Mk1 controller.

I currently don't have access to this device, so I can't be certain that it
works 100% correctly. Let me know if you run into any issues and we can
troubleshoot it together

Authors:
* Miguel Guthridge [HDSQ#2154, hdsq@outlook.com.au]
"""

from typing import Optional
from common.extensionmanager import ExtensionManager
from common.eventpattern import IEventPattern, BasicPattern
from common.types import EventData
from controlsurfaces.valuestrategies import ButtonData2Strategy, Data2Strategy
from devices import Device
from devices.matchers import BasicControlMatcher
from controlsurfaces import (
    StopButton,
    PlayButton,
    ControlSwitchButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    MuteButton,
    SoloButton,
    Fader,
    Knob,
)


class NanoKontrol(Device):
    """Korg NanoKontrol Mk1
    Note that only scene 1 is supported
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()

        # Transport controls
        matcher.addControl(RecordButton(
            BasicPattern(0xB0, 0x2C, ...),
            ButtonData2Strategy()
        ))
        matcher.addControl(PlayButton(
            BasicPattern(0xB0, 0x2D, ...),
            ButtonData2Strategy()
        ))
        matcher.addControl(StopButton(
            BasicPattern(0xB0, 0x2E, ...),
            ButtonData2Strategy()
        ))
        matcher.addControl(RewindButton(
            BasicPattern(0xB0, 0x2F, ...),
            ButtonData2Strategy()
        ))
        matcher.addControl(FastForwardButton(
            BasicPattern(0xB0, 0x30, ...),
            ButtonData2Strategy()
        ))
        matcher.addControl(ControlSwitchButton(
            BasicPattern(0xB0, 0x31, ...),
            ButtonData2Strategy()
        ))

        for i in range(9):
            # Solo - upper buttons
            matcher.addControl(SoloButton(
                BasicPattern(0xB0, 0x17 + i, ...),
                ButtonData2Strategy(),
                (0, i)
            ))
            # Mute - lower buttons
            matcher.addControl(MuteButton(
                BasicPattern(0xB0, 0x21 + i, ...),
                ButtonData2Strategy(),
                (0, i)
            ))
            # Knobs
            matcher.addControl(Knob(
                BasicPattern(0xB0, 0x0E + i, ...),
                Data2Strategy(),
                (0, i)
            ))
            # Faders
            matcher.addControl(Fader(
                BasicPattern(0xB0, 0x02 + i, ...),
                Data2Strategy(),
                (0, i)
            ))

        super().__init__(matcher)

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 0, 0

    @staticmethod
    def getUniversalEnquiryResponsePattern() -> Optional[IEventPattern]:
        return BasicPattern([
            0xF7,
            0x7E,
            ...,
            0x06,
            0x02,
            0x42,
            0x04,
            0x01,
            0x00,
            0x00,
        ])

    @classmethod
    def create(cls, event: Optional[EventData]) -> 'Device':
        return cls()

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        return False

    def getDeviceNumber(self) -> int:
        return 1

    def getId(self) -> str:
        return "Korg.NanoKontrol.Mk1"


ExtensionManager.registerDevice(NanoKontrol)