"""
devices > control matcher

Defines the IControlMatcher interface for matching up controls, as well as a
BasicControlMatcher for simple devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from typing import Optional
from abc import abstractmethod
from common.types import eventData
from controlsurfaces import ControlMapping, ControlSurface

class IControlMatcher:
    """
    The interface for matching controls from MIDI events

    This can be extended to match controls in a custom, more-efficient manner
    if required or desired. Otherwise, the BasicControlMatcher class will work.
    """
    @abstractmethod
    def matchEvent(self, event: eventData) -> Optional[ControlMapping]:
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
        Return a set of groups for all the control surfaces.

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

class BasicControlMatcher(IControlMatcher):
    """
    A basic implementation of the control mapper, using a list of controls and a
    set of groups.

    This should be usable for most basic controllers, but for more complex
    controllers with many controls, it may have poor performance compared to
    hard-coded custom matchers, which can be created by extending
    the IControlMatcher class.
    """
    def __init__(self) -> None:
        self.__controls: list[ControlSurface] = []
        self.__groups: set[str] = set()
    
    def addControl(self, control: ControlSurface) -> None:
        """
        Register and add a control to the control matcher.

        ### Args:
        * `control` (`ControlSurface`): Control to add
        """
        self.__controls.append(control)
        self.__groups.add(control.group)
    
    def matchEvent(self, event: eventData) -> Optional[ControlMapping]:
        for c in self.__controls:
            m = c.match(event)
            if m is not None:
                return m
        return None
    
    def getGroups(self) -> set[str]:
        return self.__groups
    
    def getControls(self, group: str = None) -> list[ControlSurface]:
        if group is None:
            return self.__controls
        else:
            ret = []
            for c in self.__controls:
                if c.group == group:
                    ret.append(c)
            return ret
