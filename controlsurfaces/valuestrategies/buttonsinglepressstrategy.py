"""
controlsurfaces > valuestrategies > buttonsinglepressstrategy

Contains the definition for the button single press strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.types import EventData
from . import IValueStrategy

class ButtonSinglePressStrategy(IValueStrategy):
    """
    A value strategy that is always true, for buttons that only send a press
    event, and not a release event
    """
    def getValueFromEvent(self, event: EventData) -> bool:
        return True
    
    def getValueFromFloat(self, f: float) -> bool:
        return True

    def getFloatFromValue(self, value: bool) -> float:
        return 1.0
