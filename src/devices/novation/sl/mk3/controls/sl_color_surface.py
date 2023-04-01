"""
devices > novation > sl > mk3 > controls > sl_color_surface

Contains definition for SlColorSurface class, which manages the colors of
controls on the SL Mk3.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg
from control_surfaces.managers import IColorManager
from common.types import Color
from common.util.events import forwardEvent


class SlColorSurface(IColorManager):
    """Forwarder to manage sending color events to Launchkey controls
    """

    def __init__(
        self,
        note_num: int,
        contrast_fix: bool = True,
    ) -> None:
        self.__index = note_num
        self.__contrast_fix = contrast_fix

    def onColorChange(self, new: Color) -> None:
        """Called when the color changes"""
        new = new.fadeGray(-0.5, enabled=new.enabled)
        # Ignore whenever the light isn't enabled, as a fix for bad contrast
        if not new.enabled and self.__contrast_fix:
            new = Color()
        forwardEvent(
            FlMidiMsg([
                0xF0,
                0x00,
                0x20,
                0x29,
                0x02,
                0x0A,
                0x01,
                0x03,
                self.__index,
                0x01,
                new.red // 2,
                new.green // 2,
                new.blue // 2,
                0xF7,
            ]),
            2,
        )

    def tick(self) -> None:
        return
