"""
devices > novation > sl > mk3 > controls > transport

Transport control definitions for the Novation SL Mk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
    FastForwardButton,
    LoopButton,
    PlayButton,
    RecordButton,
    RewindButton,
    StopButton,
)
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from .sl_color_surface import SlColorSurface

__all__ = [
    'SlDirectionNext',
    'SlDirectionPrevious',
    'SlFastForwardButton',
    'SlLoopButton',
    'SlPlayButton',
    'SlRecordButton',
    'SlRewindButton',
    'SlStopButton',
]


class SlStopButton(StopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x72, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x23)
        )


class SlPlayButton(PlayButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x24)
        )


class SlLoopButton(LoopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x25)
        )


class SlRecordButton(RecordButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x20)
        )


class SlDirectionNext(DirectionNext):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x1E)
        )


class SlDirectionPrevious(DirectionPrevious):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x1F)
        )


class SlRewindButton(RewindButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x70, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x21)
        )


class SlFastForwardButton(FastForwardButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x71, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x22)
        )
