"""
devices > maudio > hammer88pro > hammerpitch

Contains the definition for the Hammer 88 Pro's pitch wheel, since its behaviour
is weird

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import BasicPattern, fromNibbles
from controlsurfaces import PitchWheel
from controlsurfaces.valuestrategies import Data2Strategy

class HammerPitchWheel(PitchWheel):
    """
    Implementation of the pitch wheel on the Hammer 88 Pro since its behaviour
    is weird
    """
    def __init__(self) -> None:
        super().__init__(
            BasicPattern(fromNibbles(0xE, ...), (0x0, 0x7F), ...),
            Data2Strategy()
        )
