"""
devices > novation > incontrol > controls > transport > common

Definitions for transport controls shared between Launchkey devices
"""

from common.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces import (
    DirectionNext,
    DirectionPrevious,
    FastForwardButton,
    PlayButton,
    RecordButton,
    RewindButton,
    QuantizeButton,
    MetronomeButton,
    UndoRedoButton,
)
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)

__all__ = [
    'LkDirectionNext',
    'LkDirectionPrevious',
    'LkFastForwardButton',
    'LkPlayButton',
    'LkRecordButton',
    'LkRewindButton',
    'LkQuantizeButton',
    'LkMetronomeButton',
    'LkUndoRedoButton',
    'LkCaptureMidiButton',
]


class LkPlayButton(PlayButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x73, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkRecordButton(RecordButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkDirectionNext(DirectionNext):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x66, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkDirectionPrevious(DirectionPrevious):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x67, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


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


class LkMetronomeButton(MetronomeButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4C, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        )


class LkUndoRedoButton(UndoRedoButton):
    def __init__(self) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4D, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )


class LkCaptureMidiButton():
    def __init__(self) -> None:
        # TODO: Figure out what this does
        # super().__init__(
        #     ForwardedPattern(2, BasicPattern(0xBF, 0x4A, ...)),
        #     ForwardedStrategy(ButtonData2Strategy()),
        #     'undo'
        # )
        pass
