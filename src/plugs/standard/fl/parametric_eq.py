
import plugins
from typing import Any
from common.types import Color
from common.extension_manager import ExtensionManager
from common.util.api_fixes import GeneratorIndex
from control_surfaces import Fader, Knob, Encoder
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import event_filters, tick_filters

NUM_PARAMS = 7
LEVEL = 0
FREQUENCY = 7
BANDWIDTH = 14

COLORS = [
    Color.fromInteger(0xCD5689),  # Purple
    Color.fromInteger(0xA254C1),  # Pink
    Color.fromInteger(0x5263BC),  # Orange
    Color.fromInteger(0x57B0B2),  # Yellowish green
    Color.fromInteger(0x40BC55),  # Green
    Color.fromInteger(0x93AB46),  # Aqua
    Color.fromInteger(0xA66B43),  # Blue
]


class ParametricEq(StandardPlugin):
    """
    Used to interact with the Fruit parametric EQ 2 plugin
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
        super().__init__(shadow, [])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @tick_filters.toEffectIndex()
    def tick(self, index: GeneratorIndex):
        if len(self._levels):
            for color, (f, i) in enumerate(
                zip(self._levels, range(LEVEL, LEVEL+NUM_PARAMS))
            ):
                f.annotation = plugins.getParamName(i, *index)
                f.color = COLORS[color]
                f.value = plugins.getParamValue(i, *index)
        if len(self._frequencies):
            for color, (f, i) in enumerate(
                zip(self._frequencies, range(FREQUENCY, FREQUENCY+NUM_PARAMS))
            ):
                f.annotation = plugins.getParamName(i, *index)
                f.color = COLORS[color]
                f.value = plugins.getParamValue(i, *index)
        if len(self._frequencies):
            for color, (f, i) in enumerate(
                zip(self._bandwidths, range(BANDWIDTH, BANDWIDTH+NUM_PARAMS))
            ):
                f.annotation = plugins.getParamName(i, *index)
                f.color = COLORS[color]
                f.value = plugins.getParamValue(i, *index)

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
        plugins.setParamValue(control.value, LEVEL +
                              control.getShadow().coordinate[1], *index)
        return True

    @event_filters.toEffectIndex()
    def frequencies(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        plugins.setParamValue(control.value, FREQUENCY +
                              control.getShadow().coordinate[1], *index)
        return True

    @event_filters.toEffectIndex()
    def bandwidths(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        plugins.setParamValue(control.value, BANDWIDTH +
                              control.getShadow().coordinate[1], *index)
        return True


ExtensionManager.plugins.register(ParametricEq)
