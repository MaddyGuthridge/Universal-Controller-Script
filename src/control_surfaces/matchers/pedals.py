"""
devices > control_generators > pedals

Contains control matcher for pedal events.

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces import SustainPedal, SoftPedal, SostenutoPedal
from control_surfaces.matchers import BasicControlMatcher


class PedalMatcher(BasicControlMatcher):
    """
    Control matcher for pedal events
    """

    def __init__(self) -> None:
        super().__init__()
        self.addControls([
            SustainPedal.create(),
            SoftPedal.create(),
            SostenutoPedal.create()
        ])
