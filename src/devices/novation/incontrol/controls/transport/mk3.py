"""
devices > novation > incontrol > controls > transport > mk3

Definitions for transport controls used by Launchkey Mk3 Launchkey devices
"""

from common.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces import (
    LoopButton,
    StopButton,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)

__all__ = [
    'LkMk3LoopButton',
    'LkMk3StopButton',
]


class LkMk3StopButton(StopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkMk3LoopButton(LoopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x76, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
