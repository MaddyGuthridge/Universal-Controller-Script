"""
controlsurfaces > encoder

Defines encoder control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from ..event_patterns import IEventPattern
from control_surfaces.value_strategies import IValueStrategy
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
        from .knob import Knob
        return (Knob,)

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int],
    ) -> None:
        super().__init__(event_pattern, value_strategy, coordinate)
