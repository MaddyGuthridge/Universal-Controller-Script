"""
devices > novation > launchkey > incontrol > controls > mutes > stop_solo_mute

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy
)
from control_surfaces import NullControl
from ..incontrol_surface import ColorInControlSurface
from ...colors.mk3 import COLORS


class StopSoloMuteButton(NullControl):
    """
    Stop/solo/mute button is used to switch drum pads to a mode where they can
    be used to mute and solo tracks on smaller launchkey mk3 models.
    """
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xB0, 0x69, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=ColorInControlSurface(
                0x0,
                0x69,
                COLORS,
                event_num=0xB,
            )
        )

    @staticmethod
    def isPress(value: float) -> bool:
        return value != 0.0
