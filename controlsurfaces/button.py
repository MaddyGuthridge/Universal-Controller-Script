
from common.eventpattern import IEventPattern
from common.types import eventData
from .controlsurface import ControlSurface

class Button(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> list[type]:
        # Buttons shouldn't be reassigned to anything else
        return []

class GenericButton(Button):
    """
    A button that uses the data2 byte to determine whether it is enabled or not

    Can be overridden if necessary to add more complexity
    """
    
    def __init__(self, event_pattern: IEventPattern, name: str) -> None:
        super().__init__(event_pattern, name)
        self.__enabled = False
    
    def setValueFromEvent(self, event: eventData) -> None:
        """
        Sets the value of an event as a float between (0.0 - 1.0) from an event

        ### Args:
        * `event` (`eventData`): event to set value from
        """
        if event.data2:
            self.__enabled = True
        else:
            self.__enabled = False
    
    def _setValue(self, newValue: float) -> None:
        self.__enabled = newValue != 0.0
    
    def _getValue(self) -> float:
        return 1.0 if self.__enabled else 0.0
        
    
