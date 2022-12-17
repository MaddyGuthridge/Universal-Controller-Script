"""
devices > matchers > control_matcher

Defines the IControlMatcher interface for matching up controls, as well as a
BasicControlMatcher for simple devices.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional, Sequence
from abc import abstractmethod
from fl_classes import FlMidiMsg
from common.util.abstract_method_error import AbstractMethodError
from control_surfaces import ControlEvent, ControlSurface


class IControlMatcher:
    """
    The interface for matching controls from MIDI events

    This can be extended to match controls in a custom, more-efficient manner
    if required or desired. Otherwise, the BasicControlMatcher class will work.
    """
    @abstractmethod
    def matchEvent(self, event: FlMidiMsg) -> Optional[ControlEvent]:
        """
        Match an event to a control.

        ### Args:
        * `event` (`FlMidiMsg`): event to match

        ### Returns:
        * `ControlMapping | None`: mapping to matched control, or None if there
          was no match
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def getControls(self) -> Sequence[ControlSurface]:
        """
        Returns a list of controls contained by the control matcher.

        ### Returns:
        * `list[ControlSurface]`: list of control surfaces
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def tick(self, thorough: bool) -> None:
        """Tick this control matcher, as well as any child control matchers

        ### Args:
        * thorough (`bool`): Whether a full tick should be done.
        """
        raise AbstractMethodError(self)
