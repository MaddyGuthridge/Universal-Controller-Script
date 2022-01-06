
from common.types import eventData
from . import IValueStrategy

class ButtonData2Strategy(IValueStrategy):
    
    def getValueFromEvent(self, event: eventData) -> bool:
        return event.data2 != 0
    
    def getValueFromFloat(self, f: float) -> bool:
        return f != 0.0

    def getFloatFromValue(self, value: bool) -> float:
        return 1.0 if value else 0.0
