"""
plugs > mapping_strategies > cc_forward_strategy

Mapping strategy to forward MIDI events to VST plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import plugins
from common.consts import PARAM_CC_START
from . import IMappingStrategy
from devices import DeviceShadow
from plugs.event_filters import filterButtonLift
from common.types import Color
from common.util.api_fixes import isPluginVst

from control_surfaces import (
    ControlShadowEvent,
    GenericFader,
    GenericKnob,
    Encoder,
)

BOUND_COLOR = Color.fromInteger(0x888888)


class CcForwardStrategy(IMappingStrategy):
    """
    Forwards CC MIDI events to VST plugins, to add support for MIDI learning.
    """
    def __init__(self) -> None:
        super().__init__()

    def apply(self, shadow: DeviceShadow) -> None:
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
    def process(self, control: ControlShadowEvent, index, *args, **kwargs):
        if isPluginVst(index):
            plugins.setParamValue(
                control.value,
                PARAM_CC_START + control.midi.data1,
                *index,
            )
        return False
