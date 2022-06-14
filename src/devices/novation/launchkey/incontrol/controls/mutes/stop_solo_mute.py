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
from control_surfaces import NullEvent
from control_surfaces.matchers import ShiftMatcher
from ..incontrol_surface import ColorInControlSurface
from ...colors.mk3 import COLORS
from ..drum_pad import (
    LkDrumPadMatcher,
    LkMk3DrumPad,
    LkMk3DrumPadSolo,
    LkMk3DrumPadMute,
)


class StopSoloMuteButton(NullEvent):
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


def getMk3SmallMuteControls() -> ShiftMatcher:
    """
    Returns a control matcher used to get mappings for the drum pads and
    stop/solo/mute button on smaller launchkey models.
    """
    stop_mute_solo = StopSoloMuteButton()
    # Stop/solo/mute button not pressed
    non_shift_matcher = LkDrumPadMatcher(LkMk3DrumPad)
    # Stop/solo/mute button pressed
    shift_matcher = LkDrumPadMatcher(LkMk3DrumPadSolo, LkMk3DrumPadMute)

    return ShiftMatcher(
        stop_mute_solo,
        non_shift_matcher,
        shift_matcher,
    )
