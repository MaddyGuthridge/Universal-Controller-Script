"""
control_surfaces > event_patterns > null_pattern

An event pattern that matches with nothing

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from fl_classes import FlMidiMsg
from . import IEventPattern


class NullPattern(IEventPattern):
    """
    Null patterns won't match with any events
    """

    def matchEvent(self, event: FlMidiMsg) -> bool:
        return False

    def fulfil(self) -> FlMidiMsg:
        raise TypeError("Unable to fulfil a NullPattern")
