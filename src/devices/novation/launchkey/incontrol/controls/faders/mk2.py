"""
devices > novation > launchkey > incontrol > controls > faders > mk2

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
from control_surfaces.matchers import (
    BasicControlMatcher,
    IndexedMatcher
)

__all__ = [
    'LkMk2Fader',
    'LkMk2MasterFader',
    'LkMk2FaderButton',
    'LkMk2MasterFaderButton',
    'LkMk2FaderSet',
]

# Fader start
F_START = 0x29
# Fader button start
FB_START = 0x33


class LkMk2Fader(Fader):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, F_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMk2MasterFader(MasterFader):
    def __init__(self) -> None:
        super().__init__(
                ForwardedPattern(2, BasicPattern(0xBF, 0x07, ...)),
                ForwardedStrategy(Data2Strategy())
            )


class LkMk2FaderButton(GenericFaderButton):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, FB_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMk2MasterFaderButton(MasterGenericFaderButton):
    def __init__(self) -> None:
        super().__init__(
                    ForwardedPattern(2, BasicPattern(0xBF, 0x3B, ...)),
                    ForwardedStrategy(Data2Strategy()),
                )


class LkMk2FaderSet(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addSubMatcher(IndexedMatcher(0xBF, F_START, [
            LkMk2Fader(i) for i in range(8)
        ], 2))
        self.addSubMatcher(IndexedMatcher(0xBF, FB_START, [
            LkMk2FaderButton(i) for i in range(8)
        ], 2))
        self.addControls([
            LkMk2MasterFader(),
            LkMk2MasterFaderButton(),
        ])
