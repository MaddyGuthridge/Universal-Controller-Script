"""
control_surfaces > controls > wheel

Contains the definitions for pitch and modulation wheels

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
from ..event_patterns import BasicPattern, fromNibbles
from fl_classes import FlMidiMsg, isMidiMsgStandard
from . import ControlSurface
from ..value_strategies import Data2Strategy, IValueStrategy

__all__ = [
    'ModWheel',
    'PitchWheel',
    'StandardModWheel',
    'StandardPitchWheel',
    'Data2PitchWheel',
]


class ModWheel(ControlSurface):
    """
    Represents a modulation wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()


class StandardModWheel(ModWheel):
    """
    Standard implementation of a mod wheel
    """
    @classmethod
    def create(
        cls,
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> 'StandardModWheel':
        return cls(
            BasicPattern(fromNibbles(0xB, ...), 0x1, ...),
            Data2Strategy(),
            annotation_manager=annotation_manager,
            color_manager=color_manager,
            value_manager=value_manager,
        )


class PitchValueStrategy(IValueStrategy):
    """
    Value strategy for standard pitch bends (using 14 bits of information,
    0 - 16384, zero at 8192)
    """

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        """Returns a 14-bit int (0 - 16384)
        Zero value = 8192
        """
        assert isMidiMsgStandard(event)
        return (event.data1 + (event.data2 << 7)) / 16383

    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        assert isMidiMsgStandard(event)
        return event.status & 0xF


class PitchWheel(ControlSurface):
    """
    Represents a pitch bend wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()


class StandardPitchWheel(PitchWheel):
    """
    Standard implementation of a pitch bend wheel (using 14 bits of
    information)
    """
    @classmethod
    def create(
        cls,
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> 'StandardPitchWheel':
        return cls(
            BasicPattern(fromNibbles(0xE, ...), ..., ...),
            PitchValueStrategy(),
            annotation_manager=annotation_manager,
            color_manager=color_manager,
            value_manager=value_manager,
        )


class Data2PitchWheel(PitchWheel):
    """
    Implementation of a pitch wheel using data2 values to determine pitch, as
    some manufacturers don't follow the standard of using 14 bits or precision.
    """
    @classmethod
    def create(
        cls,
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> 'Data2PitchWheel':
        return cls(
            BasicPattern(fromNibbles(0xE, ...), 0x0, ...),
            PitchValueStrategy(),
            annotation_manager=annotation_manager,
            color_manager=color_manager,
            value_manager=value_manager,
        )
