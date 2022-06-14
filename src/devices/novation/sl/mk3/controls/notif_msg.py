"""
devices > novation > sl > mk3 > controls > notif_msg

Definition for notification message control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces import NotifMsg
from fl_classes import FlMidiMsg
from common.util.events import forwardEvent

LINE_LEN = 18


class SlNotifMsg(NotifMsg):
    """SL Mk3 notification message"""

    def __init__(self) -> None:
        super().__init__(annotation_manager=None)  # TODO

    def onAnnotationChange(self, new: str) -> None:
        new = new[:LINE_LEN]
        # TODO: Check if this encoding works
        sysex = bytes(
            [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0A, 0x01, 0x04]
        ) + new.encode('ascii') + bytes([0, 0, 0xF7])
        forwardEvent(FlMidiMsg(sysex), 2)
