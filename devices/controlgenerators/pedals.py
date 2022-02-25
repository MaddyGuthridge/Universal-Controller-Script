
from controlsurfaces import ControlSurface, SustainPedal, SoftPedal, SostenutoPedal

def getPedals() -> list[ControlSurface]:
    return [SustainPedal(), SoftPedal(), SostenutoPedal()]
