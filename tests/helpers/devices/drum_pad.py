"""
tests > helpers > devices

Device definitions

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Sequence
from control_surfaces.event_patterns import BasicPattern
from fl_classes import FlMidiMsg
from control_surfaces.matchers import BasicControlMatcher
from control_surfaces import ControlSurface, DrumPad
from control_surfaces.value_strategies import (
    Data2Strategy,
)
from .basic import DummyDeviceAbstract

__all__ = [
    'DummyDeviceDrumPads',
    'getEventForDrumPad',
]


class DummyDeviceDrumPads(DummyDeviceAbstract):
    """
    A dummy device containing a collection of drum pads of specified sizes
    """

    def __init__(self, rows: int, cols: int) -> None:
        matcher = BasicControlMatcher()

        self.drums = [[
            DrumPad(
                    BasicPattern(r, c, ...),
                    Data2Strategy(),
                    (r, c),
                )
            for c in range(cols)
        ] for r in range(rows)]

        flattened: Sequence[ControlSurface] = sum(self.drums, [])

        matcher.addControls(flattened)

        super().__init__(matcher)

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return (4, 4)


def getEventForDrumPad(row: int, col: int, value: float) -> FlMidiMsg:
    """
    Returns a MIDI message that matches the drum pad at `(row, col)` for a
    `DummyDeviceDrumPads` device.
    """
    return FlMidiMsg(row, col, int(value * 127))
