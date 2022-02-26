"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads
"""

from common.eventpattern import BasicPattern, fromNibbles
from controlsurfaces.valuestrategies import NoteStrategy
from controlsurfaces import DrumPad
from .colors import COLORS
import device

DRUM_PADS = [
    [0x28, 0x29, 0x2A, 0x2B, 0x30, 0x31, 0x32, 0x33], # Also 0x68
    [0x24, 0x25, 0x26, 0x27, 0x2C, 0x2D, 0x2E, 0x2F]  # Also 0x69
]

class LaunchkeyDrumpad(DrumPad):
    
    def __init__(self, coordinate: tuple[int, int]) -> None:
        self._note_num = DRUM_PADS[coordinate[0]][coordinate[1]]
        super().__init__(
            BasicPattern(fromNibbles((8, 9), 9), self._note_num, ...),
            NoteStrategy(),
            coordinate
        )
    
    def onColorChange(self) -> None:
        c_num = COLORS[self.color.closest(list(COLORS.keys()))]
        device.midiOutMsg(0x9F + (self._note_num << 8) + (c_num << 16))
