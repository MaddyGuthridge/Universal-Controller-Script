"""
plugins > mappingstrategies > notestrategy

Strategy for mapping notes to plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import channels

from typing import Any
from common.util.apifixes import GeneratorIndex

from controlsurfaces import Note
from controlsurfaces import ControlShadow
from devices import DeviceShadow
from plugs.eventfilters import filterToGeneratorIndex
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

    @filterToGeneratorIndex
    def noteCallback(
        self,
        control: ControlShadow,
        index: GeneratorIndex,
        *args: tuple[Any]
    ) -> bool:
        channels.midiNoteOn(
            *index,
            control.getControl().coordinate[0],
            int(control.getCurrentValue()*127),
            # TODO: Use MIDI channels
        )
        return True
