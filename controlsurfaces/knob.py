
from . import ControlSurface

class Knob(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> list[type]:
        # Knob controls should be assigned to faders if knobs aren't available
        return [Fader]

from .fader import Fader
