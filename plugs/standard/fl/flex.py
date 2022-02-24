
import plugins
from typing import Any
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces import Fader
from controlsurfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import eventfilters, tickfilters

FADER_START = 10

class Flex(StandardPlugin):
    """
    Used to interact with the Flex plugin
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            Fader,
            self.faders,
            target_num=8,
            allow_substitution=True,
            raise_on_failure=False
        )
        super().__init__(shadow, [])
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @tickfilters.filterToGeneratorIndex
    def tick(self, index: GeneratorIndex):
        pass
    
    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("FLEX",)
    
    @eventfilters.filterToGeneratorIndex
    def faders(self, control: ControlShadowEvent, index: GeneratorIndex, *args: Any) -> bool:
        plugins.setParamValue(control.value, FADER_START + control.getShadow().coordinate[1], *index)
        
        return True

ExtensionManager.registerPlugin(Flex)
