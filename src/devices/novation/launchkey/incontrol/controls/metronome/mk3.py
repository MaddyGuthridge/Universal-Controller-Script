
from .metronome import LkMetronomeButton
from ...colors.mk3 import COLORS


class LkMk3MetronomeButton(LkMetronomeButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            0,
            0x4C,
            COLORS,
            0xB
        )
