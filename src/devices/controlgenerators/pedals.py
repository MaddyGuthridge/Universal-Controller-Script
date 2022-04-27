"""
devices > controlgenerators > pedals

Contains custom control matcher for pedal events

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from controlsurfaces import SustainPedal, SoftPedal, SostenutoPedal
from devices.matchers import BasicControlMatcher


class PedalMatcher(BasicControlMatcher):
    """
    Control matcher for pedal events
    """

    def __init__(self) -> None:
        super().__init__()
        self.addControls([SustainPedal(), SoftPedal(), SostenutoPedal()])
