"""
devices > shiftmatcher

Defines a ShiftMatcher interface for matching different events depending on
whether a shift button is active or not.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from typing import Optional
from abc import abstractmethod
from common.types import EventData
from controlsurfaces import ControlEvent, ControlSurface
from . import IControlMatcher


class ShiftMatcher(IControlMatcher):
    """
    Allows a control to be designated as a "shift" button, so that pressing
    it switches between two sub control matchers.
    """
    def __init__(
        self,
        shift: ControlSurface,
        disabled: IControlMatcher,
        enabled: IControlMatcher,
    ) -> None:
        # Shift button
        self.__shift = shift
        # Submatchers
        self.__disabled = disabled
        self.__enabled = enabled
        # Whether we're currently in the shift menu
        self.__shifted = False
        # Whether the previous press was a double press
        self.__double = False
        super().__init__()

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        # If it's the shift button
        if (control_event := self.__shift.match(event)) is not None:
            # If we're pressing the shift button
            if control_event.value:
                # Update double press
                self.__double = control_event.double
                self.__shifted = True
            else:
                # Only disable if it wasn't a double press
                if not self.__double:
                    self.__shifted = False
            return control_event
        # Otherwise delegate to the required submatcher
        if self.__shifted:
            return self.__enabled.matchEvent(event)
        else:
            return self.__disabled.matchEvent(event)

    @abstractmethod
    def getControls(self) -> list[ControlSurface]:
        return (
            [self.__shift]
            + self.__enabled.getControls()
            + self.__disabled.getControls()
        )
