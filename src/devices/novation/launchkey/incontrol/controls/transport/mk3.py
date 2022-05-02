"""
devices > novation > incontrol > controls > transport > mk3

Definitions for transport controls used by Launchkey Mk3 Launchkey devices
"""

from common.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces import (
    LoopButton,
    StopButton,
    PlayButton,
    RecordButton,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from ..incontrolsurface import InControlSurface
from ...colors.standard import COLORS

__all__ = [
    'LkMk3LoopButton',
    'LkMk3StopButton',
    'LkMk3PlayButton',
    'LkMk3RecordButton',
]


class LkMk3StopButton(StopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )


class LkMk3LoopButton(LoopButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x76, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )


class LkMk3PlayButton(InControlSurface, PlayButton):
    def __init__(self) -> None:
        PlayButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )
        InControlSurface.__init__(
            self,
            0x0,
            0x73,
            COLORS,
            0xB,
        )


class LkMk3RecordButton(InControlSurface, RecordButton):
    def __init__(self) -> None:
        RecordButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )
        InControlSurface.__init__(
            self,
            0x0,
            0x75,
            COLORS,
            0xB,
        )
