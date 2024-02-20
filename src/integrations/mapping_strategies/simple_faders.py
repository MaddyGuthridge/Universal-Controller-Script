"""
integrations > mapping_strategies > simple_faders

Mapping strategy to bind faders to plugin parameters

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.param import Param, PluginParameter
from common.types import Color
from common.profiler import profilerDecoration
from control_surfaces import ControlShadowEvent, ControlShadow, Fader
from devices.device_shadow import DeviceShadow
from integrations.event_filters import toPluginIndex
from common.plug_indexes import PluginIndex

DEFAULT_COLOR = Color.fromInteger(0x222222)


class SimpleFaders:
    """
    Binds faders (or a substitute) to plugin parameters

    It also supports advanced features such as automatically updating
    plugin parameter values and names.
    """
    def __init__(
        self,
        shadow: DeviceShadow,
        parameters: list[int],
        colors: 'list[Color] | Color' = DEFAULT_COLOR,
    ) -> None:
        """
        Binds faders (or a substitute control) to the given plugin parameters

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to bind to

        * `parameters` (`list[int]`): list of parameter numbers to bind

        * `colors` (`list[Color] | Color`, optional): list of colors or a color
          to assign to each control. Defaults to `DEFAULT_COLOR`.
        """
        param_objects = list(map(Param, parameters))
        self._colors = colors
        self.__ticker = 0

        shadow.bindMatches(
            Fader,
            on_event=self.eFaders,
            on_tick=self.tFaders,
            target_num=len(param_objects),
            args_generator=param_objects,
        ).colorize(self._colors)

    @toPluginIndex()
    def eFaders(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        param: type[PluginParameter],
        *args,
    ) -> bool:
        """Fader event"""
        param(index).value = control.value
        return True

    @toPluginIndex()
    @profilerDecoration("simple-faders")
    def tFaders(
        self,
        control: ControlShadow,
        index: PluginIndex,
        param: type[PluginParameter],
        *args,
    ):
        """Fader tick"""
        # Update value
        # TODO: This used to be a huge performance bottleneck, check if it is
        # still an issue
        control.value = param(index).value
        # Update annotations
        control.annotation = param(index).name
