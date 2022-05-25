"""
plugs > special > fallback_transport

Fallback mappings for transport controls that can be overridden by other
plugins.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.mapping_strategies import DirectionStrategy, JogStrategy


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
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @staticmethod
    def shouldBeActive() -> bool:
        return True


ExtensionManager.final.register(FallbackTransport)
