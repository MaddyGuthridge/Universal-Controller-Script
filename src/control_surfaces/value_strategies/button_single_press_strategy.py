"""
control_surfaces > value_strategies > button_single_press_strategy

Contains the definition for the button single press strategy

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg
from . import IValueStrategy


class ButtonSinglePressStrategy(IValueStrategy):
    """
    A value strategy that is always true, for buttons that only send a press
    event, and not a release event
    """

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        return 1.0

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        return -1
