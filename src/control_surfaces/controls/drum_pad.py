"""
control_surfaces > controls > drum_pad

Defines a drum pad control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from . import ControlSurface


class DrumPad(ControlSurface):
    """
    Defines a drum pad control surface.
    Drum pads are usually used to trigger pads in drum plugins, or key-switches
    in orchestral plugins.

    Coordinates should be: (row, col), where (0, 0) is the top left
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return tuple()
