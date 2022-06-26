"""
devices > novation > launchkey > incontrol > controls > control_switch > mk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .control_switch import LkControlSwitchButton
from ...colors.mk3 import COLORS


class LkMk3ControlSwitchButton(LkControlSwitchButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            0,
            0x68,
            COLORS,
            0xB
        )
