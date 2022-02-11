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
from . import IControlMatcher

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
    
    def addControls(self, controls: list[ControlSurface]) -> None:
        """
        Register and add a list of controls to the control matcher.

        ### Args:
        * `controls` (`list[ControlSurface]`): Controls to add
        """
        for c in controls:
            self.addControl(c)
    
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
