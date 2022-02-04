"""
controlsurfaces > valuestrategies > forwardedstrategy

Contains the definition for the ForwardedStrategy strategy for getting values
from forwarded events

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.types import eventData
from common.util.events import eventFromForwarded
from . import IValueStrategy

class ForwardedStrategy(IValueStrategy):
    """
    Contains the definition for the value strategy used to get data out of
    forwarded events.
    """
    def __init__(self, strat: IValueStrategy) -> None:
        self._strat = strat
    
    def getValueFromEvent(self, event: eventData):
        # The value is already matching, so we can cheat somewhat with getting
        # the data out
        return self._strat.getValueFromEvent(eventFromForwarded(event))

    def getValueFromFloat(self, f: float):
        return self._strat.getValueFromFloat(f)

    def getFloatFromValue(self, value) -> float:
        return self._strat.getFloatFromValue(value)
