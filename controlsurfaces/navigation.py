"""
controlsurfaces > navigation

Defines navigation control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import IValueStrategy
from . import ControlSurface
from . import Button

# TODO: Implement navigation controls

class NavigationControl(ControlSurface):
    def __init__(self, event_pattern: IEventPattern, value_strategy: IValueStrategy) -> None:
        super().__init__(event_pattern, value_strategy, "navigation")
    
class JogWheel(NavigationControl):
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()

class JogForwards(JogWheel):
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return (DirectionNext,)

class JogBackards(JogWheel):
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return (DirectionPrevious,)

class NavigationButtons(Button, NavigationControl):
    pass

class DpadButtons(NavigationButtons):
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

class NextPrevButtons(NavigationButtons):
    pass

class DirectionNext(NextPrevButtons):
    pass

class DirectionPrevious(NextPrevButtons):
    pass
