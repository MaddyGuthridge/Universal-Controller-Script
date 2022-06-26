"""
control_surfaces > controls > null_event

Contains the definition of the NullEvent, which represents events that should
be ignored entirely.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional

from ..event_patterns import IEventPattern
from control_surfaces.value_strategies import NullStrategy, IValueStrategy
from control_surfaces.managers import (
    IAnnotationManager,
    IColorManager,
    IValueManager,
)
from . import ControlSurface


class NullControl(ControlSurface):
    """
    Represents events that should be ignored entirely by the script.
    """
    @classmethod
    def create(
        cls,
        event_pattern: IEventPattern,
        value_strategy: Optional[IValueStrategy] = None,
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> 'NullControl':
        """
        Create a NullEvent

        This is used for events which should be ignored

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to match

        * `value_strategy` (`IValueStrategy`, optional): strategy to get the
          value of the control. Defaults to None, which will lead to a
          `NullEventStrategy` being used. A value strategy should be provided
          if this control is used to toggle through a menu (eg a shift button).
        """
        if value_strategy is None:
            value_strategy = NullStrategy()
        return cls(
            event_pattern,
            value_strategy,
            annotation_manager=annotation_manager,
            color_manager=color_manager,
            value_manager=value_manager,
        )

    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Null controls shouldn't be reassigned
        return tuple()
