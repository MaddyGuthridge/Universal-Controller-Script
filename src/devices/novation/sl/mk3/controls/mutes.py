"""
devices > novation > sl > mk3 > controls > mutes

Definitions for mute and solo buttons used by the SL Mk3 device

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    MuteButton,
    SoloButton,
)
from control_surfaces.value_strategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from control_surfaces.matchers import (
    BasicControlMatcher,
    IndexedMatcher
)
from .sl_color_surface import SlColorSurface

__all__ = [
    'SlMuteButton',
    'SlMuteSet',
]


# Start values
S_START = 0x3B
S_COLOR_START = 0x0C


class SlSoloButton(SoloButton):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, S_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index),
            color_manager=SlColorSurface(S_COLOR_START + index)
        )


# Start values
M_START = 0x43
M_COLOR_START = 0x14


class SlMuteButton(MuteButton):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, M_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index),
            color_manager=SlColorSurface(M_COLOR_START + index)
        )


class SlMuteSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, S_START, [
            SlSoloButton(i) for i in range(8)
        ], 2))
        self.addSubMatcher(IndexedMatcher(0xBF, M_START, [
            SlMuteButton(i) for i in range(8)
        ], 2))
