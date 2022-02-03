"""
plugins > mappingstrategies > wheelstrategy

Strategy for mapping mod and pitch wheels to the plugin
"""

import plugins
import channels

from typing import Any
from common.util.apifixes import PluginIndex

from controlsurfaces import ModWheel, PitchWheel
from controlsurfaces import ControlShadow
from devices import DeviceShadow
from plugs.eventfilters import filterUnsafeIndex
from . import IMappingStrategy

CC_START = 4096

class WheelStrategy(IMappingStrategy):
    def __init__(self, raise_on_error: bool = True) -> None:
        """
        Create a WheelStrategy for binding mod and pitch wheel events

        ### Args:
        * `raise_on_error` (`bool`, optional): Whether an error should be raised
          if the plugin doesn't support CC parameters. Defaults to `True`.
        """
        self._raise = raise_on_error
    
    def apply(self, shadow: DeviceShadow) -> None:
        """
        Bind pedal events to the pedalCallback function

        ### Args:
        * `shadow` (`DeviceShadow`): device to bind to
        """
        
        # Bind mod wheel events to modCallback()
        shadow.bindMatches(
            ModWheel,
            self.modCallback,
            raise_on_failure=False
        )
        # And pitch events to pitchCallback()

    @filterUnsafeIndex
    def modCallback(
        self,
        control: ControlShadow,
        index: PluginIndex,
        *args: tuple[Any]
    ) -> bool:
        """
        Called when a mod wheel event is detected

        ### Args:
        * `control` (`ControlShadow`): control surface shadow that was detected
        * `index` (`PluginIndex`): index of plugin to map to

        ### Raises:
        * `TypeError`: plugin doesn't support MIDI CC events

        ### Returns:
        * `bool`: whether the event was processed
        """
        if index is None:
            return False
        
        # Filter out non-VSTs
        if 'MIDI CC' not in plugins.getParamName(CC_START, *index):
            if self._raise:
                raise TypeError("Expected a plugin of VST type - make sure that "
                                "this plugin is a VST, and not an FL Studio plugin")
            else:
                return False
        
        # Assign parameter
        plugins.setParamValue(control.getCurrentValue(), CC_START + 1, *index)
        
        return True

    @filterUnsafeIndex
    def pitchCallback(
        self,
        control: ControlShadow,
        index: PluginIndex,
        *args: tuple[Any]
    ) -> bool:
        """
        Called when a mod wheel event is detected

        ### Args:
        * `control` (`ControlShadow`): control surface shadow that was detected
        * `index` (`PluginIndex`): index of plugin to map to

        ### Raises:
        * `TypeError`: plugin doesn't support MIDI CC events

        ### Returns:
        * `bool`: whether the event was processed
        """
        
        # Filter out non-VSTs
        if 'MIDI CC' not in plugins.getParamName(CC_START, *index):
            if self._raise:
                raise TypeError("Expected a plugin of VST type - make sure that "
                                "this plugin is a VST, and not an FL Studio plugin")
            else:
                return False
        
        # Set pitch
        if isinstance(index, int):
            channels.setChannelPitch(index, control.getCurrentValue()*2 - 1)
        
        return True
