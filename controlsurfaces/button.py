
from .controlsurface import ControlSurface

class Button(ControlSurface):
    
    @staticmethod
    def getControlAssignmentPriorities() -> list[type]:
        # Buttons shouldn't be reassigned to anything else
        return []
