
import plugins
from typing import Any
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces import Fader
from controlsurfaces.controlshadow import ControlShadow
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.eventfilters import filterToGeneratorIndex

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
    
    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("FLEX",)
    
    @filterToGeneratorIndex
    def faders(self, control: ControlShadow, index: GeneratorIndex, *args: Any) -> bool:
        plugins.setParamValue(control.getCurrentValue(), FADER_START + control.coordinate[1], *index)
        
        return True

ExtensionManager.registerPlugin(Flex)
