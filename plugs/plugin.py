"""
plugins > plugin

Contains the definition of the Plugin base class, and its two main types
StandardPlugin and SpecialPlugin.
"""

from common.util.apifixes import PluginIndex
from controlsurfaces import ControlMapping
from devices import DeviceShadow
from plugs.mappingstrategies import IMappingStrategy
from abc import abstractmethod
from typing import final

class Plugin:
    
    def __init__(self, shadow: DeviceShadow, mapping_strategies: list[IMappingStrategy]) -> None:
        """
        Create a plugin object which interacts with a device shadow

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to interact with
        * `mapping_strategies` (`list[IMappingStrategy]`): list of strategies to
          quickly bind reusable mappings to plugins. This should be implemented
          by inheriting classes
        """
        # Bind the mapping strategies
        for strat in mapping_strategies:
            strat.apply(shadow)
        self._shadow = shadow
    
    @abstractmethod
    @staticmethod
    def create(shadow: DeviceShadow) -> 'Plugin':
        """
        Create and return an instance of this plugin
        
        NOTE: On release of Python 3.11, upgrade to `Self` type and remove
        redefinitions in abstract subclasses
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")
    
    @final
    def processEvent(self, mapping: ControlMapping, index: PluginIndex) -> bool:
        return self._shadow.processEvent(mapping, index)

class StandardPlugin(Plugin):
    """
    Standard plugins, representing VST or FL generators and effects
    """
    
    
    @abstractmethod
    @staticmethod
    def getPlugId() -> str:
        """
        Returns the name of the plugin this class should be associated with.

        Used to identify and map to the plugin

        ### Returns:
        * `str`: plugin name
        """
        raise NotImplementedError("This method must be implemented by child "
                                  "classes")
    
    @abstractmethod
    @staticmethod
    def create(shadow: DeviceShadow) -> 'StandardPlugin':
        """
        Create and return an instance of this plugin
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")

class SpecialPlugin(Plugin):
    """
    Special plugins, representing FL Studio windows, and the transport controls
    """
    
    @abstractmethod
    @staticmethod
    def shouldBeActive() -> bool:
        """
        Returns whether this plugin should be used to process the event

        The function should check for conditions such as the active window

        ### Returns:
        * `bool`: whether the plugin should process the event
        """
        raise NotImplementedError("This method must be implemented by child "
                                  "classes")
    
    @abstractmethod
    @staticmethod
    def create(shadow: DeviceShadow) -> 'SpecialPlugin':
        """
        Create and return an instance of this plugin
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")
