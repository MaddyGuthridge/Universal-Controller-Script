"""
integrations > plugin > fl > slicers

Adds integrations for slicer plugins, including Fruity Slicer and Slicex

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex
from common.util.grid_mapper import GridCell
from devices import DeviceShadow
from integrations import PluginIntegration, event_filters, tick_filters
from integrations.mapping_strategies.grid_strategy import (
    GridStrategy,
    color_callbacks,
)
from control_surfaces import ControlShadowEvent, ControlShadow


class Slicers(PluginIntegration):
    """
    Adds support for Slicex and Fruity Slicer
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        GridStrategy(
            shadow,
            None,
            None,
            self.trigger,
            color_callback=self.color,
        )
        self.__indexes: list[int] = []
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("Fruity Slicer", "Slicex")

    @event_filters.toGeneratorIndex()
    def trigger(
        self,
        control: ControlShadowEvent,
        ch_idx: GeneratorIndex,
        pad_idx: GridCell,
    ) -> bool:
        """
        Trigger a note at the required index
        """
        # TODO: why do we need to check <= 0?
        if 0 <= pad_idx.overall_index < len(self.__indexes):
            ch_idx.track.triggerNote(
                self.__indexes[pad_idx.overall_index],
                control.value,
            )
            return True
        else:
            return False

    @event_filters.toGeneratorIndex()
    def color(
        self,
        control: ControlShadow,
        ch_idx: GeneratorIndex,
        pad_idx: GridCell,
    ) -> Color:
        """
        Color the note at the required index
        """
        if 0 <= pad_idx.overall_index < len(self.__indexes):
            return color_callbacks.channelColor(
                control,
                ch_idx,
                pad_idx,
            )
        else:
            return Color()

    @tick_filters.toGeneratorIndex()
    def tick(self, index: GeneratorIndex) -> None:
        """
        Update the indexes for slices
        """
        self.__indexes = []
        for i in range(128):
            if index.getNoteName(i) != "":
                self.__indexes.append(i)
        return super().tick(index)


ExtensionManager.plugins.register(Slicers)
