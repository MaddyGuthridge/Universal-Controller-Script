
from typing import Optional
from common import IEventPattern
from common.types import eventData
from controlsurfaces import ControlShadow

from controlsurfaces import ControlSurface, ControlMapping
from devices import IControlMatcher

class Device:
    
    def __init__(self, control_matcher: IControlMatcher) -> None:
        self.__matcher = control_matcher
    
    @staticmethod
    def getUniversalEnquiryResponsePattern() -> IEventPattern:
        """
        Returns the event pattern from which a device can be recognised so that
        its representation can be loaded

        ### Returns:
        * `IEventPattern`: pattern to match universal device enquiry
        """
        raise NotImplementedError("This method must be overridden by child classes")

    def matchEvent(self, event: eventData) -> Optional[ControlMapping]:
        """
        Match an event from the device, so that the script can operator on it

        ### Returns:
        * `MatchedEvent`: event data
        """
        return self.__matcher.matchEvent(event)
    
    def getControlShadows(self, group:str=None) -> list[ControlShadow]:
        """
        Returns a list of new control shadows representing all the controls
        available on the device.

        ### Returns:
        * `list[ControlSurface]`: Control shadows
        """
        return [ControlShadow(c) for c in self.__matcher.getControls(group)]
    
    def getGroups(self) -> set[str]:
        return self.__matcher.getGroups()
