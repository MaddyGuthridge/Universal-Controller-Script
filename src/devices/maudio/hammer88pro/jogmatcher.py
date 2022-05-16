"""
devices > maudio > hammer88pro > shiftmatcher

Contains the definition for the Hammer 88 Pro's custom jog control matcher

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Optional
from common.types import EventData
from controlsurfaces.eventpattern import (
    BasicPattern,
    UnionPattern,
    ForwardedUnionPattern,
    NullPattern
)

from controlsurfaces.valuestrategies import (
    IValueStrategy,
    ForwardedUnionStrategy
)
from controlsurfaces import consts
from controlsurfaces import (
    ControlSurface,
    ControlEvent,
    NullEvent,
    StandardJogWheel,
    MoveJogWheel
)

from devices import IControlMatcher


class JogValueStrategy(IValueStrategy):
    """
    Value strategy for getting data out of the Hammer 88 Pro jog wheel
    """

    def getValueFromEvent(self, event: EventData):
        # Prev
        if event.data2 == 63:
            return consts.ENCODER_PREV
        # Next
        elif event.data2 == 65:
            return consts.ENCODER_NEXT
        # Release
        elif event.data2 == 0:
            return consts.ENCODER_SELECT
        # Press
        else:
            return consts.ENCODER_NULL

    def getChannelFromEvent(self, event: EventData) -> int:
        return -1

    def getValueFromFloat(self, f: float):
        return f

    def getFloatFromValue(self, value) -> float:
        return value


class JogMatcher(IControlMatcher):
    """
    The Hammer 88 Pro's jog control matcher, which allows for jog wheel
    controls to be mapped differently depending on whether the wheel is pressed
    or not.
    """

    def __init__(self) -> None:
        self._null = NullEvent(NullPattern())

        self._value_strat = ForwardedUnionStrategy(JogValueStrategy())

        self._jog_press_pattern = ForwardedUnionPattern(3, BasicPattern(
            0xBF,
            0x71,
            (0x00, 0x7F)
        ))

        self._jog_turn_pattern = ForwardedUnionPattern(3, BasicPattern(
            0xBF,
            0x71,
            (63, 65)
        ))

        self._pattern = UnionPattern(
            self._jog_turn_pattern,
            self._jog_press_pattern
        )

        self._jog_standard = StandardJogWheel(
            self._pattern,
            self._value_strat
        )

        self._jog_move = MoveJogWheel(
            self._pattern,
            self._value_strat
        )

        self._pressed = False
        self._used_since_press = False

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        # If it's not a jog wheel event, ignore it
        if not self._pattern.matchEvent(event):
            return None

        # If it's a press or release
        if self._jog_press_pattern.matchEvent(event):
            if self._value_strat.getValueFromEvent(event) == 0.0:
                self._pressed = True
                return ControlEvent(self._null, 0.0, -1, False)
            else:
                if self._used_since_press:
                    ret: Optional[ControlEvent] = ControlEvent(
                        self._null, 0.0, -1, False)
                else:
                    ret = self._jog_standard.match(event)
                self._pressed = False
                self._used_since_press = False
                return ret
        else:
            self._used_since_press = True
            if self._pressed:
                return self._jog_move.match(event)
            else:
                return self._jog_standard.match(event)

    def getControls(self, group: str = None) -> list[ControlSurface]:
        if group is not None and group != "navigation":
            return []
        else:
            return [self._jog_standard, self._jog_move]

    def getGroups(self) -> set[str]:
        return {"navigation"}

    def tick(self, thorough: bool) -> None:
        return
