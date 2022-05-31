"""
plugs > standard > fl > harmless

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

PARAMS = [
    31,  # Pluck
    65,  # Unison
    79,  # Harmonizer
    71,  # Phaser
    91,  # Chorus
    94,  # Delay feedback
    97,  # Reverb
    98,  # Compression
]

COLOR = Color.fromInteger(0x47353f)


class Harmless(StandardPlugin):
    """
    Used to interact with the Harmless plugin
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
        return ("Harmless",)


ExtensionManager.plugins.register(Harmless)
