"""
plugins > plugin

Contains the definition of the Plugin base class
"""

from common.util.apifixes import PluginIndex
from controlsurfaces import ControlMapping
from devices import DeviceShadow
from plugs.mappingstrategies import IMappingStrategy

class Plugin:
    
    def __init__(self, shadow: DeviceShadow, mapping_strategies: list[IMappingStrategy]) -> None:
        """
        Create a plugin object which interacts with a device shadow

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to interact with
        * `mapping_strategies` (`list[IMappingStrategy]`): list of strategies to
          quickly bind reusable mappings to plugins
        """
        # Bind the mapping strategies
        for strat in mapping_strategies:
            strat.apply(shadow)
        self._shadow = shadow
        
    def processEvent(self, mapping: ControlMapping, index: PluginIndex) -> bool:
        return self._shadow.processEvent(mapping, index)
