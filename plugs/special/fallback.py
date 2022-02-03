
from common import ExtensionManager
from common.util.apifixes import UnsafePluginIndex
from controlsurfaces import ControlMapping
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.mappingstrategies import PedalStrategy, WheelStrategy

class Fallback(SpecialPlugin):
    """
    Used to process events as a fallback if there isn't a plugin registered for
    the active FL plugin.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [PedalStrategy(), WheelStrategy()])
    
    @staticmethod
    def shouldBeActive() -> bool:
        return True
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

ExtensionManager.registerSpecialPlugin(Fallback)
