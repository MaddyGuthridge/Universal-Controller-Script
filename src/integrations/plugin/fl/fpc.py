"""
integrations > plugin > fl > fpc

Integration for FL Studio's FPC plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex, FlIndex
from common.util.grid_mapper import GridCell
from control_surfaces import Note
from control_surfaces import ControlShadowEvent, ControlShadow
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations import event_filters, tick_filters
from integrations.mapping_strategies import GridStrategy


def calculate_overall_index(pad_idx: GridCell) -> int:
    """
    Calculate and return the required FPC drum pad index given the index of the
    grid mapping.
    """
    # TODO: Consider integrating this with the GridCell class for something
    # like an "inner index"
    # That would probably be a much better design, and would certainly make it
    # more reusable compared to this janky poorly-placed mess you see before
    # you
    group_index = pad_idx.col + pad_idx.group_width * pad_idx.inverse_row
    return group_index + pad_idx.group_number * pad_idx.group_size


def colorPad(
    control: ControlShadow,
    ch_idx: FlIndex,
    pad_idx: GridCell,
) -> Color:
    """
    Determine the color to use for a particular drum pad
    """
    if not isinstance(ch_idx, GeneratorIndex):
        return Color()
    return ch_idx.fpcGetPadColor(calculate_overall_index(pad_idx))


@event_filters.toGeneratorIndex(False)
def triggerPad(
    control: ControlShadowEvent,
    ch_idx: GeneratorIndex,
    pad_idx: GridCell,
) -> bool:
    overall_index = calculate_overall_index(pad_idx)

    note = ch_idx.fpcGetPadSemitone(overall_index)
    ch_idx.track.triggerNote(note, control.value)
    return True


class FPC(PluginIntegration):
    """
    Used to interact with the FPC plugin, mapping drum pads to the required
    notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        GridStrategy(
            shadow,
            4,
            2,
            triggerPad,
            color_callback=colorPad,
            top_to_bottom=False,
        )

        self._notes = shadow.bindMatches(Note, self.noteEvent)

        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("FPC",)

    @tick_filters.toGeneratorIndex()
    def tick(self, index: GeneratorIndex):
        # Set properties for each keyboard note
        notes = set()
        for idx in range(32):
            # Get the note number
            note = index.fpcGetPadSemitone(idx)

            # Set values
            self._notes[note].color = index.fpcGetPadColor(idx)
            self._notes[note].annotation = index.getNoteName(note)
            notes.add(note)

        # Set colors and annotations for the others to be blank
        for i in range(128):
            if i not in notes:
                self._notes[i].color = Color()
                self._notes[i].annotation = ""

    @event_filters.toGeneratorIndex()
    def noteEvent(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        index.track.triggerNote(
            control.getControl().coordinate[1],
            control.value,
        )
        return True


ExtensionManager.plugins.register(FPC)
