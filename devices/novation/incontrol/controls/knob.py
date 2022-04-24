"""
devices > novation > incontrol > controls > knob

Definitions for knob controls shared between Launchkey devices
"""

from typing import Optional
from common.eventpattern import BasicPattern, ForwardedPattern
from common.types import EventData
from controlsurfaces import ControlEvent, ControlSurface
from controlsurfaces import Knob
from controlsurfaces.valuestrategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from devices.matchers import (
    IControlMatcher,
    IndexedMatcher
)

__all__ = [
    'LkKnob',
    'LkKnobSet',
]

# Fader start
K_START = 0x15


class LkKnob(Knob):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, K_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkKnobSet(IControlMatcher):
    def __init__(self) -> None:
        self.__matcher = IndexedMatcher(0xBF, K_START, [
            LkKnob(i) for i in range(8)
        ])

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        return self.__matcher.matchEvent(event)

    def getGroups(self) -> set[str]:
        return self.__matcher.getGroups()

    def getControls(self, group: str = None) -> list[ControlSurface]:
        return self.__matcher.getControls()
