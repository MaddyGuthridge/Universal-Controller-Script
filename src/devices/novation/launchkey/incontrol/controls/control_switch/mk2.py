"""
devices > novation > launchkey > incontrol > controls > control_switch > mk2

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .control_switch import LkControlSwitchButton
from ...colors.mk2 import COLORS


class LkMk2ControlSwitchButton(LkControlSwitchButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            0xF,
            0x68,
            COLORS,
            0x9
        )
