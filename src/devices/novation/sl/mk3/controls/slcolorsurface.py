
from common.types import EventData, Color
from common.util.events import forwardEvent


class SlColorSurface:
    """Forwarder to manage sending color events to Launchkey controls
    """

    def __init__(
        self,
        note_num: int,
    ) -> None:
        self.__note = note_num

    def onColorChange(self, new: Color) -> None:
        """Called when the color changes"""
        forwardEvent(
            EventData([
                0xF0,
                0x00,
                0x20,
                0x29,
                0x02,
                0x0A,
                0x01,
                0x03,
                self.__note,
                new.red // 2,
                new.green // 2,
                new.blue // 2,
                0xF7,
            ]),
            2,
        )
