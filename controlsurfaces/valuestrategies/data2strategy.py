"""
controlsurfaces > valuestrategies > data2strategy

Contains the Data2 value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.types import eventData
from . import IValueStrategy

class Data2Strategy(IValueStrategy):
    """
    A value strategy using the data2 property of an event as the value

    Usable for most basic event types
    """
    def getValueFromEvent(self, event: eventData) -> int:
        assert event.data2 is not None
        return event.data2
    
    def getValueFromFloat(self, f: float) -> int:
        return int(f * 127)

    def getFloatFromValue(self, value: int) -> float:
        return value / 127
