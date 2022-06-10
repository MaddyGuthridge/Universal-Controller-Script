"""
control_surfaces > controls > pedal

Defines a sustain pedal control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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

from ..event_patterns import BasicPattern
from . import ControlSurface
from ..value_strategies import ButtonData2Strategy


class Pedal(ControlSurface):
    """
    Represents pedal events, including sustain, soft and sostenuto pedals
    """

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
    @classmethod
    def create(cls) -> 'SustainPedal':
        return cls(
            BasicPattern(0xB0, SUSTAIN, ...),
            ButtonData2Strategy(),
        )


class SostenutoPedal(Pedal):
    """
    Represents a sostenuto pedal
    """
    @classmethod
    def create(cls) -> 'SostenutoPedal':
        return cls(
            BasicPattern(0xB0, SOSTENUTO, ...),
            ButtonData2Strategy(),
        )


class SoftPedal(Pedal):
    """
    Represents a soft pedal
    """
    @classmethod
    def create(cls) -> 'SoftPedal':
        return cls(
            BasicPattern(0xB0, SOFT, ...),
            ButtonData2Strategy(),
        )
