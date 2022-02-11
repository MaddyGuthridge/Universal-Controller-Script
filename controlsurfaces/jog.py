"""
controlsurfaces > navigation

Defines jog wheel control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import ControlSurface
from . import NavigationControl

class JogWheel(NavigationControl):
    """
    Jog wheels (rotary encoders) are an endless rotating knob that is used for
    navigation. Compared to endless knobs, they should be mapped to navigation
    controls, rather than standard parameters.
    
    Note that although the control surface is different, all these controls
    could be triggered through a single control, by mapping to different
    controls depending on context.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()

class StandardJogWheel(JogWheel):
    """
    Standard jog wheels are used to navigate the UI (eg scrolling)
    """

class ShiftedJogWheel(JogWheel):
    """
    Shifted jog wheels are used to navigate the UI, but on the opposite axis
    to the standard jog wheel
    """

class MoveJogWheel(JogWheel):
    """
    Move jog wheels are used to move elements within the UI.
    """
