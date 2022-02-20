"""
devices > control matcher

Defines the IControlMatcher interface for matching up controls, as well as a
BasicControlMatcher for simple devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from typing import Optional
from abc import abstractmethod
from common.types import EventData
from controlsurfaces import ControlMapping, ControlSurface

class IControlMatcher:
    """
    The interface for matching controls from MIDI events

    This can be extended to match controls in a custom, more-efficient manner
    if required or desired. Otherwise, the BasicControlMatcher class will work.
    """
    @abstractmethod
    def matchEvent(self, event: EventData) -> Optional[ControlMapping]:
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
    def getGroups(self) -> set[str]:
        """
        Return a set of groups for all the control surfaces managed by this
        matcher.

        Refer to the documentation for the group property in the ControlSurface
        type.

        ### Returns:
        * `set[str]`: set of groups
        """
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")
    
    @abstractmethod
    def getControls(self, group:str=None) -> list[ControlSurface]:
        """
        Returns a list of controls contained by the control matcher.

        The group option can be used to filter by group if required

        ### Args:
        * `group` (`str`, optional): Group to filter by. Defaults to `None`.

        ### Returns:
        * `list[ControlSurface]`: list of control surfaces
        """
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")
