"""
tests > helpers > controls

Helper code for testing with control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import Data2Strategy, ForwardedStrategy

from control_surfaces import ControlSurface


class SimpleControl(ControlSurface):
    """A simple control surface for testing

    It matches any event with a status of 0 and a data1 of i
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            BasicPattern(0, i, ...),
            Data2Strategy(),
        )

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()


class SimplerControl(ControlSurface):
    """Another simple control surface for testing

    It matches any event with a status of 0, a data1 of i and a data2 of 0
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            BasicPattern(0, i, 0),
            Data2Strategy(),
        )

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()


class SimpleForwardedControl(ControlSurface):
    """A simple control surface for testing

    It matches any forwarded event from device 2 with a status of 0 and a data1
    of i
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0, i, ...)),
            ForwardedStrategy(Data2Strategy()),
        )

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        return tuple()
