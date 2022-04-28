"""
controlsurfaces > knob

Defines a knob control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .encoder import Encoder
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import IValueStrategy
from . import ControlSurface


class GenericKnob(ControlSurface):
    """
    Knobs are limited rotating controls, which usually yield a value relative
    to the rotational position of the knob. They should be assigned to
    non-linear parameters such as pans, or mix levels.

    WARNING: Generally, you want to bind to either a generic knob or the
    master knob.
    """


class Knob(GenericKnob):
    """
    Defines a knob (as opposed to the master knob)
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        from .fader import Fader
        # Knob controls should be assigned to faders if knobs aren't available
        return (Fader, Encoder)

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int],
    ) -> None:
        super().__init__(event_pattern, value_strategy, coordinate)


class MasterKnob(GenericKnob):
    """
    Defines a master knob (as opposed to a normal knob). A controller should
    only have one master knob, which will be bound independently to the normal
    knobs.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        from .fader import MasterFader
        # If the master knob isn't available, it should be substituted for the
        # master fader
        return (MasterFader, )

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy)
