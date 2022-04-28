"""
devices > novation > incontrol > controls > hintmsg

Hint message, used by Mk3 devices
"""
from controlsurfaces import HintMsg
from common.types import EventData
from common.util.events import forwardEvent

LINE_LEN = 16


class LkNotifMsg(HintMsg):
    """Launchkey Mk3 hint message"""

    def onAnnotationChange(self, new: str) -> None:
        new = new[:LINE_LEN]
        # TODO: Check if this encoding works
        sysex = bytes(
            [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0F, 0x04]
        ) + new.encode('ascii') + bytes([0, 0, 0xF7])
        forwardEvent(EventData(sysex), 2)
