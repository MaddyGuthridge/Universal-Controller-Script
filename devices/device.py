
from typing import Optional
from common import IEventPattern
from controlsurfaces import ControlShadow

from controlsurfaces import ControlSurface

class Device:
    
    @staticmethod
    def getUniversalEnquiryResponsePattern() -> IEventPattern:
        """
        Returns the event pattern from which a device can be recognised so that
        its representation can be loaded

        ### Returns:
        * `IEventPattern`: pattern to match universal device enquiry
        """
        raise NotImplementedError("This method must be overridden by child classes")

    def matchEvent(self) -> Optional[ControlShadow]:
        """
        Match an event from the device, so that the script can operator on it

        ### Returns:
        * `MatchedEvent`: event data
        """
        raise NotImplementedError("This method must be overridden by child classes")
    
    def getControlShadows(self) -> list[ControlShadow]:
        """
        Returns a list of new control shadows representing all the controls
        available on the device.

        ### Returns:
        * `list[ControlSurface]`: Control shadows
        """
        return []
