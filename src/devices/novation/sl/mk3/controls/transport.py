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
    DirectionLeft,
    DirectionRight,
    DirectionUp,
    DirectionDown,
    FastForwardButton,
    LoopButton,
    PlayButton,
    RecordButton,
    RewindButton,
    StopButton,
    ControlSwitchButton,
    NullControl,
)
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from .sl_color_surface import SlColorSurface

__all__ = [
    'SlDirectionRight',
    'SlDirectionLeft',
    'SlDirectionDown',
    'SlDirectionUp',
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


class SlDirectionRight(DirectionRight):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x1F)
        )


class SlDirectionLeft(DirectionLeft):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x1E)
        )


class SlDirectionNext(DirectionNext):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x56, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x1)
        )


class SlDirectionPrevious(DirectionPrevious):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x55, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x0)
        )


class SlDirectionDown(DirectionDown):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x52, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x3F)
        )


class SlDirectionUp(DirectionUp):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x51, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x3E)
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


class SlControlSwitchButton(ControlSwitchButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x5A, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x41, contrast_fix=False)
        )


class SlActivitySwitchButton(NullControl):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x59, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=SlColorSurface(0x40, contrast_fix=False)
        )
