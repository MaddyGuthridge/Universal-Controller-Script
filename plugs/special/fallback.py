
from common.extensionmanager import ExtensionManager
from common.util.apifixes import UnsafePluginIndex
from controlsurfaces import ControlMapping
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.mappingstrategies import PedalStrategy, WheelStrategy, NoteStrategy

class Fallback(SpecialPlugin):
    """
    Used to process events as a fallback if there isn't a plugin registered for
    the active FL plugin.
    
    Handles:
    * Pedals
    * Mod and pitch wheels
    * Notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [
            PedalStrategy(raise_on_error=False),
            WheelStrategy(raise_on_error=False),
            NoteStrategy()
        ])
    
    @staticmethod
    def shouldBeActive() -> bool:
        return True
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

ExtensionManager.registerSpecialPlugin(Fallback)
