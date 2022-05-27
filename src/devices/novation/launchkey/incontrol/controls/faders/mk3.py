"""
devices > novation > incontrol > controls > fader

Definitions for fader controls shared between Launchkey devices
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    Fader,
    GenericFaderButton,
    MasterFader,
)
from control_surfaces.value_strategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from devices.matchers import (
    BasicControlMatcher,
    IndexedMatcher
)
from ..incontrol_surface import ColorInControlSurface
from ...colors.mk3 import COLORS

__all__ = [
    'LkMk3Fader',
    'LkMk3MasterFader',
    'LkMk3FaderButton',
    'LkMk3FaderSet',
]

# Fader start
F_START = 0x35
# Fader button start
FB_START = 0x25


class LkMk3Fader(Fader):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, F_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMk3MasterFader(MasterFader):
    def __init__(self) -> None:
        super().__init__(
                ForwardedPattern(2, BasicPattern(0xBF, 0x07, ...)),
                ForwardedStrategy(Data2Strategy())
            )


class LkMk3FaderButton(ColorInControlSurface, GenericFaderButton):
    def __init__(self, index: int) -> None:
        GenericFaderButton.__init__(
            self,
            ForwardedPattern(2, BasicPattern(0xBF, FB_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )
        ColorInControlSurface.__init__(
            self,
            0,
            FB_START + index,
            COLORS,
        )


class LkMk3FaderSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, F_START, [
            LkMk3Fader(i) for i in range(8)
        ], 2))
        self.addSubMatcher(IndexedMatcher(0xBF, FB_START, [
            LkMk3FaderButton(i) for i in range(8)
        ], 2))
        self.addControls([
            LkMk3MasterFader(),
        ])
