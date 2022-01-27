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

from common.eventpattern import EventPattern, IEventPattern
from . import ControlSurface
from .valuestrategies import ButtonData2Strategy

class Pedal(ControlSurface):
    
    def __init__(self, pattern: IEventPattern) -> None:
        super().__init__(
            pattern,
            ButtonData2Strategy(),
            "pedals"
        )
    
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface]]:
        # Pedals shouldn't be remapped
        return tuple()

SUSTAIN = 0x40
SOSTENUTO = 0x42
SOFT = 0x43

class SustainPedal(Pedal):
    def __init__(self) -> None:
        super().__init__(EventPattern(0xB0, SUSTAIN, ...))

class SostenutoPedal(Pedal):
    def __init__(self) -> None:
        super().__init__(EventPattern(0xB0, SOSTENUTO, ...))

class SoftPedal(Pedal):
    def __init__(self) -> None:
        super().__init__(EventPattern(0xB0, SOFT, ...))
