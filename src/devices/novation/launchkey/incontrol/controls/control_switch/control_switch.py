"""
devices > novation > launchkey > incontrol > controls > control_switch
> control_switch

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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


class LkControlSwitchButton(ControlSwitchButton):
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
        if event_num == 9:
            # Note
            pat: IEventPattern = NotePattern(note_num, channel)
        else:
            # Something else
            pat = BasicPattern(status, note_num, ...)
        super().__init__(
            ForwardedPattern(2, pat),
            ForwardedStrategy(NoteStrategy()),
            color_manager=ColorInControlSurface(
                channel,
                note_num,
                colors,
                event_num,
            )
        )
