"""
controlsurfaces > valuestrategies > data2strategy

Contains the Data2 value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.types.event_data import EventData, isEventStandard
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

    def getValueFromEvent(self, event: EventData, value: float) -> float:
        return getattr(event, self._prop) / 127

    def getChannelFromEvent(self, event: EventData) -> int:
        assert isEventStandard(event)
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
    aftertouch
    """

    def __init__(self) -> None:
        super().__init__("data1")