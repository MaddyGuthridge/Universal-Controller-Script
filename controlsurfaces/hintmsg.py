"""
controlsurfaces > hintmsg

Defines a hint message control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern import NullPattern
from controlsurfaces.valuestrategies import NullEventStrategy
from . import ControlSurface


class HintMsg(ControlSurface):
    """
    Defines a hint message control surface. This control surface's annotation
    property can be used to set a hint message for a value. Controllers can
    extend this class to implement code to send hint messages to the device.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return tuple()

    def __init__(self) -> None:
        super().__init__(
            NullPattern(),
            NullEventStrategy(),
            "hint",
            (0, 0)
        )
