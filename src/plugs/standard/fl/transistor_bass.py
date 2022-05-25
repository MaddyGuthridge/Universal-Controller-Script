
from common.types import Color
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import (
    SimpleFaders,
    PedalStrategy,
    WheelStrategy,
    NoteStrategy,
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
            PedalStrategy(),
            WheelStrategy(),
            NoteStrategy(),
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("Transistor Bass",)


ExtensionManager.plugins.register(TransistorBass)
