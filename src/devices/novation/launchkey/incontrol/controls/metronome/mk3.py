
from control_surfaces import MetronomeButton
from control_surfaces.event_patterns import ForwardedPattern, BasicPattern
from control_surfaces.value_strategies import (
    ForwardedStrategy,
    ButtonData2Strategy,
)


class LkMk3MetronomeButton(MetronomeButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, 0x4C, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        )
