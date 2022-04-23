"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common import profilerDecoration
from common.eventpattern import ForwardedPattern
from common.eventpattern.notepattern import NotePattern
from common.types import EventData
from common.util.events import forwardEvent
from controlsurfaces.valuestrategies import NoteStrategy, ForwardedStrategy
from controlsurfaces import DrumPad, MetronomeButton, ControlSwitchButton
from .colors import COLORS

DRUM_PADS = [
    [0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67],  # Also 0x68
    [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77],  # Also 0x78
]


class LkDrumPad(DrumPad):
    """
    Custom drum pad implementation used by the launchkey Mk2 series controller
    to provide RGB functionality
    """
    def __init__(self, coordinate: tuple[int, int]) -> None:
        self._note_num = DRUM_PADS[coordinate[0]][coordinate[1]]
        # Variables to keep the drumpad lights working
        self._ticker_timer = 0
        super().__init__(
            ForwardedPattern(2, NotePattern(self._note_num, 0)),
            ForwardedStrategy(NoteStrategy()),
            coordinate
        )

    @profilerDecoration("LaunchKey onColorChange")
    def onColorChange(self) -> None:
        c_num = COLORS[self.color.closest(list(COLORS.keys()))]
        forwardEvent(EventData(0x90, self._note_num, c_num), 2)
        # print(f"{self.coordinate} : #{self.color.integer:06X} -> {c_num}")
        pass

    def tick(self) -> None:
        # Occasionally refresh lights since launchkey lights are sorta buggy
        if self._ticker_timer % 20 == 0:
            self.onColorChange()
        self._ticker_timer += 1


# TODO: Find a way to make there be less repeated code
class LkControlSwitchButton(ControlSwitchButton):
    def __init__(self) -> None:
        self._note_num = 0x68
        self._ticker_timer = 0
        super().__init__(
            ForwardedPattern(2, NotePattern(self._note_num, 0xF)),
            ForwardedStrategy(NoteStrategy())
        )

    # def onColorChange(self) -> None:
    #     c_num = COLORS[self.color.closest(list(COLORS.keys()))]
    #     forwardEvent(EventData(0x9F, self._note_num, c_num), 2)

    def tick(self) -> None:
        if self._ticker_timer % 20 == 0:
            self.onColorChange()
        self._ticker_timer += 1


class LkMetronomeButton(MetronomeButton):
    def __init__(self) -> None:
        self._note_num = 0x78
        self._ticker_timer = 0
        super().__init__(
            ForwardedPattern(2, NotePattern(self._note_num, 0xF)),
            ForwardedStrategy(NoteStrategy())
        )

    # def onColorChange(self) -> None:
    #     c_num = COLORS[self.color.closest(list(COLORS.keys()))]
    #     forwardEvent(EventData(0x9F, self._note_num, c_num), 2)

    def tick(self) -> None:
        if self._ticker_timer % 20 == 0:
            self.onColorChange()
        self._ticker_timer += 1
