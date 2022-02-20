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
        self._controls: list[ControlSurface] = []
        self._groups: set[str] = set()
        self._sub_matchers: list[IControlMatcher] = []
    
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
        self._controls.append(control)
        self._groups.add(control.group)
    
    def addSubMatcher(self, matcher: IControlMatcher) -> None:
        """
        Register a control matcher to work as a component of this control
        matcher

        This allows for more complex control mappings to be made without the
        need to implement a full control matcher

        ### Args:
        * `matcher` (`IControlMatcher`): control matcher to add
        """
        self._sub_matchers.append(matcher)
    
    def matchEvent(self, event: EventData) -> Optional[ControlMapping]:
        for s in self._sub_matchers:
            if (m := s.matchEvent(event)) is not None:
                return m
        for c in self._controls:
            if (m := c.match(event)) is not None:
                return m
        return None
    
    def getGroups(self) -> set[str]:
        g = self._groups
        for s in self._sub_matchers:
            g |= s.getGroups()
        return g
    
    def getControls(self, group: str = None) -> list[ControlSurface]:
        controls = self._controls
        for s in self._sub_matchers:
            controls += s.getControls()
        if group is None:
            return controls
        else:
            ret = []
            for c in controls:
                if c.group == group:
                    ret.append(c)
            return ret
