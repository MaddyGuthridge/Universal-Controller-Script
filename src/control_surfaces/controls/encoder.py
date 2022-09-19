"""
control_surfaces > controls > encoder

Defines encoder control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from . import ControlSurface


class Encoder(ControlSurface):
    """
    Encoders are an endless rotating knob that is used for mapping to
    parameters. Compared to endless jog wheels, they should be mapped to plugin
    parameters, rather than navigation.

    The values of encoders are calculated using the existing value of the
    control. This means that a value strategy with support for relative
    values should be used, such as the `TwosComplimentDeltaStrategy`.

    ### Falls back to:
    * `Knob`
    * `Fader`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        from .knob import Knob
        from .fader import Fader
        return (Knob, Fader)
