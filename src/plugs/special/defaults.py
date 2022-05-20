"""
plugs > special > default

Contains the definition for the default mappings plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from typing import Any
import ui
from common.extension_manager import ExtensionManager
from control_surfaces import consts
from control_surfaces import ControlShadowEvent
from control_surfaces import (
    MoveJogWheel,
    ShiftedJogWheel,
    StandardJogWheel,
    JogWheel,
)
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.mapping_strategies import (
    PedalStrategy,
    WheelStrategy,
    NoteStrategy,
    DirectionStrategy,
)


class Defaults(SpecialPlugin):
    """
    Used to provide logical default mappings for plugins, so that devlopers
    of plugin mappings don't need to make so many manual assignments.

    Handles:
    * Pedals
    * Mod and pitch wheels
    * Notes
    * Jog wheels
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.bindMatches(
            JogWheel,
            self.jogWheel,
            one_type=False,
        )
        super().__init__(shadow, [
            PedalStrategy(),
            WheelStrategy(),
            NoteStrategy(),
            DirectionStrategy(),
        ])

    @staticmethod
    def shouldBeActive() -> bool:
        return True

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    def jogWheel(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        if control.value == consts.ENCODER_NEXT:
            increment = 1
        elif control.value == consts.ENCODER_PREV:
            increment = -1
        elif control.value == consts.ENCODER_SELECT:
            ui.enter()
            return True
        else:
            return True

        if isinstance(control.getControl(), StandardJogWheel):
            ui.jog(increment)
        elif isinstance(control.getControl(), ShiftedJogWheel):
            ui.jog(increment)
        elif isinstance(control.getControl(), MoveJogWheel):
            ui.moveJog(increment)
        return True


ExtensionManager.special.register(Defaults)
