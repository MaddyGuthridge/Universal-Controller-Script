"""
control_surfaces > value_strategies > akai_joystick_full_strategy

Contains the definition for the button data2 value strategy

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg
from . import IValueStrategy


class AkaiJoystickFullStrategy(IValueStrategy):
    """
    A value strategy using the data2 property of an event as the value, but
    only allowing binary values (0.0, 1.0)

    Usable for most basic button event types
    """

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        return 1.0 if event.data2 >= 127 else 0.0

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        return -1
