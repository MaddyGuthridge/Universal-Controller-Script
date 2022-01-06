
from typing import Any, Generic, TypeVar

from common.types import eventData

T = TypeVar("T")

class IValueStrategy(Generic[T]):
    
    def getValueFromEvent(self, event: eventData) -> T:
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")
    
    def getValueFromFloat(self, f: float) -> T:
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")

    def getFloatFromValue(self, value: T) -> float:
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")
