
from . import ControlSurface

class Fader(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> list[type]:
        # Fader controls should be assigned to knobs if faders aren't available
        return []

from .knob import Knob
