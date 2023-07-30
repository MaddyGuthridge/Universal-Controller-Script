"""
plugins > mapping_strategies > wheel_strategy

Strategy for mapping mod and pitch wheels to the plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
from common.consts import PARAM_CC_START
from common.param import Param
from common.util.api_fixes import PluginIndex, GeneratorIndex

from control_surfaces import ModWheel, PitchWheel
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs.event_filters import toPluginIndex
from . import IMappingStrategy


mod_wheel = Param(PARAM_CC_START + 1)


class WheelStrategy(IMappingStrategy):
    """
    Maps mod and pitch wheels to the current plugin.
    """
    def __init__(self, raise_on_error: bool = False) -> None:
        """
        Create a WheelStrategy for binding mod and pitch wheel events

        ### Args:
        * `raise_on_error` (`bool`, optional): Whether an error should be
          raised if the plugin doesn't support CC parameters. Defaults to
          `False`.
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
        shadow.bindMatches(
            PitchWheel,
            self.pitchCallback,
            raise_on_failure=False
        )

    @toPluginIndex()
    def modCallback(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args: tuple[Any]
    ) -> bool:
        """
        Called when a mod wheel event is detected

        ### Args:
        * `control` (`ControlShadowEvent`): control surface shadow that was
          detected
        * `index` (`PluginIndex`): index of plugin to map to

        ### Raises:
        * `TypeError`: plugin doesn't support MIDI CC events

        ### Returns:
        * `bool`: whether the event was processed
        """
        if not index.isVst():
            if self._raise:
                raise TypeError("Expected a plugin of VST type - make sure "
                                "that this plugin is a VST, and not an FL "
                                "Studio plugin")
            else:
                return False

        # Assign parameter
        mod_wheel(index).value = control.value
        return True

    @toPluginIndex()
    def pitchCallback(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args: tuple[Any]
    ) -> bool:
        """
        Called when a mod wheel event is detected

        ### Args:
        * `control` (`ControlShadowEvent`): control surface shadow that was
          detected
        * `index` (`PluginIndex`): index of plugin to map to

        ### Returns:
        * `bool`: whether the event was processed
        """
        # Only apply to generator plugins
        if isinstance(index, GeneratorIndex):
            index.pitch = control.value * 2 - 1
        return True
