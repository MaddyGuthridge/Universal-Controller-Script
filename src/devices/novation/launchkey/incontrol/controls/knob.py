"""
devices > novation > launchkey > incontrol > controls > knob

Definitions for knob controls shared between Launchkey devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import Knob
from control_surfaces.value_strategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from control_surfaces.matchers import IndexedMatcher

__all__ = [
    'LkKnob',
    'LkKnobSet',
]

# Fader start
K_START = 0x15


class LkKnob(Knob):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, K_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkKnobSet(IndexedMatcher):
    def __init__(self) -> None:
        super().__init__(0xBF, K_START, [
            LkKnob(i) for i in range(8)
        ], 2)
