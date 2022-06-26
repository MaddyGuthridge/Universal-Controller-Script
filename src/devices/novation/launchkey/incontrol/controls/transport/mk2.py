"""
devices > novation > launchkey > incontrol > controls > transport > mk2

Definitions for transport controls used by Launchkey Mk2 Launchkey devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""


from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    LoopButton,
    StopButton,
    PlayButton,
    RecordButton,
)
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)

__all__ = [
    'LkMk2LoopButton',
    'LkMk2StopButton',
    'LkMk2PlayButton',
    'LkMk2RecordButton',
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


class LkMk2PlayButton(PlayButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkMk2RecordButton(RecordButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
