"""
devices > novation > launchkey > incontrol > controls > drum_pad > mk3

Definition for the Launchkey Mk3 drum pad class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .drum_pad import (
    LkDrumPad,
    LkDrumPadMute,
    LkDrumPadSolo,
    LkDrumPadActivity,
)
from ...colors.mk3 import COLORS

DRUM_PADS = [
    [0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67],
    [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77],
]
DRUM_PADS_DEVICE_SELECT = [
    [inner - 0x20 for inner in outer] for outer in DRUM_PADS
]


class LkMk3DrumPad(LkDrumPad):

    def __init__(self, row: int, col: int) -> None:
        super().__init__(
            (row, col),
            0x0,
            DRUM_PADS[row][col],
            COLORS,
            # debug=f"Main[{row}, {col}]",
        )

    @classmethod
    def create(cls, row: int, col: int) -> 'LkMk3DrumPad':
        return cls(row, col)


class LkMk3DrumPadMute(LkDrumPadMute):
    def __init__(self, row: int, col: int) -> None:
        super().__init__(
            (row, col),
            0x0,
            DRUM_PADS[row][col],
            COLORS,
        )

    @classmethod
    def create(cls, row: int, col: int) -> 'LkMk3DrumPadMute':
        return cls(row, col)


class LkMk3DrumPadSolo(LkDrumPadSolo):
    def __init__(self, row: int, col: int) -> None:
        super().__init__(
            (row, col),
            0x0,
            DRUM_PADS[row][col],
            COLORS,
        )

    @classmethod
    def create(cls, row: int, col: int) -> 'LkMk3DrumPadSolo':
        return cls(row, col)


class LkMk3DrumPadActivity(LkDrumPadActivity):
    def __init__(self, row: int, col: int) -> None:
        super().__init__(
            (row, col),
            0x0,
            DRUM_PADS_DEVICE_SELECT[row][col],
            COLORS,
            # debug=f"Activity[{row}, {col}]",
        )

    @classmethod
    def create(cls, row: int, col: int) -> 'LkMk3DrumPadActivity':
        return cls(row, col)


class LkMk3MiniDrumPadActivity(LkDrumPadActivity):
    def __init__(self, row: int, col: int) -> None:
        super().__init__(
            (row, col),
            0x0,
            DRUM_PADS[row][col],
            COLORS,
            # debug=f"Activity[{row}, {col}]",
        )

    @classmethod
    def create(cls, row: int, col: int) -> 'LkMk3MiniDrumPadActivity':
        return cls(row, col)
