"""
control_surfaces > value_strategies > twos_compliment_delta

Contains the definitions for a two's compliment delta value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg, isMidiMsgStandard
from common.util.misc import clamp
from . import IValueStrategy


class TwosComplimentDeltaStrategy(IValueStrategy):
    """
    Defines a value strategy that gets its values relative to the current
    value, using the data2 property of events to calculate an offset using
    two's compliment. This is used by many endless encoders.
    """
    def __init__(self, scaling: float = 1.0) -> None:
        """
        Create a TwosComplimentDeltaStrategy

        ### Args:
        * `scaling` (`float`, optional): amount to scale deltas by. Defaults to
          `1.0`.
        """
        self.__scaling = scaling

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        assert isMidiMsgStandard(event)
        if event.data2 < 64:
            # Positive
            delta = event.data2
        else:
            delta = event.data2 - 128
        return clamp((delta / 64) * self.__scaling + value, 0.0, 1.0)

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        assert isMidiMsgStandard(event)
        return event.status & 0xF
