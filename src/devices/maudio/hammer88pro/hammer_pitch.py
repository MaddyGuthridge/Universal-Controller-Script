"""
devices > maudio > hammer88pro > hammer_pitch

Contains the definition for the Hammer 88 Pro's pitch wheel, since its
behavior is weird.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, fromNibbles
from control_surfaces import PitchWheel
from control_surfaces.value_strategies import Data2Strategy


class HammerPitchWheel(PitchWheel):
    """
    Implementation of the pitch wheel on the Hammer 88 Pro since its behavior
    is weird
    """

    def __init__(self) -> None:
        super().__init__(
            BasicPattern(fromNibbles(0xE, ...), (0x0, 0x7F), ...),
            Data2Strategy()
        )
