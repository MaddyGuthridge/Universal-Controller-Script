"""
plugs > mappingstrategies > simplefaders

Mapping strategy to bind faders to plugin parameters
"""

import plugins
from common.types import Color
from control_surfaces import ControlShadowEvent, ControlShadow, Fader
from devices.device_shadow import DeviceShadow
from plugs.event_filters import toPluginIndex
from common.util.api_fixes import PluginIndex
from . import IMappingStrategy

DEFAULT_COLOR = Color.fromInteger(0x222222)


class SimpleFaders(IMappingStrategy):
    """
    Binds faders (or a substitute) to plugin parameters

    It also supports advanced features such as automatically updating
    plugin parameter values and names.
    """
    def __init__(
        self,
        parameters: list[int],
        colors: 'list[Color] | Color' = DEFAULT_COLOR,
    ) -> None:
        """
        Binds faders (or a substitute control) to the given plugin parameters

        ### Args:
        * `parameters` (`list[int]`): list of parameter numbers to bind

        * `colors` (`list[Color] | Color`, optional): list of colors or a color
          to assign to each control. Defaults to `DEFAULT_COLOR`.
        """
        self._parameters = parameters
        self._colors = colors

    def apply(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            Fader,
            on_event=self.eFaders,
            on_tick=self.tFaders,
            target_num=len(self._parameters),
            args_generator=self._parameters,
        ).colorize(self._colors)

    @toPluginIndex
    def eFaders(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        param_index: int,
        *args,
    ) -> bool:
        """Fader event"""
        plugins.setParamValue(control.value, param_index, *index)
        return True

    @toPluginIndex
    def tFaders(
        self,
        control: ControlShadow,
        index: PluginIndex,
        param_index: int,
        *args,
    ):
        """Fader tick"""
        # Update value
        control.value = plugins.getParamValue(param_index, *index)
        # Update annotations
        control.annotation = plugins.getParamName(param_index, *index)
