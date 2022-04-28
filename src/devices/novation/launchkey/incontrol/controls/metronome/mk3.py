
from .metronome import LkMetronomeButton
from ...colors.standard import COLORS


class LkMk3MetronomeButton(LkMetronomeButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            0xF,
            0x4C,
            COLORS,
        )
