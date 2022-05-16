"""
devices > shiftmatcher

Defines a ShiftMatcher interface for matching different events depending on
whether a shift button is active or not.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from typing import Optional
from common.types import EventData
from controlsurfaces import ControlEvent, ControlSurface
from . import IControlMatcher


class ShiftMatcher(IControlMatcher):
    """
    Allows a control to be designated as a "shift" button, so that pressing
    it switches between two sub control matchers.

    Note that this button is still matched normally, so its events can still be
    used. If no action should be taken when pressing the button, it should be
    registered as a NullEvent.

    In order to modify the LED of the shift button, ControlSurfaces should
    determine whether the button is pressed using the onValueChange callback.
    This also implements the behaviour of the double pressed shift button.
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
                # If it was a double press, set the value such that the control
                # is enabled (since the shift button is enabled)
                # NOTE: This may cause flickering since it is set to 0.0
                # earlier - if this is an issue some major refactoring might
                # need to be done to determine how control surface update
                # callbacks are called when that control is matched.
                else:
                    self.__shift.value = 1.0
            return control_event
        # Otherwise delegate to the required submatcher
        if self.__shifted:
            return self.__enabled.matchEvent(event)
        else:
            return self.__disabled.matchEvent(event)

    def getControls(self) -> list[ControlSurface]:
        return (
            [self.__shift]
            + self.__enabled.getControls()
            + self.__disabled.getControls()
        )

    def tick(self, thorough: bool) -> None:
        # Tick the shift button
        self.__shift.doTick(thorough)
        # Tick whichever sub-matcher is active (but don't tick the non-active
        # one or we might cause clashing colors)
        if self.__shifted:
            self.__enabled.tick(thorough)
        else:
            self.__disabled.tick(thorough)
