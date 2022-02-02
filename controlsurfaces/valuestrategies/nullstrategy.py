"""
controlsurfaces > valuestrategies > nullstrategy

Contains the definition for the nullevent value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.types import eventData
from . import IValueStrategy

class NullEventStrategy(IValueStrategy):
    """
    A value strategy that is always true, for buttons that only send a press
    event, and not a release event
    """
    def getValueFromEvent(self, event: eventData) -> bool:
        return False
    
    def getValueFromFloat(self, f: float) -> bool:
        return False

    def getFloatFromValue(self, value: bool) -> float:
        return 0.0
