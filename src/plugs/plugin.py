"""
plugins > plugin

Contains the definition of the Plugin base class, and its two main types
StandardPlugin and SpecialPlugin.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import final
from common import log, verbosity
from common.util.abstract_method_error import AbstractMethodError
from common.plug_indexes import UnsafeIndex, WindowIndex
from control_surfaces import ControlEvent
from devices import DeviceShadow
from plugs.mapping_strategies import IMappingStrategy
from abc import abstractmethod


class Plugin:
    """
    Represents a plugin, which is used to describe how the script should
    interact with an FL Studio window, or a VST or FL plugin.

    Plugins can be of three types:

    * `StandardPlugin`: used for VST and FL plugins

    * `WindowPlugin`: used for FL Studio windows (mixer, etc)

    * `SpecialPlugin`: used when the plugin should decide for itself whether to
      be active or not. Used for global controls, such as transport buttons.

    Plugin definitions can be created by extending one of these plugin types.
    The base plugin type shouldn't be extended.

    For more info, refer to docs/contributing/plugins/README.md
    """
    def __init__(
        self,
        shadow: DeviceShadow,
        mapping_strategies: list[IMappingStrategy]
    ) -> None:
        """
        Create a base plugin object

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

        Ordinarily, you shouldn't need to override this behavior.
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
        to override this behavior.

        ### Args:
        * `mapping` (`ControlEvent`): event to process
        * `index` (`UnsafeIndex`): index to be used by plugin

        ### Returns:
        * `bool`: whether the event should be handled
        """
        log("plugins",
            f"Processing event at {type(self)}", verbosity=verbosity.EVENT)
        return self._shadow.processEvent(mapping, index)

    @final
    def doTick(self, index: UnsafeIndex) -> None:
        """
        Tick the plugin, to allow parameters to update if required.

        This the internal tick function, which calls the standard tick()
        function.

        ### Args:
        * `index` (`UnsafeIndex`): index of active plugin or window
        """
        # Tick the overall plugin
        self.tick(index)
        # Then tick the device shadow
        self._shadow.tick(index)

    def tick(self, index: UnsafeIndex) -> None:
        """
        Tick the plugin, to allow parameters to update if required.

        If any actions need to be taken during this time, the plugin should
        override this function

        ### Args:
        * `index` (`UnsafeIndex`): index of active plugin or window
        """


class StandardPlugin(Plugin):
    """
    Standard plugins, representing VST or FL generators and effects

    Methods to implement:
    * `@classmethod getPlugIds(cls) -> tuple[str, ...]` return a tuple of all
      the plugin names that this plugin can handle.

    * `@classmethod create(cls, shadow: DeviceShadow) -> Self` create an
      instance of this plugin. This is used so that we can ensure type safety
      of the constructor when plugins are instantiated.
    """

    @classmethod
    @abstractmethod
    def getPlugIds(cls) -> tuple[str, ...]:
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

        This method should be implemented by every plugin definition
        """
        raise AbstractMethodError(cls)


class WindowPlugin(Plugin):
    """
    Window plugins, representing FL Studio windows.

    * Mixer

    * Channel rack

    * Playlist

    * Piano roll

    * Browser

    Methods to implement:
    * `@classmethod getWindowId(cls) -> WindowIndex` return a the window index
      that this plugin should be active for.

    * `@classmethod create(cls, shadow: DeviceShadow) -> Self` create an
      instance of this plugin. This is used so that we can ensure type safety
      of the constructor when plugins are instantiated.
    """

    @classmethod
    @abstractmethod
    def getWindowId(cls) -> WindowIndex:
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

        This method should be implemented by every plugin definition
        """
        raise AbstractMethodError(cls)


class SpecialPlugin(Plugin):
    """
    Special plugins, representing plugins that are active independently of a
    VST or FL plugin or window.

    Methods to implement:
    * `@classmethod shouldBeActive(cls) -> bool` return whether the plugin
      should currently be active.

    * `@classmethod create(cls, shadow: DeviceShadow) -> Self` create an
      instance of this plugin. This is used so that we can ensure type safety
      of the constructor when plugins are instantiated.
    """

    @classmethod
    @abstractmethod
    def shouldBeActive(cls) -> bool:
        """
        Returns whether this plugin should be used to process the event

        The function should check for conditions such as the active window

        ### Returns:
        * `bool`: whether the plugin should process the event
        """
        raise AbstractMethodError(cls)

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        """
        Create and return an instance of this plugin

        This method should be implemented by every plugin definition
        """
        raise AbstractMethodError(cls)
