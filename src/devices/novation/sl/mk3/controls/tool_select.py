"""
devices > novation > sl > mk3 > controls > tool_select

Definitions for tool select controls used by the SL Mk3 device

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    ToolSelector,
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
    'SlToolSelector',
    'SlToolSelectorSet',
]

# Start values
F_START = 0x33
F_COLOR_START = 0x04


class SlToolSelector(ToolSelector):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, F_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index),
            color_manager=SlColorSurface(F_COLOR_START + index)
        )


class SlToolSelectorSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, F_START, [
            SlToolSelector(i) for i in range(8)
        ], 2))
