"""
plugs > special > final_transport

Fallback mappings for transport controls that can be overridden by other
plugins.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.mapping_strategies import (
    DirectionStrategy,
    JogStrategy,
    NoteStrategy,
    WheelStrategy,
    PedalStrategy,
)


class FallbackTransport(SpecialPlugin):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        super().__init__(shadow, [
            DirectionStrategy(),
            JogStrategy(),
            NoteStrategy(),
            WheelStrategy(),
            PedalStrategy(raise_on_error=False),
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True


ExtensionManager.special.register(FallbackTransport)
