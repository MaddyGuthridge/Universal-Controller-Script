
from .drumpad import LkDrumPad
from ..colors.standard import COLORS

DRUM_PADS = [
    [0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67],  # Also 0x68
    [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77],  # Also 0x78
]


class LkMk2DrumPad(LkDrumPad):

    def __init__(
        self,
        coordinate: tuple[int, int],
    ) -> None:
        super().__init__(
            coordinate,
            0xF,
            DRUM_PADS[coordinate[0]][coordinate[1]],
            COLORS,
        )
