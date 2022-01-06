
from common.types import eventData
from . import IValueStrategy

class Data2Strategy(IValueStrategy):
    def getValueFromEvent(self, event: eventData) -> int:
        assert event.data2 is not None
        return event.data2
    
    def getValueFromFloat(self, f: float) -> int:
        return int(f * 127)

    def getFloatFromValue(self, value: int) -> float:
        return value / 127
