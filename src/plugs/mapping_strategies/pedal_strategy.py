"""
plugins > mapping_strategies > pedal_strategy

Strategy for mapping a pedal to the plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
from common.consts import PARAM_CC_START
from common.param import Param
from common.plug_indexes import PluginIndex
from control_surfaces.controls.pedal import (
    Pedal,
    SustainPedal,
    SostenutoPedal,
    SoftPedal,
    SUSTAIN,
    SOSTENUTO,
    SOFT,
)
from control_surfaces import ControlShadowEvent, ControlShadowList
from devices import DeviceShadow
from plugs.event_filters import toPluginIndex
from . import IMappingStrategy


sustain = Param(PARAM_CC_START + SUSTAIN)
sostenuto = Param(PARAM_CC_START + SOSTENUTO)
soft = Param(PARAM_CC_START + SOFT)


class PedalStrategy(IMappingStrategy):
    """
    Binds pedals to relevant CC parameters.
    """
    def __init__(self, raise_on_error: bool = True) -> None:
        """
        Create a PedalStrategy for binding pedals to CC parameters

        ### Args:
        * `raise_on_error` (`bool`, optional): Whether an error should be
          raised
          if the plugin doesn't support CC parameters. Defaults to `True`.
        """
        self._raise = raise_on_error

    def apply(self, shadow: DeviceShadow) -> None:
        """
        Bind pedal events to the pedalCallback function

        ### Args:
        * `shadow` (`DeviceShadow`): device to bind to
        """
        # Generator function for mapping out pedal events

        # TODO: Use argument generators as strategies to the strategies?
        # Could save even more repeated code
        def gen(shadows: ControlShadowList):
            for s in shadows:
                yield (type(s.getControl()), )

        # Bind every pedal event to the pedalCallback() method, using the
        # generator to make the type of pedal be used as an argument to the
        # callback
        shadow.bindMatches(
            Pedal,
            self.pedalCallback,
            args_generator=gen,
            raise_on_failure=False,
            one_type=False,
        )

    @toPluginIndex()
    def pedalCallback(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        t_ped: type[Pedal],
        *args: tuple[Any]
    ) -> bool:
        """
        Called when a pedal event is detected

        ### Args:
        * `control` (`ControlShadowEvent`): control surface shadow that was
          detected
        * `index` (`PluginIndex`): index of plugin to map to
        * `t_ped` (`type[Pedal]`): type of pedal that was called

        ### Raises:
        * `TypeError`: plugin doesn't support MIDI CC events

        ### Returns:
        * `bool`: whether the event was processed
        """

        # Filter out non-VSTs
        if not index.isVst():
            if self._raise:
                raise TypeError("Expected a plugin of VST type - make sure "
                                "that this plugin is a VST, and not an FL "
                                "Studio plugin")
            else:
                return False

        # Assign parameters
        if t_ped is SustainPedal:
            sustain(index).value = control.value
        elif t_ped is SostenutoPedal:
            sostenuto(index).value = control.value
        elif t_ped is SoftPedal:
            soft(index).value = control.value
        else:
            raise NotImplementedError("Pedal type not recognized")

        return True
