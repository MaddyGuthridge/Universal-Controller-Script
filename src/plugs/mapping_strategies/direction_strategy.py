"""
plugs > mapping_strategies > direction_strategy

Mapping strategy to handle direction buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import ui

from common.context_manager import getContext
from . import IMappingStrategy
from devices import DeviceShadow
from plugs.event_filters import filterButtonLift
from common.types import Color

from control_surfaces import (
    IControlShadow,
    ControlShadow,
    DirectionNext,
    DirectionPrevious,
    DirectionLeft,
    DirectionRight,
    DirectionUp,
    DirectionDown,
    DirectionSelect,
)

BOUND_COLOR = Color.fromInteger(0x888888)


class DirectionStrategy(IMappingStrategy):
    """
    Mapping strategy to handle direction buttons.

    This maps controls to next or previous commands.
    """
    def __init__(self) -> None:
        self._controls: list[IControlShadow] = []

    def apply(self, shadow: DeviceShadow):
        # TODO: Find nicer way to bind colors like this
        shadow.bindMatch(
            DirectionNext,
            self.eNext,
            self.tNext,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionPrevious,
            self.ePrev,
            self.tPrev,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionRight,
            self.eNext,
            self.tNext,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionLeft,
            self.ePrev,
            self.tPrev,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionDown,
            self.eNext,
            self.tNext,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionUp,
            self.ePrev,
            self.tPrev,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionSelect,
            self.eSelect,
        ).colorize(BOUND_COLOR)

    @filterButtonLift()
    def eNext(self, control, index, *args, **kwargs):
        ui.next()
        return True

    def tNext(self, control: ControlShadow, *args):
        if (
            control.press_length
            > getContext().settings.get("controls.long_press_time")
        ):
            if not (
                getContext().getTickNumber()
                % getContext().settings.get("controls.navigation_speed")
            ):
                ui.next()

    @filterButtonLift()
    def ePrev(self, control, index, *args, **kwargs):
        ui.previous()
        return True

    def tPrev(self, control: ControlShadow, *args):
        if (
            control.press_length
            > getContext().settings.get("controls.long_press_time")
        ):
            if not (
                getContext().getTickNumber()
                % getContext().settings.get("controls.navigation_speed")
            ):
                ui.previous()

    @filterButtonLift()
    def eSelect(self, control, index, *args, **kwargs):
        # BUG: Will just echo enter - improve this
        ui.enter()
        return True
