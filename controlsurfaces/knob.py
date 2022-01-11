"""
controlsurfaces > knob

Defines a knob control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from . import ControlSurface

class Knob(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface]]:
        # Knob controls should be assigned to faders if knobs aren't available
        return (Fader, )

from .fader import Fader
