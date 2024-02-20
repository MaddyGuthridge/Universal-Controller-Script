"""
integrations > mapping_strategies > cc_forward_strategy

Mapping strategy to forward MIDI events to VST plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from consts import PARAM_CC_START
from common.param import Param
from devices import DeviceShadow
from integrations.event_filters import filterButtonLift
from common.types import Color
from common.plug_indexes import FlIndex, PluginIndex

from control_surfaces import (
    ControlShadowEvent,
    GenericFader,
    GenericKnob,
    Encoder,
)

BOUND_COLOR = Color.fromInteger(0x888888)


class CcForwardStrategy:
    """
    Forwards CC MIDI events to VST plugins, to add support for MIDI learning.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Forwards CC MIDI events to VST plugins, adding support for MIDI
        learning within them

        ### Args:
        * `shadow` (`DeviceShadow`): device to bind controls on
        """
        shadow.bindMatches(
            # God I cannot wait for https://github.com/python/mypy/issues/4717
            # to get fixed
            GenericFader,  # type: ignore
            self.process,
            allow_substitution=False,
            one_type=False,
        )
        shadow.bindMatches(
            GenericKnob,  # type: ignore
            self.process,
            allow_substitution=False,
            one_type=False,
        )
        shadow.bindMatches(Encoder, self.process)

    @filterButtonLift()
    def process(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        *args,
        **kwargs,
    ):
        if isinstance(index, PluginIndex) and index.isVst():
            param = Param(PARAM_CC_START + control.midi.data1)
            param(index).value = control.value
            return True
        return False
