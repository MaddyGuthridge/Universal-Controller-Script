"""
control_surfaces > controls > after_touch

Contains the definition of after-touch control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional
from control_surfaces.managers import (
    IAnnotationManager,
    IColorManager,
    IValueManager,
)
from ..event_patterns import BasicPattern, fromNibbles, ByteMatch
from . import ControlSurface
from ..value_strategies import Data2Strategy, Data1Strategy


class AfterTouch(ControlSurface):
    """
    The definition of a generic after-touch control surface.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        # Allow substitution between different after-touch types
        return (AfterTouch,)


class ChannelAfterTouch(AfterTouch):
    """
    The definition of channel after-touch, which represents the strongest key
    pressure out of all active keys
    """
    @classmethod
    def fromChannel(
        cls,
        channel: ByteMatch,
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> 'ChannelAfterTouch':
        return cls(
            BasicPattern(fromNibbles(0xD, channel), ..., ...),
            Data1Strategy(),
            (0, 0),
            annotation_manager,
            color_manager,
            value_manager,
        )


class NoteAfterTouch(AfterTouch):
    """
    The definition of note after-touch, which represents the pressure of a
    single key
    """
    @classmethod
    def create(
        cls,
        note: int,
        channel: ByteMatch,
        coordinate: tuple[int, int] = (0, 0),
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> 'NoteAfterTouch':
        return cls(
            BasicPattern(fromNibbles(0xA, channel), note, ...),
            Data2Strategy(),
            coordinate,
            annotation_manager,
            color_manager,
            value_manager,
        )
