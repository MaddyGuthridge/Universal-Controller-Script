"""
devices > novation > launchkey > incontrol > controls > transport > common

Definitions for transport controls shared between Launchkey devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
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
    'LkFastForwardButton',
    'LkRewindButton',
    'LkQuantizeButton',
    'LkUndoRedoButton',
]


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
