"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads
"""
from common import profilerDecoration
from common.eventpattern import BasicPattern, fromNibbles
from common.types import EventData
from common.util.events import forwardEvent
from controlsurfaces.valuestrategies import NoteStrategy
from controlsurfaces import DrumPad
from .colors import COLORS

DRUM_PADS = [
    [0x28, 0x29, 0x2A, 0x2B, 0x30, 0x31, 0x32, 0x33], # Also 0x68
    [0x24, 0x25, 0x26, 0x27, 0x2C, 0x2D, 0x2E, 0x2F]  # Also 0x69
]

class LaunchkeyDrumpad(DrumPad):
    
    def __init__(self, coordinate: tuple[int, int]) -> None:
        self._note_num = DRUM_PADS[coordinate[0]][coordinate[1]]
        # Variables to keep the drumpad lights working
        self._ticker_timer = 0
        self._need_update = False
        super().__init__(
            BasicPattern(fromNibbles((8, 9), 9), self._note_num, ...),
            NoteStrategy(),
            coordinate
        )
    
    @profilerDecoration("LaunchKey onColorChange")
    def onColorChange(self) -> None:
        c_num = COLORS[self.color.closest(list(COLORS.keys()))]
        forwardEvent(EventData(0x9F, self._note_num, c_num), 2)
        # print(f"{self.coordinate} : #{self.color.integer:06X} -> {c_num}")
    
    def onValueChange(self) -> None:
        # Ensure the lights stay on when we press them
        self._need_update = True

    def tick(self) -> None:
        # Occasionally refresh lights since launchkey lights are sorta buggy
        if self._ticker_timer % 5 == 0 or self._need_update:
            self.onColorChange()
            self._need_update = False
        self._ticker_timer += 1
