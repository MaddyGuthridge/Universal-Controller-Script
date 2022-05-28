"""
plugs > mapping_strategies > mod_xy

Mappings for ModX and ModY control
"""

import plugins
from common.util.api_fixes import PluginIndex
from control_surfaces import ModX, ModY
from control_surfaces import ControlShadow, ControlShadowEvent
from devices.device_shadow import DeviceShadow
from plugs.event_filters.index import toPluginIndex
from . import IMappingStrategy


class ModXYStrategy(IMappingStrategy):
    """
    Maps mod-x and mod-y controls to the given parameters
    """
    def __init__(self, x_param: int, y_param: int) -> None:
        """
        Create a mapping for mod-x and mod-y controls, given the param indexes
        for each value

        ### Args:
        * `x_param` (`int`): mod-x param index

        * `y_param` (`int`): mod-y param-index
        """
        self._x = x_param
        self._y = y_param

    def apply(self, shadow: DeviceShadow) -> None:
        shadow.bindMatch(ModX, self.event, self.tick, (self._x,))
        shadow.bindMatch(ModY, self.event, self.tick, (self._y,))

    @toPluginIndex()
    def event(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        param_index: int,
        *args,
    ) -> bool:
        plugins.setParamValue(control.value, param_index, *index)
        return True

    @toPluginIndex()
    def tick(
        self,
        control: ControlShadow,
        index: PluginIndex,
        param_index: int,
        *args,
    ):
        # Update value
        control.value = plugins.getParamValue(param_index, *index)
        # Update annotations
        control.annotation = plugins.getParamName(param_index, *index)
