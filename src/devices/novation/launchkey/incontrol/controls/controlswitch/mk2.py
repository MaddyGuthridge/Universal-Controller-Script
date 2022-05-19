
from .controlswitch import LkControlSwitchButton
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
