"""
devices > novation > launchkey > incontrol > controls > pause_active

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces import PauseActiveButton
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import NoteStrategy, ForwardedStrategy
from . import ColorInControlSurface
from ..colors.mk3 import COLORS


class LkPauseActive(ColorInControlSurface, PauseActiveButton):
    """
    Pause updating the active plugin.

    Stop/Solo/Mute button on larger LkMk3 models
    """
    def __init__(self) -> None:
        ColorInControlSurface.__init__(
            self,
            0,
            0x78,
            COLORS,
        )
        PauseActiveButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xB0, 0x78, ...)),
            ForwardedStrategy(NoteStrategy()),
        )
