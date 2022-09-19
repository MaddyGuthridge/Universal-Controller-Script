"""
control_surfaces > controls > navigation

Defines navigation control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from . import ControlSurface
from . import Button

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


class NavigationControl(ControlSurface):
    """
    Navigation control surfaces are used to navigate through FL Studio,
    changing or relocating selections, for example
    """


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

    ### Falls back to:
    * `DirectionRight`
    * `DirectionDown`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return (DirectionRight, DirectionDown)


class DirectionPrevious(NextPrevButton):
    """
    A previous button

    ### Falls back to:
    * `DirectionLeft`
    * `DirectionUp`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return (DirectionLeft, DirectionUp)
