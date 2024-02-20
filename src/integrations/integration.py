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
from common.plug_indexes import WindowIndex, FlIndex
from control_surfaces import ControlEvent
from devices import DeviceShadow
from abc import abstractmethod


class Integration:
    """
    Represents a script integration, which is used to describe how the script
    should interact with an FL Studio window, or a VST or FL plugin.

    Plugins can be of three types:

    * `PluginIntegration`: used for VST and FL plugins

    * `WindowIntegration`: used for FL Studio windows (mixer, piano roll, etc)

    * `CoreIntegration`: used when the integration should always be active, or
      should at least be active based on a criteria within its own control

    Integration definitions can be created by extending one of these types.
    The base `Integration` type shouldn't be extended.

    For more info, refer to docs/contributing/plugins/README.md
    """
    def __init__(
        self,
        shadow: DeviceShadow,
    ) -> None:
        """
        Create a base integration object

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to interact with
        """
        self._shadow = shadow

    def __repr__(self) -> str:
        """
        Get quick representation of integration

        ### Returns:
        * `str`: simplified representation
        """
        return f"Integration at {type(self)}"

    def __str__(self) -> str:
        """
        Get string representation of integration, giving details of the mapping

        ### Returns:
        * `str`: full representation
        """
        return f"Integration at {type(self)}:\n\n{self._shadow}"

    def apply(self, thorough: bool) -> None:
        """
        Apply this integration's device state to the physical device.

        Ordinarily, the default behavior (applying the integration's device
        shadow) is sufficient, but it is possible to override this method to
        accomplish advanced functionality. For an example, see
        `IntegrationPager.apply`.
        """
        self._shadow.apply(thorough)

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'Integration':
        """
        Create and return an instance of this integration

        NOTE: On release of Python 3.11, upgrade to `Self` type and remove
        redefinitions in abstract subclasses
        """
        raise AbstractMethodError(cls)

    def processEvent(self, mapping: ControlEvent, index: FlIndex) -> bool:
        """
        Process a MIDI event that has been sent to this integration.

        By default this forwards the event to the device shadow to allow
        associated callbacks to be called correctly. Generally, you won't want
        to override this behavior.

        ### Args:
        * `mapping` (`ControlEvent`): event to process
        * `index` (`FlIndex`): index to be used by plugin

        ### Returns:
        * `bool`: whether the event should be handled
        """
        log("plugins",
            f"Processing event at {type(self)}", verbosity=verbosity.EVENT)
        return self._shadow.processEvent(mapping, index)

    @final
    def doTick(self, index: FlIndex) -> None:
        """
        Tick the integration, to allow parameters to update if required.

        This the internal tick function, which calls the standard `tick()`
        function, as well as ticking the integration's device shadow.

        In order to perform general updates in an integration implementation,
        you should override the `tick` method, which this calls.

        ### Args:
        * `index` (`FlIndex`): index of active plugin or window
        """
        # Tick the overall plugin
        self.tick(index)
        # Then tick the device shadow
        self._shadow.tick(index)

    def tick(self, index: FlIndex) -> None:
        """
        Tick the integration, to allow parameters to update if required.

        If any actions need to be taken during this time, subclasses should
        override this method

        ### Args:
        * `index` (`FlIndex`): index of active plugin or window
        """


class PluginIntegration(Integration):
    """
    Plugin integration, used to represent VSTs and FL Studio generators and
    effects.

    ## Methods to implement:

    * `@classmethod getPlugIds(cls) -> tuple[str, ...]` return a tuple of all
      the plugin names that this integration can handle.

    * `@classmethod create(cls, shadow: DeviceShadow) -> Self` create an
      instance of this integration. This is used so that we can ensure type
      safety of the constructor when plugins are instantiated.
    """

    @classmethod
    @abstractmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        """
        Returns the names of the plugins this class should be associated with.

        Used to identify and map this integration to the plugin

        ### Returns:
        * `tuple[str, ...]`: plugin names
        """
        raise AbstractMethodError()

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        """
        Create and return an instance of this integration

        This method should be implemented by every plugin definition
        """
        raise AbstractMethodError(cls)


class WindowIntegration(Integration):
    """
    FL Studio window integrations

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
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        """
        Create and return an instance of this plugin

        This method should be implemented by every plugin definition
        """
        raise AbstractMethodError(cls)


class CoreIntegration(Integration):
    """
    Core integrations, representing integrations that are active independent of
    a VST, FL Studio plugin or window.

    Methods to implement:
    * `@classmethod shouldBeActive(cls) -> bool` return whether the integration
      should currently be active.

    * `@classmethod create(cls, shadow: DeviceShadow) -> Self` create an
      instance of this integration. This is used so that we can ensure type
      safety of the constructor when integrations are instantiated, although
      imo this is a yucky solution, which I'm planning to fix to close #151
    """

    @classmethod
    @abstractmethod
    def shouldBeActive(cls) -> bool:
        """
        Returns whether this integration is currently active, meaning it is
        open to processing events, and will impact the overall device state

        If the integration should be active, this should return `True`.

        ### Returns:
        * `bool`: whether the integration should be active
        """
        raise AbstractMethodError(cls)

    @classmethod
    @abstractmethod
    def create(cls, shadow: DeviceShadow) -> 'CoreIntegration':
        """
        Create and return an instance of this integration

        This method should be implemented by every integration definition
        """
        raise AbstractMethodError(cls)
