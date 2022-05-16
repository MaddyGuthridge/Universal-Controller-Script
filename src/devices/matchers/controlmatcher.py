"""
devices > controlmatcher

Defines the IControlMatcher interface for matching up controls, as well as a
BasicControlMatcher for simple devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from typing import Optional
from abc import abstractmethod
from common.types import EventData
from controlsurfaces import ControlEvent, ControlSurface


class IControlMatcher:
    """
    The interface for matching controls from MIDI events

    This can be extended to match controls in a custom, more-efficient manner
    if required or desired. Otherwise, the BasicControlMatcher class will work.
    """
    @abstractmethod
    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        """
        Match an event to a control.

        ### Args:
        * `event` (`eventData`): event to match

        ### Returns:
        * `ControlMapping | None`: mapping to matched control, or None if there
          was no match
        """
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")

    @abstractmethod
    def getControls(self) -> list[ControlSurface]:
        """
        Returns a list of controls contained by the control matcher.

        ### Returns:
        * `list[ControlSurface]`: list of control surfaces
        """
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")

    @abstractmethod
    def tick(self, thorough: bool) -> None:
        """Tick this control matcher, as well as any child control matchers

        ### Args:
        * thorough (`bool`): Whether a full tick should be done.
        """
        print(type(self))
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")
