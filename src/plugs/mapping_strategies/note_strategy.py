"""
plugins > mapping_strategies > note_strategy

Strategy for mapping notes to plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import channels

from typing import Any
from common.plug_indexes.fl_index import UnsafeIndex
from common import getContext

from control_surfaces import Note
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow
from . import IMappingStrategy


class NoteStrategy(IMappingStrategy):
    """
    Maps notes to the active generator plugin.
    """

    def apply(self, shadow: DeviceShadow) -> None:
        # Bind note events to noteCallback()
        shadow.bindMatches(
            Note,
            self.noteCallback,
            raise_on_failure=False
        )

    def noteCallback(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any,
        **kwargs: Any
    ) -> bool:
        try:
            i = channels.getChannelIndex(*getContext().activity.getGenerator())
        except TypeError:
            # Index out of range - we're using a plugin from a different group
            i = channels.channelNumber()
        channels.midiNoteOn(
            i,
            control.getControl().coordinate[1],
            int(control.value*127),
            # NOTE: Currently FL Studio won't set the note color correctly
            # from this channel
            control.channel
        )
        return True
