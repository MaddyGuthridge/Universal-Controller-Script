"""
plugins > mappingstrategies > pedalstrategy

Strategy for mapping a pedal to the plugin
"""

import plugins

from typing import Any, Optional
from common.util.apifixes import PluginIndex

from controlsurfaces.pedal import *
from controlsurfaces import ControlShadow
from devices import DeviceShadow
from . import IMappingStrategy

CC_START = 4096

class PedalStrategy(IMappingStrategy):
    def __init__(self) -> None:
        pass
    
    def apply(self, shadow: DeviceShadow) -> None:
        for ped in [SustainPedal, SostenutoPedal, SoftPedal]:
            matches = shadow.getControlMatches(ped, 1)
            if len(matches):
                shadow.bindControl(matches[0], self.pedalCallback)
    
    def pedalCallback(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        t_ped = type(control.getControl())
        
         # Filter out non-VSTs
        if 'MIDI CC' not in plugins.getParamName(CC_START, *index):
            raise TypeError("Expected a plugin of VST type - parameters are incorrect")
        
        # Assign parameters
        if t_ped is SustainPedal:
            plugins.setParamValue(control.getCurrentValue(), CC_START + SUSTAIN, *index)
        elif t_ped is SostenutoPedal:
            plugins.setParamValue(control.getCurrentValue(), CC_START + SOSTENUTO, *index)
        elif t_ped is SustainPedal:
            plugins.setParamValue(control.getCurrentValue(), CC_START + SOFT, *index)
        
        return True
