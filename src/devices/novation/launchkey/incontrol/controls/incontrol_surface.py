"""
devices > novation > launchkey > incontrol > controls > incontrol_surface

Contains the base class for Launchkey control surfaces that can be colorized.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common import profilerDecoration
from fl_classes import FlMidiMsg
from common.types import Color
from common.util.events import forwardEvent
from ..consts import REFRESH_INTERVAL

__all__ = [
    'ColorInControlSurface',
    'GrayscaleInControlSurface',
]


class InControlSurface:
    def __init__(self, status: int, note: int) -> None:
        self.__status = status
        self.__note = note
        self.__color = 0
        # Variable to keep the lights working, since sometimes they might be
        # set to the wrong value through other means
        self.__ticker_timer = 0

    def setColor(self, new: int):
        self.__color = new

    def updateColor(self) -> None:
        """Send a color update event from the recent color"""
        forwardEvent(
            FlMidiMsg(
                self.__status,
                self.__note,
                self.__color,
            ),
            2,
        )

    def tick(self) -> None:
        """Occasionally refresh lights since launchkey lights are sorta buggy
        """
        if self.__ticker_timer % REFRESH_INTERVAL == 0:
            self.updateColor()
        self.__ticker_timer += 1


class ColorInControlSurface(InControlSurface):
    """Forwarder to manage sending color events to Launchkey controls
    """
    def __init__(
        self,
        channel: int,
        note_num: int,
        colors: dict[Color, int],
        event_num: int = 0x9,
    ) -> None:
        status = (event_num << 4) + channel
        self.__colors = colors
        super().__init__(status, note_num)

    @profilerDecoration("LaunchKey onColorChange")
    def onColorChange(self, new: Color) -> None:
        """Called when the color changes"""
        self.setColor(self.__colors[new.closest(list(self.__colors.keys()))])
        self.updateColor()


class GrayscaleInControlSurface(InControlSurface):
    """Forwarder to manage sending grayscale color events to Launchkey controls
    """

    def __init__(
        self,
        channel: int,
        note_num: int,
        colors: dict[float, int],
        event_num: int = 0x9,
    ) -> None:
        status = (event_num << 4) + channel
        self.__colors = colors
        super().__init__(status, note_num)

    @profilerDecoration("LaunchKey onColorChange")
    def onColorChange(self, new: Color) -> None:
        """Called when the color changes"""
        self.setColor(self.__colors[new.closestGrayscale(
            list(self.__colors.keys())
        )])
        self.updateColor()
