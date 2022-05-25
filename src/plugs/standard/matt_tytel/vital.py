"""
plugs > standard > matt_tytel > vital
"""

from common.extension_manager import ExtensionManager
from common.types import Color
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import (
    SimpleFaders,
    PedalStrategy,
    WheelStrategy,
    NoteStrategy,
)

MACRO_START = 211
VITAL_COLOR = Color.fromInteger(0xAA88FF)


class Vital(StandardPlugin):
    """
    Used to interact with Matt Tytel's Vital plugin, mapping macros to faders
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        faders = SimpleFaders([MACRO_START + i for i in range(4)], VITAL_COLOR)
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
        return ("Vital",)


ExtensionManager.plugins.register(Vital)
