"""
devices > novation > sl > mk3 > fader

Definitions for fader controls used by the SL Mk3 device
"""

from controlsurfaces.eventpatterns import BasicPattern, ForwardedPattern
from controlsurfaces import (
    Fader,
)
from controlsurfaces.valuestrategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from devices.matchers import (
    BasicControlMatcher,
    IndexedMatcher
)
from .slcolorsurface import SlColorSurface

__all__ = [
    'SlFader',
    'SlFaderSet',
]

# Fader start
F_START = 0x29
F_COLOR_START = 0x36
# Fader button start
FB_START = 0x33


class SlFader(SlColorSurface, Fader):
    def __init__(self, index: int) -> None:
        Fader.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, F_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )
        SlColorSurface.__init__(
            self,
            F_COLOR_START + index,
        )


class SlFaderSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, F_START, [
            SlFader(i) for i in range(8)
        ], 2))
