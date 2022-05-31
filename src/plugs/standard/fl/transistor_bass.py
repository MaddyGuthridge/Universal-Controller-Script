"""
plugs > standard > fl > transistor_bass

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import (
    SimpleFaders,
)

PARAMS = [0, 1, 2, 4, 5, 6, 7, 8]

COLOR = Color.fromInteger(0x455765)


class TransistorBass(StandardPlugin):
    """
    Used to interact with the Transistor Bass plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        faders = SimpleFaders(
            PARAMS,
            colors=COLOR,
        )
        super().__init__(shadow, [
            faders,
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("Transistor Bass",)


ExtensionManager.plugins.register(TransistorBass)
