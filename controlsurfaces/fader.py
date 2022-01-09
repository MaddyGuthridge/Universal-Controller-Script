
from . import ControlSurface

class Fader(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface]]:
        # Fader controls should be assigned to knobs if faders aren't available
        return (Knob, )

from .knob import Knob
