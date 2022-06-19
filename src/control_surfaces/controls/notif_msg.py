"""
control_surfaces > controls > notif_msg

Defines a notification message control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional
from ..event_patterns import NullPattern
from control_surfaces.value_strategies import NullStrategy
from control_surfaces.managers import (
    IAnnotationManager,
    IColorManager,
)
from . import ControlSurface


class NotifMsg(ControlSurface):
    """
    Defines a notification message control surface. This control surface's
    annotation property can be used to set a notification message for a value.
    Controllers can extend this class to implement code to send notification
    messages to the device.

    This differs from a hint message as it should only be used to show the user
    information that they need to know (usually to do with the behavior of
    their device), whereas a hint message is whatever happens to be displaying
    in FL Studio's hint panel.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return tuple()

    @classmethod
    def create(
        cls,
        annotation_manager: IAnnotationManager,
        color_manager: Optional[IColorManager] = None,
    ) -> 'NotifMsg':
        """
        Create a hint message control surface
        """
        return cls(
            NullPattern(),
            NullStrategy(),
            annotation_manager=annotation_manager,
            color_manager=color_manager,
        )
