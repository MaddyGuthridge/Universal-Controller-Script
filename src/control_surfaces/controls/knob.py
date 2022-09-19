"""
control_surfaces > controls > knob

Defines a knob control surface

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .encoder import Encoder
from . import ControlSurface


class GenericKnob(ControlSurface):
    """
    Knobs are limited rotating controls, which usually yield a value relative
    to the rotational position of the knob. They should be assigned to
    non-linear parameters such as pans, or mix levels.

    WARNING: Generally, you want to bind to either a standard knob or the
    master knob.
    """


class Knob(GenericKnob):
    """
    Defines a standard knob (as opposed to the master knob)

    ### Falls back to:
    * `Fader`
    * `Encoder`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        from .fader import Fader
        # Knob controls should be assigned to faders if knobs aren't available
        return (Fader, Encoder)


class MasterKnob(GenericKnob):
    """
    Defines a master knob (as opposed to a normal knob). A controller should
    only have one master knob, which will be bound independently to the normal
    knobs.

    ### Falls back to:
    * `MasterFader`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        from .fader import MasterFader
        # If the master knob isn't available, it should be substituted for the
        # master fader
        return (MasterFader, )
