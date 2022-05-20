"""
devices > novation > incontrol > controls > fader

Definitions for fader controls shared between Launchkey devices
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces import (
    Fader,
    GenericFaderButton,
    MasterGenericFaderButton,
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

__all__ = [
    'LkFader',
    'LkMasterFader',
    'LkFaderButton',
    'LkMasterFaderButton',
    'LkFaderSet',
]

# Fader start
F_START = 0x29
# Fader button start
FB_START = 0x33


class LkFader(Fader):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, F_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMasterFader(MasterFader):
    def __init__(self) -> None:
        super().__init__(
                ForwardedPattern(2, BasicPattern(0xBF, 0x07, ...)),
                ForwardedStrategy(Data2Strategy())
            )


class LkFaderButton(GenericFaderButton):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, FB_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMasterFaderButton(MasterGenericFaderButton):
    def __init__(self) -> None:
        super().__init__(
                    ForwardedPattern(2, BasicPattern(0xBF, 0x3B, ...)),
                    ForwardedStrategy(Data2Strategy()),
                )


class LkFaderSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, F_START, [
            LkFader(i) for i in range(8)
        ], 2))
        self.addSubMatcher(IndexedMatcher(0xBF, FB_START, [
            LkFaderButton(i) for i in range(8)
        ], 2))
        self.addControls([
            LkMasterFader(),
            LkMasterFaderButton(),
        ])
