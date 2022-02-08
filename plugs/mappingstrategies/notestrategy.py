"""
plugins > mappingstrategies > notestrategy

Strategy for mapping notes to plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import channels

from typing import Any
from common.util.apifixes import UnsafePluginIndex, PluginIndex
from common import getContext

from controlsurfaces import Note
from controlsurfaces import ControlShadow
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
            # TODO: What on earth is up with this?
            self.noteCallback,
            raise_on_failure=False
        )

    def noteCallback(
        self,
        control: ControlShadow,
        index: UnsafePluginIndex,
        *args: Any,
        **kwargs: Any
    ) -> bool:
        channels.midiNoteOn(
            *getContext().active.getGenerator(),
            control.getControl().coordinate[1],
            int(control.getCurrentValue()*127),
            # TODO: Use MIDI channels
        )
        return True
