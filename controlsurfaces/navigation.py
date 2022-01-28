"""
controlsurfaces > navigation

Defines navigation control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from . import ControlSurface

# TODO: Implement navigation controls

class NavigationControl(ControlSurface):
    pass
    
class JogWheel(NavigationControl):
    pass

class JogForwards(JogWheel):
    pass

class JogBackards(JogWheel):
    pass
