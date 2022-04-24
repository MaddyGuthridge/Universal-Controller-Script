"""
devices > novation > incontrol > controls > knob

Definitions for knob controls shared between Launchkey devices
"""

from common.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces import Knob
from controlsurfaces.valuestrategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from devices.matchers import IndexedMatcher

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
        ])
