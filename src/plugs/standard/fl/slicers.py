"""
plugs > standard > fl > slicers

Adds support for slicer plugins, including Fruity Slicer and Slicex

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import plugins
import channels
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex
from devices import DeviceShadow
from plugs import StandardPlugin, event_filters, tick_filters
from plugs.mapping_strategies.drum_pad_strategy import (
    DrumPadStrategy,
    color_callbacks,
)
from control_surfaces import ControlShadowEvent, ControlShadow


class Slicers(StandardPlugin):
    """
    Adds support for Slicex and Fruity Slicer
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        drums = DrumPadStrategy(
            -1,
            -1,
            True,
            self.trigger,
            self.color,
        )
        self.__indexes: list[int] = []
        super().__init__(shadow, [drums])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("Fruity Slicer", "Slicex")

    @event_filters.toGeneratorIndex()
    def trigger(
        self,
        control: ControlShadowEvent,
        ch_idx: GeneratorIndex,
        pad_idx: int,
    ) -> bool:
        """
        Trigger a note at the required index
        """
        if 0 <= pad_idx < len(self.__indexes):
            channels.midiNoteOn(
                channels.getChannelIndex(*ch_idx),
                self.__indexes[pad_idx],
                int(control.value * 127),
            )
            return True
        else:
            return False

    @event_filters.toGeneratorIndex()
    def color(
        self,
        control: ControlShadow,
        ch_idx: GeneratorIndex,
        pad_idx: int,
    ) -> Color:
        """
        Color the note at the required index
        """
        if 0 <= pad_idx < len(self.__indexes):
            return color_callbacks.channelColor(control, ch_idx, pad_idx)
        else:
            return Color()

    @tick_filters.toGeneratorIndex()
    def tick(self, index: GeneratorIndex) -> None:
        """
        Update the indexes for slices
        """
        self.__indexes = []
        for i in range(128):
            if plugins.getName(*index, -1, 2, i) != "":
                self.__indexes.append(i)
        return super().tick(index)


ExtensionManager.plugins.register(Slicers)
