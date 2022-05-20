"""
controlsurfaces > valuestrategies > buttondata2strategy

Contains the definition for the button data2 value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.types import EventData
from . import IValueStrategy


class ButtonData2Strategy(IValueStrategy):
    """
    A value strategy using the data2 property of an event as the value, but
    only allowing binary values (0.0, 1.0)

    Usable for most basic button event types
    """

    def getValueFromEvent(self, event: EventData, value: float) -> float:
        return 1.0 if event.data2 != 0 else 0.0

    def getChannelFromEvent(self, event: EventData) -> int:
        return -1
