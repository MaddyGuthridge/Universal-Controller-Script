"""
devices > novation > sl > mk3 > controls > encoder

Definitions for endless encoder controls used by the SL Mk3 device

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    Encoder,
)
from control_surfaces.value_strategies import (
    TwosComplimentDeltaStrategy,
    ForwardedStrategy,
)
from control_surfaces.matchers import (
    BasicControlMatcher,
    IndexedMatcher
)
# from .sl_color_surface import SlColorSurface

__all__ = [
    'SlEncoder',
    'SlEncoderSet',
]

# Encoder start
E_START = 0x15
# E_COLOR_START = 0x36


class SlEncoder(Encoder):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, E_START + index, ...)),
            ForwardedStrategy(TwosComplimentDeltaStrategy(scaling=0.3)),
            (0, index),
            # color_manager=SlColorSurface(E_COLOR_START + index)
        )


class SlEncoderSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, E_START, [
            SlEncoder(i) for i in range(8)
        ], 2))
