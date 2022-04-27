"""
devices > control matcher

Defines the IControlMatcher interface for matching up controls, as well as a
BasicControlMatcher for simple devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Optional
from common.types import EventData
from controlsurfaces import ControlEvent, ControlSurface
from . import IControlMatcher


class BasicControlMatcher(IControlMatcher):
    """
    A basic implementation of the control mapper, using a list of controls and
    a set of groups.

    This should be usable for most basic controllers, but for more complex
    controllers with many controls, it may have poor performance compared to
    hard-coded custom matchers, which can be created by extending
    the IControlMatcher class.
    """

    def __init__(self) -> None:
        self._priorities: set[int] = set()
        self._controls: dict[int, list[ControlSurface]] = {}
        self._groups: set[str] = set()
        self._sub_matchers: dict[int, list[IControlMatcher]] = {}

    def addControls(
        self,
        controls: list[ControlSurface],
        priority: int = 0
    ) -> None:
        """
        Register and add a list of controls to the control matcher.

        ### Args:
        * `controls` (`list[ControlSurface]`): Controls to add
        * `priority` (`int`): Matcher priority of control (higher priority
          controls will be matched first)
        """
        for c in controls:
            self.addControl(c, priority)

    def addControl(self, control: ControlSurface, priority: int = 0) -> None:
        """
        Register and add a control to the control matcher.

        ### Args:
        * `control` (`ControlSurface`): Control to add
        * `priority` (`int`): Matcher priority of control (higher priority
          controls will be matched first)
        """
        if priority in self._controls:
            self._controls[priority].append(control)
        else:
            self._priorities.add(priority)
            self._controls[priority] = [control]
        self._groups.add(control.group)

    def addSubMatcher(
        self,
        matcher: IControlMatcher,
        priority: int = 0
    ) -> None:
        """
        Register a control matcher to work as a component of this control
        matcher

        This allows for more complex control mappings to be made without the
        need to implement a full control matcher

        ### Args:
        * `matcher` (`IControlMatcher`): control matcher to add
        * `priority` (`int`): Matcher priority of control (higher priority
          controls will be matched first)
        """
        if priority in self._sub_matchers:
            self._sub_matchers[priority].append(matcher)
        else:
            self._priorities.add(priority)
            self._sub_matchers[priority] = [matcher]

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        # Work through in order of priority
        for priority in reversed(sorted(self._priorities)):
            if priority in self._controls:
                for c in self._controls[priority]:
                    if (m := c.match(event)) is not None:
                        return m
            if priority in self._sub_matchers:
                for s in self._sub_matchers[priority]:
                    if (m := s.matchEvent(event)) is not None:
                        return m
        return None

    def getGroups(self) -> set[str]:
        g = self._groups
        for p in self._sub_matchers:
            for s in self._sub_matchers[p]:
                g |= s.getGroups()
        return g

    def getControls(self, group: str = None) -> list[ControlSurface]:
        controls = []
        for p in self._controls:
            controls += self._controls[p]
        for p in self._sub_matchers:
            for s in self._sub_matchers[p]:
                controls += s.getControls()
        if group is None:
            return controls
        else:
            ret = []
            for c in controls:
                if c.group == group:
                    ret.append(c)
            return ret
