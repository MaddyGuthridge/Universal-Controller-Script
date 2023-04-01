"""
devices > novation > launchkey > incontrol > controls > activity

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces import PauseActiveButton, NullControl
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import (
    Data2Strategy,
    NullStrategy,
    ForwardedStrategy,
)
from . import ColorInControlSurface
from ..colors.mk3 import COLORS


class LkPauseActive(PauseActiveButton):
    """
    Pause updating the active plugin.

    Stop/Solo/Mute button on larger LkMk3 models
    """
    def __init__(self) -> None:
        PauseActiveButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xB0, 0x69, ...)),
            ForwardedStrategy(Data2Strategy()),
            color_manager=ColorInControlSurface(
                0,
                0x69,
                COLORS,
                event_num=0xB,
            )
        )


class LkDeviceSelect(NullControl):
    """
    Open the activity switcher

    Device select button.
    """
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x33, ...)),
            ForwardedStrategy(Data2Strategy()),
        )


class LkDeviceSelectExtras(NullControl):
    """
    Handle extra events when the DeviceSelect button is pressed
    """
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x03, (0x02, 0x09))),
            NullStrategy(),
        )
