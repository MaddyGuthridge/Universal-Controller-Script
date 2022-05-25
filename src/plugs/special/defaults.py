"""
plugs > special > default

Contains the definition for the default mappings plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from common.extension_manager import ExtensionManager
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


ExtensionManager.special.register(Defaults)
