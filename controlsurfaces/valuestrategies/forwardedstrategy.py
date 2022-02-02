
from common.types import eventData
from common.util.events import eventFromForwarded
from . import IValueStrategy

class ForwardedStrategy(IValueStrategy):
    
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
