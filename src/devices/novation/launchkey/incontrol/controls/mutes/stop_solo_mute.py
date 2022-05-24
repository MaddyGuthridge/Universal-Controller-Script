
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy
)
from control_surfaces import NullEvent
from devices.matchers.shift_matcher import ShiftMatcher
from ..incontrol_surface import ColorInControlSurface
from ...colors.mk3 import COLORS
from ..drum_pad import (
    LkDrumPadMatcher,
    LkMk3DrumPad,
    LkMk3DrumPadSolo,
    LkMk3DrumPadMute,
)


class StopSoloMuteButton(ColorInControlSurface, NullEvent):
    def __init__(self) -> None:
        ColorInControlSurface.__init__(
            self,
            0x0,
            0x69,
            COLORS,
            event_num=0xB
        )
        NullEvent.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xB0, 0x69, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )

    @staticmethod
    def isPress(value: float) -> bool:
        return value != 0.0


def getMk3SmallMuteControls() -> ShiftMatcher:
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
