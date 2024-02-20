"""
integrations > mapping_strategies > note_strategy

Strategy for mapping notes to integrations

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
from common.plug_indexes.fl_index import FlIndex
from common import getContext

from control_surfaces import Note
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow


class NoteStrategy:
    """
    Maps notes to the active generator plugin.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Maps notes to the active generator plugin

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to bind to
        """
        # Bind note events to noteCallback()
        shadow.bindMatches(
            Note,
            self.noteCallback,
            raise_on_failure=False
        )

    def noteCallback(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        *args: Any,
        **kwargs: Any
    ) -> bool:
        getContext().activity.getGenerator().track.triggerNote(
            control.getControl().coordinate[1],
            control.value,
            control.channel,
        )
        return True
