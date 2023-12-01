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
from common.plug_indexes import FlIndex
from control_surfaces import ControlEvent
from devices import DeviceShadow


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

    def isEnabled(self) -> bool:
        """
        Return whether the integration should be active

        By default, this returns `True`, but if the integration has nothing to
        do, returning `False` can save some processing time

        ### Returns:
        * `bool`: whether the integration should be enabled
        """
        return True
