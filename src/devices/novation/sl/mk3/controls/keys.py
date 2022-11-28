"""
devices > novation > sl > mk3 > controls > keys

Definitions for the LEDs above the keys of the SL Mk3 controller

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types.color import Color
from control_surfaces.event_patterns import NullPattern
from control_surfaces import (
    Ambient,
)
from control_surfaces.value_strategies import (
    NullStrategy
)
from control_surfaces.managers import IColorManager
from .sl_color_surface import SlColorSurface


class AmbientColors(IColorManager):
    """
    Controls ambient colors for the SL
    """
    def __init__(self) -> None:
        self.managers = [
            SlColorSurface(i)
            for i in range(36, 73)
        ]

    def onColorChange(self, new_color: Color) -> None:
        for m in self.managers:
            m.onColorChange(new_color)

    def tick(self) -> None:
        for m in self.managers:
            m.tick()


class SlAmbientKeys(Ambient):
    """
    Allows the key LEDs to show ambient colors
    """
    def __init__(self) -> None:
        super().__init__(
            NullPattern(),
            NullStrategy(),
            color_manager=AmbientColors()
        )
