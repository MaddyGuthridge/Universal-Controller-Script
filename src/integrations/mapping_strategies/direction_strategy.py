"""
integrations > mapping_strategies > direction_strategy

Mapping strategy to handle direction buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import ui
from devices import DeviceShadow
from integrations.event_filters import filterButtonLift
from common.types import Color

from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
    DirectionLeft,
    DirectionRight,
    DirectionUp,
    DirectionDown,
    DirectionSelect,
)

BOUND_COLOR = Color.fromInteger(0x888888)


class DirectionStrategy:
    """
    Mapping strategy to handle direction buttons.

    This maps controls to next or previous commands.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Mapping strategy to handle button presses

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to bind on
        """
        shadow.bindMatch(
            DirectionNext,
            self.next,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionPrevious,
            self.previous,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionRight,
            self.next,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionLeft,
            self.previous,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionDown,
            self.next,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionUp,
            self.previous,
        ).colorize(BOUND_COLOR)

        shadow.bindMatch(
            DirectionSelect,
            self.select,
        ).colorize(BOUND_COLOR)

    @filterButtonLift()
    def next(self, control, index, *args, **kwargs):
        ui.next()
        return True

    @filterButtonLift()
    def previous(self, control, index, *args, **kwargs):
        ui.previous()
        return True

    @filterButtonLift()
    def select(self, control, index, *args, **kwargs):
        # BUG: Will just echo enter - improve this
        ui.enter()
        return True
