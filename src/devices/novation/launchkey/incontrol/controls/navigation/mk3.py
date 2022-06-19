"""
devices > novation > launchkey > incontrol > controls > navigation > mk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
    NullStrategy,
)
from control_surfaces import (
    DirectionUp,
    DirectionDown,
    DirectionLeft,
    DirectionRight,
    NullControl,
)
from .. import ColorInControlSurface, GrayscaleInControlSurface
from ...colors.mk3 import COLORS
from ...colors.grayscale import COLORS as GRAYSCALE


class MiniMk3DirectionUp(DirectionUp):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xB0, 0x68, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=ColorInControlSurface(
                0x0,
                0x68,
                COLORS,
                event_num=0xB,
            )
        )


class MiniMk3DirectionDown(DirectionDown):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xB0, 0x69, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=ColorInControlSurface(
                0x0,
                0x69,
                COLORS,
                event_num=0xB,
            )
        )


class Mk3DirectionLeft(DirectionLeft):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=GrayscaleInControlSurface(
                0xF,
                0x67,
                GRAYSCALE,
            )
        )


class Mk3DirectionRight(DirectionRight):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=GrayscaleInControlSurface(
                0xF,
                0x66,
                GRAYSCALE,
            )
        )


class Mk3DirectionUp(DirectionUp):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x6A, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=ColorInControlSurface(
                0x0,
                0x6A,
                COLORS,
            )
        )


class Mk3DirectionDown(DirectionDown):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x6B, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            color_manager=ColorInControlSurface(
                0x0,
                0x6B,
                COLORS,
            )
        )


class Mk3DirectionUpSilenced(NullControl):
    """Up/down buttons on LkMk3 seem to provide extra events, which we ignore
    """
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x68, ...)),
            NullStrategy(),
        )


class Mk3DirectionDownSilenced(NullControl):
    """Up/down buttons on LkMk3 seem to provide extra events, which we ignore
    """
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x69, ...)),
            NullStrategy(),
        )
