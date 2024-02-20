"""
integrations > mapping_strategies > pedal_strategy

Strategy for mapping pedal events to the integration

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
from consts import PARAM_CC_START
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
from integrations.event_filters import toPluginIndex


sustain = Param(PARAM_CC_START + SUSTAIN)
sostenuto = Param(PARAM_CC_START + SOSTENUTO)
soft = Param(PARAM_CC_START + SOFT)


class PedalStrategy:
    """
    Binds pedals to relevant CC parameters.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Bind pedal events to the pedalCallback function

        ### Args:
        * `shadow` (`DeviceShadow`): device to bind to
        """
        # Generator function for mapping out pedal events

        # FIXME: Honestly this design for binding pedals is kinda yucky.
        # Refactor it to remove the need for passing arguments alongside
        # control bindings at some point, since that's always been insanely
        # difficult to make type-safe
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
            # FIXME: Log that plugin wasn't a VST so binding mod wheel doesn't
            # work
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
