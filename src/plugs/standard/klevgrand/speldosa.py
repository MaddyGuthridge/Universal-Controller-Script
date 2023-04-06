"""
plugs > standard > klevgrand > speldosa

Speldosa (Wintergatan + Klevgrand)

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# import plugins
from common.types import Color
from common.extension_manager import ExtensionManager
# from common.plug_indexes import EffectIndex
# from control_surfaces import ControlShadowEvent, ControlShadow
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import SimpleFaders  # , DrumPadStrategy
# from plugs.event_filters import toEffectIndex as eEffectIndex
# from plugs.tick_filters import toEffectIndex as tEffectIndex


PLUG_COLOR = Color.fromInteger(0xccccb7)

VALS = {
    3: [0.0, 0.3, 0.6, 0.8],
    0: [0.0, 1.0],
}
MAX_VALS = [0.05, 0.15]
PARAMS = [3, 0]


class Speldosa(StandardPlugin):
    """
    Speldosa plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        faders = SimpleFaders(
            [
                1,  # Room Mix (Level)
                2,  # Space
                4,  # Volume
            ],
            PLUG_COLOR,
        )
        # drums = DrumPadStrategy(
        #     4,
        #     2,
        #     True,
        #     self.triggerDrumPads,
        #     self.colorDrumPads,
        # )

        self.__active_pads = {
            3: 0,
            0: 0,
        }

        super().__init__(shadow, [faders])

#     @eEffectIndex()
#     def triggerDrumPads(
#         self,
#         event: ControlShadowEvent,
#         plug_index: EffectIndex,
#         pad: int,
#     ) -> bool:
#         try:
#             param = PARAMS[pad // 4]
#             val = VALS[param][pad % 4]
#         except IndexError:
#             return False
#         plugins.setParamValue(val, param, *plug_index)
#         return True
#
#     def colorDrumPads(
#         self,
#         control: ControlShadow,
#         _,
#         pad: int,
#     ) -> Color:
#         param = PARAMS[pad // 4]
#         pad_col = pad % 4
#         try:
#             if pad_col == self.__active_pads[param]:
#                 return Color.WHITE
#             else:
#                 return PLUG_COLOR
#         except IndexError:
#             return Color.BLACK
#
#     @tEffectIndex()
#     def tick(self, index: EffectIndex) -> None:
#         for active_index, param in enumerate(PARAMS):
#             val = plugins.getParamValue(param, *index)
#             for i, upper in enumerate(MAX_VALS):
#                 if val < upper:
#                     self.__active_pads[active_index] = i
#                     break
#             else:
#                 self.__active_pads[active_index] = i + 1

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("Speldosa",)


ExtensionManager.plugins.register(Speldosa)
