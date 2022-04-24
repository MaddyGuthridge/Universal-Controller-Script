
from common import profilerDecoration
from common.types import EventData, Color
from common.util.events import forwardEvent
from ..consts import REFRESH_INTERVAL


class InControlSurface:
    """Forwarder to manage sending color events to Launchkey controls
    """

    def __init__(
        self,
        channel: int,
        note_num: int,
        colors: dict[Color, int],
    ) -> None:
        # Initialise whatever
        self.__channel = channel
        self.__note = note_num
        self.__colors = colors
        self.__recent_col = 0
        # Variable to keep the drumpad lights working
        self.__ticker_timer = 0

    @profilerDecoration("LaunchKey onColorChange")
    def onColorChange(self, new: Color) -> None:
        """Called when the color changes"""
        c_num = self.__colors[new.closest(list(self.__colors.keys()))]
        self.__recent_col = c_num
        self.updateColor()

    def updateColor(self) -> None:
        """Send a color update event from the recent color"""
        forwardEvent(
            EventData(
                (9 << 4) + self.__channel,
                self.__note,
                self.__recent_col,
            ),
            2,
        )

    def tick(self) -> None:
        """Occasionally refresh lights since launchkey lights are sorta buggy
        """
        if self.__ticker_timer % REFRESH_INTERVAL == 0:
            self.updateColor()
        self.__ticker_timer += 1
