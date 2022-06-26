"""
control_surfaces > controls > button

Defines a button control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .control_surface import ControlSurface


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
