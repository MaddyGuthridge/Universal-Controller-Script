"""
controlsurfaces > fader

Defines a fader control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from . import ControlSurface

class Fader(ControlSurface):
    """
    Defines a fader (slider) control surface.
    Faders are generally mapped to linear parameters, such as volumes or effect
    levels.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Fader controls should be assigned to knobs if faders aren't available
        return (Knob, )

from .knob import Knob
