"""
controlsurfaces > controlsurface

Contains the ControlSurface class, which defines the abstract base type for
all control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from typing import Optional

from common import IEventPattern, MatchedEvent
from common.types import eventData, Color

class ControlSurface:
    """
    Defines an abstract base class for a control surface.

    This class is extended by all other control surfaces.
    """
    
    def __init__(self, event_pattern: IEventPattern) -> None:
        """
        Create a ControlSurface

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to use when recognising the
        event
        """
        self._pattern =  event_pattern
        self.__color = Color()

    def match(self, event: eventData) -> Optional[MatchedEvent]:
        """
        Returns a MatchedEvent if the given event matches this control surface,
        otherwise returns None

        ### Args:
        * `event` (`eventData`): event to potentially match

        ### Returns:
        * `Optional[MatchedEvent]`: match design
        """
        if self._pattern.matchEvent(event):
            return MatchedEvent(self, self.getValueFromEvent(event))
        else:
            return None

    def getValueFromEvent(self, event: eventData) -> float:
        """
        Returns the value of an event as a float between (0.0 - 1.0)

        ### Args:
        * `event` (`eventData`): event to get value from

        ### Returns:
        * `float`: value
        """
        raise NotImplementedError("This function should be overridden by a "
                                  "child class")

    @property
    def color(self) -> Color:
        return self.__color
