"""
plugins > mappingstrategies > notestrategy

Strategy for mapping notes to plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import channels

from typing import Any
from common.util.apifixes import UnsafeIndex, PluginIndex
from common import getContext

from controlsurfaces import Note
from controlsurfaces import ControlShadowEvent
from devices import DeviceShadow
# from plugs.eventfilters import filterToGeneratorIndex
from . import IMappingStrategy

class NoteStrategy(IMappingStrategy):
    """
    Maps notes to the active generator plugin
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
            i = channels.getChannelIndex(*getContext().active.getGenerator())
            print("A")
        except TypeError:
            # Index out of range - we're using a plugin from a different group
            i = channels.channelNumber()
        print(i)
        channels.midiNoteOn(
            i,
            control.getControl().coordinate[1],
            int(control.value*127),
            # NOTE: Currently FL Studio won't set the note color correctly
            # from this channel
            control.channel
        )
        return True
