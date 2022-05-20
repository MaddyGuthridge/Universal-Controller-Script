"""
plugs > standard > matttytel > vital
"""

from common.extensionmanager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mappingstrategies import SimpleFaders

MACRO_START = 211


class Vital(StandardPlugin):
    """
    Used to interact with Matt Tytel's Vital plugin, mapping macros to faders
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        faders = SimpleFaders([MACRO_START + i for i in range(4)])
        super().__init__(shadow, [faders])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("Vital",)


ExtensionManager.plugins.register(Vital)
