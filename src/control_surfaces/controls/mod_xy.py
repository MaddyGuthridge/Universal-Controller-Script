"""
control_surfaces > controls > mod_xy

Defines ModX and ModY control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from ..event_patterns import IEventPattern
from control_surfaces.value_strategies import IValueStrategy
from . import ControlSurface


class ModXY(ControlSurface):
    """
    ModXY controls are a 2D cartesian control surface, where the position of
    some controller (such as a finger or slider) in the grid determines the
    properties of both the X and Y coordinates. These coordinates can then be
    bound to controls to allow for advanced sound manipulation, particularly
    in live performance.

    ModXY is an abstract class. Devices should implement a ModX and a ModY
    control separately.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        from .fader import Fader
        from .knob import Knob
        from .encoder import Encoder
        return (Fader, Knob, Encoder)

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int],
    ) -> None:
        super().__init__(event_pattern, value_strategy, coordinate)


class ModX(ModXY):
    """
    ModX control
    """


class ModY(ModXY):
    """
    ModY control

    Can also be substituted with a mod wheel
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        from .wheels import ModWheel
        return super(ModY, ModY).getControlAssignmentPriorities() + (ModWheel,)
