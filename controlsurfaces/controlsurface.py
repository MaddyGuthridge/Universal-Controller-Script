"""
controlsurfaces > controlsurface

Contains the ControlSurface class, which defines the abstract base type for
all control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from common.eventpattern import IEventPattern

class ControlSurface:
    """
    Defines an abstract base class for a control surface.

    This class is extended by all other control surfaces.
    """
    
    def __init__(self, event: IEventPattern) -> None:
        pass
