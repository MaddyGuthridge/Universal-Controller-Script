"""
integrations > plugin > fl > flex

Integration with FL Studio's "FLEX" plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from common.extension_manager import ExtensionManager
from control_surfaces import Ambient
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations.mapping_strategies import (
    SimpleFaders,
    PresetNavigationStrategy,
)

FADER_START = 10
NUM_FADERS = 8

FLEX_COLOR = Color.fromRgb(255, 100, 50)


class Flex(PluginIntegration):
    """
    Used to interact with the Flex plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        # TODO: Grey out faders when they're not used
        SimpleFaders(
            shadow,
            [FADER_START + i for i in range(NUM_FADERS)],
            colors=FLEX_COLOR,
        )
        PresetNavigationStrategy(shadow)
        shadow.bindMatch(Ambient, None).colorize(FLEX_COLOR)
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("FLEX",)


ExtensionManager.plugins.register(Flex)
