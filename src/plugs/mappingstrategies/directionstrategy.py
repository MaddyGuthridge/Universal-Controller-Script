import ui
from . import IMappingStrategy
from devices import DeviceShadow
from plugs.eventfilters import filterButtonLift
from common.types import Color

from controlsurfaces import (
    IControlShadow,
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
    def __init__(self) -> None:
        self._controls: list[IControlShadow] = []

    def apply(self, shadow: DeviceShadow):
        # TODO: Find nicer way to bind colors like this
        shadow.bindMatch(
            DirectionNext,
            self.next,
            raise_on_failure=False,
        ).color = BOUND_COLOR

        shadow.bindMatch(
            DirectionPrevious,
            self.previous,
            raise_on_failure=False,
        ).color = BOUND_COLOR

        shadow.bindMatch(
            DirectionRight,
            self.next,
            raise_on_failure=False,
        ).color = BOUND_COLOR

        shadow.bindMatch(
            DirectionLeft,
            self.previous,
            raise_on_failure=False,
        ).color = BOUND_COLOR

        shadow.bindMatch(
            DirectionDown,
            self.next,
            raise_on_failure=False,
        ).color = BOUND_COLOR

        shadow.bindMatch(
            DirectionUp,
            self.previous,
            raise_on_failure=False,
        ).color = BOUND_COLOR

        shadow.bindMatch(
            DirectionSelect,
            self.select,
            raise_on_failure=False,
        ).color = BOUND_COLOR

    @filterButtonLift
    def next(self, control, index, *args, **kwargs):
        ui.next()
        return True

    @filterButtonLift
    def previous(self, control, index, *args, **kwargs):
        ui.previous()
        return True

    @filterButtonLift
    def select(self, control, index, *args, **kwargs):
        # BUG: Will just echo enter - improve this
        ui.enter()
        return True
