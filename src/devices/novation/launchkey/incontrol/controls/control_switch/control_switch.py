"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from control_surfaces.event_patterns import (
    BasicPattern,
    NotePattern,
    IEventPattern,
    ForwardedPattern
)
from common.types import Color
from control_surfaces.value_strategies import NoteStrategy, ForwardedStrategy
from control_surfaces import ControlSwitchButton
from ..incontrol_surface import ColorInControlSurface


class LkControlSwitchButton(ColorInControlSurface, ControlSwitchButton):
    def __init__(
        self,
        channel: int,
        note_num: int,
        colors: dict[Color, int],
        event_num: int,
    ) -> None:
        status = (event_num << 4) + channel
        self._color_manager = ColorInControlSurface(status, note_num, colors)
        # Variable to keep lights working
        self._ticker_timer = 0
        ColorInControlSurface.__init__(
            self,
            channel,
            note_num,
            colors,
            event_num,
        )
        if event_num == 9:
            # Note
            pat: IEventPattern = NotePattern(note_num, channel)
        else:
            # Something else
            pat = BasicPattern(status, note_num, ...)
        ControlSwitchButton.__init__(
            self,
            ForwardedPattern(2, pat),
            ForwardedStrategy(NoteStrategy()),
        )
