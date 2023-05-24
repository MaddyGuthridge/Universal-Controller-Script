"""
plugs > standard > fl > fpc

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import plugins
import channels
from typing import Any
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex, UnsafeIndex
from common.util.grid_mapper import GridCell
from control_surfaces import Note
from control_surfaces import ControlShadowEvent, ControlShadow
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import event_filters, tick_filters
from plugs.mapping_strategies import GridStrategy


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
    ch_idx: UnsafeIndex,
    pad_idx: GridCell,
) -> Color:
    """
    Determine the color to use for a particular drum pad
    """
    if not isinstance(ch_idx, tuple):
        return Color()
    chan = ch_idx[0]
    return Color.fromInteger(plugins.getPadInfo(
        chan,
        -1,
        2,
        calculate_overall_index(pad_idx),
    ))


@event_filters.toGeneratorIndex(False)
def triggerPad(
    control: ControlShadowEvent,
    ch_idx: GeneratorIndex,
    pad_idx: GridCell,
) -> bool:
    overall_index = calculate_overall_index(pad_idx)
    note = plugins.getPadInfo(*ch_idx, -1, 1, overall_index)
    # Work-around for horrible bug where wrong note numbers are given
    if note > 127:
        note = note >> 16
    channels.midiNoteOn(*ch_idx, note, int(control.value*127))
    return True


class FPC(StandardPlugin):
    """
    Used to interact with the FPC plugin, mapping drum pads to the required
    notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        drums = GridStrategy(
            4,
            2,
            triggerPad,
            color_callback=colorPad,
            top_to_bottom=False,
        )

        self._notes = shadow.bindMatches(Note, self.noteEvent)

        super().__init__(shadow, [drums])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("FPC",)

    @tick_filters.toGeneratorIndex()
    def tick(self, index: GeneratorIndex):
        notes = set()
        for idx in range(32):
            # Get the note number
            note = plugins.getPadInfo(*index, -1, 1, idx)
            # Get the color
            color = plugins.getPadInfo(*index, -1, 2, idx)
            # get the annotation
            annotation = plugins.getName(*index, -1, 2, note)

            # Set values
            self._notes[note].color = Color.fromInteger(color)
            self._notes[note].annotation = annotation
            notes.add(note)

        # Set colors and annotations for the others
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
        channels.midiNoteOn(
            *index,
            control.getControl().coordinate[1],
            int(control.value * 127),
            control.channel
        )
        return True


ExtensionManager.plugins.register(FPC)
