"""
controlsurfaces > hintmsg

Defines a hint message control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from ..event_patterns import NullPattern
from control_surfaces.value_strategies import NullEventStrategy
from . import ControlSurface


class HintMsg(ControlSurface):
    """
    Defines a hint message control surface. This control surface's annotation
    property is used to represent FL Studio's hint message. Controllers can
    extend this class to implement code to send hint messages to the device.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return tuple()

    def __init__(self) -> None:
        super().__init__(
            NullPattern(),
            NullEventStrategy(),
            (0, 0)
        )
