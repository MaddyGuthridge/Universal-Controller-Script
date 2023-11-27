"""
integrations > mapping_strategies > wheel_strategy

Strategy for mapping mod and pitch wheels to the integration

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
from consts import PARAM_CC_START
from common.param import Param
from common.plug_indexes import PluginIndex, GeneratorIndex

from control_surfaces import ModWheel, PitchWheel
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow
from integrations.event_filters import toPluginIndex


mod_wheel = Param(PARAM_CC_START + 1)


class WheelStrategy:
    """
    Maps mod and pitch wheels to the current plugin.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Create a WheelStrategy for binding mod and pitch wheel events

        ### Args:
        * `shadow` (`DeviceShadow`): device to bind to
        """

        # Bind mod wheel events to modCallback()
        shadow.bindMatches(
            ModWheel,
            self.modCallback,
        )
        # And pitch events to pitchCallback()
        shadow.bindMatches(
            PitchWheel,
            self.pitchCallback,
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
            # FIXME: Log that plugin wasn't a VST so binding mod wheel doesn't
            # work
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
