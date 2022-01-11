"""
controlsurfaces > button

Defines a button control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .controlsurface import ControlSurface

class Button(ControlSurface):
    """
    Defines a button control surface
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Buttons shouldn't be reassigned to anything else
        return tuple()
