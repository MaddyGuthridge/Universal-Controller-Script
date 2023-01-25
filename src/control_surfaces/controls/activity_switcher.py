"""
control_surfaces > controls > window_switcher

Contains the definition of window switcher control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .control_surface import ControlSurface
from .button import Button


class ActivitySwitcher(Button):
    """
    Allows users to switch between FL Studio windows and recent plugins
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
