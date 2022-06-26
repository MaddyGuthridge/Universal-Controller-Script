"""
control_surfaces > value_strategies > note_strategy

Contains the definition for the note value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg, isMidiMsgStandard
from . import IValueStrategy


class NoteStrategy(IValueStrategy):
    """
    The strategy to get data values from note events
    """

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        assert isMidiMsgStandard(event)
        if 0x80 <= event.status < 0x90:
            return 0.0
        else:
            return event.data2 / 127

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        assert isMidiMsgStandard(event)
        return event.status & 0xF
