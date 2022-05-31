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
from common.plug_indexes import GeneratorIndex
from control_surfaces import DrumPad, Note
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import event_filters, tick_filters


class FPC(StandardPlugin):
    """
    Used to interact with the FPC plugin, mapping drum pads to the required
    notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:

        # Bind a different callback depending on drum pad size
        size = shadow.getDevice().getDrumPadSize()
        if size[0] >= 4 and size[1] >= 8:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad4x8)
            # TODO: Figure out the logic of this at some point
            self._coordToIndex = lambda r, c: 16 - (c + 1) * 4 + r
        if size[0] >= 4 and size[1] >= 4:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad4x4)
            self._coordToIndex = lambda r, c: 16 - (c + 1) * 4 + r
        elif size[0] >= 2 and size[1] >= 8:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad2x8)
            self._coordToIndex = lambda r, c: 4 * (1-r) + c + 4 * (c >= 4)

        self._notes = shadow.bindMatches(Note, self.noteEvent)

        super().__init__(shadow, [
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return ("FPC",)

    @tick_filters.toGeneratorIndex()
    def tick(self, index: GeneratorIndex):
        for p in self._pads:
            p.color = Color.fromInteger(
                plugins.getPadInfo(
                    index[0], -1, 2, self._coordToIndex(*p.coordinate))
            )
        # Also update notes
        # Hardcoded due to bug with plugins.getPadInfo() returning wrong values
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

    @staticmethod
    def triggerPad(
        pad_idx: int,
        control: ControlShadowEvent,
        ch_idx: int
    ) -> None:
        note = plugins.getPadInfo(ch_idx, -1, 1, pad_idx)
        # Work-around for horrible bug where wrong note numbers are given
        if note > 127:
            note = note >> 16
        channels.midiNoteOn(ch_idx, note, int(control.value*127))

    @event_filters.toGeneratorIndex()
    def drumPad4x8(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds as well
        if row >= 4 or col >= 8:
            return True
        self.triggerPad(self._coordToIndex(row, col), control, *index)
        return True

    @event_filters.toGeneratorIndex()
    def drumPad4x4(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds as well
        if row >= 4 or col >= 4:
            return True
        self.triggerPad(self._coordToIndex(row, col), control, *index)
        return True

    @event_filters.toGeneratorIndex()
    def drumPad2x8(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds
        if row >= 2 or col >= 8:
            return True
        self.triggerPad(self._coordToIndex(row, col), control, *index)
        return True

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
