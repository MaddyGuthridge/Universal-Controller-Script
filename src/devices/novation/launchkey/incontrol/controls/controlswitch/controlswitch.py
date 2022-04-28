"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import ForwardedPattern
from common.eventpattern import BasicPattern
from common.types import Color
from controlsurfaces.valuestrategies import NoteStrategy, ForwardedStrategy
from controlsurfaces import ControlSwitchButton
from ..incontrolsurface import InControlSurface


class LkControlSwitchButton(InControlSurface, ControlSwitchButton):
    """
    Custom drum pad implementation used by Lunchkey series controllers
    to provide RGB functionality
    """
    def __init__(
        self,
        status: int,
        channel: int,
        note_num: int,
        colors: dict[Color, int],
    ) -> None:
        self._color_manager = InControlSurface(status, note_num, colors)
        # Variable to keep the drumpad lights working
        self._ticker_timer = 0
        InControlSurface.__init__(
            self,
            channel,
            note_num,
            colors,
        )
        ControlSwitchButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(status, note_num, ...)),
            ForwardedStrategy(NoteStrategy()),
        )
