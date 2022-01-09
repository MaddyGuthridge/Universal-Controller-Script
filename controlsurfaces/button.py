
from .controlsurface import ControlSurface

class Button(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface]]:
        # Buttons shouldn't be reassigned to anything else
        return tuple()
