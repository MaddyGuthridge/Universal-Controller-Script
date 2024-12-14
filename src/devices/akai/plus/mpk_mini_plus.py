"""
devices > akai > mpk > mini > mpk_mini_plus

Device definitions for Akai MPK Mini Plus

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional

from control_surfaces.event_patterns import (
    BasicPattern,
    NotePattern,
    UnionPattern,
)
from control_surfaces.value_strategies import (
    Data1Strategy,
    Data2Strategy,
    AkaiJoystickFullStrategy,
    TwosComplimentDeltaStrategy,
)
from common.extension_manager import ExtensionManager
from fl_classes import FlMidiMsg
from control_surfaces import (
    Encoder,
    StandardPitchWheel,
    StandardModWheel,
    DrumPad,
    PlayButton,
    StopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    ChannelAfterTouch,
    DirectionLeft,
    DirectionRight,
    DirectionUp,
    DirectionDown,
)
from devices import Device
from control_surfaces.matchers import (
    BasicControlMatcher,
    NoteMatcher,
    PedalMatcher,
)


PAD_NOTES = [
    48, 47, 45, 43,
    49, 55, 51, 53,
    37, 36, 42, 54,
    40, 38, 46, 44,
]
PAD_CCS = list(range(0x10, 0x20))
PAD_PROG_CHANGES = [
    8, 9, 10, 11,
    12, 13, 14, 15,
    0, 1, 2, 3,
    4, 5, 6, 7,
]


class MpkMiniPlus(Device):
    """
    Akai MPK Mini Plus
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()

        matcher.addSubMatcher(NoteMatcher())
        matcher.addSubMatcher(PedalMatcher())

        matcher.addControl(StandardPitchWheel.create())
        matcher.addControl(StandardModWheel.create())
        # Drums
        # For now just link all the kinds to the one type
        for i, (note, cc, prog) in enumerate(zip(
            PAD_NOTES,
            PAD_CCS,
            PAD_PROG_CHANGES,
        )):
            # Yucky maths
            row = 1 - i // 4 if i < 8 else 5 - i // 4
            matcher.addControl(DrumPad(
                UnionPattern(
                    NotePattern(note, 9),
                    BasicPattern(0xB9, cc, ...),
                    BasicPattern(0xC9, prog, ...),
                ),
                Data2Strategy(),
                coordinate=(row, i % 4),
            ), priority=1)
        matcher.addControl(ChannelAfterTouch(
            BasicPattern(0xD9, ..., ...),
            Data1Strategy(),
            coordinate=(4, 0),
        ), priority=3)
        # Encoders
        for i, cc in enumerate(range(0x46, 0x4E)):
            matcher.addControl(Encoder(
                BasicPattern(range(0xB0, 0xC0), cc, ...),
                TwosComplimentDeltaStrategy(),
                coordinate=(0, i),
            ), priority=2)
        # Joystick
        matcher.addControl(DirectionDown(
            BasicPattern(range(0xB0, 0xBF), 0x02, ...),
            AkaiJoystickFullStrategy(),
            coordinate=(1, 0),
        ), priority=3)
        matcher.addControl(DirectionUp(
            BasicPattern(range(0xB0, 0xBF), 0x03, ...),
            AkaiJoystickFullStrategy(),
            coordinate=(1, 1),
        ), priority=3)
        matcher.addControl(DirectionLeft(
            BasicPattern(range(0xB0, 0xBF), 0x0C, ...),
            AkaiJoystickFullStrategy(),
            coordinate=(1, 2),
        ), priority=3)
        matcher.addControl(DirectionRight(
            BasicPattern(range(0xB0, 0xBF), 0x0D, ...),
            AkaiJoystickFullStrategy(),
            coordinate=(1, 3),
        ), priority=3)
        # Transport buttons
        matcher.addControl(StopButton(
            BasicPattern(range(0xB0, 0xBF), 0x75, ...),
            Data2Strategy(),
            coordinate=(2, 2),
        ), priority=4)
        matcher.addControl(PlayButton(
            BasicPattern(range(0xB0, 0xBF), 0x76, ...),
            Data2Strategy(),
            coordinate=(2, 3),
        ), priority=4)
        matcher.addControl(RecordButton(
            BasicPattern(range(0xB0, 0xBF), 0x77, ...),
            Data2Strategy(),
            coordinate=(2, 4),
        ), priority=4)
        matcher.addControl(RewindButton(
            BasicPattern(range(0xB0, 0xBF), 0x73, ...),
            Data2Strategy(),
            coordinate=(2, 0),
        ), priority=4)
        matcher.addControl(FastForwardButton(
            BasicPattern(range(0xB0, 0xBF), 0x74, ...),
            Data2Strategy(),
            coordinate=(2, 1),
        ), priority=4)

        super().__init__(matcher)

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        return "Akai.Mpk.Mini.Plus"

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        return 4, 4

    def getDeviceNumber(self) -> int:
        return 1

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return ("Akai.Mpk.Mini.Plus",)

    @classmethod
    def getUniversalEnquiryResponsePattern(cls):
        return BasicPattern([
                0xF0,
                0x7E,
                0x7F,
                0x06,
                0x02,
                0x47,
                0x54,
                0x00,
                0x19,
                0x00,
            ]
        )


ExtensionManager.devices.register(MpkMiniPlus)
