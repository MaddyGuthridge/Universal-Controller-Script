"""
controlsurfaces > encoder

Defines encoder control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import IValueStrategy
from . import ControlSurface

class Encoder(ControlSurface):
    """
    Encoders are an endless rotating knob that is used for mapping to
    parameters. Compared to endless jog wheels, they should be mapped to plugin
    parameters, rather than navigation.

    NOTE: Encoders use the ENCODER values found in controlsurfaces.consts.
    TODO: Create a function for getting from an encoder value to a constant
    value.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return (Knob,)

    def __init__(self, event_pattern: IEventPattern, value_strategy: IValueStrategy, coordinate: tuple[int, int], group: str = "encoders") -> None:
        super().__init__(event_pattern, value_strategy, group, coordinate)

from .knob import Knob
