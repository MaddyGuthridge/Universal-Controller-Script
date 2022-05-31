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
)


class Defaults(StandardPlugin):
    """
    Used to provide logical default mappings for plugins where a definition
    hasn't been created.

    Handles:
    * Pedals
    * Mod and pitch wheels
    * Notes
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [
            PedalStrategy(),
            WheelStrategy(),
            NoteStrategy(),
        ])

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return tuple()

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)


ExtensionManager.plugins.registerFallback(Defaults)
