"""
control_surfaces > value_strategies > data_strategy

Contains Data2Strategy and Data1Strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from fl_classes import FlMidiMsg, isMidiMsgStandard
from . import IValueStrategy


class DataStrategy(IValueStrategy):
    """
    A value strategy using a data property of an event as the value

    Usable for most basic event types
    """

    def __init__(self, prop: str) -> None:
        """
        Create a data strategy, given the property to use

        ### Args:
        * `prop` (`str`): property to use
        """
        self._prop = prop

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        val = getattr(event, self._prop)
        if not isinstance(val, int):
            raise TypeError("Property value must be an int")
        return val / 127

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        assert isMidiMsgStandard(event)
        return event.status & 0xF


class Data2Strategy(DataStrategy):
    """
    A value strategy using the data2 property of an event as the value

    Usable for most basic event types
    """

    def __init__(self) -> None:
        super().__init__("data2")


class Data1Strategy(DataStrategy):
    """
    A value strategy using the data1 property of an event as the value

    Usable for event types where the value is stored in data1, such as channel
    after-touch
    """

    def __init__(self) -> None:
        super().__init__("data1")
