"""
integrations > plugin > default_integration

Contains the definition for the fallback plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations.mapping_strategies import (
    PedalStrategy,
    WheelStrategy,
    NoteStrategy,
    PresetNavigationStrategy,
)


class DefaultIntegration(PluginIntegration):
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
        PedalStrategy(shadow)
        WheelStrategy(shadow)
        NoteStrategy(shadow)
        PresetNavigationStrategy(shadow)
        super().__init__(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return tuple()

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)


ExtensionManager.plugins.registerFallback(DefaultIntegration)
