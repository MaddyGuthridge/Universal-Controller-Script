"""
devices > novation > launchkey > incontrol > controls > navigation > mk2

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
)
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)

__all__ = [
    'LkMk2DirectionNext',
    'LkMk2DirectionPrevious',
]


class LkMk2DirectionNext(DirectionNext):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkMk2DirectionPrevious(DirectionPrevious):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
