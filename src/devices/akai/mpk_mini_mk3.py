"""
devices > akai > mpk_mini_mk3

Device definitions for Akai MPK Mini Mk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional

from control_surfaces.event_patterns import (
    BasicPattern,
    NotePattern,
    UnionPattern,
)
from control_surfaces.value_strategies import Data2Strategy
from common.extension_manager import ExtensionManager
from fl_classes import FlMidiMsg
from control_surfaces import (
    Knob,
    StandardPitchWheel,
    StandardModWheel,
    DrumPad,
)
from devices import Device
from control_surfaces.matchers import BasicControlMatcher, NoteMatcher


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


class MpkMiniMk3(Device):
    """
    Akai MPK Mini Mk3
    """
    def __init__(self) -> None:
        matcher = BasicControlMatcher()

        matcher.addSubMatcher(NoteMatcher())

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

        # Knobs
        for i, cc in enumerate(range(0x46, 0x4E)):
            matcher.addControl(Knob(
                BasicPattern(0xB0, cc, ...),
                Data2Strategy(),
                coordinate=(0, i)
            ))

        super().__init__(matcher)

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        return "Akai.Mpk.Mini.Mk3"

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        return 4, 4

    def getDeviceNumber(self) -> int:
        return 1

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return ("Akai.Mpk.Mini.Mk3",)

    @classmethod
    def getUniversalEnquiryResponsePattern(cls):
        return BasicPattern(
            [
                0xF0,
                0x7E,
                0x7F,
                0x06,
                0x02,
                0x47,
                0x49,
                0x00,
                0x19,
                0x00,
            ]
        )


ExtensionManager.devices.register(MpkMiniMk3)
