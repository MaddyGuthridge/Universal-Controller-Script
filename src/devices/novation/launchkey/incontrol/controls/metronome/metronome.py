"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from controlsurfaces.eventpattern import ForwardedPattern,  NotePattern
from common.types import Color
from controlsurfaces.valuestrategies import NoteStrategy, ForwardedStrategy
from controlsurfaces import MetronomeButton
from ..incontrolsurface import ColorInControlSurface


class LkMetronomeButton(ColorInControlSurface, MetronomeButton):
    """
    Custom drum pad implementation used by Lunchkey series controllers
    to provide RGB functionality
    """
    def __init__(
        self,
        channel: int,
        note_num: int,
        colors: dict[Color, int],
        event_num: int,
    ) -> None:
        self._color_manager = ColorInControlSurface(channel, note_num, colors)
        # Variable to keep the drumpad lights working
        self._ticker_timer = 0
        ColorInControlSurface.__init__(
            self,
            channel,
            note_num,
            colors,
            event_num,
        )
        MetronomeButton.__init__(
            self,
            ForwardedPattern(2, NotePattern(note_num, channel)),
            ForwardedStrategy(NoteStrategy()),
        )
