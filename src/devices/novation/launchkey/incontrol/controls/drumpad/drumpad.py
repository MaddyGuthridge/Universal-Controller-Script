"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import ForwardedPattern
from common.eventpattern.notepattern import NotePattern
from common.types import Color
from controlsurfaces.valuestrategies import NoteStrategy, ForwardedStrategy
from controlsurfaces import DrumPad
from .. import InControlSurface
from ...consts import DRUM_ROWS, DRUM_COLS
from devices.matchers import (
    BasicControlMatcher,
)


class LkDrumPad(InControlSurface, DrumPad):
    """
    Custom drum pad implementation used by Lunchkey series controllers
    to provide RGB functionality
    """
    def __init__(
        self,
        coordinate: tuple[int, int],
        channel: int,
        note_num: int,
        colors: dict[Color, int]
    ) -> None:
        InControlSurface.__init__(
            self,
            channel,
            note_num,
            colors,
        )
        DrumPad.__init__(
            self,
            ForwardedPattern(2, NotePattern(note_num, channel)),
            ForwardedStrategy(NoteStrategy()),
            coordinate
        )

    @classmethod
    def create(cls, row: int, col: int) -> 'LkDrumPad':
        raise NotImplementedError()


class LkDrumPadMatcher(BasicControlMatcher):
    """Matcher for launchkey drum pads"""
    def __init__(self, drum_type: type[LkDrumPad]) -> None:
        super().__init__()
        for r in range(DRUM_ROWS):
            for c in range(DRUM_COLS):
                self.addControl(drum_type.create(r, c), 10)
