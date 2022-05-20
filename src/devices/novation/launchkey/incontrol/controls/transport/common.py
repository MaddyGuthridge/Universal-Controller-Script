"""
devices > novation > incontrol > controls > transport > common

Definitions for transport controls shared between Launchkey devices
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
    FastForwardButton,
    RewindButton,
    QuantizeButton,
    UndoRedoButton,
)
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)

__all__ = [
    'LkDirectionNext',
    'LkDirectionPrevious',
    'LkFastForwardButton',
    'LkRewindButton',
    'LkQuantizeButton',
    'LkUndoRedoButton',
]


class LkDirectionNext(DirectionNext):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkDirectionPrevious(DirectionPrevious):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkRewindButton(RewindButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x70, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkFastForwardButton(FastForwardButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x71, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkQuantizeButton(QuantizeButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4B, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )


class LkUndoRedoButton(UndoRedoButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4D, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )
