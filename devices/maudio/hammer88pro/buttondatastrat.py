
from common.types import eventData
from controlsurfaces import IValueStrategy


class HammerButtonStrategy(IValueStrategy):
    """
    Strategy for buttons on Hammer 88 Pro

    Since it mashes events together we need a special way to get the data
    """
    def __init__(self, on: int) -> None:
        """
        Create Hammer 88 Pro button value strategy

        ### Args:
        * `on` (`int`): value interpreted as a press (all others will be 
          interpreted as a release)
        """
        self._on = on
        super().__init__()
        
    def getValueFromEvent(self, event: eventData):
        return event.data2 == self._on
    
    def getValueFromFloat(self, f: float):
        return f == 1.0

    def getFloatFromValue(self, value) -> float:
        return 1.0 if value else 0.0
