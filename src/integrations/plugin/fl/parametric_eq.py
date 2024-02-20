"""
plugs > standard > fl > parametric_eq

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
from common.param import Param
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex
from control_surfaces import Fader, Knob, Encoder
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations import event_filters, tick_filters

# Number of parameters in the parametric EQ
NUM_PARAMS = 7
# Start indexes for each param set
LEVEL = 0
FREQUENCY = 7
BANDWIDTH = 14

# Colors of the bands in the eq
COLORS = [
    Color.fromInteger(0xCD5689),  # Purple
    Color.fromInteger(0xA254C1),  # Pink
    Color.fromInteger(0x5263BC),  # Orange
    Color.fromInteger(0x57B0B2),  # Yellowish green
    Color.fromInteger(0x40BC55),  # Green
    Color.fromInteger(0x93AB46),  # Aqua
    Color.fromInteger(0xA66B43),  # Blue
]


class ParametricEq(PluginIntegration):
    """
    Used to interact with the Fruity Parametric EQ 2 plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        # Faders > levels
        self._levels = shadow.bindMatches(
            Fader,
            self.levels,
            target_num=NUM_PARAMS,
        )
        self._frequencies = shadow.bindMatches(
            Knob,
            self.frequencies,
            target_num=NUM_PARAMS,
        )
        self._bandwidths = shadow.bindMatches(
            Encoder,
            self.bandwidths,
            target_num=NUM_PARAMS,
        )
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)

    @tick_filters.toEffectIndex()
    def tick(self, index: GeneratorIndex):
        # List of (color_index, (control, param_index))
        # CHECK: Does this work if some properties weren't bound?
        properties = list(
            enumerate(
                zip(self._levels, range(LEVEL, LEVEL+NUM_PARAMS))
            )
        ) + list(
            enumerate(
                zip(self._frequencies, range(FREQUENCY, FREQUENCY+NUM_PARAMS))
            )
        ) + list(
            enumerate(
                zip(self._bandwidths, range(BANDWIDTH, BANDWIDTH+NUM_PARAMS))
            )
        )

        # Set each property
        for color_index, (control, param_index) in properties:
            param = Param(param_index)(index)
            control.annotation = param.name
            control.color = COLORS[color_index]
            control.value = param.value

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("Fruity parametric EQ 2",)

    @event_filters.toEffectIndex()
    def levels(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        param = Param(LEVEL + control.getShadow().coordinate[1])
        param(index).value = control.value
        return True

    @event_filters.toEffectIndex()
    def frequencies(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        param = Param(FREQUENCY + control.getShadow().coordinate[1])
        param(index).value = control.value
        return True

    @event_filters.toEffectIndex()
    def bandwidths(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        param = Param(BANDWIDTH + control.getShadow().coordinate[1])
        param(index).value = control.value
        return True


ExtensionManager.plugins.register(ParametricEq)
