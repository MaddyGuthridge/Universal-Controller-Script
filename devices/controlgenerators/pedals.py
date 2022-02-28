
from controlsurfaces import ControlSurface, SustainPedal, SoftPedal, SostenutoPedal
from devices.matchers import BasicControlMatcher

class PedalMatcher(BasicControlMatcher):
    def __init__(self) -> None:
        super().__init__()
        self.addControls([SustainPedal(), SoftPedal(), SostenutoPedal()])
