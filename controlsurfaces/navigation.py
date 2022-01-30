"""
controlsurfaces > navigation

Defines navigation control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from . import ControlSurface
from . import Button

# TODO: Implement navigation controls

class NavigationControl(ControlSurface):
    pass
    
class JogWheel(NavigationControl):
    pass

class JogForwards(JogWheel):
    pass

class JogBackards(JogWheel):
    pass

class DirectionButtons(Button, NavigationControl):
    pass

class DpadButtons(DirectionButtons):
    pass

class DirectionUp(DpadButtons):
    pass

class DirectionDown(DpadButtons):
    pass

class DirectionLeft(DpadButtons):
    pass

class DirectionRight(DpadButtons):
    pass

class DirectionSelect(DpadButtons):
    pass

class NextPrevButtons(DirectionButtons):
    pass

class DirectionNext(NextPrevButtons):
    pass

class DirectionPrevious(NextPrevButtons):
    pass
