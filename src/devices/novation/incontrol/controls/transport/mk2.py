"""
devices > novation > incontrol > controls > transport > mk2

Definitions for transport controls used by Launchkey Mk2 Launchkey devices
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
    'LkMk2LoopButton',
    'LkMk2StopButton',
]


class LkMk2StopButton(StopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x72, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkMk2LoopButton(LoopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
