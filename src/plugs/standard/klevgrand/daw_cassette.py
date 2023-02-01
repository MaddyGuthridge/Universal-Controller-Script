"""
plugs > standard > klevgrand > daw_cassette

DAW Cassette plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import plugins
from typing import Any
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import EffectIndex
from control_surfaces import ControlShadowEvent, ControlShadow
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import SimpleFaders, DrumPadStrategy
from plugs.event_filters import toEffectIndex as eEffectIndex
from plugs.tick_filters import toEffectIndex as tEffectIndex
from plugs import event_filters, tick_filters


PLUG_COLOR = Color.fromInteger(0xd9d9c4)


VALS = [0.0, 0.1, 0.2]
MAX_VALS = [0.05, 0.15]
PARAMS = [7, 6]


class DawCassette(StandardPlugin):
    """
    DAW Cassette plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        faders = SimpleFaders(
            [
                5,  # TAPE QUALITY
                4,  # HEAD QUALITY
                3,  # MOTOR QUALITY
                0,  # INPUT GAIN
                1,  # OUTPUT GAIN
                2,  # DRY/WET MIX
            ],
            PLUG_COLOR,
        )
        drums = DrumPadStrategy(3, 2, True, self.triggerDrumPads)

        self.__active_pads = [0, 0]

        super().__init__(shadow, [faders, drums])

    @eEffectIndex()
    def triggerDrumPads(
        self,
        event: ControlShadowEvent,
        plug_index: EffectIndex,
        pad: int,
    ) -> bool:
        param = PARAMS[pad // 3]
        val = VALS[pad % 3]
        plugins.setParamValue(val, param, *plug_index)
        return False

    @tEffectIndex()
    def colorDrumPads(
        self,
        control: ControlShadow,
        plug_index: EffectIndex,
        pad: int,
    ) -> Color:
        pad_row = pad // 3
        pad_col = pad % 3
        if pad_col == self.__active_pads[pad_row]:
            return Color.WHITE
        else:
            return PLUG_COLOR

    @tEffectIndex()
    def tick(self, index: EffectIndex) -> None:
        for active_index, param in enumerate(PARAMS):
            val = plugins.getParamValue(param, *index)
            for i, upper in enumerate(MAX_VALS):
                if val < upper:
                    self.__active_pads[active_index] = i
                    break
            else:
                self.__active_pads[active_index] = i + 1

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)
