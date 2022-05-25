"""
plugs > special > default

Contains the definition for the default mappings plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import (
    PedalStrategy,
    WheelStrategy,
    NoteStrategy,
    DirectionStrategy,
    JogStrategy
)


class Defaults(StandardPlugin):
    """
    Used to provide logical default mappings for plugins where a definition
    hasn't been created.

    If you create a plugin definition, these behaviors won't be implemented
    by default, so you'll need to include the strategies used here.

    Handles:
    * Pedals
    * Mod and pitch wheels
    * Notes
    * Jog wheels
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [
            PedalStrategy(),
            WheelStrategy(),
            NoteStrategy(),
            DirectionStrategy(),
            JogStrategy(),
        ])

    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return tuple()

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)


ExtensionManager.plugins.register(Defaults)
