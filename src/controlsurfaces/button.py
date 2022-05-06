"""
controlsurfaces > button

Defines a button control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .eventpattern import IEventPattern
from controlsurfaces.valuestrategies import IValueStrategy
from .controlsurface import ControlSurface


class Button(ControlSurface):
    """
    Defines a button control surface
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Buttons shouldn't be reassigned to anything else
        return tuple()

    @staticmethod
    def isPress(value: float):
        return value == 1.0


# TODO: Find a proper home for this
class ControlSwitchButton(Button):
    """
    A button that is used to switch modes in some plugins (for example when
    changing between views). In order to get full control of the script,
    devices should implement this button somewhere.
    """
    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy)
