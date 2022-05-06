"""
devices > novation > incontrol > controls > transport > mk3

Definitions for transport controls used by Launchkey Mk3 Launchkey devices
"""

from controlsurfaces.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces import (
    LoopButton,
    StopButton,
    PlayButton,
    RecordButton,
    CaptureMidiButton,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from ..incontrolsurface import GrayscaleInControlSurface
from ...colors.greyscale import COLORS

__all__ = [
    'LkMk3LoopButton',
    'LkMk3StopButton',
    'LkMk3PlayButton',
    'LkMk3RecordButton',
]


class LkMk3StopButton(GrayscaleInControlSurface, StopButton):
    def __init__(self) -> None:
        val = 0x74
        StopButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        GrayscaleInControlSurface.__init__(
            self,
            0x0,
            val,
            COLORS,
            0xB,
        )


class LkMk3LoopButton(GrayscaleInControlSurface, LoopButton):
    def __init__(self) -> None:
        val = 0x76
        LoopButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        GrayscaleInControlSurface.__init__(
            self,
            0x0,
            val,
            COLORS,
            0xB,
        )


class LkMk3PlayButton(GrayscaleInControlSurface, PlayButton):
    def __init__(self) -> None:
        val = 0x73
        PlayButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        GrayscaleInControlSurface.__init__(
            self,
            0x0,
            val,
            COLORS,
            0xB,
        )


class LkMk3RecordButton(GrayscaleInControlSurface, RecordButton):
    def __init__(self) -> None:
        val = 0x75
        RecordButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        GrayscaleInControlSurface.__init__(
            self,
            0x0,
            val,
            COLORS,
            0xB,
        )


class LkMk3CaptureMidiButton(CaptureMidiButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4A, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )
        pass
