
from .controlswitch import LkControlSwitchButton
from ...colors.standard import COLORS


class LkMk3ControlSwitchButton(LkControlSwitchButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            0xB0,
            0x0,
            0x68,
            COLORS,
        )
