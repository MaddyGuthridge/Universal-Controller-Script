"""
control_surfaces > controls > hint_msg

Defines a hint message control surface.

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


class HintMsg(ControlSurface):
    """
    Defines a hint message control surface. This control surface's annotation
    property is used to represent FL Studio's hint message. Controllers can
    extend this class to implement code to send hint messages to the device.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return tuple()

    @classmethod
    def create(
        cls,
        annotation_manager: IAnnotationManager,
        color_manager: Optional[IColorManager] = None,
    ) -> 'HintMsg':
        """
        Create a hint message control surface
        """
        return cls(
            NullPattern(),
            NullStrategy(),
            annotation_manager=annotation_manager,
            color_manager=color_manager,
        )
