"""
control_surfaces > value_strategies > null_strategy

Contains the definition for the null event value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg
from . import IValueStrategy


class NullStrategy(IValueStrategy):
    """
    A value strategy that is always true, for buttons that only send a press
    event, and not a release event
    """

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        return 0.0

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        return -1
