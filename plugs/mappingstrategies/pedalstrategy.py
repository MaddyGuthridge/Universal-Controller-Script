"""
plugins > mappingstrategies > pedalstrategy

Strategy for mapping a pedal to the plugin
"""

import plugins

from typing import Any
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
        """
        Bind pedal events to the pedalCallback function

        ### Args:
        * `shadow` (`DeviceShadow`): device to bind to
        """
        # Generator function for mapping out pedal events
        
        # TODO: Use argument generators as strategies to the strategies?
        # Could save even more repeated code
        def argument_generator(shadows: list[ControlShadow]):
            for s in shadows:
                yield (type(s.getControl()), )
        
        # Bind every pedal event to the pedalCallback() method, using the
        # generator to make the type of pedal be used as an argument to the
        # callback
        shadow.bindMatches(
            Pedal,
            self.pedalCallback,
            argument_generator,
            raise_on_failure=False
        )
    
    def pedalCallback(
        self,
        control: ControlShadow,
        index: PluginIndex,
        t_ped: type[Pedal],
        *args: tuple[Any]
    ) -> bool:
        """
        Called when a pedal event is detected

        ### Args:
        * `control` (`ControlShadow`): control surface shadow that was detected
        * `index` (`PluginIndex`): index of plugin to map to
        * `t_ped` (`type[Pedal]`): type of pedal that was called

        ### Raises:
        * `TypeError`: plugin doesn't support MIDI CC events

        ### Returns:
        * `bool`: whether the event was processed
        """
        
         # Filter out non-VSTs
        if 'MIDI CC' not in plugins.getParamName(CC_START, *index):
            raise TypeError("Expected a plugin of VST type - make sure that "
                            "this plugin is a VST, and not an FL Studio plugin")
        
        # Assign parameters
        if t_ped is SustainPedal:
            plugins.setParamValue(control.getCurrentValue(), CC_START + SUSTAIN, *index)
        elif t_ped is SostenutoPedal:
            plugins.setParamValue(control.getCurrentValue(), CC_START + SOSTENUTO, *index)
        elif t_ped is SustainPedal:
            plugins.setParamValue(control.getCurrentValue(), CC_START + SOFT, *index)
        else:
            raise NotImplementedError("Pedal type not recognised")
        
        return True