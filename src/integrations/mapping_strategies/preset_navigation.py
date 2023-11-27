"""
integrations > mapping_strategies > preset_navigation

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.plug_indexes import PluginIndex
from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
    ControlShadowEvent,
)
from devices import DeviceShadow
from integrations.event_filters import toPluginIndex, filterButtonLift


class PresetNavigationStrategy:
    """
    Mapping strategy that binds next/previous buttons to change plugins to
    their next/previous preset
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Mapping strategy that binds next/previous buttons to change plugins
        to their next/previous preset

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to bind to
        """
        shadow.bindMatch(DirectionNext, self.eDirectionNext)
        shadow.bindMatch(DirectionPrevious, self.eDirectionPrev)

    @filterButtonLift()
    @toPluginIndex()
    def eDirectionNext(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args,
    ) -> bool:
        index.presetNext()
        return True

    @filterButtonLift()
    @toPluginIndex()
    def eDirectionPrev(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args,
    ) -> bool:
        index.presetPrevious()
        return True
