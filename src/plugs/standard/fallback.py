"""
plugs > standard > fallback

Contains the definition for the fallback plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import (
    PedalStrategy,
    WheelStrategy,
    NoteStrategy,
    PresetNavigationStrategy,
)


class Defaults(StandardPlugin):
    """
    Used to provide logical default mappings for plugins where a definition
    hasn't been created.

    Handles:
    * Pedals
    * Mod and pitch wheels
    * Notes
    * Direction buttons (for preset navigation)
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setDebug(True)
        super().__init__(shadow, [
            PedalStrategy(),
            WheelStrategy(),
            NoteStrategy(),
            PresetNavigationStrategy(),
        ])

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return tuple()

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)


ExtensionManager.plugins.registerFallback(Defaults)
