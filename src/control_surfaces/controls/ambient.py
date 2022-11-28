"""
control_surfaces > controls > ambient

Defines ambient control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from . import ControlSurface


class Ambient(ControlSurface):
    """
    Used to control ambient lighting of the controller. Devices which have LEDs
    that don't have a clear use can use this controller to be assigned a color
    based on the active plugin/window.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
