"""
controlsurfaces > navigation

Defines navigation control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'NavigationControl',
    'NavigationButton',
    'DpadButtons',
    'DirectionUp',
    'DirectionDown',
    'DirectionLeft',
    'DirectionRight',
    'DirectionSelect',
    'NextPrevButton',
    'DirectionNext',
    'DirectionPrevious',
]

from ..event_patterns import IEventPattern
from control_surfaces.value_strategies import IValueStrategy
from . import ControlSurface
from . import Button


class NavigationControl(ControlSurface):
    """
    Navigation control surfaces are used to navigate through FL Studio,
    changing or relocating selections, for example
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy)


class NavigationButton(Button, NavigationControl):
    """
    Navigation buttons are used to navigate FL Studio
    """


class DpadButtons(NavigationButton):
    """
    D-pad buttons are used to navigate FL Studio with directional inputs
    """


class DirectionUp(DpadButtons):
    """
    An upward direction button
    """


class DirectionDown(DpadButtons):
    """
    A downward direction button
    """


class DirectionLeft(DpadButtons):
    """
    A leftward direction button
    """


class DirectionRight(DpadButtons):
    """
    A right direction button
    """


class DirectionSelect(DpadButtons):
    """
    A select button (usually in the centre of a d-pad)
    """


class NextPrevButton(NavigationButton):
    """
    Represents next or previous buttons
    """


class DirectionNext(NextPrevButton):
    """
    A next button
    """


class DirectionPrevious(NextPrevButton):
    """
    A previous button
    """
