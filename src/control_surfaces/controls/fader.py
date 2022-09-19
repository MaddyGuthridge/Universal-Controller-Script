"""
control_surfaces > controls > fader

Defines a fader control surface.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .knob import Knob, MasterKnob
from .encoder import Encoder
from . import ControlSurface


class GenericFader(ControlSurface):
    """
    Defines a fader (slider) control surface.
    Faders are generally mapped to linear parameters, such as volumes or effect
    levels.
    """


class Fader(GenericFader):
    """
    Defines a fader (as opposed to the master fader)

    ### Falls back to:
    * `Knob`
    * `Encoder`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Fader controls should be assigned to knobs if faders aren't available
        return (Knob, Encoder)


class MasterFader(GenericFader):
    """
    Defines a master fader (as opposed to a normal fader). A controller should
    only have one master fader, which will be bound independently to the normal
    faders.

    ### Falls back to:
    * `MasterKnob`
    """
    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        # Fader controls should be assigned to knobs if faders aren't available
        return (MasterKnob, )
