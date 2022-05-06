"""
devices > novation > sl > mk3 > controls > transport

Definitions for transport controls shared between Launchkey devices
"""

from controlsurfaces.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces import (
    DirectionNext,
    DirectionPrevious,
    FastForwardButton,
    LoopButton,
    PlayButton,
    RecordButton,
    RewindButton,
    StopButton,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from .slcolorsurface import SlColorSurface

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


class SlStopButton(SlColorSurface, StopButton):
    def __init__(self) -> None:
        StopButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x72, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x23,
        )


class SlPlayButton(SlColorSurface, PlayButton):
    def __init__(self) -> None:
        PlayButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x24,
        )


class SlLoopButton(SlColorSurface, LoopButton):
    def __init__(self) -> None:
        LoopButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x25,
        )


class SlRecordButton(SlColorSurface, RecordButton):
    def __init__(self) -> None:
        RecordButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x20,
        )


class SlDirectionNext(SlColorSurface, DirectionNext):
    def __init__(self) -> None:
        DirectionNext.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x1E,
        )


class SlDirectionPrevious(SlColorSurface, DirectionPrevious):
    def __init__(self) -> None:
        DirectionPrevious.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x1F,
        )


class SlRewindButton(SlColorSurface, RewindButton):
    def __init__(self) -> None:
        RewindButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x70, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x21,
        )


class SlFastForwardButton(SlColorSurface, FastForwardButton):
    def __init__(self) -> None:
        FastForwardButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x71, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        SlColorSurface.__init__(
            self,
            0x22,
        )
