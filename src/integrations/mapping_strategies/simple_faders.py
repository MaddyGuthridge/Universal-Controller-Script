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
from common.profiler import profilerDecoration, ProfilerContext
from control_surfaces import ControlShadowEvent, ControlShadow, Fader
from devices.device_shadow import DeviceShadow
from integrations.event_filters import toPluginIndex
from common.plug_indexes import PluginIndex
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
        self._parameters = list(map(Param, parameters))
        self._colors = colors
        self.__ticker = 0

    def apply(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            Fader,
            on_event=self.eFaders,
            on_tick=self.tFaders,
            target_num=len(self._parameters),
            args_generator=self._parameters,
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
        # FIXME: Test to see if it is safe to remove this hack
        with ProfilerContext("value"):
            # HACK: Workaround for performance issues with getParamValue()
            self.__ticker += 1
            self.__ticker %= 10
            if self.__ticker == 0:
                control.value = param(index).value
        # Update annotations
        with ProfilerContext("annotation"):
            control.annotation = param(index).name
