"""
plugins > plugin

Contains the definition of the Plugin base class, and its two main types
StandardPlugin and SpecialPlugin.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common import log, verbosity
from common.util.abstractmethoderror import AbstractMethodError
from common.util.apifixes import UnsafeIndex, WindowIndex, PluginIndex
from controlsurfaces import ControlEvent
from devices import DeviceShadow
from plugs.mappingstrategies import IMappingStrategy
from abc import abstractmethod


class Plugin:

    def __init__(
        self,
        shadow: DeviceShadow,
        mapping_strategies: list[IMappingStrategy]
    ) -> None:
        """
        Create a plugin object which interacts with a device shadow

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to interact with
        * `mapping_strategies` (`list[IMappingStrategy]`): list of strategies
          to quickly bind reusable mappings to plugins. This should be
          implemented by inheriting classes
        """
        # Bind the mapping strategies
        for strat in mapping_strategies:
            strat.apply(shadow)
        self._shadow = shadow

    def __repr__(self) -> str:
        """
        Get quick representation of plugin

        ### Returns:
        * `str`: simplified representation
        """
        return f"Plugin at {type(self)}"

    def __str__(self) -> str:
        """
        Get string representation of plugin

        ### Returns:
        * `str`: full representation
        """
        return f"Plugin at {type(self)}:\n\n{self._shadow}"

    def apply(self, thorough: bool) -> None:
        """
        Apply the current state of this plugin to the device

        Ordinarily, you shouldn't need to override this behaviour.
        """
        self._shadow.apply(thorough)

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'Plugin':
        """
        Create and return an instance of this plugin

        NOTE: On release of Python 3.11, upgrade to `Self` type and remove
        redefinitions in abstract subclasses
        """
        raise AbstractMethodError(cls)

    def processEvent(self, mapping: ControlEvent, index: UnsafeIndex) -> bool:
        """
        Process the event

        By default this forwards the event to the device shadow to allow
        associated callbacks to be called correctly. Generally, you won't want
        to override this behaviour.

        ### Args:
        * `mapping` (`ControlEvent`): event to process
        * `index` (`UnsafeIndex`): index to be used by plugin

        ### Returns:
        * `bool`: whether the event should be handled
        """
        log("plugins",
            f"Processing event at {type(self)}", verbosity=verbosity.EVENT)
        return self._shadow.processEvent(mapping, index)


class StandardPlugin(Plugin):
    """
    Standard plugins, representing VST or FL generators and effects
    """

    @staticmethod
    @abstractmethod
    def getPlugIds() -> tuple[str, ...]:
        """
        Returns the names of the plugins this class should be associated with.

        Used to identify and map to the plugin

        ### Returns:
        * `tuple[str, ...]`: plugin names
        """
        raise AbstractMethodError()

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        """
        Create and return an instance of this plugin
        """
        raise AbstractMethodError(cls)

    @abstractmethod
    def tick(self, index: PluginIndex) -> None:
        """
        Tick the plugin, to allow parameters to update if required

        ### Args:
        * `index` (`PluginIndex`): index of plugin
        """
        raise AbstractMethodError(self)


class WindowPlugin(Plugin):
    """
    Window plugins, representing FL Studio windows
    """

    @staticmethod
    @abstractmethod
    def getWindowId() -> WindowIndex:
        """
        Returns the ID of the window this class should be associated with.

        Used to identify and map to the plugin

        ### Returns:
        * `int`: window ID
        """
        raise AbstractMethodError()

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        """
        Create and return an instance of this plugin
        """
        raise AbstractMethodError(cls)

    @abstractmethod
    def tick(self) -> None:
        """
        Tick the plugin, to allow parameters to update if required
        """
        raise AbstractMethodError(self)


class SpecialPlugin(Plugin):
    """
    Special plugins, representing other plugins
    """

    @staticmethod
    @abstractmethod
    def shouldBeActive() -> bool:
        """
        Returns whether this plugin should be used to process the event

        The function should check for conditions such as the active window

        ### Returns:
        * `bool`: whether the plugin should process the event
        """
        raise AbstractMethodError()

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        """
        Create and return an instance of this plugin
        """
        raise AbstractMethodError(cls)

    @abstractmethod
    def tick(self) -> None:
        """
        Tick the plugin, to allow parameters to update if required
        """
        raise AbstractMethodError(self)
