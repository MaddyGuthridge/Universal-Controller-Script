"""
integrations > plugin > klevgrand > daw_cassette

DAW Cassette plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.param import Param
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import EffectIndex
from common.util.grid_mapper import GridCell
from control_surfaces import ControlShadowEvent, ControlShadow
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations.mapping_strategies import SimpleFaders, GridStrategy
from integrations.event_filters import toEffectIndex as eEffectIndex
from integrations.tick_filters import toEffectIndex as tEffectIndex


PLUG_COLOR = Color.fromInteger(0xccccb7)


VALS = [0.0, 0.1, 0.2]
MAX_VALS = [0.05, 0.15]
PARAMS = [Param(7), Param(6)]


class DawCassette(PluginIntegration):
    """
    DAW Cassette plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        SimpleFaders(
            shadow,
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
        GridStrategy(
            shadow,
            3,
            2,
            self.triggerDrumPads,
            color_callback=self.colorDrumPads,
        )

        self.__active_pads = [0, 0]

        super().__init__(shadow)

    @eEffectIndex()
    def triggerDrumPads(
        self,
        event: ControlShadowEvent,
        plug_index: EffectIndex,
        pad: GridCell,
    ) -> bool:
        try:
            param = PARAMS[pad.overall_index // 3](plug_index)
            val = VALS[pad.overall_index % 3]
        except IndexError:
            return False

        param.value = val
        return True

    def colorDrumPads(
        self,
        control: ControlShadow,
        _,
        pad: GridCell,
    ) -> Color:
        pad_row = pad.overall_index // 3
        pad_col = pad.overall_index % 3
        try:
            if pad_col == self.__active_pads[pad_row]:
                return Color.WHITE
            else:
                return PLUG_COLOR
        except IndexError:
            return Color.BLACK

    @tEffectIndex()
    def tick(self, index: EffectIndex) -> None:
        for active_index, param in enumerate(PARAMS):
            val = param(index).value
            for i, upper in enumerate(MAX_VALS):
                if val < upper:
                    self.__active_pads[active_index] = i
                    break
            else:
                self.__active_pads[active_index] = i + 1

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("DAW Cassette",)


ExtensionManager.plugins.register(DawCassette)
