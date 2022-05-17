"""
controlsurfaces > notifmsg

Defines a notification message control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .eventpattern import NullPattern
from controlsurfaces.valuestrategies import NullEventStrategy
from . import ControlSurface


class NotifMsg(ControlSurface):
    """
    Defines a notification message control surface. This control surface's
    annotation property can be used to set a notification message for a value.
    Controllers can extend this class to implement code to send notification
    messages to the device.

    This differs from a hint message as it should only be used to show the user
    information that they need to know (usually to do with the behaviour of
    their device), whereas a hint message is whatever happens to be displaying
    in FL Studio's hint panel.
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
