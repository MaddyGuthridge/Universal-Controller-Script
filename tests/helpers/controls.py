"""
tests > helpers > controls

Helper code for testing with control surfaces
"""
from common.eventpattern import BasicPattern
from controlsurfaces.valuestrategies import Data2Strategy

from controlsurfaces import ControlSurface


class SimpleControl(ControlSurface):
    """A simple control surface for testing

    It matches any event with a status of 0 and a data1 of i
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            BasicPattern(0, i, ...),
            Data2Strategy(),
        )


class SimplerControl(ControlSurface):
    """Another simple control surface for testing

    It matches any event with a status of 0, a data1 of i and a data2 of 0
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            BasicPattern(0, i, 0),
            Data2Strategy(),
        )
