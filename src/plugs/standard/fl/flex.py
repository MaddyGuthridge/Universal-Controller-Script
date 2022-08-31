"""
plugs > standard > fl > flex

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import SimpleFaders

FADER_START = 10
NUM_FADERS = 8

FLEX_COLOR = Color.fromRgb(255, 140, 0)


class Flex(StandardPlugin):
    """
    Used to interact with the Flex plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        # TODO: Grey out faders when they're not used
        faders = SimpleFaders(
            [FADER_START + i for i in range(NUM_FADERS)],
            colors=FLEX_COLOR,
        )
        super().__init__(shadow, [
            faders,
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("FLEX",)


ExtensionManager.plugins.register(Flex)
