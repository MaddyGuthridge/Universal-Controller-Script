"""
controlsurfaces > pedal

Defines a sustain pedal control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
__all__ = [
    'Pedal',
    'SustainPedal',
    'SostenutoPedal',
    'SoftPedal',
    'SUSTAIN',
    'SOSTENUTO',
    'SOFT'
]

from ..eventpatterns import BasicPattern, IEventPattern
from . import ControlSurface
from ..valuestrategies import ButtonData2Strategy


class Pedal(ControlSurface):
    """
    Represents pedal events, including sustain, soft and sostenuto pedals
    """

    def __init__(self, pattern: IEventPattern) -> None:
        super().__init__(
            pattern,
            ButtonData2Strategy(),
        )

    @staticmethod
    def isPress(value: float):
        return value != 0

    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Pedals shouldn't be remapped
        return tuple()


# Constants for event recognition
SUSTAIN = 0x40
SOSTENUTO = 0x42
SOFT = 0x43

# TODO: Make these all channel independent


class SustainPedal(Pedal):
    """
    Represents a sustain pedal
    """

    def __init__(self) -> None:
        super().__init__(BasicPattern(0xB0, SUSTAIN, ...))


class SostenutoPedal(Pedal):
    """
    Represents a sostenuto pedal
    """

    def __init__(self) -> None:
        super().__init__(BasicPattern(0xB0, SOSTENUTO, ...))


class SoftPedal(Pedal):
    """
    Represents a soft pedal
    """

    def __init__(self) -> None:
        super().__init__(BasicPattern(0xB0, SOFT, ...))
