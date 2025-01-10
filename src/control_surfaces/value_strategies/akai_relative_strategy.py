"""
control_surfaces > value_strategies > akai_relative_strategy

Contains the definitions for Akai relative encoder value strategies

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg, isMidiMsgStandard
from common.util.misc import clamp
from . import IValueStrategy


class AkaiRelativeStrategy(IValueStrategy):
    """
    Defines a value strategy that gets its values as either a 1 for an increase
    or a 127 for a decrease, using the data2 property of events
    This is used by the AKAI MPK mini (plus or Mk3) endless encoders.
    """
    def __init__(self, scaling: float = 1.0) -> None:
        """
        Create a AkaiRelativeStrategy

        ### Args:
        * `scaling` (`float`, optional): amount to scale delta by. Defaults to
          `1.0`.
        """
        self.__scaling = scaling

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        assert isMidiMsgStandard(event)
        event.inEv = event.data2
        if event.inEv >= 0x40:
            event.outEv = event.inEv - 0x80
        else:
            event.outEv = event.inEv
        # event.isIncrement = 1
        # # 1-63 are right turns; 64-127 is a left turn
        # inc = event.data2 if event.data2 < 64 else (event.data2 - 128)
        inc = event.outEv
        return clamp((inc / 127) * self.__scaling + value, 0.0, 1.0)

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        assert isMidiMsgStandard(event)
        return event.status & 0xF
