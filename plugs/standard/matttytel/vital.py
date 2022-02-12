
from typing import Any

import plugins
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces.controlshadow import ControlShadow
from controlsurfaces import Fader
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.eventfilters import filterToGeneratorIndex

MACRO_START = 211

class Vital(StandardPlugin):
    """
    Used to interact with Matt Tytel's Vital plugin, mapping macros to faders
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            Fader, self.faders, ..., target_num=4, raise_on_failure=False)
        super().__init__(shadow, [])
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)
    
    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("Vital",)

    @filterToGeneratorIndex
    def faders(self, control: ControlShadow, index: GeneratorIndex, idx: int, *args: Any) -> bool:
        plugins.setParamValue(control.getCurrentValue(), MACRO_START + control.coordinate[1], *index)
        return True

ExtensionManager.registerPlugin(Vital)
