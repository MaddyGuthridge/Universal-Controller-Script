"""
devices > novation > launchkey > incontrol > controls > transport > mk3

Definitions for transport controls used by Launchkey Mk3 Launchkey devices

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
    CaptureMidiButton,
)
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from ..incontrol_surface import GrayscaleInControlSurface
from ...colors.grayscale import COLORS

__all__ = [
    'LkMk3LoopButton',
    'LkMk3StopButton',
    'LkMk3PlayButton',
    'LkMk3RecordButton',
]


class LkMk3StopButton(StopButton):
    def __init__(self) -> None:
        val = 0x74
        StopButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )


class LkMk3LoopButton(LoopButton):
    def __init__(self) -> None:
        val = 0x76
        LoopButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )


class LkMk3PlayButton(PlayButton):
    def __init__(self) -> None:
        val = 0x73
        PlayButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=GrayscaleInControlSurface(
                0x0,
                val,
                COLORS,
                0xB,
            )
        )


class LkMk3RecordButton(RecordButton):
    def __init__(self) -> None:
        val = 0x75
        RecordButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, val, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=GrayscaleInControlSurface(
                0x0,
                val,
                COLORS,
                0xB,
            )
        )


class LkMk3CaptureMidiButton(CaptureMidiButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4A, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )
